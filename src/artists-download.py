import argparse
import os
import json
from datetime import UTC, datetime, timedelta
from pathlib import Path
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from tqdm import tqdm

DATA_DIR = Path(__file__).parent.parent / "data"
CACHE_DIR = DATA_DIR / "artists"
CACHE_DIR.mkdir(parents=True, exist_ok=True)
CACHE_AGE_MAX = timedelta(days=30)

parser = argparse.ArgumentParser(description="Download followed artists and cache their albums and top tracks.")
parser.add_argument("--refresh", action="store_true", help="download albums and top tracks again for every artist, not only new or older than 30 days")
args = parser.parse_args()

# ------------------------------------------------------------------------------
# Login
# ------------------------------------------------------------------------------
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=os.getenv("SPOTIFY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"),
    redirect_uri="http://127.0.0.1:8888/callback",
    scope="user-follow-read",
    cache_path=".spotipy-cache",
))

# ------------------------------------------------------------------------------
# Fetch followed list (always fresh, defines rank)
# ------------------------------------------------------------------------------
artists, after = [], None
while True:
    page = sp.current_user_followed_artists(limit=50, after=after)["artists"]
    artists.extend(page["items"])
    after = (page.get("cursors") or {}).get("after")
    if not after:
        break

(DATA_DIR / "followed.json").write_text(
    data=json.dumps(obj=artists, ensure_ascii=False, indent=2),
    encoding="utf-8",
)

# ------------------------------------------------------------------------------
# Download raw data per artist (cached for 30 days; --refresh downloads again)
# ------------------------------------------------------------------------------
progress = tqdm(iterable=artists, desc="Refreshing" if args.refresh else "Downloading")
for artist in progress:
    # log
    progress.set_postfix_str(s=artist["name"])

    # cached: the followed list is always fresh, so keep followers and popularity current at no extra cost
    artist_file = CACHE_DIR / f"{artist['id']}.json"
    data = json.loads(s=artist_file.read_text(encoding="utf-8")) if artist_file.exists() else {}
    downloaded_at = datetime.fromisoformat(data["downloaded_at"]) if "downloaded_at" in data else None
    if downloaded_at and datetime.now(UTC) - downloaded_at < CACHE_AGE_MAX and not args.refresh:
        if data["artist"] != artist:
            data["artist"] = artist
            artist_file.write_text(data=json.dumps(obj=data, ensure_ascii=False, indent=2), encoding="utf-8")
        continue

    # download
    albums_page = sp.artist_albums(artist_id=artist["id"], album_type="album", limit=50)
    albums = albums_page["items"]
    while albums_page["next"]:
        albums_page = sp.next(albums_page)
        albums.extend(albums_page["items"])

    data = {
        "downloaded_at": datetime.now(UTC).isoformat(timespec="seconds"),
        "artist": artist,
        "albums": albums,
        "top_tracks": sp.artist_top_tracks(artist_id=artist["id"], country="US")["tracks"],
    }
    artist_file.write_text(data=json.dumps(obj=data, ensure_ascii=False, indent=2), encoding="utf-8")
