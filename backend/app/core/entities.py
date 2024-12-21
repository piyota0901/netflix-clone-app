import datetime
from typing import List
from uuid import UUID

class Actor:
    """俳優を表現するドメインモデル"""
    def __init__(self, id: UUID, name: str):
        self._id = id
        self._name = name

    @property
    def id(self) -> UUID:
        return self._id

    @property
    def name(self) -> str:
        return self._name
    
    def __repr__(self):
        return f"<Actor(id={self.id!r}, name={self.name!r})>"
    
    def __eq__(self, other: "Actor"):
        return self.name == other.name


class Director:
    """監督を表現するドメインモデル"""
    def __init__(self, id: UUID, name: str):
        self._id = id
        self._name = name

    @property
    def id(self) -> UUID:
        return self._id

    @property
    def name(self) -> str:
        return self._name
    
    def __repr__(self):
        return f"<Director(id={self.id!r}, name={self.name!r})>"
    
    def __eq__(self, other: "Director"):
        return self.name == other.name


class CountryOfProduction:
    """製作国を表現するドメインモデル"""
    def __init__(self, id: UUID, name: str):
        self._id = id
        self._name = name

    @property
    def id(self) -> UUID:
        return self._id

    @property
    def name(self) -> str:
        return self._name
    
    def __repr__(self):
        return f"<CountryOfProduction(id={self.id!r}, name={self.name!r})>"
    
    def __eq__(self, other: "CountryOfProduction"):
        return self.name == other.name


class Genre:
    """ジャンルを表現するドメインモデル"""
    def __init__(self, id: UUID, name: str):
        self._id = id
        self._name = name

    @property
    def id(self) -> UUID:
        return self._id

    @property
    def name(self) -> str:
        return self._name
    
    def __repr__(self):
        return f"<Genre(id={self.id!r}, name={self.name!r})>"
    
    def __eq__(self, other: "Genre"):
        return self.name == other.name


# NOTE: ファイルオブジェクトなどの基底クラスを作成して抽象化したほうがよいかもしれない
class Poster:
    """映画のポスター画像を表現するドメインモデル"""
    
    def __init__(
        self,
        id: UUID,
        binary: bytes,
        filename: str
    ):
        self._id = id
        self._binary = binary
        self._filename = filename
    
    @property
    def id(self):
        return self._id
    
    @property
    def binary(self):
        return self._binary
    
    @property
    def filename(self):
        return self._filename
    
    def __repr__(self):
        return f"<Poster(id={self.id!r}, filename={self.filename!r})>"


class Movie:
    """映画を表現するドメインモデル"""
    def __init__(
        self, id: UUID, 
        title: str, 
        description: str, 
        published_date: datetime.date,
        directors: List[Director], 
        actors: List[Actor], 
        genres: List[Genre], 
        country_of_production: CountryOfProduction, 
        poster: Poster
    ):
        self._id = id
        self._title = title
        self._description = description
        self._directors = directors
        self._actors = actors
        self._genres = genres
        self._country_of_production = country_of_production
        self._published_date = published_date
        self._poster = poster

    @property
    def id(self) -> UUID:
        return self._id

    @property
    def title(self) -> str:
        return self._title

    @property
    def description(self) -> str:
        return self._description

    @property
    def directors(self) -> List[Director]:
        return self._directors

    @property
    def actors(self) -> List[Actor]:
        return self._actors

    @property
    def genres(self) -> List[Genre]:
        return self._genres

    @property
    def country_of_production(self) -> CountryOfProduction:
        return self._country_of_production

    @property
    def published_date(self) -> datetime.date:
        return self._published_date
    
    @property
    def poster(self) -> Poster:
        return self._poster
    
    def __repr__(self):
        return f"<Movie(id={self.id!r}, \
                        description={self.description!r}, \
                        title={self.title!r}, \
                        published_date={self.published_date!r}, \
                        country_of_production={self.country_of_production!r}, \
                        directors={self.directors!r}, \
                        actors={self.actors!r}, \
                        genres={self.genres!r} \
                        poster={self.poster!r} \
                )>"
    
    def __eq__(self, other: "Movie"):
        return self.title == other.title and self.published_date == other.published_date