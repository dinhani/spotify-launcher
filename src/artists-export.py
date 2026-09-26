import json
from pathlib import Path
import polars
from collections import Counter

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
    artist, albums, tracks = data["artist"], data["albums"], data["top_tracks"]

    # find top album
    top_albums = Counter([(track["album"]["name"], track["album"]["images"][0]["url"]) for track in tracks])
    if len(top_albums) > 0:
        top_album_name, top_album_image = top_albums.most_common(1)[0][0]
    else:
        top_album_name, top_album_image = "", ""

    rows.append({
        "id": artist["id"],
        "name": artist["name"],
        "genres": "|".join(artist.get("genres", [])),
        "popularity": artist["popularity"],
        "followers": artist["followers"]["total"],
        "image": artist["images"][0]["url"] if artist.get("images") else "",
        "top_album_name": top_album_name or "",
        "top_album_image": top_album_image or "",
        "albums": len(albums),
        "last_release": max((al.get("release_date", "") for al in albums), default=""),
        "top_song": tracks[0]["name"] if tracks else "",
        "top_song_popularity": tracks[0]["popularity"] if tracks else 0,
        "last_follow": rank[artist["id"]],
    })

rows.sort(key=lambda r: r["name"])
out = DATA_DIR / "artistas.tsv"
polars.DataFrame(data=rows).write_csv(file=out, separator="\t")
print(f"Wrote {out}")
