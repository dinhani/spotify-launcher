import json
import re
from collections import Counter
from pathlib import Path

import polars

DATA_DIR = Path(__file__).parent.parent / "data"
CACHE_DIR = DATA_DIR / "artists"

FIRST_RELEASE_OVERRIDES = {
    "Agnes Obel": "2010-10-04",
}

ALBUM_NAME_SUFFIX = re.compile(r"\s*(?:[\(\[][^\)\]]*[\)\]]|\s-\s.*)$")
ALBUM_EDITION_WORDS = re.compile(r"deluxe|edition|version|remaster|re-?issue|bonus|expanded|anniversary|extended|\bmix\b|soundtrack|instrumentals?|commentary|without dialogue", re.IGNORECASE)
ALBUM_NON_STUDIO_WORDS = re.compile(r"\blive\b|ao vivo|\bdemos?\b|greatest|best of|\bhits\b|collection|anthology|b-sides|rarities|music from the motion picture", re.IGNORECASE)

def parse_album_title(name: str) -> str:
    while (suffix := ALBUM_NAME_SUFFIX.search(name)) and ALBUM_EDITION_WORDS.search(suffix.group()):
        name = name[:suffix.start()]
    return re.sub(r"\W+", " ", name).strip().casefold()

# ------------------------------------------------------------------------------
# Load followed list (defines rank)
# ------------------------------------------------------------------------------
artists = json.loads(s=(DATA_DIR / "followed.json").read_text(encoding="utf-8"))
rank = {artist["id"]: i + 1 for i, artist in enumerate(artists)}

# ------------------------------------------------------------------------------
# Find albums listened as albums: 5+ distinct tracks of the same album in a row, covering 80%+ of the album
# ------------------------------------------------------------------------------
album_sizes = polars.DataFrame(
    data=[
        {"artist_key": artist["name"].casefold(), "album": album["name"], "album_title": parse_album_title(album["name"]), "size": album["total_tracks"]}
        for artist in artists
        for album in json.loads(s=(CACHE_DIR / f"{artist['id']}.json").read_text(encoding="utf-8"))["albums"]
    ],
    schema={"artist_key": polars.String, "album": polars.String, "album_title": polars.String, "size": polars.Int64},
)
streams = (
    polars.read_csv(source=DATA_DIR / "streams.tsv", separator="	", try_parse_dates=True)
    .sort("ended_at")
    .with_columns(
        artist_key=polars.col("artist").map_elements(str.casefold, return_dtype=polars.String),
        album_title=polars.col("album").map_elements(parse_album_title, return_dtype=polars.String),
    )
    .with_columns(session=polars.struct("artist_key", "album_title").rle_id())
)
album_sessions = (
    streams
    .group_by("session", "artist_key", "album_title")
    .agg(album=polars.col("album").mode().first(), tracks=polars.col("track").n_unique())
    .join(album_sizes.select("artist_key", "album", size_album="size"), on=["artist_key", "album"], how="left")
    .join(album_sizes.group_by("artist_key", "album_title").agg(size_title=polars.col("size").min()), on=["artist_key", "album_title"], how="left")
    .join(streams.group_by("artist_key", "album_title").agg(size_history=polars.col("track").n_unique()), on=["artist_key", "album_title"], how="left")
    .with_columns(size=polars.coalesce("size_album", "size_title", "size_history"))
    .filter(polars.col("tracks") >= 5, polars.col("tracks") >= 0.8 * polars.col("size"))
)
albums_listened = dict(
    album_sessions
    .group_by("artist_key", "album_title")
    .agg(sessions=polars.len(), album=polars.col("album").mode().first())
    .sort("sessions", "album", descending=[True, False])
    .group_by("artist_key", maintain_order=True)
    .agg(polars.col("album").str.join("|"))
    .iter_rows()
)

# ------------------------------------------------------------------------------
# Parse cached data → TSV
# ------------------------------------------------------------------------------
rows = []
for artist in artists:
    data = json.loads(s=(CACHE_DIR / f"{artist['id']}.json").read_text(encoding="utf-8"))
    artist, albums, tracks = data["artist"], data["albums"], data["top_tracks"]
    albums_studio = [album for album in albums if not ALBUM_NON_STUDIO_WORDS.search(album["name"])]
    album_release_dates: dict[str, str] = {}
    for album in albums_studio:
        title = parse_album_title(album["name"])
        album_release_dates[title] = min(album_release_dates.get(title, album["release_date"]), album["release_date"])
    album_release_dates_original = {
        title: release_date for title, release_date in album_release_dates.items()
        if not any(title.startswith(other + " ") and ALBUM_EDITION_WORDS.search(title[len(other):]) for other in album_release_dates)
    }

    # find last album (original edition of the latest studio album)
    last_title = max(album_release_dates_original, key=lambda title: album_release_dates_original[title], default=None)
    last_album = min(
        (album for album in albums_studio if parse_album_title(album["name"]) == last_title and album.get("images")),
        key=lambda album: album["release_date"], default=None,
    )

    # find top album
    top_albums = [
        track["album"] for track in tracks
        if track["album"].get("images") and any(album_artist["id"] == artist["id"] for album_artist in track["album"]["artists"])
    ]
    top_album_tracks = Counter(album["id"] for album in top_albums)
    top_album = max(top_albums, key=lambda album: top_album_tracks[album["id"]], default=None)

    rows.append({
        "id": artist["id"],
        "name": artist["name"],
        "genres": "|".join(artist.get("genres", [])),
        "popularity": artist["popularity"],
        "followers": artist["followers"]["total"],
        "image": artist["images"][0]["url"] if artist.get("images") else "",
        "top_album_name": top_album["name"] if top_album else "",
        "top_album_image": top_album["images"][0]["url"] if top_album else "",
        "albums": len(album_release_dates_original),
        "albums_listened": albums_listened.get(artist["name"].casefold(), ""),
        "first_release": FIRST_RELEASE_OVERRIDES.get(artist["name"]) or min(album_release_dates_original.values(), default=""),
        "last_release": max(album_release_dates_original.values(), default=""),
        "last_release_name": last_album["name"] if last_album else "",
        "last_release_image": last_album["images"][0]["url"] if last_album else "",
        "top_song": tracks[0]["name"] if tracks else "",
        "top_song_popularity": tracks[0]["popularity"] if tracks else 0,
        "last_follow": rank[artist["id"]],
    })

rows.sort(key=lambda r: r["name"])
out = DATA_DIR / "artists.tsv"
polars.DataFrame(data=rows).write_csv(file=out, separator="\t")
print(f"Wrote {out}")
