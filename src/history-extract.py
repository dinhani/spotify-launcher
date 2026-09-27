import json
import sys
from pathlib import Path

import polars

EXPORT_DIR = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("Z:/pessoal/redes-sociais/spotify-2026-09")
OUT = Path(__file__).parent.parent / "data" / "history.parquet"
TIMEZONE = "America/Sao_Paulo"

KIND = polars.Enum(["track", "episode"])
DEVICE = polars.Enum(["desktop", "phone", "tablet", "speaker", "tv", "unknown"])
DEVICE_PLATFORM_PREFIXES = {
    "desktop": ("windows", "osx", "web_player", "webplayer", "partner spotify web_player"),
    "tablet": ("android-tablet",),
    "phone": ("android", "ios"),
    "speaker": ("partner amazon_salmon",),
    "tv": ("partner scei", "partner android_tv", "partner lg_tv", "playstation"),
}

def parse_device(platform: str) -> str:
    platform = platform.casefold()
    return next((device for device, prefixes in DEVICE_PLATFORM_PREFIXES.items() if platform.startswith(prefixes)), "unknown")

# ------------------------------------------------------------------------------
# Load every streaming history file (audio and video)
# ------------------------------------------------------------------------------
streams = [
    stream
    for file in sorted(EXPORT_DIR.glob("Streaming_History_*.json"))
    for stream in json.loads(s=file.read_text(encoding="utf-8"))
]

# ------------------------------------------------------------------------------
# Keep only what is relevant: what played, when, for how long and how
# ------------------------------------------------------------------------------
rows = [
    {
        "ended_at": stream["ts"],
        "played": stream["ms_played"],
        "kind": "track" if stream["spotify_track_uri"] else "episode",
        "artist": stream["master_metadata_album_artist_name"],
        "album": stream["master_metadata_album_album_name"],
        "track": stream["master_metadata_track_name"],
        "track_id": stream["spotify_track_uri"] and stream["spotify_track_uri"].removeprefix("spotify:track:"),
        "show": stream["episode_show_name"],
        "episode": stream["episode_name"],
        "episode_id": stream["spotify_episode_uri"] and stream["spotify_episode_uri"].removeprefix("spotify:episode:"),
        "device": parse_device(stream["platform"]),
        "reason_start": stream["reason_start"],
        "reason_end": stream["reason_end"],
        "shuffle": stream["shuffle"],
        "skipped": bool(stream["skipped"]),
    }
    for stream in streams
    if stream["spotify_track_uri"] or stream["spotify_episode_uri"]
]

history = (
    polars.DataFrame(data=rows, schema={
        "ended_at": polars.String,
        "played": polars.Int64,
        "kind": KIND,
        "artist": polars.String,
        "album": polars.String,
        "track": polars.String,
        "track_id": polars.String,
        "show": polars.String,
        "episode": polars.String,
        "episode_id": polars.String,
        "device": DEVICE,
        "reason_start": polars.String,
        "reason_end": polars.String,
        "shuffle": polars.Boolean,
        "skipped": polars.Boolean,
    })
    .with_columns(
        polars.col("ended_at").str.to_datetime(format="%Y-%m-%dT%H:%M:%SZ", time_zone="UTC").dt.convert_time_zone(TIMEZONE),
        polars.duration(milliseconds=polars.col("played"), time_unit="ms").alias("played"),
    )
    .sort("ended_at")
)

OUT.parent.mkdir(exist_ok=True)
history.write_parquet(file=OUT)
print(f"Wrote {OUT}: {len(history)} streams ({len(streams) - len(history)} without content dropped)")
