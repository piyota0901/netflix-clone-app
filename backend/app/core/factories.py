import uuid

from app.core.entities import (
    Actor,
    Director,
    CountryOfProduction,
    Genre,
    Movie,
)

def _generate_uuid():
    return str(uuid.uuid4())

def create_actor(name: str) -> Actor:
    """Create an actor.

    Args:
        name (str): name of the actor

    Returns:
        Actor: an actor
    """
    return Actor(id=_generate_uuid(), name=name)

def create_director(name: str) -> Director:
    """Create a director.

    Args:
        name (str): name of the director

    Returns:
        Director: a director
    """
    return Director(id=_generate_uuid(), name=name)

def create_country_of_production(name: str) -> CountryOfProduction:
    """Create a country of production.

    Args:
        name (str): name of the country of production

    Returns:
        CountryOfProduction: a country of production
    """
    return CountryOfProduction(id=_generate_uuid(), name=name)

def create_genre(name: str) -> Genre:
    """Create a genre.

    Args:
        name (str): name of the genre

    Returns:
        Genre: a genre
    """
    return Genre(id=_generate_uuid(), name=name)

def create_movie(
    title: str, 
    description: str, 
    published_date: str, 
    country_of_production: CountryOfProduction, 
    genres: list[Genre], 
    actors: list[Actor], 
    directors: list[Director]
    ) -> Movie:
    """Create a movie.

    Args:
        title (str): title of the movie
        description (str): description of the movie
        published_date (str): published date of the movie
        country_of_production (CountryOfProduction): country of production of the movie
        genres (list[Genre]): genres of the movie
        actors (list[Actor]): actors of the movie
        directors (list[Director]): directors of the movie

    Returns:
        Movie: a movie
    """
    return Movie(
        id=_generate_uuid(),
        title=title,
        description=description,
        published_date=published_date,
        country_of_production=country_of_production,
        genres=genres,
        actors=actors,
        directors=directors
    )