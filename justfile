set windows-shell := ["pwsh.exe", "-NoLogo", "-Command"]


# List available tasks
[group("project")]
default:
    @just --list --unsorted

# Install Python dependencies
[group("project")]
setup:
    python -m pip install -r requirements.txt

# Render static artists page
[group("run")]
render:
    python src/artists-render.py
    Start-Process docs/index.html
alias run := render

# Download Spotify data
[group("run")]
download *args:
    python src/artists-download.py {{args}}
alias dl := download

# Export Spotify data to TSV
[group("run")]
export:
    python src/artists-export.py

# Compare Last.fm top artists with followed artists
[group("run")]
lastfm:
    python src/artists-lastfm.py

# Extract Spotify extended streaming history to data/spotify-history.tsv
[group("run")]
spotify-history *export_dir:
    python src/spotify-history.py {{export_dir}}

# Fetch Last.fm scrobbles to data/lastfm-history.tsv (only new ones after the first run)
[group("run")]
lastfm-history:
    python src/lastfm-history.py
