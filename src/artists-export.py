import json
from pathlib import Path
import polars

DATA_DIR = Path(__file__).parent.parent / "data"
CACHE_DIR = DATA_DIR / "artists"

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
    artist, albums, top = data["artist"], data["albums"], data["top_tracks"]
    cover_album = max(
        (album for album in albums if album.get("images")),
        key=lambda album: album.get("release_date", ""),
        default=None,
    )
    rows.append({
        "id": artist["id"],
        "name": artist["name"],
        "genres": "|".join(artist.get("genres", [])),
        "popularity": artist["popularity"],
        "followers": artist["followers"]["total"],
        "image": artist["images"][0]["url"] if artist.get("images") else "",
        "album_image": cover_album["images"][0]["url"] if cover_album else "",
        "albums": len(albums),
        "last_release": max((al.get("release_date", "") for al in albums), default=""),
        "top_song": top[0]["name"] if top else "",
        "top_song_popularity": top[0]["popularity"] if top else 0,
        "last_follow": rank[artist["id"]],
    })

rows.sort(key=lambda r: r["name"])
out = DATA_DIR / "artistas.tsv"
polars.DataFrame(data=rows).write_csv(file=out, separator="\t")
print(f"Wrote {out}")
