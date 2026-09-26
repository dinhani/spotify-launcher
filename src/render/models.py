from typing import NamedTuple

# ------------------------------------------------------------------------------
# Classes
# ------------------------------------------------------------------------------
class Tag(NamedTuple):
    name: str
    icon: str
    description: str = ""

class Family(NamedTuple):
    tag: Tag
    discover: Tag
    favorites: Tag
    non_favorites: Tag
    granular: tuple[Tag, ...]

    @property
    def tags_umbrella(self) -> list[Tag]:
        return [self.tag, self.discover, self.favorites, self.non_favorites]

    @property
    def tags_menu(self) -> list[Tag]:
        return [*self.tags_umbrella, *self.granular]

class Family(NamedTuple):
    tag: Tag
    discover: Tag
    favorites: Tag
    non_favorites: Tag
    granular: tuple[Tag, ...]

    @property
    def tags_umbrella(self) -> list[Tag]:
        return [self.tag, self.discover, self.favorites, self.non_favorites]

    @property
    def tags_menu(self) -> list[Tag]:
        return [*self.tags_umbrella, *self.granular]

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

        self.tags: set[Tag] = set()
        self.tags_granular: list[Tag] = []

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
