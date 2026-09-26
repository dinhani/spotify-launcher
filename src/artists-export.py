import json
from collections import Counter
from pathlib import Path

import polars

DATA_DIR = Path(__file__).parent.parent / "data"
CACHE_DIR = DATA_DIR / "artists"

FIRST_RELEASE_OVERRIDES = {
    "Agnes Obel": "2010-10-04",
}

# ------------------------------------------------------------------------------
# Load followed list (defines rank)
# ------------------------------------------------------------------------------
artists = json.loads(s=(DATA_DIR / "followed.json").read_text(encoding="utf-8"))
rank = {artist["id"]: i + 1 for i, artist in enumerate(artists)}

# ------------------------------------------------------------------------------
# Parse cached data → TSV
# ------------------------------------------------------------------------------
rows = []
for artist in artists:
    data = json.loads(s=(CACHE_DIR / f"{artist['id']}.json").read_text(encoding="utf-8"))
    artist, albums, tracks = data["artist"], data["albums"], data["top_tracks"]

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
        "albums": len(albums),
        "first_release": FIRST_RELEASE_OVERRIDES.get(artist["name"]) or min((al.get("release_date", "") for al in albums), default=""),
        "last_release": max((al.get("release_date", "") for al in albums), default=""),
        "top_song": tracks[0]["name"] if tracks else "",
        "top_song_popularity": tracks[0]["popularity"] if tracks else 0,
        "last_follow": rank[artist["id"]],
    })

rows.sort(key=lambda r: r["name"])
out = DATA_DIR / "artistas.tsv"
polars.DataFrame(data=rows).write_csv(file=out, separator="\t")
print(f"Wrote {out}")
