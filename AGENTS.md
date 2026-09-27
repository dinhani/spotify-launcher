# Spotify Launcher

A personal launcher for the Spotify artists I follow: it helps me decide what to listen to right now and jump straight into it.

## Purpose

- The universe is artists I already follow, and I have listened to every one of them a lot at some point. The app helps me get back to them, not discover new artists.
- Picking and playing must be fast: type to search, arrows to navigate, `Enter` opens the artist in Spotify, `Shift+Enter` opens it in Last.fm, `Esc` clears the search from anywhere and returns to it from a card, `Ctrl+Z` also clears the search from anywhere (a habit from another app; it replaces undo in the search input), `Ctrl+1`, `Ctrl+2` and `Ctrl+3` cycle filter, sort and group, in screen order (`Shift` goes back; the chosen option gets focus), `Ctrl+4` focuses the card grid, `Ctrl+P` opens the command palette (see below), `Ctrl+Up/Down` cycle the filter and `Ctrl+Left/Right` the group (not inside the search input, where they move by word). Mobile must stay comfortable to tap.
- There are exactly two shared views, each a group and a sort, both persisted in `localStorage` with the last chosen tab (a URL hash wins over the saved tab): one for all Discover pages (default Style, Name) and one for every other page (default Followers, Followers). A change on any page applies to every page sharing its view; nothing else is remembered. Choosing a group also applies that group's default sort (Followers for None and Followers, Name for Style and Substyle, the matching sort for Longevity and Release). Search is not persisted. Changing the filter clears the search (a new filter is a new context, and the command palette finds artists in any tab); changing group or sort keeps it.
- Last.fm (`just lastfm`) only covers what I have listened to recently; there is no long-term history. Few or no plays means "not lately", never "unknown" or "disliked". Listening history is deliberately not used in the page: the Spotify export does not update, and it is not worth the upkeep.
- Favorites are curated by taste, not by play count.
- When I say "the app should answer X" I mean a feature of this page, not an analysis by the agent.

## Design: Delight

Delight is an explicit product goal. Choosing an artist should feel inviting, personal and enjoyable. Think like an artist: consider composition, visual rhythm, breathing room and how the page makes someone want to listen.

- Before a visual change, decide what should draw the eye first and how secondary information supports it. A change must improve the experience, beyond fitting information or reducing height.
- Artist photos and names lead the cards. Preserve the character of the photos; place supporting information with restraint, keeping important parts of the image visible.
- Stats are secondary, passive information. Keep them legible and quiet; avoid turning them into prominent panels or covering photos unnecessarily.
- Use spacing, typography, contrast and subtle treatments deliberately. More boxes, bars, borders or colorful icons do not automatically make a design better.
- Card photo corners: a small star at top left marks favorites; a green corner label at top right marks a last release within 90 days, computed in the browser.
- On mobile, going back to the top is a discreet floating arrow (small translucent white circle, bottom right, safe-area aware) that fades in once the page has scrolled past one screen; no button at the end of the page.
- Consider the whole composition on desktop and mobile, including long genre labels, favorites and dense cards. Avoid overlaps and preserve comfortable interactions.

## Discover

Discover suggests artists to revisit from the artists already followed; it does not introduce new artists.

4 artists per family: each family's Discover shows its 4, All's Discover shows all 12, and nobody repeats within a period. Picks are drawn freely from the whole family, with no quota per substyle: chance sets the mood of the period, and if it brings four extreme metal bands, that is the day for extreme metal. Guaranteeing one per substyle was tried and dropped; it turned the draw into a balanced menu that always leaves a comfortable way out. Picked in the browser, seeded by period: morning (6h-12h), afternoon (12h-18h), night (18h-6h). Same picks within a period, no reroll. Picks are drawn independently each period, so an artist may repeat; this is intended. Do not replace it with a rotation that walks through the whole library. When two good artists come up together, one is chosen and the other can come back soon; a rotation would hold it back until the whole cycle passes. Independent draws also never tie an artist to a time of day.

Folk's Discover pool excludes any artist who also belongs to Rock or Alt & Pop, regardless of whether that artist was selected for another family's Discover. This only affects Discover eligibility; family classifications, favorites and filters keep their overlaps.

A Discover button opens All's Discover from outside the sidebar and is marked active while Discover is open. It is the only button on the page, so it reads as an emblem rather than another control: on desktop a small round blue compass (no text, tooltip "Discover") at the right end of the top bar, inside the Group control after its menu, so the bar keeps two blocks (Sort, Group) and wraps as before; on mobile a labeled full-width button under the search, matching the control height. The compass turns slightly on hover, focus or press, and an open Discover shows a soft blue halo.

## Grouping

Sort and Group sit in the top bar on desktop and in the accordion on mobile, Sort on the left and Group on the right (Group first was tried and did not feel natural). Group is still the main lens (it defines the sections and picks the default sort), so it keeps `Ctrl+Left/Right`. Control labels use Title Case, matching the sidebar options; use style in the interface (family is an internal classification term).

- **Sort**: Name, Followers, Popularity, Longevity, Albums, Release, Followed: the neutral option, then reach, then career in career order (debut, discography, latest), then my relation to the artist.
- **Group**: None, Style, Substyle, Followers, Longevity, Release. None comes first as the neutral option, then Style and Substyle, which describe the artist; options shared with Sort keep Sort's relative order.
- Do not keep an option that duplicates another: Top Song was removed because it ordered artists almost exactly like Popularity.
- **Style**: Rock, Folk, Alt & Pop and Others. **Substyle**: each family's granular tags in `FAMILIES` order plus Others. Substyle headings show the family icon, the style name in quiet gray, then the substyle name (Rock, in gray, then Heavy Metal), with no separator symbol, and the tag description from `data.py` in the summary. A family filter shows only that family's sections.
- **Followers**: the tiers below. **Longevity**: years since the first album, newest first (under 5, 5-year ranges up to 35–39, 40–49, 50+, Unknown). **Release**: calendar years since the last release, most recent first (this year, last year, 2–4, 5–9, 10–19, 20+ years ago, Unknown). Year-based ranges are computed in the browser so artists move between ranges without re-rendering.
- With Release grouping, cards show the last release instead of the top song: the album name on the song line and that album's cover (a `release-mode` class on `body` swaps them with CSS; artists without albums keep the top song).
- The selected sort applies within each section, and choosing a group applies its default sort (see Purpose). Grouping does not change Discover picks. Search hides empty sections.
- Section headings stay on one line: the title, then a quiet summary (visible artists, favorites, and the description or year range), with no divider line; they must not add vertical space.

### Followers tiers

Tiers describe how far an artist's audience reaches, measured by Spotify followers. They never describe career age (that is Longevity), stage billing or how an artist became known. Largest first; the tier name is the section title and the range goes in the summary:

- **Superstar** (8M+): the biggest names overall, known to everyone (Queen, Metallica, Madonna, Ozzy Osbourne, Chappell Roan). The cut sits below the 8.5M–12M block of legends so the block stays together.
- **Mainstream** (3M–8M): known to the general public, with hits that topped general charts or went platinum (Florence + The Machine, Pantera, Lynyrd Skynyrd, Judas Priest, Mägo de Oz, Stromae, Whitesnake, Phoebe Bridgers, Dio). The cut sits in the Volbeat/Dio gap.
- **Beyond Niche** (1M–3M): the audience is larger than a niche sustains, so people outside the niche listen to them, whatever the genre, metal included (Volbeat, Sabaton, Nightwish, Opeth, Paris Paloma).
- **Niche Reference** (110K–1M): a reference within their niche, relevant and known by everyone in it without necessarily being a star, meaning the audience of a specific taste (power metal, fado, dream pop). Niche audiences top out around 800K–1M (Blind Guardian, Stratovarius, HammerFall, ANGRA, Madredeus, Agnes Obel).
- **Niche** (20K–110K): part of a niche, but not its stars (HÆLOS, Jorn, Bitter Ruin).
- **Underground** (under 20K): barely on the radar, even within their niche (Confraria da Costa, Stress). Few followers mean small reach, not a data error.

Trust the numbers over impressions of who "really" left their niche. Followers cannot tell where an audience came from: pre-streaming hits and sync placements (Vengaboys, Aqua, Boz Scaggs, Ruelle) land in Niche Reference, which is accepted.

Breakpoints sit in gaps between neighbouring artists, where an artist really changes tier (found with natural breaks on log followers in 2026-09, then checked by looking at the artists on each side). Prefer the roundest number inside the gap, even over a slightly wider gap (1M over 950K); never cut through a dense stretch, since 10K and 11K are equally unknown. The breakpoints are deliberate decisions, discussed artist by artist: new artists or refreshed numbers do not move them, and they are not recomputed from the data.

Generate browser grouping names, icons and descriptions from the tags in `data.py` (`FAMILIES`, their granular tags and `T_OTHERS`); do not maintain a separate hardcoded JavaScript list.

## Command palette

`Ctrl+P` opens a Fomantic modal (`command_palette`) to reach any option or artist without knowing where it lives.

- **Options**: every sidebar filter and every top bar group and sort, read from the page when the palette opens. Choosing one clicks the real item, so it follows the same rules; never keep a separate list. Sidebar items carry their palette data in `data-command-*` attributes.
- **Artists**: an Artists section appears once something is typed (the empty palette stays about the page's options), with up to the 8 best matches from every followed artist, never restricted to the current filter: the page search filters the current tab, the palette reaches anyone. As on cards, `Enter` opens the artist in Spotify and `Shift+Enter` in Last.fm.
- **Two lines per entry, always.** The first line says at a glance exactly what the entry is: a whole style in bold, like the sidebar headers; an option inside a style with the style in quiet gray, slightly smaller and never bolded by the search, then its name (Folk, then Folk Folk, Folk Steampunk); an artist with a square photo with rounded corners spanning both lines, the favorite star and a green NEW chip for a release in the last 90 days. The second line starts with a soft tag (small uppercase text on a light gray chip, no border) saying what kind of entry it is (STYLE, SUBSTYLE, FILTER, GROUP, SORT, ARTIST), then a short description: styles and substyles from `data.py`; filters, groups and sorts from the renderer (group and sort descriptions are also the top bar tooltips); an artist's substyles and top song (♪).
- **Right edge**: only the secondary number, the artist count of a filter or an artist's followers in the card's format; no checkmark for the active option. Popularity, albums and career years stay on the card.
- **Look**: a large borderless search, sections (Filters, Group, Sort, Artists) with blue icon titles and a hairline between them, matched characters in bold, a soft blue selection, a blurred page behind and a small keyboard hint footer.
- **Ranking**: within each section, by match quality (exact name, name start, word start, anywhere, then only the style or section; shorter names win ties), so `folk` puts Folk before Rock Folk Metal. Search ignores accents and word order.
- **Refining it**: change only what was asked and keep what already works; do not redesign it. Tried and dropped: the style after the name or at the right edge, a description subtitle as the only difference between same-named rows (it comes too late for the eye), a flat list without sections, and a tree nesting substyles under their style.

## Judgment: accept the evidence

When the data or my own knowledge of an artist settles a question, accept it. Do not keep second-guessing it with personal impressions. This reluctance has already derailed long discussions:

- Mägo de Oz was repeatedly treated as "only regional" despite 5M followers and 30 years filling stadiums across Spain and Latin America. Do not treat the English-speaking audience as "the general public" and everyone else as regional.
- Metal artists above 1M followers (Death, Opeth, Arch Enemy) were singled out as "not really" beyond their niche. The numbers say otherwise; do not exempt a genre from the criterion because of a belief about how far that genre travels.
- Stress was called a probable data error for having few followers; it is the first Brazilian metal band. Low numbers mean small reach, not a mistake.

Rules that follow:

- Once a criterion is agreed (e.g. follower tiers), apply it to everyone. If a case looks wrong, say it once with the evidence, then accept the answer.
- Work from first principles: define what the members of a group have in common before proposing names or cut points. Look at the actual artists, not at impressions of their genre.
- When asked to analyse or define, do not answer with a menu of name suggestions. Offer one recommendation when a decision is asked for.
- When wrong, say so plainly and move on; do not reintroduce the same argument in a new form.

## Pipeline

- `just download`: fetches followed artists into `data/followed.json` and caches each artist's albums and top tracks in `data/artists/<id>.json`. Only new artists are downloaded; cached artists get their followers and popularity updated from the followed list at no extra API cost. `just download --refresh` downloads albums and top tracks again for every artist, to pick up new releases; run it now and then.
- `just export`: flattens the cache into `data/artists.tsv`, including the name and cover of the last release (original edition of the latest studio album). `FIRST_RELEASE_OVERRIDES` fixes first release dates Spotify gets wrong (e.g. a compilation dated by its oldest track). Album count, first release and last release ignore live albums, compilations and demos by name, and count editions of the same album (deluxe, remaster, anniversary...) once, dated by the original release.
- `just render`: classifies artists and writes `docs/index.html` plus summaries.

## Workflow

After any change, re-render and commit it (source and generated `docs/` together) without asking. Commits are authored by me, Renato Dinhani <renatodinhani@gmail.com>, with Claude only as `Co-Authored-By`: I guide the work. Set `git config user.name` and `user.email` accordingly at the start of a session. In remote sessions without the Python dependencies, do not try to render: commit the source only; I render and commit `docs/` myself.

Renderer functions such as `menu_filter`, `menu_sort`, `menu_group`, `list_controls`, `discover_button`, `command_palette`, `scroll_top_button` and `card` are page components; keep them as functions even with a single caller.

The page renders in standards mode (`render_html` emits the HTML5 doctype); keep it. Quirks mode made line heights inside inline content ignore their parent.

Cards are rendered once, in the All tab, which is active in the HTML so cards show while the page loads. Each cell lists its tabs in `data-tabs`; other tabs start empty and clone their cells from All when first shown, and Discover tabs are filled on load. Keep it that way: rendering every tab's cards made the page 4.9 MB.

Keyboard navigation measures the grid cells (`.artist`), not the cards, because focused and hovered cards are scaled. In the top bar, Left/Right move between options and Down goes to the grid; in the sidebar, Right goes to the grid; Left on the first card of a row returns to the active filter.

Keep static styling in the renderer's `CSS_GLOBAL` block, alongside the embedded JavaScript blocks. Render elements with classes instead of inline `style=` attributes; do not extract a separate CSS file.

Prefer Fomantic UI components and variations for layout and presentation before adding custom CSS. On desktop the sidebar is the search plus a plain vertical Filter menu, with Sort and Group in the top bar. The Filter menu lists All, Discover, Favorites and Non-Favorites, then each family, then Others as its own header last, matching the Style grouping order. The mobile accordion follows the desktop reading order: Filter, Sort, Group. The accordion is mobile/tablet only: a styled accordion with separate title/content pairs and vertical menus inside the content. Keep that structure: replacing titles with attached segments and making menus the accordion content disrupted the layout. Section titles use Fomantic blue with the default accordion font size and weight, with no custom background or extra dividers. The search input, accordion titles and menu items share the same height. Count labels have a fixed width and centered numbers. The active filter is solid Fomantic blue with bold white text, and its count label inverts to white with a blue number: it is the anchor of the sidebar. The top bar puts Sort on the left and Group on the right, each a separate `ui small compact blue secondary menu`; custom CSS only adds the option track and the white active pill. Do not nest menus inside a Fomantic menu: it broke the bar. Family icons always render through `control-symbol` so they stay grayscale, in the sidebar and in group headings. Do not take screenshots; the user validates visual appearance. Pin stable frontend versions and verify compatibility before upgrades. Checked on 2026-09-26: Fomantic UI 2.9.4 and jQuery Address 1.6.0 are current stable releases; jQuery stays on 3.7.1 because 4.0.0 removes APIs used by this stack.

## How classification works

Families are declared once in `FAMILIES` in `src/render/data.py`: each `Family` holds its main, Discover, Favorites, Non-Favorites and granular tags. The umbrella, header and menu order lists derive from it, so a new family or granular tag is added there.

All rules live in `TAG_RULES` in `src/render/data.py`. Each tag lists patterns that pull artists into it:

- `genre` (e.g. `"power metal"`): any artist whose Spotify genres include it.
- `+Name`: forces the artist into the tag, regardless of genres.
- `-Name`: removes the artist from the tag.
- another tag name: artists with that tag also get this one (used by the family tags: `Rock`, `Folk`, `Alt & Pop`).

Artists without Spotify genres must be placed via `+Name`.

Tags reflect how I hear the artist, not Spotify's genre labels. Spotify genres are unreliable: they are attached loosely (folk metal on Nightwish, Sabaton and OMNIA; progressive metal on Storm Corrosion), which is why so many manual rules exist. When reviewing or proposing classifications, judge each artist by what their music actually is, from knowledge of their work; never use their Spotify genres as evidence, and never justify a classification by the genre that pulled the artist in. Genre patterns are only a convenience for the initial placement. A `+Name` or `-Name` that contradicts the genres is usually intentional; flag only isolated cases that look like real mistakes, never a whole tag based on genre names.

Rules that currently have no effect (a `-Name` for a tag the artist doesn't get, a `+Name` already covered by a genre) are kept on purpose: Spotify genres change, and they were relevant when added.

`Others` is a valid final place for artists that fit no family, such as instrumental acts (Hollywood Burns, Escala, Lorien Testard). Its icon is `🎶`, music in general, because the group has no identity of its own.

Precedents for new artists:

- Power or symphonic metal that Spotify also labels `folk metal` goes to Heavy Metal, via `-Name` in Folk Metal (Nightwish, Epica, Rhapsody).
- Pure death metal stays in Extreme Metal only, via `-Name` in Heavy Metal when a thrash or speed genre pulls it in (Death, Carcass, Vader).
- Electronic acts with an old or ethereal feel go to Alt & Pop, not Folk (Leandra, ERA).
- Theatrical packaging on pop production is Alt & Pop, not Steampunk (Haute & Freddy).

After matching, `src/render/parser.py` applies:

1. `Folk Metal` wins over `Heavy Metal` (an artist never has both).
2. A favorite goes to `<Family> - Favorites` in each of its families; any other family member goes to `<Family> - Non-Favorites`.
3. Artists not in `Favorites` → `Non-Favorites`.
4. No other tag → `Others`.

An artist may belong to more than one family (e.g. Daughter is Rock and Alt & Pop). Folk Metal already covers the folk side of a band, so a Folk Metal artist is not also in Folk; remove it via `-Name` in Folk (Eluveitie, Cruachan).

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

`indie folk` is not Folk; it goes to Alt - Vox/Guitar.

### Alt & Pop

Alternative and pop: indie, electronic, dream pop, singer-songwriters and mainstream pop (Dua Lipa, Madonna). Neither word alone covers it; Alt comes first because it is still the core. Tags use the short `Alt - ` prefix. The family icon is `🎤`: like `🎸` and `🎻`, an instrument, here the voice that leads almost every artist in the family.

- **Atmospheric**: layered arrangements: strings, electronics, ambience.
- **Vox/Guitar**: minimalist: voice with guitar or piano.
- **Energetic**: upbeat, danceable; can overlap with Atmospheric, not with Vox/Guitar.

### Favorites

Favorite is a property of the artist, not of a family: one manual `Favorites` list in `TAG_RULES` (`+Name` only). Family favorites are derived: a favorite appears in `<Family> - Favorites` for every family it belongs to.
