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
download:
    python src/artists-download.py
alias dl := download

# Export Spotify data to TSV
[group("run")]
export:
    python src/artists-export.py
