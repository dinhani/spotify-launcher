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
FOMANTIC_UI = "https://cdn.jsdelivr.net/npm/fomantic-ui@2.9.4/dist/semantic.min"

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
.ui.menu.sidebar-options .active.item,
.ui.menu.sidebar-options .active.item:hover {
    background: #2185d0;
    color: #fff;
    font-weight: bold;
}
.ui.menu.sidebar-options .active.item > .ui.basic.label.artist-count {
    border-color: #fff !important;  /* Fomantic basic colored labels use !important */
    background: #fff !important;
    color: #2185d0 !important;
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
.ui.fluid.button.discover-button {
    margin-bottom: 0.5rem;
    font-size: var(--control-font-size);
    line-height: var(--control-line-height);
    padding-top: var(--control-padding);
    padding-bottom: var(--control-padding);
}
.nowrap {
    white-space: nowrap;
}

/* List controls (group and order bar) */
.list-controls {
    display: flex;
    flex-wrap: wrap;
    justify-content: space-between;
    align-items: center;
    gap: 0.5rem 2rem;
    margin: 0 10px;
}
.list-control > .discover-button {
    margin: 0 0 0 1.25rem;
}
.discover-button .compass.icon {
    transition: transform 0.45s ease;
}
.discover-button:hover .compass.icon, .discover-button:focus-visible .compass.icon, .discover-button:active .compass.icon {
    transform: rotate(45deg);
}
.ui.blue.button.discover-button.active {
    box-shadow: 0 0 0 3px rgba(33, 133, 208, 0.3) !important;
}
.list-control {
    display: flex;
    align-items: center;
    gap: 0.75rem;
}
.list-control-label {
    min-width: 3.5em; /* same width for Group and Order, so wrapped menus align */
    font-weight: bold;
}
.list-controls .ui.secondary.menu {
    padding: 3px 0;
    background: #f1f2f3;
    border-radius: 0.5rem;
}
.list-controls .direction-description {
    display: none;
}
.list-controls .item[data-direction] > i.icon {
    margin: 0;
}
.list-controls .ui.secondary.menu .active.item {
    background: #fff;
    box-shadow: 0 1px 2px rgba(34, 36, 38, 0.15);
}

/* Artist cards */
.artists-wrapper {
    padding: 0.5rem;
    background: #f3f4f6;
    border-radius: 0.5rem;
}
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
/* Release grouping shows the last release instead of the top song and album */
.release-text {
    display: none;
}
.ui.card > .image > img.album-cover.release-cover,
body.release-mode .ui.card > .image > img.album-cover.top-cover,
body.release-mode .top-song-text {
    display: none;
}
body.release-mode .ui.card > .image > img.album-cover.release-cover {
    display: block;
}
body.release-mode .release-text {
    display: inline;
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
        height: 100%;
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
        margin-top: 0.5rem;
        padding: 10px;
    }
    .artist-image {
        height: 140px !important;
    }
}
/* Back to top arrow (mobile) */
.scroll-top {
    display: none;
}
@media only screen and (max-width: 991.9px) {
    .scroll-top {
        position: fixed;
        right: 1rem;
        bottom: calc(1rem + env(safe-area-inset-bottom));
        z-index: 20;
        display: flex;
        align-items: center;
        justify-content: center;
        width: 2.75rem;
        height: 2.75rem;
        border: none;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.9);
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
        color: rgba(0, 0, 0, 0.55);
        opacity: 0;
        pointer-events: none;
        transition: opacity 0.25s ease;
        cursor: pointer;
    }
    .scroll-top.visible {
        opacity: 1;
        pointer-events: auto;
    }
    .scroll-top > i.icon {
        margin: 0;
    }
}

/* Command palette (Ctrl+P) */
.ui.modal.command-palette {
    overflow: hidden;
    border-radius: 0.75rem;
}
.ui.modal.command-palette > .content {
    padding: 0;
}
.command-palette .ui.input {
    padding: 0.9rem 1.1rem;
    border-bottom: 1px solid rgba(34, 36, 38, 0.1);
}
.command-palette .ui.input > input.command-input {
    font-size: 1.15rem;
}
.command-list {
    max-height: 55vh;
    padding: 0.35rem 0.5rem 0.5rem;
    overflow-y: auto;
}
.command-section {
    display: flex;
    align-items: center;
    gap: 0.4rem;
    margin-top: 0.5rem;
    padding: 0.75rem 0.6rem 0.35rem;
    border-top: 1px solid rgba(34, 36, 38, 0.08);
    color: #2185d0;
    font-size: 0.8rem;
    font-weight: bold;
    letter-spacing: 0.06em;
    text-transform: uppercase;
}
.command-section:first-child {
    margin-top: 0;
    border-top: none;
}
.command-section > i.icon {
    margin: 0;
}
.command-item {
    display: flex;
    align-items: center;
    gap: 0.35rem;
    padding: 0.5rem 0.6rem;
    border-radius: 0.4rem;
    cursor: pointer;
}
.command-item:hover {
    background: #f5f6f7;
}
.command-item.selected {
    background: #eaf3fb;
    color: #1a69a4;
}
.command-item .command-title > i.icon.command-favorite {
    margin: 0 0 0 0.3rem;
    color: #f5d76e;
    font-size: 0.85em;
}
.command-item .command-new {
    display: inline-block;
    margin-left: 0.4rem;
    padding: 0.05rem 0.35rem;
    border-radius: 0.25rem;
    background: #21ba45;
    color: #fff;
    font-size: 0.65rem;
    font-weight: bold;
    letter-spacing: 0.06em;
    line-height: 1.3;
    text-transform: uppercase;
    vertical-align: 0.15em;
}
.command-item > img.command-photo {
    flex-shrink: 0;
    width: 2.75rem;  /* spans both lines: the photo leads, as on the cards */
    height: 2.75rem;
    margin-right: 0.45rem;
    border-radius: 0.4rem;
    object-fit: cover;
}
.command-item > i.icon {
    width: 1.18em;
    margin: 0 0.35rem 0 0;
    opacity: 0.6;
}
.command-item .command-label {
    flex: 1;
    min-width: 0;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}
.group-heading .section-parent {
    margin-right: 0.35em;
    color: rgba(0, 0, 0, 0.4);
    font-weight: normal;
}
.command-item .command-parent {
    margin-right: 0.45em;
    color: rgba(0, 0, 0, 0.4);
    font-size: 0.9em;
}
.command-item.selected .command-parent {
    color: rgba(26, 105, 164, 0.6);
}
.command-item.style-row .command-name {
    font-weight: bold;
}
.command-item .command-tag {
    display: inline-block;
    margin-right: 0.45rem;
    padding: 0.05rem 0.35rem;
    border-radius: 0.25rem;
    background: rgba(0, 0, 0, 0.05);
    color: rgba(0, 0, 0, 0.5);
    font-size: 0.65rem;
    font-weight: bold;
    letter-spacing: 0.06em;
    line-height: 1.3;
    text-transform: uppercase;
    vertical-align: 0.15em;
}
.command-item.selected .command-tag {
    background: rgba(33, 133, 208, 0.12);
    color: #1a69a4;
}
.command-item .command-title, .command-item .command-subtitle {
    display: block;
    overflow: hidden;
    text-overflow: ellipsis;
}
.command-item .command-subtitle {
    margin-top: 0.1rem;
    color: rgba(0, 0, 0, 0.45);
    font-size: 0.8rem;
}
.command-item.selected .command-subtitle {
    color: rgba(26, 105, 164, 0.7);
}
.command-item .command-count {
    min-width: 2.5em;
    color: rgba(0, 0, 0, 0.62);
    font-size: 0.9rem;
    text-align: right;
    font-variant-numeric: tabular-nums;
}
.command-item.selected .command-count {
    color: #1a69a4;
}
.command-empty {
    padding: 1rem 0.6rem;
    color: rgba(0, 0, 0, 0.45);
}
.command-hints {
    padding: 0.5rem 1.1rem;
    border-top: 1px solid rgba(34, 36, 38, 0.06);
    color: rgba(0, 0, 0, 0.4);
    font-size: 0.8rem;
}
.command-hints kbd {
    font-family: inherit;
    font-weight: bold;
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

JS_FUNC_ONTAB = """
function onTab(tabPath) {
    $('.artist-search').val('');  // a new filter is a new context; group and direction changes keep the search
    applyView(tabPath);
    fillTab($('.ui.tab[data-tab="' + tabPath + '"]')[0]);
    if ($(document.activeElement).is('body, .ui.card') && matchMedia('(min-width: 992px)').matches) {
        visibleCards().first().focus();
    }

    // change header
    var title = $('.item[data-tab="' + tabPath + '"]').data('tab-name');
    $('#mobile-menu-header-filter').text('Filter: ' + title);
    savePreference('tab', tabPath);
    $('.discover-button').toggleClass('active', tabPath === 'discover');
}

function openDiscover() {
    $('.item[data-tab="discover"]').first().click();
}
"""

JS_FUNC_SELECT_OPTION = """
function selectOption(element, kind, label) {
    var value = element.dataset[kind];
    $('.item[data-' + kind + ']').removeClass('active').filter('[data-' + kind + '="' + value + '"]').addClass('active');
    $('#mobile-menu-header-' + kind).text(label + ': ' + $(element).text().trim());
}
"""

JS_FUNC_PREFERENCES = """
var PREFERENCES_KEY = 'spotify-launcher:preferences';

function loadPreferences() {
    try {
        return JSON.parse(localStorage.getItem(PREFERENCES_KEY)) || {};
    } catch (error) {
        console.warn('Preferences unavailable', error);
        return {};
    }
}

function savePreference(name, value) {
    try {
        var preferences = loadPreferences();
        preferences[name] = value;
        localStorage.setItem(PREFERENCES_KEY, JSON.stringify(preferences));
    } catch (error) {
        console.warn('Preferences unavailable', error);
    }
}

// Two shared views, each a group and its direction: one for Discover pages, one for every other page.
var VIEW_DEFAULTS = {discover: {group: 'style'}, main: {group: 'followers'}};
var activeTab = 'all';

function viewName(tab) {
    return $('.ui.tab[data-tab="' + tab + '"]').is('[data-discover-per-family], [data-discover-family]') ? 'discover' : 'main';
}

function viewOf(tab) {
    var name = viewName(tab);
    return $.extend({}, VIEW_DEFAULTS[name], (loadPreferences().views || {})[name]);
}

function saveView(tab, update) {
    var stored = loadPreferences().views || {};
    var views = {main: stored.main, discover: stored.discover};
    var view = viewOf(tab);
    update(view);
    views[viewName(tab)] = view;
    savePreference('views', views);
}

function applyView(tab) {
    activeTab = tab;
    var view = viewOf(tab);
    setGrouping($('.item[data-group="' + view.group + '"]')[0] || $('.item[data-group]')[0]);
    if (view.direction === 'asc' || view.direction === 'desc') setDirection(view.direction);
    applyGrouping();
}

function applyPreferences() {
    var preferences = loadPreferences();
    var savedTab = $('.item[data-tab="' + preferences.tab + '"]').length ? preferences.tab : null;
    if (!location.hash && savedTab) {
        history.replaceState(null, '', '#/' + savedTab);
    }
    applyView(location.hash.replace(/^#\/?/, '') || 'all');
}
"""

JS_FUNC_ORDER = """
function orderArtists(element) {
    setDirection(element.dataset.direction);
    saveView(activeTab, function(view) { view.direction = direction; });
    applyGrouping();
}

function setDirection(order) {
    direction = order;
    var group = $('.item.active[data-group]')[0].dataset;
    $('.item[data-direction]').each(function() {
        var description = group[this.dataset.direction + 'Description'];
        this.title = description;
        this.dataset.commandDescription = description;
        $(this).find('.direction-description').text(description);
        $(this).toggleClass('active', this.dataset.direction === order);
    });
    $('#mobile-menu-header-direction').text('Order: ' + group[order + 'Description']);
}

var SORTS_ELAPSED = ['first-release', 'last-release'];

// read each value once; groupGrid places the cells by viewOrder
function rankArtists() {
    $('.artists').each(function(_, artists) {
        var keyed = uniqueArtists(artists).map(function(cell) {
            var value = cell.getAttribute('data-' + groupSort) || '';
            if (value === '') return {cell: cell, value: null};
            // a date ranks by the time since it, so ascending means fewer years (shortest career, newest release)
            if (SORTS_ELAPSED.includes(groupSort)) return {cell: cell, value: -Date.parse((value + '-01-01').slice(0, 10))};
            return {cell: cell, value: $.isNumeric(value) ? Number(value) : value};
        });
        keyed.sort(function(a, b) {
            if (a.value === null || b.value === null) return (a.value === null) - (b.value === null);  // unknown stays last
            var ascending = typeof a.value === 'number' ? a.value - b.value : String(a.value).localeCompare(String(b.value));
            return direction === 'asc' ? ascending : -ascending;
        });
        keyed.forEach(function(item, index) { item.cell.dataset.viewOrder = index; });
    });
}
"""

JS_FUNC_GROUP = """
var grouping = 'none';
var groupSort = 'name';
var groupOrder = 'asc';
var direction = 'asc';
var artistFamilies = __ARTIST_FAMILIES__;
var artistSubstyles = __ARTIST_SUBSTYLES__;
var longevityRanges = [
    {label: 'Under 5 Years', from: 0, to: 4},
    {label: '5–9 Years', from: 5, to: 9},
    {label: '10–14 Years', from: 10, to: 14},
    {label: '15–19 Years', from: 15, to: 19},
    {label: '20–24 Years', from: 20, to: 24},
    {label: '25–29 Years', from: 25, to: 29},
    {label: '30–34 Years', from: 30, to: 34},
    {label: '35–39 Years', from: 35, to: 39},
    {label: '40–49 Years', from: 40, to: 49},
    {label: '50+ Years', from: 50, to: Infinity},
];
var followersRanges = [
    {label: 'Superstar', description: '8M+ followers', from: 8000000, to: Infinity},
    {label: 'Mainstream', description: '3M–8M followers', from: 3000000, to: 7999999},
    {label: 'Beyond Niche', description: '1M–3M followers', from: 1000000, to: 2999999},
    {label: 'Niche Reference', description: '110K–1M followers', from: 110000, to: 999999},
    {label: 'Niche', description: '20K–110K followers', from: 20000, to: 109999},
    {label: 'Underground', description: 'Under 20K followers', from: 0, to: 19999},
];
var albumsRanges = [
    {label: '20+ Albums', description: 'Monumental, a lifetime of releases', from: 20, to: Infinity},
    {label: '15–19 Albums', description: 'Prolific, decades of nonstop releases', from: 15, to: 19},
    {label: '10–14 Albums', description: 'Veteran, a long and steady career', from: 10, to: 14},
    {label: '7–9 Albums', description: 'Established, well past the early years', from: 7, to: 9},
    {label: '4–6 Albums', description: 'Consolidated, a solid identity', from: 4, to: 6},
    {label: '2–3 Albums', description: 'Early, an early career or a band that ended soon', from: 2, to: 3},
    {label: '1 Album', description: 'Debut, the only album so far', from: 1, to: 1},
    {label: 'No Albums', description: 'Singles and EPs only', from: 0, to: 0},
];
// Spotify gives no follow date, only the order: 1 is the latest follow
var releaseRanges = [
    {label: 'This Year', from: 0, to: 0},
    {label: 'Last Year', from: 1, to: 1},
    {label: '2–4 Years Ago', from: 2, to: 4},
    {label: '5–9 Years Ago', from: 5, to: 9},
    {label: '10–19 Years Ago', from: 10, to: 19},
    {label: '20+ Years Ago', from: 20, to: Infinity},
];

function familiesOf(cell) {
    return cell.dataset.families.split('|').filter(Boolean);
}

function uniqueArtists(grid) {
    var seen = new Set();
    return $(grid).find('.artist').toArray().filter(function(cell) {
        if (seen.has(cell.dataset.name)) return false;
        seen.add(cell.dataset.name);
        return true;
    });
}

function groupSections(grid) {
    if (grouping === 'followers') {
        return rangeSections(followersRanges, function(cell) { return Number(cell.dataset.followers); });
    }
    if (grouping === 'albums') {
        return rangeSections(albumsRanges, function(cell) { return Number(cell.dataset.albums); });
    }
    if (grouping === 'style' || grouping === 'substyle') {
        // a style filter shows only its own sections; Others shows only without one
        var scope = $(grid).closest('.ui.tab').attr('data-group-family');
        var styles = artistFamilies.filter(function(family) { return scope ? family.name === scope : true; });
        var others = styles.filter(function(family) { return family.fallback; }).map(function(family) {
            return {label: family.name, icon: family.icon, description: family.description, includes: function(cell) {
                return familiesOf(cell).length === 0;
            }};
        });
        var named = grouping === 'style'
            ? styles.filter(function(family) { return !family.fallback; }).map(function(family) {
                return {label: family.name, icon: family.icon, description: family.description, includes: function(cell) {
                    return familiesOf(cell).includes(family.name);
                }};
            })
            : artistSubstyles.filter(function(substyle) { return !scope || substyle.family === scope; }).map(function(substyle) {
                return {label: substyle.name, parent: substyle.family, icon: substyle.icon, description: substyle.description, includes: function(cell) {
                    return cell.dataset.substyles.split('|').includes(substyle.tag);
                }};
            });
        return named.concat(others);
    }

    var currentYear = new Date().getFullYear();
    var yearsSince = function(date) { return date ? currentYear - Number(date.slice(0, 4)) : null; };
    var years = function(prefix) {
        return function(range) {
            return range.to === Infinity
                ? prefix + ' ' + (currentYear - range.from) + ' or earlier'
                : range.from === range.to
                    ? prefix + ' ' + (currentYear - range.from)
                    : prefix + ' ' + (currentYear - range.to) + '–' + (currentYear - range.from);
        };
    };
    if (grouping === 'release') {
        return rangeSections(releaseRanges, function(cell) { return yearsSince(cell.dataset.lastRelease); }, years('Released'));
    }
    return rangeSections(longevityRanges, function(cell) { return yearsSince(cell.dataset.firstRelease); }, years('Debut'));
}

function rangeSections(ranges, valueOf, describe) {
    var ordered = direction === groupOrder ? ranges : ranges.slice().reverse();
    var sections = ordered.map(function(range) {
        return {label: range.label, description: describe ? describe(range) : range.description || '', includes: function(cell) {
            var value = valueOf(cell);
            return value !== null && value >= range.from && value <= range.to;
        }};
    });
    sections.push({label: 'Unknown', description: '', includes: function(cell) { return valueOf(cell) === null; }});
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

function groupGrid(grid) {
    var byViewOrder = function(a, b) { return Number(a.dataset.viewOrder) - Number(b.dataset.viewOrder); };
    var cells = uniqueArtists(grid);
    $(grid).empty();
    // Spotify gives no follow date, only the order, so Followed has no sections to draw
    if (grouping === 'none' || grouping === 'followed') {
        $(grid).append(cells.sort(byViewOrder));
    } else {
        groupSections(grid).forEach(function(section) {
            var members = cells.filter(section.includes);
            if (!members.length) return;
            var heading = $('<div>', {class: 'sixteen wide column group-heading'});
            var title = $('<h2>', {class: 'ui medium header'});
            if (section.icon) title.append($('<span>', {class: 'control-symbol', 'aria-hidden': 'true', text: section.icon}));
            if (section.parent) title.append($('<span>', {class: 'section-parent', text: section.parent}));
            title.append(document.createTextNode(section.label));
            heading.append(title);
            heading.append($('<span>', {class: 'group-summary', 'data-description': section.description}));
            $(grid).append(heading);
            members.sort(byViewOrder).forEach(function(cell) { $(grid).append($(cell).clone()); });
        });
    }
}

function applyGrouping() {
    rankArtists();
    $('.artists').each(function(_, grid) { groupGrid(grid); });
    search($('.artist-search').val());
}

// a group starts in its own direction
function setGrouping(element) {
    selectOption(element, 'group', 'Group');
    grouping = element.dataset.group;
    groupSort = element.dataset.groupSort;
    groupOrder = element.dataset.groupOrder;
    $('body').toggleClass('release-mode', grouping === 'release');
    setDirection(groupOrder);
}

function groupArtists(element) {
    setGrouping(element);
    saveView(activeTab, function(view) { view.group = grouping; view.direction = direction; });
    applyGrouping();
}
""".replace("__ARTIST_FAMILIES__", json.dumps([
    {"name": family.name, "icon": family.icon, "description": family.description, "fallback": family == T_OTHERS}
    for family in [*(family.tag for family in FAMILIES), T_OTHERS]
], ensure_ascii=False)).replace("__ARTIST_SUBSTYLES__", json.dumps([
    {"tag": tag.name, "name": tag.name.split(' - ')[-1].strip(), "family": family.tag.name, "icon": family.tag.icon, "description": tag.description}
    for family in FAMILIES for tag in family.granular
], ensure_ascii=False))

JS_FUNC_FILL_TAB = """
// Only All is rendered with cards; other tabs clone its cells when first shown.
function allArtists() {
    return uniqueArtists($('.ui.tab[data-all-artists] .artists'));
}

function fillTab(tab) {
    if (!tab || !tab.hasAttribute('data-lazy')) return;
    tab.removeAttribute('data-lazy');
    var grid = $(tab).find('.artists')[0];
    $(grid).append(allArtists()
        .filter(function(cell) { return cell.dataset.tabs.split(' ').includes(tab.dataset.tab); })
        .map(function(cell) { return $(cell).clone()[0]; }));
    groupGrid(grid);
    search($('.artist-search').val());
}
"""

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
    var cells = allArtists();
    var showOnly = function(tab, names) {
        $(tab).find('.artists').empty().append(names.map(function(name) {
            return $(cells.find(function(cell) { return cell.dataset.name === name; })).clone()[0];
        }));
    };

    var picked = [];
    var allTab = $('.ui.tab[data-discover-per-family]')[0];
    $('.ui.tab[data-discover-family]').each(function(_, tab) {
        var excludedFamilies = JSON.parse(tab.dataset.discoverExcludedFamilies);
        var candidates = cells
            .filter(function(cell) { return familiesOf(cell).includes(tab.dataset.discoverFamily); })
            .filter(function(cell) {
                var families = familiesOf(cell);
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
function visibleCards() {
    return $('.ui.tab.active .artist:visible .card');
}

function cellRect(card) {
    return card.closest('.artist').getBoundingClientRect();
}

function focusVisibleCard() {
    var cards = visibleCards();
    if (!cards.length) return;
    var top = Math.max(0, cards.closest('.artists-wrapper')[0].getBoundingClientRect().top);
    var card = cards.filter(function() { return cellRect(this).top >= top; }).first();
    (card.length ? card : cards.first()).focus();
}

$(document).on('keydown', '.menu .item', function(e) {
    if (e.ctrlKey || e.altKey) return;
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
    if (e.ctrlKey || e.altKey) return;
    if (e.key === 'Enter') visibleCards().first().focus();

    var items = $(this).closest('.column').find('.menu .item:visible');
    if (e.key === 'ArrowDown') items.first().focus();
    if (e.key === 'ArrowUp') items.last().focus();
    if (e.key === 'ArrowDown' || e.key === 'ArrowUp') e.preventDefault();
});

$(document).on('keydown', function(e) {
    if (e.code === 'Digit4' && e.ctrlKey && !e.altKey && !e.metaKey) {
        e.preventDefault();
        focusVisibleCard();
        return;
    }
    if (e.altKey && !e.ctrlKey && !e.metaKey && !e.shiftKey) {
        var groups = $('.list-controls .item[data-group]');
        var groupStep = {ArrowLeft: -1, ArrowRight: 1}[e.code];
        var directionFixed = {ArrowUp: 'asc', ArrowDown: 'desc'}[e.code];
        if (!groupStep && !directionFixed) return;
        e.preventDefault();  // Left and Right would also go back or forward in the browser
        var chosen = directionFixed
            ? $('.list-controls .item[data-direction="' + directionFixed + '"]')
            : groups.eq((groups.index(groups.filter('.active')) + groupStep + groups.length) % groups.length);
        chosen.click().focus();
        return;
    }
    var kind = {
        Digit1: 'tab', ArrowUp: 'tab', ArrowDown: 'tab',
        Digit2: 'group', ArrowLeft: 'group', ArrowRight: 'group',
        Digit3: 'direction',
    }[e.code];
    if (!kind || !e.ctrlKey || e.altKey || e.metaKey) return;
    if ((e.code === 'ArrowLeft' || e.code === 'ArrowRight') && $(e.target).is('input')) return;
    e.preventDefault();
    var items = $('.ui.vertical.desktop.menu, .list-controls').find('.item[data-' + kind + ']');
    var step = (e.shiftKey || e.code === 'ArrowUp' || e.code === 'ArrowLeft') ? -1 : 1;
    var next = items.eq((items.index(items.filter('.active')) + step + items.length) % items.length);
    next.click();
    next.focus();
});

$(document).on('keydown', function(e) {
    if ($(e.target).closest('.command-palette').length) return;
    if (e.key === 'Escape') search('');
    if ((e.ctrlKey || e.metaKey) && !e.altKey && !e.shiftKey && e.code === 'KeyZ') {
        e.preventDefault();  // like Esc, even inside the search input
        search('');
        return;
    }
    if (e.key.length !== 1 || e.key === ' ' || e.ctrlKey || e.metaKey || e.altKey) return;
    if ($(e.target).is('input')) return;
    $('.artist-search:visible').focus();
});

$(document).on('keydown', '.ui.card', function(e) {
    if (e.ctrlKey || e.altKey) return;
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

    var cards = visibleCards();
    var index = cards.index(this);
    var rect = cellRect(this);
    var row = cards.filter(function() { return Math.abs(cellRect(this).top - rect.top) < 2; });
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
        var delta = cellRect(card).top - rect.top;
        return below ? delta > 2 : delta < -2;
    });
    candidates.sort(function(a, b) {
        var aRect = cellRect(a), bRect = cellRect(b);
        return Math.abs(aRect.top - rect.top) - Math.abs(bRect.top - rect.top)
            || Math.abs(aRect.left - rect.left) - Math.abs(bRect.left - rect.left);
    });
    if (candidates.length) candidates[0].focus();
});
"""

JS_SCROLL_TOP = """
// the back to top arrow shows once the page has scrolled past one screen (mobile; desktop scrolls inside the grid)
$(window).on('scroll', function() {
    $('.scroll-top').toggleClass('visible', window.scrollY > window.innerHeight);
});
"""

JS_COMMAND_PALETTE = """
// Ctrl+P lists every sidebar and top bar option; choosing one clicks it, so it follows the same rules.
var paletteCommands = [];
var paletteSelected = 0;

var PALETTE_SECTIONS = {
    Filter: {title: 'Filters', icon: 'filter'},
    Group: {title: 'Group', icon: 'object group outline'},
    Order: {title: 'Order', icon: 'sort amount down'},
    Artist: {title: 'Artists', icon: 'user'},
};
var PALETTE_KINDS = ['Filter', 'Group', 'Order', 'Artist'];
var PALETTE_ARTISTS_SHOWN = 8;

// artists join only once something is typed, so the empty palette stays about the page's options
function paletteArtists() {
    return allArtists().map(function(cell) {
        var card = $(cell).find('.ui.card')[0];
        var song = $(cell).find('.top-song-text').text();
        return {kind: 'Artist', tag: 'Artist', label: cell.dataset.name,
                description: $(cell).find('.artist-tags').text() + (song && song !== '-' ? ' · ♪ ' + song : ''),
                favorite: $(cell).find('.favorite-star').length > 0,
                recent: $(cell).find('.corner.label').length > 0,
                count: $(cell).find('.artist-stats > [aria-label^="Followers"]').text().trim(),
                photo: $(cell).find('img.artist-image').attr('src'), spotify: card.dataset.spotify, lastfm: card.dataset.lastfm};
    });
}

// lower is better: exact name, then name start, then word start, then anywhere; shorter names win ties
function paletteScore(command, words) {
    if (!words.length) return 0;
    var label = normalizeText(fullLabel(command));
    var labelWords = label.split(/[^\\p{L}\\p{N}]+/u).filter(Boolean);
    var score = words.reduce(function(total, word) {
        if (label === word) return total;
        if (label.startsWith(word)) return total + 1;
        if (labelWords.some(function(labelWord) { return labelWord.startsWith(word); })) return total + 2;
        if (label.includes(word)) return total + 3;
        return total + 4;  // matched only the section name
    }, 0);
    return score * 1000 + label.length;
}

function paletteItems() {
    var filters = $('.ui.vertical.desktop.menu .item[data-tab]').toArray().map(function(item) {
        return {kind: 'Filter', label: item.dataset.commandLabel, parent: item.dataset.commandParent,
                description: item.dataset.commandDescription, symbol: item.dataset.commandIcon, header: $(item).hasClass('header'),
                tag: item.dataset.commandTag,
                count: $(item).find('.artist-count').text(), item: item};
    });
    var controls = function(kind, attribute) {
        return $('.list-controls .item[data-' + attribute + ']').toArray().map(function(item) {
            return {kind: kind, tag: kind, label: item.dataset.commandLabel || $(item).text().trim(), description: item.dataset.commandDescription,
                    icon: $(item).find('i.icon').attr('class'), item: item};
        });
    };
    return filters.concat(controls('Group', 'group'), controls('Order', 'direction'));
}

// a substyle reads as its style, then its own name
function fullLabel(command) {
    return command.parent ? command.parent + ' ' + command.label : command.label;
}

// text with the characters matching the query in bold, ignoring accents and case
function highlightMatches(label, words, className) {
    var normalized = '';
    var origin = [];
    Array.from(label).forEach(function(char, index) {
        var part = normalizeText(char);
        normalized += part;
        for (var i = 0; i < part.length; i++) origin.push(index);
    });
    var chars = Array.from(label);
    var marked = chars.map(function() { return false; });
    words.forEach(function(word) {
        for (var at = normalized.indexOf(word); at !== -1; at = normalized.indexOf(word, at + 1)) {
            for (var i = at; i < at + word.length; i++) marked[origin[i]] = true;
        }
    });
    var fragment = $('<span>', {class: className});
    chars.forEach(function(char, index) {
        var last = fragment.contents().last();
        var bold = marked[index];
        if (last.length && last.is('b') === bold && (bold || last[0].nodeType === 3)) {
            if (bold) last.append(document.createTextNode(char)); else last[0].textContent += char;
        } else {
            fragment.append(bold ? $('<b>').text(char) : document.createTextNode(char));
        }
    });
    return fragment;
}

function renderPalette() {
    var words = normalizeText($('.command-input').val()).split(/\\s+/).filter(Boolean);
    paletteCommands = paletteItems().concat(words.length ? paletteArtists() : []).filter(function(command) {
        var text = normalizeText(command.kind + ' ' + PALETTE_SECTIONS[command.kind].title + ' ' + fullLabel(command));
        return words.every(function(word) { return text.includes(word); });
    }).map(function(command, order) {
        return {command: command, order: order, score: paletteScore(command, words)};
    }).sort(function(a, b) {
        return PALETTE_KINDS.indexOf(a.command.kind) - PALETTE_KINDS.indexOf(b.command.kind) || a.score - b.score || a.order - b.order;
    }).map(function(ranked) { return ranked.command; });
    var artistsSeen = 0;
    paletteCommands = paletteCommands.filter(function(command) {
        return command.kind !== 'Artist' || artistsSeen++ < PALETTE_ARTISTS_SHOWN;
    });
    paletteSelected = Math.min(paletteSelected, Math.max(0, paletteCommands.length - 1));
    var list = $('.command-list').empty();
    var section = null;
    paletteCommands.forEach(function(command, index) {
        if (command.kind !== section) {
            section = command.kind;
            var heading = $('<div>', {class: 'command-section'});
            heading.append($('<i>', {class: PALETTE_SECTIONS[section].icon + ' icon', 'aria-hidden': 'true'}));
            heading.append(document.createTextNode(PALETTE_SECTIONS[section].title));
            list.append(heading);
        }
        var row = $('<div>', {class: 'command-item' + (index === paletteSelected ? ' selected' : ''), role: 'option'}).data('index', index);
        if (command.photo) row.append($('<img>', {class: 'command-photo', src: command.photo, alt: ''}));
        else if (command.icon) row.append($('<i>', {class: command.icon, 'aria-hidden': 'true'}));
        else row.append($('<span>', {class: 'control-symbol', 'aria-hidden': 'true', text: command.symbol || ''}));
        // first line says exactly what the option is: a whole style in bold (like the sidebar headers),
        // an option inside a style with the style in quiet gray first; the second line describes it
        var label = $('<span>', {class: 'command-label'});
        var title = $('<span>', {class: 'command-title'});
        if (command.parent) title.append($('<span>', {class: 'command-parent', text: command.parent}));
        title.append(highlightMatches(command.label, words, 'command-name'));
        if (command.favorite) title.append($('<i>', {class: 'star icon command-favorite', title: 'Favorite'}));
        if (command.recent) title.append($('<span>', {class: 'command-new', text: 'New', title: 'Released in the last 90 days'}));
        label.append(title);
        var subtitle = $('<span>', {class: 'command-subtitle'});
        subtitle.append($('<span>', {class: 'command-tag', text: command.tag}));
        if (command.description) subtitle.append(document.createTextNode(command.description));
        label.append(subtitle);
        row.append(label);
        if (command.header) row.addClass('style-row');
        if (command.count) row.append($('<span>', {class: 'command-count', text: command.count}));
        list.append(row);
    });
    if (!paletteCommands.length) list.append($('<div>', {class: 'command-empty', text: 'No option matches'}));
}

function selectPaletteItem(index) {
    paletteSelected = index;
    var rows = $('.command-list .command-item').removeClass('selected');
    var row = rows.eq(index).addClass('selected')[0];
    if (row) row.scrollIntoView({block: 'nearest'});
}

function runPaletteItem(index, shift) {
    var command = paletteCommands[index];
    if (!command) return;
    $('.command-palette').modal('hide');
    if (command.kind !== 'Artist') $(command.item).click();
    else if (shift) window.open(command.lastfm, '_blank');  // as on cards: Enter opens Spotify, Shift+Enter Last.fm
    else window.location.href = command.spotify;
}

function openPalette() {
    paletteSelected = 0;
    $('.command-input').val('');
    renderPalette();
    $('.command-palette').modal({centered: false, blurring: true, duration: 180, onVisible: function() { $('.command-input').focus(); }}).modal('show');
}

$(document).on('keydown', function(e) {
    if ((e.ctrlKey || e.metaKey) && !e.altKey && !e.shiftKey && e.code === 'KeyP') {
        e.preventDefault();
        openPalette();
    }
});

$(document).on('input', '.command-input', function() {
    paletteSelected = 0;
    renderPalette();
});

$(document).on('keydown', '.command-input', function(e) {
    var step = {ArrowDown: 1, ArrowUp: -1}[e.key];
    if (step && paletteCommands.length) {
        e.preventDefault();
        selectPaletteItem((paletteSelected + step + paletteCommands.length) % paletteCommands.length);
    } else if (e.key === 'Enter') {
        e.preventDefault();
        runPaletteItem(paletteSelected, e.shiftKey);
    }
});

$(document).on('click', '.command-list .command-item', function() {
    runPaletteItem($(this).data('index'), false);
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
    return tag.name.lower().translate(str.maketrans("", "", "():/")).translate(str.maketrans("ãéó", "aeo")).replace(" - ", "-").replace(" & ", "-").replace(" ", "-").strip()

def menu_wrapper(label: str, name: str):
    """Render a mobile accordion section wrapping a menu."""

    # accordion title
    with div(cls="title"):
        with span(cls="ui blue text"):
            span(label, id=f"mobile-menu-header-{name}")
            i(cls="right dropdown icon")

    # accordion content
    with div(cls="content"):
        return div(cls="ui fluid vertical attached menu sidebar-options")

def menu_filter(mobile: bool, tags_with_artists: dict[Tag, list[Artist]]):
    """Render filter menu according to mobile or desktop rules."""
    menu = menu_wrapper("Filter", "filter") if mobile else div(cls="ui fluid vertical desktop menu sidebar-options")
    with menu:
        for tag in TAGS_MENU_ORDER:
            artists_count = len(tags_with_artists[tag])
            family = find_family(tag)
            if tag == T_DISCOVER:
                artists_count = DISCOVER_ARTISTS_PER_FAMILY * len(FAMILIES)
            elif family and tag == family.discover:
                artists_count = DISCOVER_ARTISTS_PER_FAMILY

            # item attributes
            item_display = tag_display(tag)
            item_active = "active" if tag == T_ALL else ""
            item_header = "header" if tag in TAGS_HEADER else ""
            command_parent = family.tag.name if family and tag != family.tag else ""
            # what the entry is, and what it holds, for the command palette's second line
            if tag == T_OTHERS or (family and tag == family.tag):
                command_tag, command_description = "Style", tag.description
            elif family and tag in family.granular:
                command_tag, command_description = "Substyle", tag.description
            else:
                command_tag = "Filter"
                command_description = {
                    T_ALL: "Every followed artist",
                    T_DISCOVER: f"{DISCOVER_ARTISTS_PER_FAMILY} picks per style, new each period",
                    T_FAVORITES: "Curated favorites",
                    T_NON_FAVORITES: "Everyone not in Favorites",
                }.get(tag) or {
                    family.discover: f"{DISCOVER_ARTISTS_PER_FAMILY} {family.tag.name} picks, new each period",
                    family.favorites: f"{family.tag.name} favorites",
                    family.non_favorites: f"{family.tag.name} artists not in Favorites",
                }.get(tag, "")
            command_icon = family.tag.icon if family else tag.icon

            # menu item
            with div(cls=f"{item_active} {item_header} link item nowrap",
                    data_tab=id(tag),
                    data_tab_name=tag.name,
                    data_command_label=item_display,
                    data_command_parent=command_parent,
                    data_command_tag=command_tag,
                    data_command_description=command_description,
                    data_command_icon=command_icon,
                    tabindex="0",
                ):
                if tag.icon:
                    span(tag.icon, cls="control-symbol", aria_hidden="true")
                span(item_display)
                span(f"{artists_count}", cls="ui tiny basic blue label artist-count")

def menu_direction():
    with menu_wrapper("Order", "direction"):
        direction_items()

def menu_group():
    with menu_wrapper("Group", "group"):
        group_items()

def scroll_top_button():
    """Render the discreet mobile arrow that returns to the top once the page has scrolled past a screen."""
    with button(cls="scroll-top", type="button", title="Back to top", aria_label="Back to top",
                onClick="window.scrollTo({top: 0, behavior: 'smooth'})"):
        i(cls="arrow up icon", aria_hidden="true")

def command_palette():
    """Render the Ctrl+P command palette; its options are listed in the browser from the sidebar and top bar."""
    with div(cls="ui tiny modal command-palette"):
        with div(cls="content"):
            with div(cls="ui fluid large transparent left icon input"):
                input_(cls="command-input", type="text", placeholder="Filter, group or order…", aria_label="Command palette", autocomplete="off")
                i(cls="search icon")
            div(cls="command-list", role="listbox")
            with div(cls="command-hints"):
                kbd("↑↓")
                span(" navigate · ")
                kbd("↵")
                span(" apply · ")
                kbd("⇧↵")
                span(" Last.fm · ")
                kbd("esc")
                span(" close")

def discover_button(fluid: bool):
    """Render the Discover shortcut: a round compass emblem on desktop, a labeled full-width button on mobile."""
    if fluid:
        with button(cls="ui fluid blue button discover-button", type="button", onClick="openDiscover()"):
            i(cls="compass icon", aria_hidden="true")
            span("Discover")
    else:
        with button(cls="ui small circular blue icon button discover-button", type="button", onClick="openDiscover()",
                    title="Discover", aria_label="Discover"):
            i(cls="compass icon", aria_hidden="true")

def list_controls():
    with div(cls="list-controls"):
        with div(cls="list-control"):
            span("Group", cls="ui blue text list-control-label", title="Ctrl+2, Ctrl+Right or Alt+Right next, Ctrl+Shift+2, Ctrl+Left or Alt+Left previous")
            with div(cls="ui small compact blue secondary menu"):
                group_items()
        with div(cls="list-control"):
            span("Order", cls="ui blue text list-control-label", title="Ctrl+3 switches, Alt+Up ascending, Alt+Down descending")
            with div(cls="ui small compact blue secondary menu"):
                direction_items()
            discover_button(fluid=False)

def direction_items():
    # the description follows the group, filled in the browser
    for icon, label, direction in [
        ("sort amount up", "Ascending", "asc"),
        ("sort amount down", "Descending", "desc"),
    ]:
        with div(cls="link item nowrap", data_direction=direction, data_command_label=label, aria_label=label,
                 onClick="orderArtists(this)", tabindex="0"):
            i(cls=f"{icon} icon control-icon", aria_hidden="true")
            span(cls="direction-description")

def group_items():
    # sort and order: how artists are ordered, inside and across sections, until the direction is reversed
    for icon, label, mode, sort, order, description, desc_description, asc_description in [
        ("ban", "None", "none", "name", "asc", "No sections", "Z to A", "A to Z"),
        ("music", "Style", "style", "followers", "desc", f"Sections by {', '.join(family.tag.name for family in FAMILIES)} and {T_OTHERS.name}",
         "Most followed first in each style", "Least followed first in each style"),
        ("tags", "Substyle", "substyle", "followers", "desc", "Sections by substyle",
         "Most followed first in each substyle", "Least followed first in each substyle"),
        ("user", "Followers", "followers", "followers", "desc", "Sections by audience reach", "Most followed first", "Least followed first"),
        ("hourglass half", "Longevity", "longevity", "first-release", "asc", "Sections by years since the first album",
         "Longest career first", "Shortest career first"),
        ("compact disc", "Albums", "albums", "albums", "desc", "Sections by number of albums", "Most albums first", "Fewest albums first"),
        ("calendar alternate", "Release", "release", "last-release", "asc", "Sections by years since the last release",
         "Oldest release first", "Newest release first"),
        ("bell", "Followed", "followed", "last-follow", "asc", "No sections, in the order I followed",
         "Followed longest ago first", "Most recently followed first"),
    ]:
        with div(cls="link item nowrap", data_group=mode, data_group_sort=sort, data_group_order=order,
                 data_desc_description=desc_description, data_asc_description=asc_description,
                 title=description, data_command_description=description, onClick="groupArtists(this)", tabindex="0"):
            i(cls=f"{icon} icon control-icon", aria_hidden="true")
            span(label)

def menu_search():
    with div(cls="ui fluid icon input search-control"):
        input_(cls="artist-search", type="search", placeholder="Search artist",
            oninput="search(this.value)",
        )
        i(cls="search icon")

def cards(artists: list[Artist], tabs_by_artist: dict[str, list[str]]):
    """Render the card grid."""
    with div(cls="artists-wrapper"): # scroll-helper
        with div(cls="ui grid artists"):
            for artist in artists:
                with card_cell(artist, tabs_by_artist[artist.id]):
                    card(artist)

def card_cell(artist: Artist, tabs: list[str]):
    """Render a card cell in the cards grid."""
    return div(cls="eight wide mobile   four wide tablet   four wide computer   two wide large screen  two wide widescreen   column   artist",
        data_name=artist.name,
        data_followers=str(artist.followers),
        data_albums=str(artist.albums),
        data_first_release=artist.first_release,
        data_last_release=artist.last_release,
        data_last_follow=str(artist.last_follow),
        data_families="|".join(family.tag.name for family in FAMILIES if family.tag in artist.tags),
        data_substyles="|".join(tag.name for tag in artist.tags_granular),
        data_tabs=" ".join(tabs),
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
            release_image = artist.last_release_image or artist.top_album_image
            caption_class = "artist-image-caption has-album-cover" if artist.top_album_image or release_image else "artist-image-caption"
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
                img(src=artist.top_album_image, cls="album-cover top-cover", alt=f"Album cover — {artist.top_album_name}", title=artist.top_album_name,
                    loading="lazy", width="40", height="40")
            if release_image:
                release_title = artist.last_release_name or artist.top_album_name
                img(src=release_image, cls="album-cover release-cover", alt=f"Album cover — {release_title}", title=release_title,
                    loading="lazy", width="40", height="40")

        # header
        with a(cls="content", href=spotify_url, tabindex="-1"):
            div(artist.name, cls="ui small header artist-name")
            with div(cls="meta"):
                with div(cls="artist-song"):
                    span(artist.top_song or "-", cls="top-song-text")
                    release_text = artist.last_release_name or artist.top_song or "-"
                    span(release_text, cls="release-text", title=artist.last_release)

        # links
        with div(cls="ui two bottom attached mini basic buttons"):
            with a(cls="ui button", href=spotify_url, tabindex="-1"):
                i(cls="green spotify icon")
                span("Spotify")
            with a(cls="ui button", href=lastfm_url, target="_blank", tabindex="-1"):
                i(cls="red lastfm icon")
                span("Last.fm")


def render_html(tags_with_artists: dict[Tag, list[Artist]]) -> str:
    logging.info("🧱 Generating HTML")
    missing_release = [artist.name for artist in tags_with_artists[T_ALL] if artist.last_release and not artist.last_release_name]
    if missing_release:
        logging.warning(f"⚠️ {len(missing_release)} artists have a last release date but no release name; run `just export` first")

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
            script(src="https://cdn.jsdelivr.net/npm/jquery@3.7.1/dist/jquery.min.js")
            script(src="https://cdn.jsdelivr.net/npm/jquery-address@1.6.0/src/jquery.address.js")
            script(src=f"{FOMANTIC_UI}.js")
            script(raw(JS_FUNC_ONTAB))
            script(raw(JS_FUNC_SELECT_OPTION))
            script(raw(JS_FUNC_PREFERENCES))
            script(raw(JS_FUNC_ORDER))
            script(raw(JS_FUNC_GROUP))
            script(raw(JS_FUNC_FILL_TAB))
            script(raw(JS_FUNC_SEARCH))
            script(raw(JS_FUNC_PICK_DISCOVER))
            script(raw(JS_FUNC_MARK_RECENT_RELEASES))
            script(raw(JS_KEYBOARD_NAVIGATION))
            script(raw(JS_COMMAND_PALETTE))
            script(raw(JS_SCROLL_TOP))

            # style
            link(href=f"{FOMANTIC_UI}.css", rel="stylesheet")
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
                    discover_button(fluid=True)
                    with div(cls="ui fluid styled mobile accordion"):
                        menu_filter(mobile=True, tags_with_artists=tags_with_artists)
                        menu_group()
                        menu_direction()

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

                    # cards are rendered once, in All; the browser fills the other tabs
                    tabs_by_artist: dict[str, list[str]] = {artist.id: [] for artist in tags_with_artists[T_ALL]}
                    for tag in TAGS_MENU_ORDER:
                        family = find_family(tag)
                        if tag == T_DISCOVER or (family and tag == family.discover):
                            continue
                        for artist in tags_with_artists[tag]:
                            tabs_by_artist[artist.id].append(id(tag))

                    for tag in TAGS_MENU_ORDER:
                        family = find_family(tag)
                        if tag == T_DISCOVER:
                            artists = []
                            tab_attributes = {"data_discover_per_family": str(DISCOVER_ARTISTS_PER_FAMILY)}
                        elif family and tag == family.discover:
                            artists = []
                            tab_attributes = {
                                "data_discover_family": family.tag.name,
                                "data_discover_excluded_families": json.dumps([
                                    excluded.tag.name for excluded in FAMILY_DISCOVER_EXCLUSIONS.get(family, [])
                                ], ensure_ascii=False),
                            }
                        elif tag == T_ALL:
                            artists = tags_with_artists[T_ALL]
                            tab_attributes = {"data_all_artists": "true"}
                        else:
                            artists = []
                            tab_attributes = {"data_lazy": "true"}
                            if family:
                                tab_attributes["data_group_family"] = family.tag.name

                        with div(cls="ui active tab" if tag == T_ALL else "ui tab", data_tab=id(tag), **tab_attributes):
                            cards(sorted(artists, key=lambda x: x.name.lower()), tabs_by_artist)

                command_palette()

            # ------------------------------------------------------------------
            # Scroll to top (mobile)
            # ------------------------------------------------------------------
            scroll_top_button()

        # ----------------------------------------------------------------------
        # Script initialization
        # ----------------------------------------------------------------------
        script("markRecentReleases();")
        script("pickDiscover();")
        script("applyPreferences();")
        script("$('.menu .item').tab({history:true, historyType: 'hash', onLoad: onTab});")
        script("$('.ui.accordion.mobile').accordion({exclusive:true});")

    return f"<!DOCTYPE html>\n{doc}"
