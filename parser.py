# ------------------------------------------------------------------------------
# Libraries
# ------------------------------------------------------------------------------
import logging
import polars
from collections import defaultdict
from data import *

# ------------------------------------------------------------------------------
# Functions
# ------------------------------------------------------------------------------
def parse(filename: str) -> defaultdict[str, list[dict]]:
    artists_by_tag = defaultdict(list)

    logging.info(f"📄 Reading CSV file: {filename}")
    artists_df = polars.read_csv(filename, separator="\t")

    logging.info("🧱 Parsing tags")
    for artist in artists_df.to_dicts():
        # parse row
        artist_genres = artist["genres"]
        if artist_genres is None:
            artist_genres = []
        else:
            artist_genres = artist_genres.split("|")
        artist_tags = {T_ALL}

        # match genres
        for genre in artist_genres:
            for tag in TAGS_ALL.get(genre, []):
                artist_tags.add(tag)

        # match names (positive)
        for tag in TAGS_ALL.get(f"+{artist["name"]}", []):
            artist_tags.add(tag)

        # match names (negative)
        for tag in TAGS_ALL.get(f"-{artist["name"]}", []):
            if tag in artist_tags:
                artist_tags.remove(tag)

        # match other tags
        for tagged_tag in artist_tags.copy():
            for tag in TAGS_ALL.get(tagged_tag, []):
                artist_tags.add(tag)

        # rule: folk metal cannot be traditional
        if T_ROCK_FOLK_METAL in artist_tags and T_ROCK_HEAVY_METAL in artist_tags:
            artist_tags.remove(T_ROCK_HEAVY_METAL)

        # rule: non-favorites
        if T_ROCK_ALL in artist_tags and T_ROCK_FAVORITES not in artist_tags:
            artist_tags.add(T_ROCK_NON_FAVORITES)
        if T_FOLK_ALL in artist_tags and T_FOLK_FAVORITES not in artist_tags:
            artist_tags.add(T_FOLK_NON_FAVORITES)
        if T_ALT_ALL in artist_tags and T_ALT_FAVORITES not in artist_tags:
            artist_tags.add(T_ALT_NON_FAVORITES)

        # rule: general favorites / non-
        favorite = any(tag in TAGS_FAVORITES for tag in artist_tags)
        if favorite:
            artist_tags.add(T_FAVORITES)
        else:
            artist_tags.add(T_NON_FAVORITES)

        # add tags
        artist["tags"] = artist_tags
        for tags in artist["tags"]:
            artists_by_tag[tags].append(artist)
        if len(artist["tags"]) == 2: # (default tags: all + favorite or non-favorite)
            artists_by_tag[T_OTHERS].append(artist)
    return artists_by_tag