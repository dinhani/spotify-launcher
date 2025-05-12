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
    genres = artist["genres"]
    if genres is None:
        genres = []
    else:
        genres = genres.split("|")
    tags = {T_ALL}

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
    if T_METAL_EXTREME in tags and T_METAL_TRADITIONAL in tags:
        tags.remove(T_METAL_TRADITIONAL)
    if T_METAL_TRADITIONAL in tags or T_METAL_EXTREME in tags:
        tags.add(T_METAL_ALL)

    # add tags
    artist["tags"] = tags
    for tag in artist["tags"]:
        artists_by_tag[tag].append(artist)
    if len(artist["tags"]) == 1:
        artists_by_tag[T_OTHERS].append(artist)

# ------------------------------------------------------------------------------
# Generate HTML
# ------------------------------------------------------------------------------
logging.info("🧱 Generating HTML")

CSS_STYLE_NOWRAP = "white-space: nowrap; "

CSS_GLOBAL = """
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
    .artists-wrapper::-webkit-scrollbar {
        display: none;
    }
    .artist-image {
        height: 140px !important;
    }
}
"""

JS_FUNC_SORT = """
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

def menu_category(mobile: bool):
    with menu_wrapper(mobile, "Category"):
        label_size = "" if mobile else "tiny"
        for index, tag in enumerate(TAGS_ORDER):
            artists = artists_by_tag[tag]
            active = "active" if index == 0 else ""
            with div(cls=f"{active} link item", data_tab=tab_id(tag)):
                span(f"{len(artists)}", cls=f"ui {label_size} label")
                span(tag)

def menu_sorting(mobile):
    with menu_wrapper(mobile, "Sorting"):
        div("🎶 Name", cls="ui active link item", onClick="sort(this, 'name', 'asc')", style=CSS_STYLE_NOWRAP)
        div("🔥 Popularity", cls="ui link item", onClick="sort(this, 'popularity', 'desc')", style=CSS_STYLE_NOWRAP)
        div("👤 Followers", cls="ui link item", onClick="sort(this, 'followers', 'desc')", style=CSS_STYLE_NOWRAP)
        div("💿 Albums", cls="ui link item", onClick="sort(this, 'albums', 'desc')", style=CSS_STYLE_NOWRAP)
        div("🔔 Last Follow", cls="ui link item", onClick="sort(this, 'last-follow', 'asc')", style=CSS_STYLE_NOWRAP)
        div("📅 Last Release", cls="ui link item", onClick="sort(this, 'last-release', 'desc')", style=CSS_STYLE_NOWRAP)

def menu_wrapper(mobile: bool, label: str):
    active = "" if mobile else "active"
    font_size = "1.71428571rem" if mobile else "1.28571429rem"
    with div(cls=f"{active} title", style=f"font-size: {font_size};"):
            span(label)
            i(cls="right dropdown icon")
    with div(cls=f"{active} content", style="padding: 0rem;"):
        return div(cls="ui fluid vertical attached menu", style="margin: 0; border-left: 0; border-right: 0; border-bottom: 0;")

def cards(artists: list[dict]):
    # scroll
    with div(cls="artists-wrapper"):
        # grid
        with div(cls="ui padded grid artists"):
            # cards
            for artist in artists:
                followers_precision = 1 if artist["followers.total"] >= 1_000_000 else 0

                with div(cls="eight wide mobile   four wide tablet   four wide computer   two wide large screen  two wide widescreen   column   artist", style="padding: 0.25rem;",
                        data_name=artist["name"],
                        data_followers=str(artist["followers.total"]),
                        data_popularity=str(artist["popularity"]),
                        data_albums=str(artist["album_count"]),
                        data_last_release=str(artist["last_release"]),
                        data_last_follow=str(artist["last_follow"]),
                    ):
                    with a(cls="ui card", href=f"spotify:artist:{artist["id"]}", style="width: 100%"):
                        # image
                        with div(cls="image"):
                            img(src=artist["image"], cls="ui image artist-image", style="object-fit: cover;")

                        # header
                        with div(cls="content", style="padding: 0.5rem;"):
                            div(artist["name"], cls="ui small header", style=f"{CSS_STYLE_NOWRAP} overflow:hidden; text-overflow: ellipsis;")

                        # footer
                        with div(cls="extra content", style="padding: 0.5rem 0.5rem; display: flex; flex-wrap: nowrap; justify-content: space-between"):
                            div("🔥" + str(artist["popularity"]), style=CSS_STYLE_NOWRAP)
                            div("👤" + millify(artist["followers.total"], precision=followers_precision), style=CSS_STYLE_NOWRAP)
                            div("💿" + str(artist["album_count"]), style=CSS_STYLE_NOWRAP)


def tab_id(tag: str) -> str:
    id = tag.lower().translate(str.maketrans("", "", "():/")).translate(str.maketrans("ãéó", "aeo")).replace(" ", "-").strip()
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
        style(CSS_GLOBAL)
        script(JS_FUNC_SORT)

    # body
    with body(cls="ui fluid container"):
        with div(cls="ui padded grid"):
            # ------------------------------------------------------------------
            # Menu (mobile)
            # ------------------------------------------------------------------
            with div(cls="sixteen wide mobile tablet only   column", style="padding: 0.5rem"):
                with div(cls="ui fluid styled mobile accordion"):
                    menu_category(mobile=True)
                    menu_sorting(mobile=True)

            # ------------------------------------------------------------------
            # Menu (desktop)
            # ------------------------------------------------------------------
            with div(cls="computer only three wide computer   two wide large screen   two wide widescreen   column", style="padding: 0.5rem"):
                with div(cls="ui fluid styled desktop accordion"):
                    menu_category(mobile=False)
                    menu_sorting(mobile=False)

            # ------------------------------------------------------------------
            # Content
            # ------------------------------------------------------------------
            with div(cls="sixteen wide mobile tablet   thirteen wide computer   fourteen wide large screen   fourteen wide widescreen   column", style="padding: 0.5rem;"):
                # tab contents
                for tag in TAGS_ORDER:
                    artists = sorted(artists_by_tag[tag], key=lambda x: x["name"].lower())
                    active = "active" if i == 0 else ""

                    with div(cls="ui tab", data_tab=tab_id(tag)):
                        cards(artists)

            # ------------------------------------------------------------------
            # Scroll to top
            # ------------------------------------------------------------------
            with div(cls="sixteen wide column mobile tablet only"):
                div("⬆️ Back to top", cls="ui fluid massive button", onClick="window.scrollTo({top:0})")


    # script
    script("$('.menu .item').tab({history:true, historyType: 'hash'});")
    script("$('.ui.accordion.desktop').accordion({exclusive:false});")
    script("$('.ui.accordion.mobile').accordion({exclusive:true});")

# write to file
logging.info(f"💾 Writing: {OUTPUT_LAUNCHER}")
with open(OUTPUT_LAUNCHER, "w", encoding="utf-8", newline="\n") as f:
    f.write(str(doc))

# write summary
logging.info(f"💾 Writing: {OUTPUT_SUMMARY}")
with open(OUTPUT_SUMMARY, "w", encoding="utf-8", newline="\n") as f:
    for tag in TAGS_ORDER:
        f.write("\n")
        f.write(tag + ":\n")
        for artist in artists_by_tag[tag]:
            f.write("* " + artist["name"] + "\n")

logging.info("✅ Done")