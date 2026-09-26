# ------------------------------------------------------------------------------
# Libraries
# ------------------------------------------------------------------------------
from dominate.tags import *
from dominate.util import raw
from millify import millify
import json
import logging
from urllib.parse import quote_plus

from render.data import *
from render.models import Artist, Tag

# ------------------------------------------------------------------------------
# Constants
# ------------------------------------------------------------------------------
DISCOVER_ARTISTS_PER_FAMILY = 4

CSS_GLOBAL = """
/* Layout */
html {
    height: 100%;
}
.ui.grid > .column.app-column {
    padding: 0.5rem;
}
.ui.styled.desktop.accordion {
    max-height: calc(98vh - 3.5rem);
    overflow: hidden;
    overflow-y: scroll;
}

/* Sidebar controls */
:root {
    --control-font-size: 1rem;
    --control-line-height: 1.25rem;
    --control-padding: 0.5625rem;
}
.ui.input > input.artist-search, .ui.menu .item {
    font-size: var(--control-font-size) !important;
    line-height: var(--control-line-height) !important;
    padding-top: var(--control-padding) !important;
    padding-bottom: var(--control-padding) !important;
    padding-left: 0.75rem !important;
}
.ui.menu .item {
    padding-right: 0.75rem !important;
}
.ui.input > input.artist-search {
    padding-top: calc(var(--control-padding) - 1px) !important;
    padding-bottom: calc(var(--control-padding) - 1px) !important;
}
.ui.styled.accordion > .content {
    padding: 0;
}
.ui.styled.accordion > .title.section-title {
    color: #2185d0;
    font-size: calc(var(--control-font-size) + 2px);
    font-weight: 700;
}
.ui.vertical.attached.menu.sidebar-options {
    margin: 0;
    border-left: 0;
    border-right: 0;
    border-bottom: 0;
}
.ui.menu .item > .label.artist-count {
    width: 3.5em;
    text-align: center;
    font-variant-numeric: tabular-nums;
}
.ui.vertical.menu .item > i.control-icon {
    float: none;
    margin: 0 0.35rem 0 0;
}
.ui.input.search-control {
    margin-bottom: 0.5rem;
}
.nowrap {
    white-space: nowrap;
}

/* Artist cards */
.ui.grid.artists {
    margin: -0.25rem;
}
.ui.grid.artists > .column.artist {
    padding: 0.25rem;
}
.ui.card.artist-card {
    width: 100%;
    scroll-margin: 16px;
}
.artist-image {
    object-fit: cover;
}
.artist-tags {
    position: absolute;
    bottom: 0;
    font-size: 0.75rem;
    font-weight: bold;
    line-height: 1;
    color: white;
    padding: 0.25rem;
    background: rgba(0,0,0,0.2);
    backdrop-filter: blur(4px);
}
.ui.card > .content {
    padding: 0.5rem;
}
.artist-name, .artist-song {
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}
.ui.card .artist-name {
    margin-bottom: 0.25rem;
}
.ui.card > .extra.content {
    display: flex;
    flex-wrap: nowrap;
    justify-content: space-between;
}
.ui.card > .extra.content::after {
    display: none !important;
}
.artist-stats > div {
    white-space: nowrap;
}
.ui.card > .buttons > .ui.button {
    white-space: nowrap;
    padding: 0.5rem 0;
}

/* Responsive layout */
@media only screen and (max-width: 991.9px) {
    :root {
        --control-font-size: 16px;
        --control-line-height: 1.5rem;
        --control-padding: 0.8rem;
    }
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
/* Group headings */
.ui.grid.artists > .family-heading {
    padding: 1.5rem 0.5rem 0.75rem;
}
.ui.grid.artists > .family-heading:first-child {
    padding-top: 0.5rem;
}
.family-heading .ui.header {
    margin: 0;
}

/* Focus and hover */
.menu .item:focus-visible {
    outline: 3px solid #2185d0;
    outline-offset: -3px;
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
    var sortIndex = $(element).index();
    $('.sort-options').each(function() {
        $(this).children().removeClass('active').eq(sortIndex).addClass('active');
    });

    // reorder
    $('.artists').each(function(_, artists) {
        var sorted = uniqueArtists(artists).sort(function(a, b) {
            var valA = $(a).data(attribute);
            var valB = $(b).data(attribute);

            // Check if the values are numeric
            if ($.isNumeric(valA)) {
                return order === 'asc' ? valA - valB : valB - valA; // Numeric comparison
            } else {
                return order === 'asc' ? String(valA).localeCompare(String(valB)) : String(valB).localeCompare(String(valA)); // String comparison
            }
        });
        sorted.forEach(function(cell, index) { cell.dataset.viewOrder = index; });
        $(artists).empty().append(sorted);
    });
    applyGrouping();
}
"""

JS_FUNC_GROUP = """
var groupByFamily = false;
var artistFamilies = __ARTIST_FAMILIES__;

function uniqueArtists(grid) {
    var seen = new Set();
    return $(grid).find('.artist').toArray().filter(function(cell) {
        if (seen.has(cell.dataset.name)) return false;
        seen.add(cell.dataset.name);
        return true;
    });
}

function refreshGroupHeadings() {
    $('.family-heading').each(function() {
        var members = $(this).nextUntil('.family-heading', '.artist');
        $(this).toggle(members.toArray().some(function(cell) { return cell.style.display !== 'none'; }));
    });
}

function applyGrouping() {
    var query = normalizeText($('.artist-search').first().val() || '');
    $('.artists').each(function(_, grid) {
        var cells = uniqueArtists(grid);
        $(grid).empty();
        if (!groupByFamily) {
            cells.sort(function(a, b) { return Number(a.dataset.viewOrder) - Number(b.dataset.viewOrder); });
            $(grid).append(cells);
        } else {
            var scope = $(grid).closest('.ui.tab').attr('data-group-family');
            artistFamilies.forEach(function(family) {
                if (scope && family.name !== scope) return;
                var members = cells.filter(function(cell) {
                    var families = cell.dataset.families.split('|').filter(Boolean);
                    return family.fallback ? families.length === 0 : families.includes(family.name);
                });
                if (!members.length) return;
                var heading = $('<div>', {class: 'sixteen wide column family-heading'});
                heading.append($('<h2>', {class: 'ui medium header', text: family.label}));
                $(grid).append(heading);
                members.sort(function(a, b) { return Number(a.dataset.viewOrder) - Number(b.dataset.viewOrder); });
                members.forEach(function(cell) { $(grid).append($(cell).clone()); });
            });
        }
        $(grid).find('.artist').each(function() {
            $(this).toggle(normalizeText(this.dataset.name).includes(query));
        });
    });
    refreshGroupHeadings();
}

function groupArtists(byFamily) {
    groupByFamily = byFamily;
    $('.group-options').each(function() {
        $(this).children().removeClass('active').eq(byFamily ? 1 : 0).addClass('active');
    });
    $('#mobile-menu-header-group').text('Group: ' + (byFamily ? 'By Style' : 'None'));
    applyGrouping();
}
""".replace("__ARTIST_FAMILIES__", json.dumps([
    {"name": family.name, "label": f"{family.icon} {family.name}".strip(), "fallback": family == T_OTHERS}
    for family in [*TAGS_DISCOVER.values(), T_OTHERS]
], ensure_ascii=False))

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
    refreshGroupHeadings();
}
"""

JS_FUNC_PICK_DISCOVER = """
function pickDiscover() {
    var shifted = new Date(Date.now() - 6 * 60 * 60 * 1000);
    var period = shifted.getHours() < 6 ? 0 : shifted.getHours() < 12 ? 1 : 2;
    var seed = (shifted.getFullYear() * 10000 + (shifted.getMonth() + 1) * 100 + shifted.getDate()) * 10 + period;
    var random = function() {
        seed = (seed + 0x6D2B79F5) | 0;
        var t = Math.imul(seed ^ (seed >>> 15), 1 | seed);
        t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
        return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
    var showOnly = function(tab, names) {
        var grid = $(tab).find('.artists');
        var cells = grid.find('.artist').toArray();
        grid.empty().append(names.map(function(name) {
            return cells.find(function(cell) { return cell.dataset.name === name; });
        }));
    };

    var cells = $('.ui.tab[data-tab="all"] .artist').toArray();
    var picked = [];
    var allTab = $('.ui.tab[data-discover-per-family]')[0];
    $('.ui.tab[data-discover-family]').each(function(_, tab) {
        var candidates = cells
            .filter(function(cell) { return cell.dataset.families.split('|').includes(tab.dataset.discoverFamily); })
            .filter(function(cell) {
                var families = cell.dataset.families.split('|');
                return tab.dataset.discoverFamily !== 'Folk'
                    || (!families.includes('Rock') && !families.includes('Alternative'));
            })
            .map(function(cell) { return cell.dataset.name; })
            .filter(function(name) { return !picked.includes(name); });
        var familyPicked = [];
        for (var i = 0; i < Number(allTab.dataset.discoverPerFamily) && candidates.length > 0; i++) {
            familyPicked.push(candidates.splice(Math.floor(random() * candidates.length), 1)[0]);
        }
        showOnly(tab, familyPicked);
        picked.push(...familyPicked);
    });
    showOnly(allTab, picked);
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
        if (!cards.length) return;
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
    if (e.key === 'Enter' && e.shiftKey) {
        e.preventDefault();
        window.open($(this).data('lastfm'), '_blank');
        return;
    }
    if (e.key === 'Enter') {
        window.location.href = $(this).data('spotify');
        return;
    }

    var cards = $('.ui.tab.active .artist:visible .card');
    var index = cards.index(this);
    var rect = this.getBoundingClientRect();
    var row = cards.filter(function() { return Math.abs(this.getBoundingClientRect().top - rect.top) < 2; });
    if (e.key === 'ArrowLeft' && row.index(this) === 0) {
        e.preventDefault();
        $('.menu .item.active[data-tab]:visible').focus();
        return;
    }

    if (!['ArrowRight', 'ArrowLeft', 'ArrowDown', 'ArrowUp'].includes(e.key)) return;
    e.preventDefault();
    if (e.key === 'ArrowLeft' || e.key === 'ArrowRight') {
        var target = index + (e.key === 'ArrowRight' ? 1 : -1);
        if (target >= 0 && target < cards.length) cards.eq(target).focus();
        return;
    }
    var below = e.key === 'ArrowDown';
    var candidates = cards.toArray().filter(function(card) {
        var delta = card.getBoundingClientRect().top - rect.top;
        return below ? delta > 2 : delta < -2;
    });
    candidates.sort(function(a, b) {
        var aRect = a.getBoundingClientRect(), bRect = b.getBoundingClientRect();
        return Math.abs(aRect.top - rect.top) - Math.abs(bRect.top - rect.top)
            || Math.abs(aRect.left - rect.left) - Math.abs(bRect.left - rect.left);
    });
    if (candidates.length) candidates[0].focus();
});
"""

# ------------------------------------------------------------------------------
# Functions
# ------------------------------------------------------------------------------
def tag_display(tag: Tag) -> str:
    """Parse the display name of a tag."""
    return tag.name.split(" - ")[-1].strip()

def id(tag: Tag) -> str:
    """Parse a tag to HTML identifier."""
    return tag.name.lower().translate(str.maketrans("", "", "():/")).translate(str.maketrans("ãéó", "aeo")).replace(" - ", "-").replace(" ", "-").strip()

def menu_wrapper(mobile: bool, label: str, id: str):
    """Render menu wrapper component according to mobile or desktop rules."""

    item_kind = "mobile" if mobile else "desktop"
    item_active = "" if mobile else "active"

    # accordion title
    with div(cls=f"{item_active} title section-title"):
            span(label, id=f"{item_kind}-menu-header-{id}")
            i(cls="right dropdown icon")

    # accordion content
    with div(cls=f"{item_active} content"):
        return div(cls="ui fluid vertical attached menu sidebar-options")

def menu_filter(mobile: bool, tags_with_artists: dict[Tag, list[Artist]]):
    """Render filter menu according to mobile or desktop rules."""
    with menu_wrapper(mobile, "Filter", "filter"):
        item_kind = "mobile" if mobile else "desktop"

        for index, tag in enumerate(TAGS_MENU_ORDER):
            artists_count = len(tags_with_artists[tag])
            if tag == T_DISCOVER:
                artists_count = DISCOVER_ARTISTS_PER_FAMILY * len(TAGS_DISCOVER)
            elif tag in TAGS_DISCOVER:
                artists_count = DISCOVER_ARTISTS_PER_FAMILY

            # item attributes
            item_display = f"{tag.icon} {tag_display(tag)}".strip()
            item_active = "active" if index == 0 else ""
            item_header = "header" if tag in TAGS_HEADER else ""

            # menu item
            with div(cls=f"{item_active} {item_header} link item nowrap",
                    id=f"{item_kind}-menu-item-{id(tag)}",
                    data_tab=id(tag),
                    data_tab_name=tag.name,
                    tabindex="0"
                ):
                span(item_display)
                span(f"{artists_count}", cls="ui tiny label artist-count")

def menu_sort(mobile):
    """Render sort menu according to mobile or desktop rules."""
    label = "Sort: Name" if mobile else "Sort"
    with menu_wrapper(mobile, label, "sort") as menu:
        menu['class'] += " sort-options"
        div("🎶 Name", cls="ui active link item nowrap", onClick="sort(this, 'name', 'asc')", tabindex="0")
        div("🔥 Popularity (artist)", cls="ui link item nowrap", onClick="sort(this, 'popularity', 'desc')", tabindex="0")
        div("🏆 Popularity (song)", cls="ui link item nowrap", onClick="sort(this, 'song-popularity', 'desc')", tabindex="0")
        div("👤 Followers", cls="ui link item nowrap", onClick="sort(this, 'followers', 'desc')", tabindex="0")
        div("💿 Albums", cls="ui link item nowrap", onClick="sort(this, 'albums', 'desc')", tabindex="0")
        div("📅 Last Release", cls="ui link item nowrap", onClick="sort(this, 'last-release', 'desc')", tabindex="0")
        div("🔔 Last Follow", cls="ui link item nowrap", onClick="sort(this, 'last-follow', 'asc')", tabindex="0")

def menu_group(mobile):
    label = "Group: None" if mobile else "Group"
    with menu_wrapper(mobile, label, "group") as menu:
        menu['class'] += " group-options"
        with div(cls="ui active link item", onClick="groupArtists(false)", tabindex="0"):
            i(cls="th icon control-icon", aria_hidden="true")
            span("None")
        div("🎼 By Style", cls="ui link item", onClick="groupArtists(true)", tabindex="0")

def menu_search():
    with div(cls="ui fluid icon input search-control"):
        input_(cls="artist-search", type="search", placeholder="Search artist",
            oninput="search(this.value)",
        )
        i(cls="search icon")

def cards(artists: list[dict]):
    """"Render the card grid."""
    with div(cls="artists-wrapper"): # scroll-helper
        with div(cls="ui grid artists"):
            for artist in artists:
                with card_cell(artist):
                    card(artist)

def card_cell(artist):
    """Render a carl cell in the cards grid."""
    return div(cls="eight wide mobile   four wide tablet   four wide computer   two wide large screen  two wide widescreen   column   artist",
        data_name=artist.name,
        data_followers=str(artist.followers),
        data_popularity=str(artist.popularity),
        data_song_popularity=str(artist.top_song_popularity),
        data_albums=str(artist.albums),
        data_last_release=str(artist.last_release),
        data_last_follow=str(artist.last_follow),
        data_families="|".join(family.name for family in TAGS_DISCOVER.values() if family in artist.tags),
    )

def card(artist: Artist):
    """Render a card."""
    followers_precision = 1 if artist.followers >= 1_000_000 else 0
    artist_tags = ", ".join([tag_display(t) for t in artist.tags_granular])

    spotify_url = f"spotify:artist:{artist.id}"
    lastfm_url = f"https://www.last.fm/user/{LASTFM_USER}/library/music/{quote_plus(artist.name)}"

    with div(cls="ui card artist-card", tabindex="0", data_spotify=spotify_url, data_lastfm=lastfm_url):
        # image
        with a(cls="image", href=spotify_url, tabindex="-1"):
            img(src=artist.image, cls="ui image artist-image")
            if T_FAVORITES in artist.tags:
                with div(cls="ui mini yellow right corner label"):
                    i(cls="star icon")
            div(artist_tags, cls="artist-tags")

        # header
        with a(cls="content", href=spotify_url, tabindex="-1"):
            div(artist.name, cls="ui small header artist-name")
            with div(cls="meta"):
                div(artist.top_song, cls="artist-song")

        # footer
        with div(cls="extra content artist-stats"):
            div("🔥" + str(artist.popularity))
            div("👤" + millify(artist.followers, precision=followers_precision))
            div("💿" + str(artist.albums))

        # links
        with div(cls="ui two bottom attached mini basic buttons"):
            with a(cls="ui button", href=spotify_url, tabindex="-1"):
                i(cls="green spotify icon")
                span("Spotify")
            with a(cls="ui button", href=lastfm_url, target="_blank", tabindex="-1"):
                i(cls="red lastfm icon")
                span("Last.fm")


def render_html(tags_with_artists: dict[Tag, list[Artist]]):
    logging.info("🧱 Generating HTML")

    doc = html()
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
            script(raw(JS_FUNC_GROUP))
            script(raw(JS_FUNC_SEARCH))
            script(raw(JS_FUNC_PICK_DISCOVER))

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
                with div(cls="sixteen wide mobile tablet only   column app-column"):
                    menu_search()
                    with div(cls="ui fluid styled mobile accordion"):
                        menu_sort(mobile=True)
                        menu_group(mobile=True)
                        menu_filter(mobile=True, tags_with_artists=tags_with_artists)

                # ------------------------------------------------------------------
                # Menu (desktop)
                # ------------------------------------------------------------------
                with div(cls="computer only three wide computer   two wide large screen   two wide widescreen   column app-column"):
                    menu_search()
                    with div(cls="ui fluid styled desktop accordion"):
                        menu_sort(mobile=False)
                        menu_group(mobile=False)
                        menu_filter(mobile=False, tags_with_artists=tags_with_artists)

                # ------------------------------------------------------------------
                # Content (cards)
                # ------------------------------------------------------------------
                with div(cls="sixteen wide mobile tablet   thirteen wide computer   fourteen wide large screen   fourteen wide widescreen   column app-column"):
                    for tag in TAGS_MENU_ORDER:
                        artists = tags_with_artists[tag]
                        tab_attributes = {}
                        for family in TAGS_DISCOVER.values():
                            prefix = "Alt" if family == T_ALT_ALL else family.name
                            if tag == family or tag.name.startswith(prefix + " - "):
                                tab_attributes['data_group_family'] = family.name
                        if tag == T_DISCOVER:
                            artists = tags_with_artists[T_ALL]
                            tab_attributes = {"data_discover_per_family": str(DISCOVER_ARTISTS_PER_FAMILY)}
                        elif tag in TAGS_DISCOVER:
                            artists = tags_with_artists[TAGS_DISCOVER[tag]]
                            tab_attributes = {"data_discover_family": TAGS_DISCOVER[tag].name}

                        with div(cls="ui tab", data_tab=id(tag), **tab_attributes):
                            cards(sorted(artists, key=lambda x: x.name.lower()))

                # ------------------------------------------------------------------
                # Scroll to top
                # ------------------------------------------------------------------
                with div(cls="sixteen wide column mobile tablet only app-column"):
                    div("⬆️ Back to top", cls="ui fluid button", onClick="window.scrollTo({top:0})")

        # ----------------------------------------------------------------------
        # Script initialization
        # ----------------------------------------------------------------------
        script("pickDiscover();")
        script("sort($('.desktop .sort-options .item')[0], 'name', 'asc');")
        script("$('.menu .item').tab({history:true, historyType: 'hash', onLoad: onTab});")
        script("$('.ui.accordion.desktop').accordion({exclusive:false});")
        script("$('.ui.accordion.mobile').accordion({exclusive:true});")
        script(raw(JS_KEYBOARD_NAVIGATION))

    return doc
