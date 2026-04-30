set windows-shell := ["pwsh.exe", "-NoLogo", "-Command"]


# List available tasks
[group("project")]
default:
    @just --list --unsorted

# Render static artists page
[group("run")]
render:
    python src/artists-render.py

# Download Spotify data
[group("run")]
download:
    python src/artists-download.py

# Export Spotify data to TSV
[group("run")]
export:
    python src/artists-export.py
