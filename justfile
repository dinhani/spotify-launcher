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

# Render the page
[group("run")]
render:
    uv run src/artists-render.py
    Start-Process docs/index.html
alias run := render

# Update all data
[group("data")]
update: spotify-download lastfm-download export

# Download followed artists
[group("data")]
spotify-download *args:
    uv run src/artists-download.py {{args}}
alias sd := spotify-download

# Import the streaming history export
[group("data")]
spotify-import *export_dir:
    uv run src/spotify-history.py {{export_dir}}

# Download listening history
[group("data")]
lastfm-download:
    uv run src/lastfm-history.py

# Compare top artists with followed
[group("data")]
lastfm-compare:
    uv run src/artists-lastfm.py

# Export artists to TSV
[group("data")]
export:
    uv run src/artists-export.py
