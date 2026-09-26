import os
import json
from pathlib import Path
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from tqdm import tqdm

DATA_DIR = Path(__file__).parent.parent / "data"
CACHE_DIR = DATA_DIR / "artists"
CACHE_DIR.mkdir(parents=True, exist_ok=True)

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
# Download raw data per artist (cached)
# ------------------------------------------------------------------------------
progress = tqdm(iterable=artists, desc="Downloading")
for artist in progress:
    # log
    progress.set_postfix_str(s=artist["name"])

    # check exist
    artist_file = CACHE_DIR / f"{artist['id']}.json"
    if artist_file.exists():
        continue

    # download
    albums_page = sp.artist_albums(artist_id=artist["id"], album_type="album", limit=50)
    albums = albums_page["items"]
    while albums_page["next"]:
        albums_page = sp.next(albums_page)
        albums.extend(albums_page["items"])

    data = {
        "artist": artist,
        "albums": albums,
        "top_tracks": sp.artist_top_tracks(artist_id=artist["id"], country="US")["tracks"],
    }
    artist_file.write_text(data=json.dumps(obj=data, ensure_ascii=False, indent=2), encoding="utf-8")
