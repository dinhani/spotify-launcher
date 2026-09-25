import os
import pylast

from render.data import *
import render.parser as parser

INPUT_ARTISTS = "data/artistas.tsv"

network = pylast.LastFMNetwork(api_key=os.environ["LASTFM_API_KEY"])
top_artists = network.get_user(LASTFM_USER).get_top_artists(period=pylast.PERIOD_OVERALL, limit=300)

artists, _ = parser.parse(INPUT_ARTISTS)
artists_by_name = {artist.name.casefold(): artist for artist in artists}

print("Listened, not followed:")
for top_artist in top_artists:
    name = top_artist.item.get_name()
    if name.casefold() not in artists_by_name:
        print(f"  {top_artist.weight:>6}  {name}")

print("\nListened, followed, not favorite:")
for top_artist in top_artists:
    name = top_artist.item.get_name()
    artist = artists_by_name.get(name.casefold())
    if artist and T_FAVORITES not in artist.tags:
        print(f"  {top_artist.weight:>6}  {name}")
