# ------------------------------------------------------------------------------
# Libraries
# ------------------------------------------------------------------------------
from data import *
from dominate.tags import *
from dominate.util import raw
from millify import millify
import logging

# ------------------------------------------------------------------------------
# Constants
# ------------------------------------------------------------------------------
CSS_STYLE_NOWRAP = "white-space: nowrap; "

CSS_STYLE_MENU_ITEM = CSS_STYLE_NOWRAP + "padding: 0.75rem; "

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
    var title = removeEmoji($(id).data("tab-name"));
    $("#mobile-menu-header-filter").text("Filter: " + title)
}
"""

_JS_FUNC_SORT = """
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

# ------------------------------------------------------------------------------
# Functions
# ------------------------------------------------------------------------------
def id(tag: str) -> str:
    """Parse any str to HTML identifier."""
    return tag.lower().translate(str.maketrans("", "", "():/")).translate(str.maketrans("ãéó", "aeo")).replace(" - ", "-").replace(" ", "-").strip()

def menu_wrapper(mobile: bool, label: str, id: str):
    """Render menu wrapper component according to mobile or desktop rules."""

    item_kind = "mobile" if mobile else "desktop"
    item_active = "" if mobile else "active"
    item_font_size = "1.71428571rem" if mobile else "1.28571429rem"

    # accordion title
    with div(cls=f"{item_active} title", style=f"font-size: {item_font_size}; padding-left: 0.75rem; padding-right: 0.75rem;"):
            span(label, id=f"{item_kind}-menu-header-{id}")
            i(cls="right dropdown icon")

    # accordion content
    with div(cls=f"{item_active} content", style="padding: 0;"):
        return div(cls="ui fluid vertical attached menu", style="margin: 0; border-left: 0; border-right: 0; border-bottom: 0;")

def menu_filter(mobile: bool, tags_with_artists: dict[str, list[dict]]):
    """Render filter menu according to mobile or desktop rules."""
    with menu_wrapper(mobile, "Filter", "filter"):
        item_kind = "mobile" if mobile else "desktop"
        item_label_size = "" if mobile else "tiny"

        for index, tag in enumerate(TAGS_MENU_ORDER):
            artists = tags_with_artists[tag]

            # item attributes
            is_header = len(tag.split(" - ")) == 1 and tag != "All" and tag != "Others"
            item_display = tag.split(" - ")[-1].strip()
            item_active = "active" if index == 0 else ""
            item_header = "header" if is_header else ""
            item_font_size = "1.2rem" if is_header else "1rem"

            # menu item
            with div(cls=f"{item_active} {item_header} link item",
                    style=CSS_STYLE_MENU_ITEM + f"font-size: {item_font_size};",
                    id=f"{item_kind}-menu-item-{id(tag)}",
                    data_tab=id(tag),
                    data_tab_name=tag
                ):
                span(item_display)
                span(f"{len(artists)}", cls=f"ui {item_label_size} label")

def menu_sort(mobile):
    """Render sort menu according to mobile or desktop rules."""
    label = "Sort: Name" if mobile else "Sort"
    with menu_wrapper(mobile, label, "sort"):
        div("🎶 Name", cls="ui active link item", onClick="sort(this, 'name', 'asc')", style=CSS_STYLE_MENU_ITEM)
        div("🔥 Popularity (artist)", cls="ui link item", onClick="sort(this, 'popularity', 'desc')", style=CSS_STYLE_MENU_ITEM)
        div("🏆 Popularity (song)", cls="ui link item", onClick="sort(this, 'song-popularity', 'desc')", style=CSS_STYLE_MENU_ITEM)
        div("👤 Followers", cls="ui link item", onClick="sort(this, 'followers', 'desc')", style=CSS_STYLE_MENU_ITEM)
        div("💿 Albums", cls="ui link item", onClick="sort(this, 'albums', 'desc')", style=CSS_STYLE_MENU_ITEM)
        div("📅 Last Release", cls="ui link item", onClick="sort(this, 'last-release', 'desc')", style=CSS_STYLE_MENU_ITEM)
        div("🔔 Last Follow", cls="ui link item", onClick="sort(this, 'last-follow', 'asc')", style=CSS_STYLE_MENU_ITEM)

def cards(artists: list[dict]):
    """"Render the card grid."""
    with div(cls="artists-wrapper"): # scroll-helper
        with div(cls="ui padded grid artists"):
            for artist in artists:
                with card_cell(artist):
                    card(artist)

def card_cell(artist):
    """Render a carl cell in the cards grid."""
    return div(cls="eight wide mobile   four wide tablet   four wide computer   two wide large screen  two wide widescreen   column   artist",
        style="padding: 0.25rem;",
        data_name=artist["name"],
        data_followers=str(artist["followers.total"]),
        data_popularity=str(artist["popularity"]),
        data_song_popularity=str(artist["top_song_popularity"]),
        data_albums=str(artist["album_count"]),
        data_last_release=str(artist["last_release"]),
        data_last_follow=str(artist["last_follow"]),
    )

def card(artist):
    """Render a card."""
    followers_precision = 1 if artist["followers.total"] >= 1_000_000 else 0

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


def render_html(tags_with_artists: dict[str, list[dict]]):
    logging.info("🧱 Generating HTML")

    doc = html(style="height:100%;")
    with doc:
        # ----------------------------------------------------------------------
        # Head
        # ----------------------------------------------------------------------
        with head():
            # meta
            meta(name="viewport", content="width=device-width, initial-scale=1")

            # scripts
            script(src = "https://cdn.jsdelivr.net/npm/jquery@3.7.1/dist/jquery.min.js")
            script(src = "https://cdn.jsdelivr.net/npm/jquery-address@1.6.0/src/jquery.address.js")
            script(src = "https://cdn.jsdelivr.net/npm/fomantic-ui@2.9.4/dist/semantic.min.js")
            script(raw(JS_FUNC_REMOVE_EMOJI))
            script(raw(JS_FUNC_ONTAB))
            script(raw(_JS_FUNC_SORT))

            # style
            link(href =  "https://cdn.jsdelivr.net/npm/fomantic-ui@2.9.4/dist/semantic.min.css", rel = "stylesheet")
            style(raw(CSS_GLOBAL))

        # ----------------------------------------------------------------------
        # Body
        # ----------------------------------------------------------------------
        with body(cls="ui fluid container"):
            with div(cls="ui padded grid"):
                # ------------------------------------------------------------------
                # Menu (mobile)
                # ------------------------------------------------------------------
                with div(cls="sixteen wide mobile tablet only   column", style="padding: 0.5rem"):
                    with div(cls="ui fluid styled mobile accordion"):
                        menu_filter(mobile=True, tags_with_artists=tags_with_artists)
                        menu_sort(mobile=True)

                # ------------------------------------------------------------------
                # Menu (desktop)
                # ------------------------------------------------------------------
                with div(cls="computer only three wide computer   two wide large screen   two wide widescreen   column", style="padding: 0.5rem"):
                    with div(cls="ui fluid styled desktop accordion", style="max-height: 98vh; overflow: hidden; overflow-y: scroll"):
                        menu_filter(mobile=False, tags_with_artists=tags_with_artists)
                        menu_sort(mobile=False)

                # ------------------------------------------------------------------
                # Content (cards)
                # ------------------------------------------------------------------
                with div(cls="sixteen wide mobile tablet   thirteen wide computer   fourteen wide large screen   fourteen wide widescreen   column", style="padding: 0.5rem;"):
                    for tags in TAGS_MENU_ORDER:
                        artists = sorted(tags_with_artists[tags], key=lambda x: x["name"].lower())
                        active = "active" if i == 0 else ""

                        with div(cls="ui tab", data_tab=id(tags)):
                            cards(artists)

                # ------------------------------------------------------------------
                # Scroll to top
                # ------------------------------------------------------------------
                with div(cls="sixteen wide column mobile tablet only"):
                    div("⬆️ Back to top", cls="ui fluid huge button", onClick="window.scrollTo({top:0})")

        # ----------------------------------------------------------------------
        # Script initialization
        # ----------------------------------------------------------------------
        script("$('.menu .item').tab({history:true, historyType: 'hash', onLoad: onTab});")
        script("$('.ui.accordion.desktop').accordion({exclusive:false});")
        script("$('.ui.accordion.mobile').accordion({exclusive:true});")

    return doc