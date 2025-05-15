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
OUTPUT_SUMMARY_FAVORITES = "docs/summary-favorites.txt"
OUTPUT_SUMMARY_TAGS = "docs/summary-tags.txt"

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

# write summaries to file
logging.info(f"💾 Writing: {OUTPUT_SUMMARY_TAGS}")
with open(OUTPUT_SUMMARY_TAGS, "w", encoding="utf-8", newline="\n") as f:
    for tag in TAGS_MENU_ORDER:
        if tag in TAGS_UMBRELLA:
            continue
        f.write(f"\n{tag}:\n")
        for artist in tags_with_artists[tag]:
            f.write("* " + artist["name"] + "\n")

logging.info(f"💾 Writing: {OUTPUT_SUMMARY_FAVORITES}")
with open(OUTPUT_SUMMARY_FAVORITES, "w", encoding="utf-8", newline="\n") as f:
    f.write(f"{T_FAVORITES}\n")
    for artist in tags_with_artists[T_FAVORITES]:
        f.write("* " + artist["name"] + "\n")

# verify untouched keys
logging.info("🧱 Checking untouched keys")
for key in TAGS_ALL.untouched_keys():
    logging.warning(f"🛑 Untouched key: {key}")

logging.info("✅ Done")