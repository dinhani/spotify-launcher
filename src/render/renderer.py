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
.ui.vertical.desktop.menu {
    max-height: calc(100vh - 3.875rem);
    margin: 0;
    overflow-y: scroll;
}

/* Sidebar controls */
:root {
    --control-font-size: 1rem;
    --control-line-height: 1.25rem;
    --control-padding: 0.5625rem;
}
.ui.input > input.artist-search, .ui.menu.sidebar-options .item {
    font-size: var(--control-font-size) !important;
    line-height: var(--control-line-height) !important;
    padding-top: var(--control-padding) !important;
    padding-bottom: var(--control-padding) !important;
    padding-left: 0.75rem !important;
}
.ui.menu.sidebar-options .item {
    padding-right: 0.75rem !important;
}
.ui.input > input.artist-search {
    padding-top: calc(var(--control-padding) - 1px) !important;
    padding-bottom: calc(var(--control-padding) - 1px) !important;
}
.ui.styled.accordion > .title {
    padding-top: var(--control-padding);
    padding-bottom: var(--control-padding);
}
.ui.styled.accordion > .title > .ui.text {
    line-height: var(--control-line-height);
}
.ui.styled.accordion > .title ~ .title {
    padding-top: calc(var(--control-padding) - 1px);
}
.ui.styled.accordion > .content {
    padding: 0;
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
.control-symbol {
    display: inline-block;
    width: 1.18em;
    margin-right: 0.35rem;
    text-align: center;
    filter: grayscale(1);
}
.ui.input.search-control {
    margin-bottom: 0.5rem;
}
.nowrap {
    white-space: nowrap;
}

/* List controls (group and sort bar) */
.list-controls {
    display: flex;
    flex-wrap: wrap;
    justify-content: space-between;
    align-items: center;
    gap: 0.5rem 2rem;
    margin: 0 10px;
}
.list-control {
    display: flex;
    align-items: center;
    gap: 0.75rem;
}
.list-control-label {
    font-weight: bold;
}
.list-controls .ui.secondary.menu {
    padding: 3px 0;
    background: #f1f2f3;
    border-radius: 0.5rem;
}
.list-controls .ui.secondary.menu .active.item {
    background: #fff;
    box-shadow: 0 1px 2px rgba(34, 36, 38, 0.15);
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
.artist-image-caption {
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    gap: 0.2rem;
    padding: 1.25rem 0.35rem 0.35rem;
    background: linear-gradient(transparent, rgba(0, 0, 0, 0.65));
    color: white;
    text-shadow: 0 1px 2px rgba(0, 0, 0, 0.6);
    pointer-events: none;
}
.ui.card > .image > i.favorite-star.icon {
    position: absolute;
    top: 0.35rem;
    left: 0.35rem;
    margin: 0;
    font-size: 0.9rem;
    color: #f5d76e;
    text-shadow: 0 1px 3px rgba(0, 0, 0, 0.7);
    pointer-events: none;
}
.artist-image-caption.has-album-cover {
    padding-right: 3.25rem;
}
.ui.card > .image > img.album-cover {
    position: absolute;
    right: 0.35rem;
    bottom: 0.35rem;
    width: 2.5rem;
    height: 2.5rem;
    object-fit: cover;
    border: 1px solid rgba(255, 255, 255, 0.85);
    border-radius: 0.15rem;
    box-shadow: 0 0 0 1px rgba(0, 0, 0, 0.25), 0 2px 6px rgba(0, 0, 0, 0.5);
}
.has-album-cover .artist-stats {
    gap: 0.35rem;
}
.artist-tags {
    width: 100%;
    text-align: left;
    min-width: 0;
    overflow-wrap: anywhere;
    font-size: 0.75rem;
    font-weight: bold;
    line-height: 1.2;
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
.artist-stats {
    display: flex;
    width: 100%;
    justify-content: flex-start;
    align-items: baseline;
    flex-shrink: 0;
    gap: 0.5rem;
    text-align: left;
    font-size: 0.75rem;
    line-height: 1.2;
    font-variant-numeric: tabular-nums;
    pointer-events: none;
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
    .list-controls {
        display: none;
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
    .content-column {
        display: flex !important;
        flex-direction: column;
        height: 100vh;
    }
    .content-column > .ui.tab.active {
        display: flex;
        flex-direction: column;
        flex: 1;
        min-height: 0;
    }
    .artists-wrapper {
        flex: 1;
        min-height: 0;
        overflow-y: scroll;
        padding: 10px;
    }
    .artist-image {
        height: 140px !important;
    }
}
/* Group headings */
.ui.grid.artists > .group-heading {
    display: flex;
    align-items: baseline;
    gap: 0.75rem;
    padding: 1rem 0.5rem 0.5rem;
}
.ui.grid.artists > .group-heading:first-child {
    padding-top: 0.5rem;
}
.group-heading .ui.header {
    margin: 0;
    white-space: nowrap;
}
.group-summary {
    color: rgba(0, 0, 0, 0.5);
    font-size: 0.92857143rem;
}
.group-rule {
    flex: 1;
    align-self: center;
    border-top: 1px solid rgba(34, 36, 38, 0.15);
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
    $('.item[data-sort]').removeClass('active').filter('[data-sort="' + attribute + '"]').addClass('active');

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
var grouping = 'none';
var artistFamilies = __ARTIST_FAMILIES__;
var longevityRanges = [
    {label: 'Under 5 Years', from: 0, to: 4},
    {label: '5–9 Years', from: 5, to: 9},
    {label: '10–14 Years', from: 10, to: 14},
    {label: '15–19 Years', from: 15, to: 19},
    {label: '20–24 Years', from: 20, to: 24},
    {label: '25–29 Years', from: 25, to: 29},
    {label: '30–34 Years', from: 30, to: 34},
    {label: '35–39 Years', from: 35, to: 39},
    {label: '40+ Years', from: 40, to: Infinity},
];

function uniqueArtists(grid) {
    var seen = new Set();
    return $(grid).find('.artist').toArray().filter(function(cell) {
        if (seen.has(cell.dataset.name)) return false;
        seen.add(cell.dataset.name);
        return true;
    });
}

function groupSections(grid) {
    if (grouping === 'style') {
        var scope = $(grid).closest('.ui.tab').attr('data-group-family');
        return artistFamilies
            .filter(function(family) { return !scope || family.name === scope; })
            .map(function(family) {
                return {label: family.label, description: family.description, includes: function(cell) {
                    var families = cell.dataset.families.split('|').filter(Boolean);
                    return family.fallback ? families.length === 0 : families.includes(family.name);
                }};
            });
    }

    var currentYear = new Date().getFullYear();
    var sections = longevityRanges.map(function(range) {
        var description = range.to === Infinity
            ? 'Debut ' + (currentYear - range.from) + ' or earlier'
            : 'Debut ' + (currentYear - range.to) + '–' + (currentYear - range.from);
        return {label: range.label, description: description, includes: function(cell) {
            if (!cell.dataset.firstRelease) return false;
            var years = currentYear - Number(cell.dataset.firstRelease.slice(0, 4));
            return years >= range.from && years <= range.to;
        }};
    });
    sections.push({label: 'Unknown', description: '', includes: function(cell) { return !cell.dataset.firstRelease; }});
    return sections;
}

function refreshGroupHeadings() {
    $('.group-heading').each(function() {
        var members = $(this).nextUntil('.group-heading', '.artist').filter(function() { return this.style.display !== 'none'; });
        $(this).toggle(members.length > 0);

        var summary = $(this).find('.group-summary').empty();
        summary.append(members.length + (members.length === 1 ? ' artist' : ' artists'));
        var favorites = members.find('.favorite-star').length;
        if (favorites) summary.append(' · ', $('<i>', {class: 'yellow star icon'}), favorites);
        if (summary.data('description')) summary.append(' · ' + summary.data('description'));
    });
}

function applyGrouping() {
    var query = normalizeText($('.artist-search').first().val() || '');
    var byViewOrder = function(a, b) { return Number(a.dataset.viewOrder) - Number(b.dataset.viewOrder); };
    $('.artists').each(function(_, grid) {
        var cells = uniqueArtists(grid);
        $(grid).empty();
        if (grouping === 'none') {
            $(grid).append(cells.sort(byViewOrder));
        } else {
            groupSections(grid).forEach(function(section) {
                var members = cells.filter(section.includes);
                if (!members.length) return;
                var heading = $('<div>', {class: 'sixteen wide column group-heading'});
                heading.append($('<h2>', {class: 'ui medium header', text: section.label}));
                heading.append($('<span>', {class: 'group-summary', 'data-description': section.description}));
                heading.append($('<div>', {class: 'group-rule'}));
                $(grid).append(heading);
                members.sort(byViewOrder).forEach(function(cell) { $(grid).append($(cell).clone()); });
            });
        }
        $(grid).find('.artist').each(function() {
            $(this).toggle(normalizeText(this.dataset.name).includes(query));
        });
    });
    refreshGroupHeadings();
}

function groupArtists(element, mode) {
    grouping = mode;
    $('.item[data-group]').removeClass('active').filter('[data-group="' + mode + '"]').addClass('active');
    var title = removeEmoji($(element).text());
    $('#mobile-menu-header-group').text('Group: ' + title);
    applyGrouping();
}
""".replace("__ARTIST_FAMILIES__", json.dumps([
    {"name": family.name, "label": f"{family.icon} {family.name}".strip(), "description": family.description, "fallback": family == T_OTHERS}
    for family in [*TAGS_DISCOVER.values(), T_OTHERS]
], ensure_ascii=False))

JS_FUNC_SEARCH = """
function normalizeText(s) {
    var letters = {'æ': 'ae', 'ø': 'o', 'œ': 'oe', 'ß': 'ss'};
    return String(s).normalize('NFD').replace(/\\p{Diacritic}/gu, '').toLowerCase()
        .replace(/[æøœß]/g, function(letter) { return letters[letter]; });
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

    var cells = $('.ui.tab[data-all-artists] .artist').toArray();
    var picked = [];
    var allTab = $('.ui.tab[data-discover-per-family]')[0];
    $('.ui.tab[data-discover-family]').each(function(_, tab) {
        var excludedFamilies = JSON.parse(tab.dataset.discoverExcludedFamilies);
        var candidates = cells
            .filter(function(cell) { return cell.dataset.families.split('|').includes(tab.dataset.discoverFamily); })
            .filter(function(cell) {
                var families = cell.dataset.families.split('|');
                return !excludedFamilies.some(function(family) { return families.includes(family); });
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

JS_FUNC_MARK_RECENT_RELEASES = """
function markRecentReleases() {
    var recentSince = Date.now() - 90 * 24 * 60 * 60 * 1000;
    $('.artist').each(function(_, cell) {
        if (!cell.dataset.lastRelease || new Date(cell.dataset.lastRelease).getTime() < recentSince) return;
        var label = $('<div>', {class: 'ui mini green right corner label', title: 'Released ' + cell.dataset.lastRelease});
        label.append($('<i>', {class: 'compact disc icon'}));
        $(cell).find('.card > .image').append(label);
    });
}
"""

JS_KEYBOARD_NAVIGATION = """
function focusVisibleCard() {
    var cards = $('.ui.tab.active .artist:visible .card');
    if (!cards.length) return;
    var top = Math.max(0, cards.closest('.artists-wrapper')[0].getBoundingClientRect().top);
    var card = cards.filter(function() { return this.getBoundingClientRect().top >= top; }).first();
    (card.length ? card : cards.first()).focus();
}

$(document).on('keydown', '.menu .item', function(e) {
    if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        $(this).click();
        return;
    }
    if ($(this).closest('.list-controls').length) {
        var barStep = { ArrowRight: 1, ArrowLeft: -1 }[e.key];
        if (e.key === 'ArrowDown') {
            e.preventDefault();
            focusVisibleCard();
        } else if (barStep) {
            e.preventDefault();
            var barItems = $('.list-controls .item[tabindex]');
            barItems.eq(Math.max(0, barItems.index(this) + barStep)).focus();
        }
        return;
    }
    if (e.key === 'ArrowRight') {
        e.preventDefault();
        focusVisibleCard();
        return;
    }

    var step = { ArrowDown: 1, ArrowUp: -1 }[e.key];
    if (!step) return;
    e.preventDefault();
    var items = $(this).closest('.column').find('.menu .item:visible');
    var target = items.index(this) + step;
    if (target < 0) $('.artist-search:visible').focus();
    else items.eq(target).focus();
});

$(document).on('keydown', '.artist-search', function(e) {
    if (e.key === 'Enter') $('.ui.tab.active .artist:visible .card').first().focus();

    var items = $(this).closest('.column').find('.menu .item:visible');
    if (e.key === 'ArrowDown') items.first().focus();
    if (e.key === 'ArrowUp') items.last().focus();
    if (e.key === 'ArrowDown' || e.key === 'ArrowUp') e.preventDefault();
});

$(document).on('keydown', function(e) {
    if (e.key === 'Escape') search('');
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

def menu_wrapper(label: str, id: str):
    """Render a mobile accordion section wrapping a menu."""

    # accordion title
    with div(cls="title"):
        with span(cls="ui blue text"):
            span(label, id=f"mobile-menu-header-{id}")
            i(cls="right dropdown icon")

    # accordion content
    with div(cls="content"):
        return div(cls="ui fluid vertical attached menu sidebar-options")

def menu_filter(mobile: bool, tags_with_artists: dict[Tag, list[Artist]]):
    """Render filter menu according to mobile or desktop rules."""
    menu = menu_wrapper("Filter", "filter") if mobile else div(cls="ui fluid vertical desktop menu sidebar-options")
    with menu:
        item_kind = "mobile" if mobile else "desktop"

        for index, tag in enumerate(TAGS_MENU_ORDER):
            artists_count = len(tags_with_artists[tag])
            if tag == T_DISCOVER:
                artists_count = DISCOVER_ARTISTS_PER_FAMILY * len(TAGS_DISCOVER)
            elif tag in TAGS_DISCOVER:
                artists_count = DISCOVER_ARTISTS_PER_FAMILY

            # item attributes
            item_display = tag_display(tag)
            item_active = "active" if index == 0 else ""
            item_header = "header" if tag in TAGS_HEADER else ""

            # menu item
            with div(cls=f"{item_active} {item_header} link item nowrap",
                    id=f"{item_kind}-menu-item-{id(tag)}",
                    data_tab=id(tag),
                    data_tab_name=tag.name,
                    tabindex="0"
                ):
                if tag.icon:
                    span(tag.icon, cls="control-symbol", aria_hidden="true")
                span(item_display)
                span(f"{artists_count}", cls="ui tiny basic blue label artist-count")

def menu_sort():
    """Render the mobile sort menu."""
    with menu_wrapper("Sort: Name", "sort") as menu:
        menu['class'] += " sort-options"
        sort_items()

def menu_group():
    with menu_wrapper("Group: None", "group") as menu:
        menu['class'] += " group-options"
        group_items()

def list_controls():
    with div(cls="list-controls"):
        with div(cls="list-control"):
            span("Sort", cls="ui blue text list-control-label")
            with div(cls="ui small compact blue secondary menu"):
                sort_items()
        with div(cls="list-control"):
            span("Group", cls="ui blue text list-control-label")
            with div(cls="ui small compact blue secondary menu"):
                group_items()

def sort_items():
    for index, (icon, label, description, attribute, order) in enumerate([
        ("music", "Name", "Name", "name", "asc"),
        ("fire", "Popularity", "Artist popularity", "popularity", "desc"),
        ("trophy", "Top Song", "Top song popularity", "song-popularity", "desc"),
        ("user", "Followers", "Followers", "followers", "desc"),
        ("compact disc", "Albums", "Albums", "albums", "desc"),
        ("hourglass half", "Longevity", "Years since the first album", "first-release", "desc"),
        ("calendar alternate", "Release", "Last release", "last-release", "desc"),
        ("bell", "Followed", "Last followed", "last-follow", "asc"),
    ]):
        active = "active" if index == 0 else ""
        with div(cls=f"ui {active} link item nowrap", data_sort=attribute, title=description,
                 onClick=f"sort(this, '{attribute}', '{order}')", tabindex="0"):
            i(cls=f"{icon} icon control-icon", aria_hidden="true")
            span(label)

def group_items():
    for index, (icon, label, mode) in enumerate([
        ("th", "None", "none"),
        ("music", "Style", "style"),
        ("hourglass half", "Longevity", "longevity"),
    ]):
        active = "active" if index == 0 else ""
        with div(cls=f"ui {active} link item nowrap", data_group=mode, onClick=f"groupArtists(this, '{mode}')", tabindex="0"):
            i(cls=f"{icon} icon control-icon", aria_hidden="true")
            span(label)

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
        data_first_release=artist.first_release,
        data_last_release=artist.last_release,
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
            img(src=artist.image, cls="ui image artist-image", alt=artist.name, loading="lazy")
            if T_FAVORITES in artist.tags:
                i(cls="star icon favorite-star", role="img", aria_label="Favorite")
            caption_class = "artist-image-caption has-album-cover" if artist.top_album_image else "artist-image-caption"
            with div(cls=caption_class):
                div(artist_tags, cls="artist-tags")
                with div(cls="artist-stats"):
                    for icon, value, label in [
                        ("fire", str(artist.popularity), "Popularity"),
                        ("user", millify(artist.followers, precision=followers_precision), "Followers"),
                        ("compact disc", str(artist.albums), "Albums"),
                    ]:
                        with div(aria_label=f"{label}: {value}"):
                            i(cls=f"{icon} icon", aria_hidden="true")
                            span(value)
            if artist.top_album_image:
                img(src=artist.top_album_image, cls="album-cover", alt=f"Album cover — {artist.top_album_name}", title=artist.top_album_name,
                    loading="lazy", width="40", height="40")

        # header
        with a(cls="content", href=spotify_url, tabindex="-1"):
            div(artist.name, cls="ui small header artist-name")
            with div(cls="meta"):
                div(artist.top_song or "-", cls="artist-song")

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
            script(raw(JS_FUNC_MARK_RECENT_RELEASES))

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
                        menu_group()
                        menu_sort()
                        menu_filter(mobile=True, tags_with_artists=tags_with_artists)

                # ------------------------------------------------------------------
                # Menu (desktop)
                # ------------------------------------------------------------------
                with div(cls="computer only three wide computer   two wide large screen   two wide widescreen   column app-column"):
                    menu_search()
                    menu_filter(mobile=False, tags_with_artists=tags_with_artists)

                # ------------------------------------------------------------------
                # Content (cards)
                # ------------------------------------------------------------------
                with div(cls="sixteen wide mobile tablet   thirteen wide computer   fourteen wide large screen   fourteen wide widescreen   column app-column content-column"):
                    list_controls()
                    for tag in TAGS_MENU_ORDER:
                        artists = tags_with_artists[tag]
                        tab_attributes = {}
                        if tag == T_ALL:
                            tab_attributes['data_all_artists'] = 'true'
                        for family in TAGS_DISCOVER.values():
                            prefix = "Alt" if family == T_ALT_ALL else family.name
                            if tag == family or tag.name.startswith(prefix + " - "):
                                tab_attributes['data_group_family'] = family.name
                        if tag == T_DISCOVER:
                            artists = tags_with_artists[T_ALL]
                            tab_attributes = {"data_discover_per_family": str(DISCOVER_ARTISTS_PER_FAMILY)}
                        elif tag in TAGS_DISCOVER:
                            family = TAGS_DISCOVER[tag]
                            artists = tags_with_artists[family]
                            tab_attributes = {
                                "data_discover_family": family.name,
                                "data_discover_excluded_families": json.dumps([
                                    excluded.name for excluded in TAGS_DISCOVER_EXCLUSIONS.get(family, [])
                                ], ensure_ascii=False),
                            }

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
        script("markRecentReleases();")
        script("pickDiscover();")
        script("sort($('.item[data-sort]')[0], 'name', 'asc');")
        script("$('.menu .item').tab({history:true, historyType: 'hash', onLoad: onTab});")
        script("$('.ui.accordion.mobile').accordion({exclusive:true});")
        script(raw(JS_KEYBOARD_NAVIGATION))

    return doc
