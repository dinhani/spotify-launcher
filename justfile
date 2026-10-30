set windows-shell := ["pwsh.exe", "-NoLogo", "-Command"]
export UV_PROJECT_ENVIRONMENT := data_local_directory() / "uv" / "envs" / "spotify-launcher"


# List available tasks
[group("project")]
default:
    @just --list --unsorted

# Install Python dependencies
[group("project")]
setup:
    uv sync

# Render static artists page
[group("run")]
render:
    uv run src/artists-render.py
    Start-Process docs/index.html
alias run := render

# Download and export all data for a new render
[group("data")]
update: spotify-download lastfm-download export

# Download Spotify data
[group("data")]
spotify-download *args:
    uv run src/artists-download.py {{args}}
alias sd := spotify-download

# Extract Spotify extended streaming history to data/spotify-history.tsv
[group("data")]
spotify-import *export_dir:
    uv run src/spotify-history.py {{export_dir}}

# Fetch Last.fm scrobbles to data/lastfm-history.tsv (only new ones after the first run)
[group("data")]
lastfm-download:
    uv run src/lastfm-history.py

# Compare Last.fm top artists with followed artists
[group("data")]
lastfm-compare:
    uv run src/artists-lastfm.py

# Export Spotify data to TSV
[group("data")]
export:
    uv run src/artists-export.py
