# ------------------------------------------------------------------------------
# Libraries
# ------------------------------------------------------------------------------
import sys
import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s.%(msecs)03d | %(levelname)-5s | %(message)s',
    datefmt='%H:%M:%S',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logging.info("🚀 Starting script")

from collections import defaultdict
from data import *
from dominate.tags import *
from millify import millify
import polars

# ------------------------------------------------------------------------------
# CONSTANTS
# ------------------------------------------------------------------------------
INPUT_ARTISTS = "data/artistas.tsv"
OUTPUT_LAUNCHER = "docs/index.html"
OUTPUT_SUMMARY = "docs/summary.txt"

# ------------------------------------------------------------------------------
# Parse artists tags
# ------------------------------------------------------------------------------
artists_by_tag = defaultdict(list)


logging.info(f"📄 Reading CSV file: {INPUT_ARTISTS}")
artists_df = polars.read_csv(INPUT_ARTISTS, separator="\t")

logging.info("🧱 Parsing tags")
for artist in artists_df.to_dicts():
    # parse row
    tags = set()
    genres = artist["genres"]
    if genres is None:
        genres = []
    else:
        genres = genres.split("|")

    # match genres
    for genre in genres:
        tag = TAGS.get(genre)
        if tag:
            tags.add(tag)

    # match names (positive)
    tag = TAGS.get(f"+{artist["name"]}")
    if tag:
        tags.add(tag)

    # match names (negative)
    tag = TAGS.get(f"-{artist["name"]}")
    if tag:
        tags.remove(tag)

    # specific rules
    if T_METAL_EXTREMO in tags and T_METAL_TRADICIONAL in tags:
        tags.remove(T_METAL_TRADICIONAL)
    if T_METAL_TRADICIONAL in tags or T_METAL_EXTREMO in tags:
        tags.add(T_METAL_TODOS)

    # add tags
    artist["tags"] = tags
    for tag in artist["tags"]:
        artists_by_tag[tag].append(artist)
    if len(artist["tags"]) == 0:
        artists_by_tag[T_OUTROS].append(artist)

# ------------------------------------------------------------------------------
# Generate HTML
# ------------------------------------------------------------------------------
logging.info("🧱 Generating HTML")

CSS_INLINE = """
.extra.content::after {
    display: none !important;
}
@media only screen and (max-width: 991.9px) {
    .artist-image {
        height: 200px !important;
    }
}
@media only screen and (min-width: 992px) {
    body {
        height:100%;
        overflow-y: hidden;
    }
    .artists-wrapper {
        height: 98vh;
        overflow-y: scroll;
    }
    .artist-image {
        height: 140px !important;
    }
}
"""

JS_INLINE_SORT_FUNCTION = """
function sort(button, attribute, order) {
    $(button).addClass('active');
    $(button).siblings().removeClass('active');
    $('.artists').each(function(_, artists) {
        var sorted = $(artists).find('.artist').sort(function(a, b) {
            var valA = $(a).data(attribute);
            var valB = $(b).data(attribute);

            // Check if the values are numeric
            if ($.isNumeric(valA)) {
                return order === 'asc' ? valA - valB : valB - valA; // Numeric comparison
            } else {
                return order === 'asc' ? String(valA).localeCompare(String(valB)) : String(valB).localeCompare(String(valA)); // String comparison
            }
        });
        $(artists).empty().append(sorted);
    });
}
"""

def menu_categories():
    with div(cls="ui fluid vertical menu"):
        for i, tag in enumerate(TAGS_ORDER):
            artists = artists_by_tag[tag]
            active = "active" if i == 0 else ""
            with div(cls=f"{active} item", data_tab=tab_id(tag)):
                span(f"{len(artists):02}", cls="ui tiny label")
                span(tag)

def menu_sort():
    with div(cls="ui fluid vertical menu"):
        div("🎶 Nome", cls="ui active item", onClick="sort(this, 'name', 'asc')")
        div("🔥 Popularidade", cls="ui item", onClick="sort(this, 'popularity', 'desc')")
        div("👤 Seguidores", cls="ui item", onClick="sort(this, 'followers', 'desc')")
        div("💿 Discos", cls="ui item", onClick="sort(this, 'albums', 'desc')")


def cards(artists: list[dict]):
    # scroll
    with div(cls="artists-wrapper"):
        # grid
        with div(cls="ui padded grid artists"):
            # cards
            for artist in artists:
                followers_precision = 1 if artist["followers.total"] >= 1_000_000 else 0

                with div(cls="ui eight wide mobile four wide tablet two wide computer column artist", style="padding: 0.25rem;", data_name=artist["name"], data_followers=str(artist["followers.total"]), data_popularity=str(artist["popularity"]), data_albums=str(artist["album_count"])):
                    with a(cls="ui card", href=f"spotify:artist:{artist["id"]}", style="width: 100%"):
                        # image
                        with div(cls="image"):
                            img(src=artist["image"], cls="ui image artist-image", style="object-fit: cover;")

                        # header
                        with div(cls="content", style="padding: 0.5rem;"):
                            div(artist["name"], cls="ui small header", style="white-space: nowrap; overflow:hidden; text-overflow: ellipsis;")

                        # footer
                        with div(cls="extra content", style="padding: 0.5rem; display: flex; justify-content: space-between"):
                            div("🔥" + str(artist["popularity"]), style="width: 33.333%; text-align: left;")
                            div("👤" + millify(artist["followers.total"], precision=followers_precision), style="width: 33.333%; text-align: center;")
                            div("💿" + str(artist["album_count"]), style="width: 33.333%; text-align: right")


def tab_id(tag: str) -> str:
    id = tag.lower().replace("(", "").replace(")", "").replace(":", "").replace(" ", "-").translate(str.maketrans("ãéó", "aeo"))
    return f"tab-{id}"

doc = html(style="height:100%;")
with doc:
    # head
    with head():
        meta(name="viewport", content="width=device-width, initial-scale=1")
        script(src = "https://cdn.jsdelivr.net/npm/jquery@3.7.1/dist/jquery.min.js")
        script(src = "https://cdn.jsdelivr.net/npm/jquery-address@1.6.0/src/jquery.address.js")
        script(src = "https://cdn.jsdelivr.net/npm/fomantic-ui@2.9.4/dist/semantic.min.js")
        link(href =  "https://cdn.jsdelivr.net/npm/fomantic-ui@2.9.4/dist/semantic.min.css", rel = "stylesheet")
        style(CSS_INLINE)
        script(JS_INLINE_SORT_FUNCTION)

    # body
    with body(cls="ui fluid container"):
        with div(cls="ui padded grid"):
            # ------------------------------------------------------------------
            # Menu
            # ------------------------------------------------------------------
            with div(cls="ui sixteen wide mobile two wide computer column", style="padding: 0.5rem"):
                menu_categories()
                menu_sort()

            # ------------------------------------------------------------------
            # Content
            # ------------------------------------------------------------------
            with div(cls="ui sixteen wide mobile fourteen wide computer column", style="padding: 0.5rem;"):
                # tab contents
                for tag in TAGS_ORDER:
                    artists = sorted(artists_by_tag[tag], key=lambda x: x["name"].lower())
                    active = "active" if i == 0 else ""

                    with div(cls="ui tab", data_tab=tab_id(tag)):
                        cards(artists)

    # script
    script("$('.menu .item').tab({history:true, historyType: 'hash'});")
    script("$('.ui.rating').rating();")

# write to file
logging.info(f"💾 Writing: {OUTPUT_LAUNCHER}")
with open(OUTPUT_LAUNCHER, "w", encoding="utf-8") as f:
    f.write(str(doc))

# write summary
logging.info(f"💾 Writing: {OUTPUT_SUMMARY}")
with open(OUTPUT_SUMMARY, "w", encoding="utf-8") as f:
    for tag in TAGS_ORDER:
        f.write("\n")
        f.write(tag + ":\n")
        for artist in artists_by_tag[tag]:
            f.write("* " + artist["name"] + "\n")

logging.info("✅ Done")