# ------------------------------------------------------------------------------
# Libraries
# ------------------------------------------------------------------------------
import sys
import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s.%(msecs)03d | %(levelname).4s | %(message)s',
    datefmt='%H:%M:%S',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logging.info("🚀 Starting script")

from data import *
import parser
import renderer

# ------------------------------------------------------------------------------
# CONSTANTS
# ------------------------------------------------------------------------------
INPUT_ARTISTS = "data/artistas.tsv"
OUTPUT_LAUNCHER = "docs/index.html"
OUTPUT_SUMMARY = "docs/summary.txt"

# ------------------------------------------------------------------------------
# Execution
# ------------------------------------------------------------------------------
# parse / render
tags_with_artists = parser.parse(INPUT_ARTISTS)
doc = renderer.render_html(tags_with_artists)

# write html to file
logging.info(f"💾 Writing: {OUTPUT_LAUNCHER}")
with open(OUTPUT_LAUNCHER, "w", encoding="utf-8", newline="\n") as f:
    f.write(str(doc))

# write summary to file
logging.info(f"💾 Writing: {OUTPUT_SUMMARY}")
with open(OUTPUT_SUMMARY, "w", encoding="utf-8", newline="\n") as f:
    for tag in TAGS_MENU_ORDER:
        if tag not in TAGS_GRANULAR:
            continue
        f.write(f"\n{tag}:\n")
        for artist in tags_with_artists[tag]:
            f.write("* " + artist["name"] + "\n")

# verify untouched keys
logging.info("🧱 Checking untouched keys")
for key in TAGS_ALL.untouched_keys():
    logging.warning(f"🛑 Untouched key: {key}")

logging.info("✅ Done")