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
        genres = artist["genres"]
        if genres is None:
            genres = []
        else:
            genres = genres.split("|")
        tagged = {T_ALL}

        # match genres
        for genre in genres:
            tags = TAGS.get(genre, [])
            for tag in tags:
                tagged.add(tag)

        # match names (positive)
        tags = TAGS.get(f"+{artist["name"]}", [])
        for tag in tags:
            tagged.add(tag)

        # match names (negative)
        tags = TAGS.get(f"-{artist["name"]}", [])
        for tag in tags:
            tagged.remove(tag)

        # match other tags
        for tagged_tag in tagged.copy():
            tags = TAGS.get(tagged_tag, [])
            for tag in tags:
                tagged.add(tag)

        # rule: extreme cannot be traditional
        if T_ROCK_EXTREME_METAL in tagged and T_ROCK_HEAVY_METAL in tagged:
            tagged.remove(T_ROCK_HEAVY_METAL)

        # add tags
        artist["tags"] = tagged
        for tags in artist["tags"]:
            artists_by_tag[tags].append(artist)
        if len(artist["tags"]) == 1:
            artists_by_tag[T_OTHERS].append(artist)
    return artists_by_tag