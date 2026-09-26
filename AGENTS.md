# Spotify Launcher

A personal launcher for the Spotify artists I follow: it helps me decide what to listen to right now and jump straight into it.

## Purpose

- The universe is artists I already follow, and I have listened to every one of them a lot at some point. The app helps me get back to them, not discover new artists.
- Picking and playing must be fast: type to search, arrows to navigate, `Enter` opens the artist in Spotify, `Shift+Enter` opens it in Last.fm, `Esc` clears the search from anywhere and returns to it from a card, `Ctrl+1`, `Ctrl+2` and `Ctrl+3` cycle filter, sort and group (`Shift` goes back), `Ctrl+Up/Down` cycle the filter and `Ctrl+Left/Right` the sort (not inside the search input, where they move by word). Mobile must stay comfortable to tap.
- Sort, group and the filter tab persist in `localStorage` and are restored on open; a URL hash wins over the saved tab. Search is not persisted.
- Last.fm (`just lastfm`) only covers what I have listened to recently; there is no long-term history. Few or no plays means "not lately", never "unknown" or "disliked".
- Favorites are curated by taste, not by play count.
- When I say "the app should answer X" I mean a feature of this page, not an analysis by the agent.

## Design: Delight

Delight is an explicit product goal. Choosing an artist should feel inviting, personal and enjoyable. Think like an artist: consider composition, visual rhythm, breathing room and how the page makes someone want to listen.

- Before a visual change, decide what should draw the eye first and how secondary information supports it. A change must improve the experience, beyond fitting information or reducing height.
- Artist photos and names lead the cards. Preserve the character of the photos; place supporting information with restraint, keeping important parts of the image visible.
- Stats are secondary, passive information. Keep them legible and quiet; avoid turning them into prominent panels or covering photos unnecessarily.
- Use spacing, typography, contrast and subtle treatments deliberately. More boxes, bars, borders or colorful icons do not automatically make a design better.
- Card photo corners: a small star at top left marks favorites; a green corner label at top right marks a last release within 90 days, computed in the browser.
- Consider the whole composition on desktop and mobile, including long genre labels, favorites and dense cards. Avoid overlaps and preserve comfortable interactions.

## Discover

Discover suggests artists to revisit from the artists already followed; it does not introduce new artists.

4 artists per family: each family's Discover shows its 4, All's Discover shows all 12. Picked in the browser, seeded by period: morning (6h-12h), afternoon (12h-18h), night (18h-6h). Same picks within a period, no reroll.

Folk's Discover pool excludes any artist who also belongs to Rock or Alternative, regardless of whether that artist was selected for another family's Discover. This only affects Discover eligibility; family classifications, favorites and filters keep their overlaps.

## Grouping

The Group control (top bar on desktop, accordion on mobile) offers None (default), Style and Longevity. Style uses Rock, Folk, Alternative and Others; Longevity uses years since the first album, newest first (under 5, then 5-year ranges up to 35–39, then 40–49 and 50+, and Unknown for artists without albums), computed in the browser so artists move between ranges without re-rendering. The selected sort applies within each section. Artists belonging to multiple families appear in each applicable section; family filters show only that family's section. Search hides empty sections. Section headings stay on one line: the title, then a quiet summary (visible artists, favorites, and the style description or debut years), with no divider line; they must not add vertical space. Grouping does not change Discover picks. Use style in the interface; family is an internal classification term. Control labels use Title Case, matching the existing sidebar options.

Generate browser grouping names and icons from the tags in `data.py` (`FAMILIES` and `T_OTHERS`); do not maintain a separate hardcoded JavaScript list.

## Planned: long-term history

Spotify extended streaming history requested on 2026-09-26. When it arrives, aggregate per artist (time listened, last played) into `data/`; commit only the aggregate.

## Pipeline

- `just download`: fetches followed artists into `data/followed.json` and caches each artist in `data/artists/<id>.json` (cached files are never re-downloaded).
- `just export`: flattens the cache into `data/artistas.tsv`. `FIRST_RELEASE_OVERRIDES` fixes first release dates Spotify gets wrong (e.g. a compilation dated by its oldest track). Album count, first release and last release ignore live albums, compilations and demos by name, and count editions of the same album (deluxe, remaster, anniversary...) once, dated by the original release.
- `just render`: classifies artists and writes `docs/index.html` plus summaries.

## Workflow

After any change, re-render and commit it (source and generated `docs/` together) without asking.

Keep static styling in the renderer's `CSS_GLOBAL` block, alongside the embedded JavaScript blocks. Render elements with classes instead of inline `style=` attributes; do not extract a separate CSS file.

Prefer Fomantic UI components and variations for layout and presentation before adding custom CSS. On desktop the sidebar is the search plus a plain vertical Filter menu, with Sort and Group in the top bar. The accordion is mobile/tablet only: a styled accordion with separate title/content pairs and vertical menus inside the content. Keep that structure: replacing titles with attached segments and making menus the accordion content disrupted the layout. Section titles use Fomantic blue with the default accordion font size and weight, with no custom background or extra dividers. The search input, accordion titles and menu items share the same height. Count labels have a fixed width and centered numbers. Do not take screenshots; the user validates visual appearance. Pin stable frontend versions and verify compatibility before upgrades. Checked on 2026-09-26: Fomantic UI 2.9.4 and jQuery Address 1.6.0 are current stable releases; jQuery stays on 3.7.1 because 4.0.0 removes APIs used by this stack.

## How classification works

All rules live in `TAG_RULES` in `src/render/data.py`. Each tag lists patterns that pull artists into it:

- `genre` (e.g. `"power metal"`): any artist whose Spotify genres include it.
- `+Name`: forces the artist into the tag, regardless of genres.
- `-Name`: removes the artist from the tag.
- another tag name: artists with that tag also get this one (used by the family tags: `Rock`, `Folk`, `Alternative`).

Artists without Spotify genres must be placed via `+Name`.

Tags reflect how I hear the artist, not Spotify's genre labels. A `+Name` or `-Name` that contradicts the genres is usually intentional; flag only isolated cases that look like real mistakes, never a whole tag based on genre names.

Rules that currently have no effect (a `-Name` for a tag the artist doesn't get, a `+Name` already covered by a genre) are kept on purpose: Spotify genres change, and they were relevant when added.

`Others` is a valid final place for artists that fit no family.

After matching, `src/render/parser.py` applies:

1. `Folk Metal` wins over `Heavy Metal` (an artist never has both).
2. A favorite goes to `<Family> - Favorites` in each of its families; any other family member goes to `<Family> - Non-Favorites`.
3. Artists not in `Favorites` → `Non-Favorites`.
4. No other tag → `Others`.

An artist may belong to more than one family (e.g. Eluveitie is Folk Metal and Folk).

`just render` warns about rule keys never used and artists without granular tags; both should be empty.

## Tags

### Rock

Metal and rock.

- **Heavy Metal**: non-extreme metal: power, progressive, thrash, gothic, industrial, nu metal, glam metal.
- **Extreme Metal**: death, black, doom/drone.
- **Folk Metal**: metal with folk, celtic or medieval elements.
- **Rock**: rock without metal: classic, hard rock, grunge, alternative and indie rock.

### Folk

Traditional, storytelling and theatrical music. The family's identity brings together celtic and medieval music, maritime/pirate songs, fado, and steampunk/dark cabaret. It evokes old-world settings and staged characters, without requiring strictly acoustic instruments or historically authentic music. Traditional music and steampunk belong together here on purpose.

The family icon is `🎻`: it represents this traditional and theatrical character. A banjo (`🪕`) overemphasizes American bluegrass/country, which is only one part of this family, not its defining identity. Choose visual cues from the actual artists in the family, including its curated favorites, rather than from the generic meaning of “folk”.

- **Folk**: traditional and roots music: celtic, medieval, fado, bluegrass, pirate songs and shanties.
- **Steampunk**: steampunk and dark cabaret, theatrical songs.

`indie folk` is not Folk; it goes to Alternative - Vox/Guitar. Electronic acts with an old or ethereal feel (e.g. Leandra) are not Folk.

### Alternative

Alternative and indie pop.

- **Atmospheric**: layered arrangements: strings, electronics, ambience.
- **Vox/Guitar**: minimalist: voice with guitar or piano.
- **Energetic**: upbeat, danceable; can overlap with Atmospheric, not with Vox/Guitar.

### Favorites

Favorite is a property of the artist, not of a family: one manual `Favorites` list in `TAG_RULES` (`+Name` only). Family favorites are derived: a favorite appears in `<Family> - Favorites` for every family it belongs to.
