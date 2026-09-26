from typing import NamedTuple

# ------------------------------------------------------------------------------
# Classes
# ------------------------------------------------------------------------------
class Tag(NamedTuple):
    name: str
    icon: str
    description: str = ""

class Artist:
    def __init__(self,
                id: str, name: str, image: str,
                genres: str | list[str], popularity: int, followers: int, albums: int,
                first_release: str | None, last_release: str | None, last_follow: str, top_song: str, top_song_popularity: int,
                top_album_name: str, top_album_image: str):

        self.id = id
        self.name = name
        self.image = image
        self.top_album_name = top_album_name
        self.top_album_image = top_album_image

        self.genres = genres
        self.popularity = popularity
        self.followers = followers
        self.albums = albums

        self.tags = set()
        self.tags_granular = set()

        self.first_release = first_release or ""
        self.last_release = last_release or ""
        self.last_follow = last_follow
        self.top_song = top_song
        self.top_song_popularity = top_song_popularity

        # parse genres
        if self.genres is None:
            self.genres = []
        if isinstance(self.genres, str):
            self.genres = self.genres.split("|")

    def __repr__(self) -> str:
        return f"{self.__dict__}"
