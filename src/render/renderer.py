# ------------------------------------------------------------------------------
# Libraries
# ------------------------------------------------------------------------------
from dominate.tags import *
from dominate.util import raw
from millify import millify
import logging
from urllib.parse import quote_plus

from render.data import *
from render.models import Artist

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
        padding: 10px;
    }
    .artist-image {
        height: 140px !important;
    }
}
.menu .item:focus-visible {
    outline: 3px solid #2185d0;
    outline-offset: -3px;
}
.ui.card {
    scroll-margin: 16px;
}
.ui.card:focus-visible, .ui.card:hover {
    outline: none;
    z-index: 5;
    transform: scale(1.04);
    box-shadow: 0 0 0 3px #2185d0, 0 8px 20px rgba(0, 0, 0, 0.35) !important;
}
"""

JS_FUNC_REMOVE_EMOJI = """
function removeEmoji(s) {
    return s.replace(/[\\p{Emoji_Presentation}\\p{Extended_Pictographic}]/gu, '').trim()
}
"""

JS_FUNC_ONTAB = """
function onTab(tabPath) {
    if ($(document.activeElement).is('body, .ui.card') && matchMedia('(min-width: 992px)').matches) {
        $('.ui.tab.active .artist:visible .card').first().focus();
    }

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

JS_FUNC_SEARCH = """
function normalizeText(s) {
    return String(s).normalize('NFD').replace(/\\p{Diacritic}/gu, '').toLowerCase();
}

function search(text) {
    $('.artist-search').val(text);
    var query = normalizeText(text);
    $('.artist').each(function(_, artist) {
        $(artist).toggle(normalizeText($(artist).data('name')).includes(query));
    });
}
"""

JS_KEYBOARD_NAVIGATION = """
$(document).on('keydown', '.menu .item', function(e) {
    if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        $(this).click();
        return;
    }
    if (e.key === 'ArrowRight') {
        e.preventDefault();
        var cards = $('.ui.tab.active .artist:visible .card');
        var top = Math.max(0, cards.closest('.artists-wrapper')[0].getBoundingClientRect().top);
        var card = cards.filter(function() { return this.getBoundingClientRect().top >= top; }).first();
        (card.length ? card : cards.first()).focus();
        return;
    }

    var step = { ArrowDown: 1, ArrowUp: -1 }[e.key];
    if (!step) return;
    e.preventDefault();
    var items = $(this).closest('.accordion').find('.menu .item:visible');
    var target = items.index(this) + step;
    if (target < 0) $('.artist-search:visible').focus();
    else items.eq(target).focus();
});

$(document).on('keydown', '.artist-search', function(e) {
    if (e.key === 'Escape') search('');
    if (e.key === 'Enter') $('.ui.tab.active .artist:visible .card').first().focus();

    var items = $(this).closest('.column').find('.menu .item:visible');
    if (e.key === 'ArrowDown') items.first().focus();
    if (e.key === 'ArrowUp') items.last().focus();
    if (e.key === 'ArrowDown' || e.key === 'ArrowUp') e.preventDefault();
});

$(document).on('keydown', function(e) {
    if (e.key.length !== 1 || e.key === ' ' || e.ctrlKey || e.metaKey || e.altKey) return;
    if ($(e.target).is('input')) return;
    $('.artist-search:visible').focus();
});

$(document).on('keydown', '.ui.card', function(e) {
    if (e.key === 'Escape') {
        $('.artist-search:visible').focus();
        return;
    }
    if (e.key === 'Enter') {
        window.location.href = $(this).data('spotify');
        return;
    }
    if (e.key === 'l' || e.key === 'L') {
        e.preventDefault();
        e.stopPropagation();
        window.open($(this).data('lastfm'), '_blank');
        return;
    }

    var cards = $('.ui.tab.active .artist:visible .card');
    var index = cards.index(this);
    var top = cards[0].parentElement.offsetTop;
    var columns = cards.filter(function() { return this.parentElement.offsetTop === top; }).length;
    if (e.key === 'ArrowLeft' && index % columns === 0) {
        e.preventDefault();
        $('.menu .item.active[data-tab]:visible').focus();
        return;
    }

    var step = { ArrowRight: 1, ArrowLeft: -1, ArrowDown: columns, ArrowUp: -columns }[e.key];
    if (!step) return;
    e.preventDefault();
    var target = index + step;
    if (target >= 0 && target < cards.length) cards.eq(target).focus();
});
"""

# ------------------------------------------------------------------------------
# Functions
# ------------------------------------------------------------------------------
def tag_display(tag: str) -> str:
    """Parse the display name of a tag."""
    return tag.split(" - ")[-1].strip()

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
            is_header = tag in TAGS_HEADER
            item_display = tag_display(tag)
            item_active = "active" if index == 0 else ""
            item_header = "header" if is_header else ""
            item_font_size = "1.2rem" if is_header else "1rem"

            # menu item
            with div(cls=f"{item_active} {item_header} link item",
                    style=CSS_STYLE_MENU_ITEM + f"font-size: {item_font_size};",
                    id=f"{item_kind}-menu-item-{id(tag)}",
                    data_tab=id(tag),
                    data_tab_name=tag,
                    tabindex="0"
                ):
                span(item_display)
                span(f"{len(artists)}", cls=f"ui {item_label_size} label")

def menu_sort(mobile):
    """Render sort menu according to mobile or desktop rules."""
    label = "Sort: Name" if mobile else "Sort"
    with menu_wrapper(mobile, label, "sort"):
        div("🎶 Name", cls="ui active link item", onClick="sort(this, 'name', 'asc')", style=CSS_STYLE_MENU_ITEM, tabindex="0")
        div("🔥 Popularity (artist)", cls="ui link item", onClick="sort(this, 'popularity', 'desc')", style=CSS_STYLE_MENU_ITEM, tabindex="0")
        div("🏆 Popularity (song)", cls="ui link item", onClick="sort(this, 'song-popularity', 'desc')", style=CSS_STYLE_MENU_ITEM, tabindex="0")
        div("👤 Followers", cls="ui link item", onClick="sort(this, 'followers', 'desc')", style=CSS_STYLE_MENU_ITEM, tabindex="0")
        div("💿 Albums", cls="ui link item", onClick="sort(this, 'albums', 'desc')", style=CSS_STYLE_MENU_ITEM, tabindex="0")
        div("📅 Last Release", cls="ui link item", onClick="sort(this, 'last-release', 'desc')", style=CSS_STYLE_MENU_ITEM, tabindex="0")
        div("🔔 Last Follow", cls="ui link item", onClick="sort(this, 'last-follow', 'asc')", style=CSS_STYLE_MENU_ITEM, tabindex="0")

def menu_search():
    with div(cls="ui fluid icon input", style="margin-bottom: 0.5rem;"):
        input_(cls="artist-search", type="search", placeholder="Search artist",
            oninput="search(this.value)",
        )
        i(cls="search icon")

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
        data_name=artist.name,
        data_followers=str(artist.followers),
        data_popularity=str(artist.popularity),
        data_song_popularity=str(artist.top_song_popularity),
        data_albums=str(artist.albums),
        data_last_release=str(artist.last_release),
        data_last_follow=str(artist.last_follow),
    )

def card(artist: Artist):
    """Render a card."""
    followers_precision = 1 if artist.followers >= 1_000_000 else 0
    artist_tags = ", ".join([tag_display(t) for t in artist.tags_granular])

    spotify_url = f"spotify:artist:{artist.id}"
    lastfm_url = f"https://www.last.fm/user/{LASTFM_USER}/library/music/{quote_plus(artist.name)}"

    with div(cls="ui card", style="width: 100%", tabindex="0", data_spotify=spotify_url, data_lastfm=lastfm_url):
        # image
        with a(cls="image", href=spotify_url, tabindex="-1"):
            img(src=artist.image, cls="ui image artist-image", style="object-fit: cover;")
            if T_FAVORITES in artist.tags:
                with div(cls="ui mini yellow right corner label"):
                    i(cls="star icon")
            div(artist_tags, style="position: absolute; bottom: 0; font-size: 0.75rem; font-weight: bold; line-height: 1; color: white; padding: 0.25rem; background: rgba(0,0,0,0.2); backdrop-filter: blur(4px)")

        # header
        with a(cls="content", href=spotify_url, tabindex="-1", style="padding: 0.5rem;"):
            div(artist.name, cls="ui small header artist-name", style=f"{CSS_STYLE_NOWRAP} overflow:hidden; text-overflow: ellipsis; margin-bottom: 0.25rem")
            with div(cls="meta"):
                div(artist.top_song, style=f"{CSS_STYLE_NOWRAP} overflow:hidden; text-overflow: ellipsis;")

        # footer
        with div(cls="extra content", style="padding: 0.5rem 0.5rem; display: flex; flex-wrap: nowrap; justify-content: space-between"):
            div("🔥" + str(artist.popularity), style=CSS_STYLE_NOWRAP)
            div("👤" + millify(artist.followers, precision=followers_precision), style=CSS_STYLE_NOWRAP)
            div("💿" + str(artist.albums), style=CSS_STYLE_NOWRAP)

        # links
        with div(cls="ui two bottom attached mini basic buttons"):
            with a(cls="ui button", href=spotify_url, tabindex="-1", style=CSS_STYLE_NOWRAP + "padding: 0.5rem 0;"):
                i(cls="green spotify icon")
                span("Spotify")
            with a(cls="ui button", href=lastfm_url, target="_blank", tabindex="-1", style=CSS_STYLE_NOWRAP + "padding: 0.5rem 0;"):
                i(cls="red lastfm icon")
                span("Last.fm")


def render_html(tags_with_artists: dict[str, list[dict]]):
    logging.info("🧱 Generating HTML")

    doc = html(style="height:100%;")
    with doc:
        # ----------------------------------------------------------------------
        # Head
        # ----------------------------------------------------------------------
        with head():
            title("Dinhani Spotify Launcher")

            # meta
            meta(charset="utf-8")
            meta(name="viewport", content="width=device-width, initial-scale=1")

            # scripts
            script(src = "https://cdn.jsdelivr.net/npm/jquery@3.7.1/dist/jquery.min.js")
            script(src = "https://cdn.jsdelivr.net/npm/jquery-address@1.6.0/src/jquery.address.js")
            script(src = "https://cdn.jsdelivr.net/npm/fomantic-ui@2.9.4/dist/semantic.min.js")
            script(raw(JS_FUNC_REMOVE_EMOJI))
            script(raw(JS_FUNC_ONTAB))
            script(raw(_JS_FUNC_SORT))
            script(raw(JS_FUNC_SEARCH))

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
                    menu_search()
                    with div(cls="ui fluid styled mobile accordion"):
                        menu_sort(mobile=True)
                        menu_filter(mobile=True, tags_with_artists=tags_with_artists)

                # ------------------------------------------------------------------
                # Menu (desktop)
                # ------------------------------------------------------------------
                with div(cls="computer only three wide computer   two wide large screen   two wide widescreen   column", style="padding: 0.5rem"):
                    menu_search()
                    with div(cls="ui fluid styled desktop accordion", style="max-height: calc(98vh - 3.5rem); overflow: hidden; overflow-y: scroll"):
                        menu_sort(mobile=False)
                        menu_filter(mobile=False, tags_with_artists=tags_with_artists)

                # ------------------------------------------------------------------
                # Content (cards)
                # ------------------------------------------------------------------
                with div(cls="sixteen wide mobile tablet   thirteen wide computer   fourteen wide large screen   fourteen wide widescreen   column", style="padding: 0.5rem;"):
                    for tags in TAGS_MENU_ORDER:
                        artists = sorted(tags_with_artists[tags], key=lambda x: x.name.lower())
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
        script(raw(JS_KEYBOARD_NAVIGATION))

    return doc