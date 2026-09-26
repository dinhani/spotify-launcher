# ------------------------------------------------------------------------------
# Libraries
# ------------------------------------------------------------------------------
from collections import defaultdict
import logging
import polars

from render.data import *
from render.models import Artist, Tag

# ------------------------------------------------------------------------------
# Functions
# ------------------------------------------------------------------------------
def parse(filename: str) -> tuple[list[Artist], defaultdict[Tag, list[Artist]]]:
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
            for tag in TAGS_BY_RULE.get(genre, []):
                artist.tags.add(tag)

        # match names (positive)
        for tag in TAGS_BY_RULE.get(f"+{artist.name}", []):
            artist.tags.add(tag)

        # match names (negative)
        for tag in TAGS_BY_RULE.get(f"-{artist.name}", []):
            if tag in artist.tags:
                artist.tags.remove(tag)

        # match other tags
        for tagged_tag in artist.tags.copy():
            for tag in TAGS_BY_RULE.get(tagged_tag, []):
                artist.tags.add(tag)

        # rule: folk metal cannot be traditional
        if T_ROCK_FOLK_METAL in artist.tags and T_ROCK_HEAVY_METAL in artist.tags:
            artist.tags.remove(T_ROCK_HEAVY_METAL)

        # rule: favorites and non-favorites follow the artist into each of its families
        favorite = T_FAVORITES in artist.tags
        if not favorite:
            artist.tags.add(T_NON_FAVORITES)
        for family in FAMILIES:
            if family.tag in artist.tags:
                artist.tags.add(family.favorites if favorite else family.non_favorites)

        # rule: others (artists outside every family)
        if not any(family.tag in artist.tags for family in FAMILIES):
            artist.tags.add(T_OTHERS)

        # finish: add tags to artist and add artist to collections
        artist.tags_granular = [t for t in TAGS_MENU_ORDER if t in artist.tags and t not in TAGS_UMBRELLA]
        artists.append(artist)
        for tag in artist.tags:
            artists_by_tag[tag].append(artist)

    return (artists, artists_by_tag)
