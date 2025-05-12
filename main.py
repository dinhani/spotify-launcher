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
from dominate.util import raw
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
    tagged = {T_ALL}

    # match genres
    for genre in genres:
        tag = TAGS.get(genre)
        if tag:
            tagged.add(tag)

    # match names (positive)
    tag = TAGS.get(f"+{artist["name"]}")
    if tag:
        tagged.add(tag)

    # match names (negative)
    tag = TAGS.get(f"-{artist["name"]}")
    if tag:
        tagged.remove(tag)

    # match other tags
    for tagged_tag in tagged.copy():
        tag = TAGS.get(tagged_tag)
        if tag:
            tagged.add(tag)

    # rule: extreme cannot be traditional
    if T_ROCK_EXTREME in tagged and T_ROCK_TRADITIONAL in tagged:
        tagged.remove(T_ROCK_TRADITIONAL)

    # add tags
    artist["tags"] = tagged
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
    div::-webkit-scrollbar {
        display: none;
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

JS_FUNC_REMOVE_EMOJI = """
function removeEmoji(s) {
    return s.replace(/[\\p{Emoji_Presentation}\\p{Extended_Pictographic}]/gu, '').trim()
}
"""

JS_FUNC_ONTAB = """
function onTab(tabPath) {
    // change header
    var id = "#mobile-menu-item-" + tabPath.replace("tab-", "");
    var title = removeEmoji($(id).data("tab-name")).replace("::", " (") + ")";
    $("#mobile-menu-header-filter").text("Filter: " + title)
}
"""

JS_FUNC_SORT = """
function sort(element, attribute, order) {
    // change header
    var title = removeEmoji($(element).text());
    $("#mobile-menu-header-sort").text("Sort: " + title);

    // mark active
    $(element).addClass('active');
    $(element).siblings().removeClass('active');

    // reorder
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

def menu_filter(mobile: bool):
    with menu_wrapper(mobile, "Filter", "filter"):
        kind = "mobile" if mobile else "desktop"
        label_size = "" if mobile else "tiny"

        for index, tag in enumerate(TAGS_ORDER):
            artists = artists_by_tag[tag]

            item_display = tag.split("::")[-1]
            item_active = "active" if index == 0 else ""
            item_header = "header disabled" if tag.startswith("Header::") else ""

            with div(cls=f"{item_active} {item_header} link item",
                    id=f"{kind}-menu-item-{id(tag)}",
                    data_tab=tab_id(tag),
                    data_tab_name=tag
                ):
                span(item_display)
                if not item_header:
                    span(f"{len(artists)}", cls=f"ui {label_size} label")

def menu_sort(mobile):
    label = "Sort: Name" if mobile else "Sort"
    with menu_wrapper(mobile, label, "sort"):
        div("🎶 Name", cls="ui active link item", onClick="sort(this, 'name', 'asc')", style=CSS_STYLE_NOWRAP)
        div("🔥 Popularity (artist)", cls="ui link item", onClick="sort(this, 'popularity', 'desc')", style=CSS_STYLE_NOWRAP)
        div("🏆 Popularity (song)", cls="ui link item", onClick="sort(this, 'song-popularity', 'desc')", style=CSS_STYLE_NOWRAP)
        div("👤 Followers", cls="ui link item", onClick="sort(this, 'followers', 'desc')", style=CSS_STYLE_NOWRAP)
        div("💿 Albums", cls="ui link item", onClick="sort(this, 'albums', 'desc')", style=CSS_STYLE_NOWRAP)
        div("📅 Last Release", cls="ui link item", onClick="sort(this, 'last-release', 'desc')", style=CSS_STYLE_NOWRAP)
        div("🔔 Last Follow", cls="ui link item", onClick="sort(this, 'last-follow', 'asc')", style=CSS_STYLE_NOWRAP)

def menu_wrapper(mobile: bool, label: str, id: str):
    active = "" if mobile else "active"
    kind = "mobile" if mobile else "desktop"
    font_size = "1.71428571rem" if mobile else "1.28571429rem"

    with div(cls=f"{active} title", style=f"font-size: {font_size};"):
            span(label, id=f"{kind}-menu-header-{id}")
            i(cls="right dropdown icon")

    with div(cls=f"{active} content", style="padding: 0;"):
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
                        data_song_popularity=str(artist["top_song_popularity"]),
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
                            div(artist["name"], cls="ui small header", style=f"{CSS_STYLE_NOWRAP} overflow:hidden; text-overflow: ellipsis; margin-bottom: 0.25rem")
                            with div(cls="meta"):
                                div(artist["top_song"], style=f"{CSS_STYLE_NOWRAP} overflow:hidden; text-overflow: ellipsis;")

                        # footer
                        with div(cls="extra content", style="padding: 0.5rem 0.5rem; display: flex; flex-wrap: nowrap; justify-content: space-between"):
                            div("🔥" + str(artist["popularity"]), style=CSS_STYLE_NOWRAP)
                            div("👤" + millify(artist["followers.total"], precision=followers_precision), style=CSS_STYLE_NOWRAP)
                            div("💿" + str(artist["album_count"]), style=CSS_STYLE_NOWRAP)


def id(tag: str) -> str:
    return tag.lower().replace("::", "-").translate(str.maketrans("", "", "():/")).translate(str.maketrans("ãéó", "aeo")).replace(" ", "-").strip()

def tab_id(tag: str) -> str:
    return f"tab-{id(tag)}"

doc = html(style="height:100%;")
with doc:
    # head
    with head():
        meta(name="viewport", content="width=device-width, initial-scale=1")
        script(src = "https://cdn.jsdelivr.net/npm/jquery@3.7.1/dist/jquery.min.js")
        script(src = "https://cdn.jsdelivr.net/npm/jquery-address@1.6.0/src/jquery.address.js")
        script(src = "https://cdn.jsdelivr.net/npm/fomantic-ui@2.9.4/dist/semantic.min.js")
        link(href =  "https://cdn.jsdelivr.net/npm/fomantic-ui@2.9.4/dist/semantic.min.css", rel = "stylesheet")
        style(raw(CSS_GLOBAL))
        script(raw(JS_FUNC_REMOVE_EMOJI))
        script(raw(JS_FUNC_ONTAB))
        script(raw(JS_FUNC_SORT))

    # body
    with body(cls="ui fluid container"):
        with div(cls="ui padded grid"):
            # ------------------------------------------------------------------
            # Menu (mobile)
            # ------------------------------------------------------------------
            with div(cls="sixteen wide mobile tablet only   column", style="padding: 0.5rem"):
                with div(cls="ui fluid styled mobile accordion"):
                    menu_filter(mobile=True)
                    menu_sort(mobile=True)

            # ------------------------------------------------------------------
            # Menu (desktop)
            # ------------------------------------------------------------------
            with div(cls="computer only three wide computer   two wide large screen   two wide widescreen   column", style="padding: 0.5rem"):
                with div(cls="ui fluid styled desktop accordion", style="max-height: 98vh; overflow: hidden; overflow-y: scroll"):
                    menu_filter(mobile=False)
                    menu_sort(mobile=False)

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
    script("$('.menu .item').tab({history:true, historyType: 'hash', onLoad: onTab});")
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