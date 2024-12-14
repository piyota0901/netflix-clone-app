import datetime

from sqlalchemy import (
    ForeignKey,
    String,
    TEXT,
    DATE,
    Table,
    Column,
    UniqueConstraint
)
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
)


# https://docs.sqlalchemy.org/en/20/orm/quickstart.html#declare-models
class Base(DeclarativeBase):
    pass


# https://docs.sqlalchemy.org/en/20/orm/declarative_mixins.html#mixing-in-columns
class TimestampMixin:
    created_at: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.now(tz=datetime.timezone.utc))
    updated_at: Mapped[datetime.datetime] = mapped_column(
                                                default=datetime.datetime.now(tz=datetime.timezone.utc), 
                                                onupdate=datetime.datetime.now(tz=datetime.timezone.utc)
                                            )


class ActorModel(Base,TimestampMixin):
    __tablename__ = 'actors'

    id: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    
    movies: Mapped[list["MovieModel"]] = relationship(
        secondary="movie_to_actor",
        back_populates="actors",
        lazy="joined"
    )

    def __repr__(self):
        return f"<ActorModel(id={self.id!r}, name={self.name!r})>"
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name
        }


class DirectorModel(Base,TimestampMixin):
    __tablename__ = 'directors'

    id: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), unique=True)
    
    movies: Mapped[list["MovieModel"]] = relationship(
        secondary="movie_to_director",
        back_populates="directors",
        lazy="joined"
    )

    def __repr__(self):
        return f"<DirectorModel(id={self.id!r}, name={self.name!r})>"

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name
        }
        

class CountryOfProductionModel(Base,TimestampMixin):
    __tablename__ = 'countries_of_production'

    id: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255),unique=True)
    
    # https://docs.sqlalchemy.org/en/20/orm/basic_relationships.html#many-to-one
    movies: Mapped[list["MovieModel"]] = relationship(back_populates="country_of_production")

    def __repr__(self):
        return f"<CountryOfProductionModel(id={self.id!r}, name={self.name!r})>"
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name
        }


class GenreModel(Base,TimestampMixin):
    __tablename__ = 'genres'

    id: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), unique=True)
    
    # https://docs.sqlalchemy.org/en/20/orm/basic_relationships.html#many-to-many
    movies: Mapped[list["MovieModel"]] = relationship(
        secondary="movie_to_genre",
        back_populates="genres",
        lazy="joined"
    )

    def __repr__(self):
        return f"<GenreModel(id={self.id!r}, name={self.name!r})>"
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name
        }


class MovieModel(Base,TimestampMixin):
    __tablename__ = 'movies'

    id: Mapped[str] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(TEXT)
    published_date: Mapped[datetime.date] = mapped_column(DATE)
    
    # https://docs.sqlalchemy.org/en/20/orm/declarative_tables.html#declarative-table-configuration
    __table_args__ = (
        UniqueConstraint('title', 'published_date'),
    )
    
    # https://docs.sqlalchemy.org/en/20/orm/basic_relationships.html#many-to-one
    country_of_production_id: Mapped[str] = mapped_column(ForeignKey('countries_of_production.id'))
    country_of_production: Mapped["CountryOfProductionModel"] = relationship(back_populates="movies",lazy="joined")
    
    # https://docs.sqlalchemy.org/en/20/orm/basic_relationships.html#many-to-many
    genres: Mapped[list["GenreModel"]] = relationship(
        secondary="movie_to_genre",
        back_populates="movies",
        lazy="joined"
    )

    actors: Mapped[list["ActorModel"]] = relationship(
        secondary="movie_to_actor",
        back_populates="movies",
        lazy="joined"
    )
    
    directors: Mapped[list["DirectorModel"]] = relationship(
        secondary="movie_to_director",
        back_populates="movies",
        lazy="joined"
    )
    
    def __repr__(self):
        return f"<MovieModel(id={self.id!r}, \
                             title={self.title!r}, \
                             description={self.description!r}, \
                             published_date={self.published_date!r}, \
                             genres={self.genres!r} \
                             actors={self.actors!r} \
                             directors={self.directors!r} \
                             country_of_production={self.country_of_production!r} \
                )>"

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "published_date": self.published_date,
            "genres": [genre.to_dict() for genre in self.genres],
            "actors": [actor.to_dict() for actor in self.actors],
            "directors": [director.to_dict() for director in self.directors]
        }


# ------------------------------------------------------------
# Many to Many
# https://docs.sqlalchemy.org/en/20/orm/basic_relationships.html#many-to-many
# ------------------------------------------------------------
movie_to_actor = Table(
    "movie_to_actor",
    Base.metadata,
    Column("movie_id", ForeignKey("movies.id"), primary_key=True),
    Column("actor_id", ForeignKey("actors.id"), primary_key=True)   
)

movie_to_director = Table(
    "movie_to_director",
    Base.metadata,
    Column("movie_id", ForeignKey("movies.id"), primary_key=True),
    Column("director_id", ForeignKey("directors.id"), primary_key=True)
)

movie_to_genre = Table(
    "movie_to_genre",
    Base.metadata,
    Column("movie_id", ForeignKey("movies.id"), primary_key=True),
    Column("genre_id", ForeignKey("genres.id"), primary_key=True)
)
