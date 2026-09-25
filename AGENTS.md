# Spotify Launcher

Static page to browse the Spotify artists I follow, grouped by tags.

## Pipeline

- `just download`: fetches followed artists into `data/followed.json` and caches each artist in `data/artists/<id>.json` (cached files are never re-downloaded).
- `just export`: flattens the cache into `data/artistas.tsv`.
- `just render`: classifies artists and writes `docs/index.html` plus summaries.

## Workflow

After any change, re-render and commit it (source and generated `docs/` together) without asking.

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
2. In a family but not in its favorites → `<Family> - Non-Favorites`.
3. In any family favorites → `Favorites`, otherwise `Non-Favorites`.
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

Acoustic, old-time, storytelling music. Traditional music and steampunk belong together here on purpose.

- **Folk**: traditional and roots music: celtic, medieval, fado, bluegrass, pirate songs and shanties.
- **Steampunk**: steampunk and dark cabaret, theatrical songs.

`indie folk` is not Folk; it goes to Alternative - Vox/Guitar. Electronic acts with an old or ethereal feel (e.g. Leandra) are not Folk.

### Alternative

Alternative and indie pop.

- **Atmospheric**: layered arrangements: strings, electronics, ambience.
- **Vox/Guitar**: minimalist: voice with guitar or piano.
- **Energetic**: upbeat, danceable; can overlap with Atmospheric, not with Vox/Guitar.

### Favorites

Each family has a manual `Favorites` list (`+Name` only). A favorite must also be in some granular tag of the same family.
