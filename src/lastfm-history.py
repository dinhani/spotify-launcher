import os
from datetime import UTC, datetime
from pathlib import Path

import polars
import pylast

from render.data import LASTFM_USER

OUT = Path(__file__).parent.parent / "data" / "scrobbles.tsv"
TIMEZONE = "America/Sao_Paulo"

# ------------------------------------------------------------------------------
# Load scrobbles already saved, to fetch only newer ones
# ------------------------------------------------------------------------------
scrobbles_saved = polars.read_csv(source=OUT, separator="\t", try_parse_dates=True) if OUT.exists() else None
time_from = int(scrobbles_saved["listened_at"].max().timestamp()) + 1 if scrobbles_saved is not None else None

# ------------------------------------------------------------------------------
# Fetch scrobbles from Last.fm, within its rate limit
# ------------------------------------------------------------------------------
network = pylast.LastFMNetwork(api_key=os.environ["LASTFM_API_KEY"])
network.enable_rate_limit()
rows = [
    {
        "listened_at": datetime.fromtimestamp(int(played.timestamp), tz=UTC),
        "artist": played.track.artist.name,
        "album": played.album,
        "track": played.track.title,
    }
    for played in network.get_user(LASTFM_USER).get_recent_tracks(limit=None, time_from=time_from, stream=True)
]

# ------------------------------------------------------------------------------
# Append to the saved scrobbles
# ------------------------------------------------------------------------------
scrobbles_new = polars.DataFrame(data=rows, schema={
    "listened_at": polars.Datetime(time_unit="us", time_zone="UTC"),
    "artist": polars.String,
    "album": polars.String,
    "track": polars.String,
})
scrobbles = (
    polars.concat([scrobbles_saved, scrobbles_new]) if scrobbles_saved is not None else scrobbles_new
).with_columns(polars.col("listened_at").dt.convert_time_zone(TIMEZONE)).sort("listened_at")

OUT.parent.mkdir(exist_ok=True)
scrobbles.write_csv(file=OUT, separator="\t", datetime_format="%Y-%m-%dT%H:%M:%S%:z")
print(f"Wrote {OUT}: {len(scrobbles)} scrobbles ({len(scrobbles_new)} new)")
