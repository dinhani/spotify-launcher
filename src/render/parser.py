# ------------------------------------------------------------------------------
# Libraries
# ------------------------------------------------------------------------------
from collections import defaultdict
from typing import Tuple
import logging
import polars

from render.data import *
from render.models import Artist

# ------------------------------------------------------------------------------
# Functions
# ------------------------------------------------------------------------------
def parse(filename: str) -> Tuple[list[Artist], defaultdict[str, list[Artist]]]:
    artists = []
    artists_by_tag = defaultdict(list)

    logging.info(f"📄 Reading CSV file: {filename}")
    artists_df = polars.read_csv(filename, separator="\t")

    logging.info("🧱 Parsing tags")
    for artist_dict in artists_df.to_dicts():
        artist = Artist(**artist_dict)

        # parse row
        artist.tags = {T_ALL}

        # match genres
        for genre in artist.genres:
            for tag in TAGS_ALL.get(genre, []):
                artist.tags.add(tag)

        # match names (positive)
        for tag in TAGS_ALL.get(f"+{artist.name}", []):
            artist.tags.add(tag)

        # match names (negative)
        for tag in TAGS_ALL.get(f"-{artist.name}", []):
            if tag in artist.tags:
                artist.tags.remove(tag)

        # match other tags
        for tagged_tag in artist.tags.copy():
            for tag in TAGS_ALL.get(tagged_tag, []):
                artist.tags.add(tag)

        # rule: folk metal cannot be traditional
        if T_ROCK_FOLK_METAL in artist.tags and T_ROCK_HEAVY_METAL in artist.tags:
            artist.tags.remove(T_ROCK_HEAVY_METAL)

        # rule: non-favorites
        if T_ROCK_ALL in artist.tags and T_ROCK_FAVORITES not in artist.tags:
            artist.tags.add(T_ROCK_NON_FAVORITES)
        if T_FOLK_ALL in artist.tags and T_FOLK_FAVORITES not in artist.tags:
            artist.tags.add(T_FOLK_NON_FAVORITES)
        if T_ALT_ALL in artist.tags and T_ALT_FAVORITES not in artist.tags:
            artist.tags.add(T_ALT_NON_FAVORITES)

        # rule: general favorites / non-
        favorite = any(tag in TAGS_FAVORITES for tag in artist.tags)
        if favorite:
            artist.tags.add(T_FAVORITES)
        else:
            artist.tags.add(T_NON_FAVORITES)

        # rule: others (only have the 2 default tags: all + favorite or non-favorite)
        if len(artist.tags) == 2:
            artist.tags.add(T_OTHERS)

        # finish: add tags to artist and add artist to collections
        artist.tags_granular = [t for t in TAGS_MENU_ORDER if t in artist.tags and t not in TAGS_UMBRELLA]
        artists.append(artist)
        for tags in artist.tags:
            artists_by_tag[tags].append(artist)

    return (artists, artists_by_tag)
