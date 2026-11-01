set windows-shell := ["pwsh.exe", "-NoLogo", "-Command"]
export UV_PROJECT_ENVIRONMENT := data_local_directory() / "uv" / "envs" / "spotify-launcher"


# List tasks
[group("project")]
default:
    @just --list --unsorted

# Install dependencies
[group("project")]
setup:
    uv sync

# List line counts
[group("project")]
cloc:
    cloc src

# Render page
[group("run")]
render:
    uv run src/artists-render.py
    Start-Process Z:/apps/web/spotify-launcher.html
alias run := render

# Download all datasources
[group("data")]
update: spotify-download lastfm-download export

# Download Spotify artists
[group("data")]
spotify-download *args:
    uv run src/artists-download.py {{args}}
alias sd := spotify-download

# Import Spotify history
[group("data")]
spotify-import *export_dir:
    uv run src/spotify-history.py {{export_dir}}

# Download Last.fm history
[group("data")]
lastfm-download:
    uv run src/lastfm-history.py

# Compare Last.fm artists with Spotify artists
[group("data")]
lastfm-compare:
    uv run src/artists-lastfm.py

# Export artists to TSV
[group("data")]
export:
    uv run src/artists-export.py
