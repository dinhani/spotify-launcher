set windows-shell := ["pwsh.exe", "-NoLogo", "-Command"]
export UV_PROJECT_ENVIRONMENT := if env("UV_ENVS", "") != "" { env("UV_ENVS") / "spotify-launcher" } else { ".venv" }


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

# Download Spotify data
[group("run")]
download *args:
    uv run src/artists-download.py {{args}}
alias dl := download

# Export Spotify data to TSV
[group("run")]
export:
    uv run src/artists-export.py

# Compare Last.fm top artists with followed artists
[group("run")]
lastfm:
    uv run src/artists-lastfm.py

# Extract Spotify extended streaming history to data/spotify-history.tsv
[group("run")]
spotify-history *export_dir:
    uv run src/spotify-history.py {{export_dir}}

# Fetch Last.fm scrobbles to data/lastfm-history.tsv (only new ones after the first run)
[group("run")]
lastfm-history:
    uv run src/lastfm-history.py
