import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from app.persistence.repositories import (
    ActorRepository,
    DirectorRepository,
    CountryOfProductionRepository,
    GenreRepository,
    MovieRepository,
)

from app.core.entities import (
    Actor,
    Director,
    CountryOfProduction,
    Genre,
    Movie,
)

from app.core.factories import (
    create_actor,
    create_director,
    create_country_of_production,
    create_genre,
    create_movie,
)

@pytest.fixture(scope="function")
def session():
    """Create a new session for each test.
    """
    engine = create_engine("sqlite:////home/tatsuro/workspaces/netflix-clone-app/backend/netflix.db")
    session = scoped_session(
                sessionmaker(
                    bind=engine,
                    autocommit=False,
                    autoflush=False
                )
            )
    yield session
    session.close()


def test_actor_repository_when_add_actor(session):
    """Test ActorRepository
    """
    # -------------------
    # Arrange
    # -------------------
    actor_name = "Robert Downey Jr."
    actor_repository = ActorRepository(session=session)
    robert = create_actor(name=actor_name)
    
    # -------------------
    # Act
    # -------------------
    actor_repository.add(robert)
    session.flush()
    
    # -------------------
    # Assert
    # -------------------
    assert actor_repository.find_by_name(name=actor_name) == robert

def test_director_repository_when_add_director(session):
    """Test DirectorRepository
    """
    # -------------------
    # Arrange
    # -------------------
    director_name = "Christopher Nolan"
    director_repository = DirectorRepository(session=session)
    christopher = create_director(name=director_name)
    
    # -------------------
    # Act
    # -------------------
    director_repository.add(christopher)
    session.flush()
    
    # -------------------
    # Assert
    # -------------------
    assert director_repository.find_by_name(name=director_name) == christopher

def test_country_of_production_repository_when_add_country_of_production(session):
    """Test CountryOfProductionRepository
    """
    # -------------------
    # Arrange
    # -------------------
    country_name = "USA"
    country_repository = CountryOfProductionRepository(session=session)
    usa = create_country_of_production(name=country_name)
    
    # -------------------
    # Act
    # -------------------
    country_repository.add(usa)
    session.flush()
    
    # -------------------
    # Assert
    # -------------------
    assert country_repository.find_by_name(name=country_name) == usa

def test_genre_repository_when_add_genre(session):
    """Test GenreRepository
    """
    # -------------------
    # Arrange
    # -------------------
    genre_name = "Action"
    genre_repository = GenreRepository(session=session)
    action = create_genre(name=genre_name)
    
    # -------------------
    # Act
    # -------------------
    genre_repository.add(action)
    session.flush()
    
    # -------------------
    # Assert
    # -------------------
    assert genre_repository.find_by_name(name=genre_name) == action

# def test_movie_repository_when_add_movie(session):
#     """Test MovieRepository
#     """
#     # -------------------
#     # Arrange
#     # -------------------
#     movie_repository = MovieRepository(session=session)
#     actor_repository = ActorRepository(session=session)
#     director_repository = DirectorRepository(session=session)
#     country_repository = CountryOfProductionRepository(session=session)
#     genre_repository = GenreRepository(session=session)
    
#     # Create entities
#     leo = create_actor(name="Leonardo DiCaprio")
#     christopher = create_director(name="Christopher Nolan")
#     usa = create_country_of_production(name="USA")
#     sci_fi = create_genre(name="Sci-Fi")
    
#     # Add entities
#     actor_repository.add(leo)
#     director_repository.add(christopher)
#     country_repository.add(usa)
#     genre_repository.add(sci_fi)
    
#     # Create a movie
#     movie = create_movie(
#         title="Inception",
#         description="A thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea into the mind of a C.E.O.",
#         directors=[christopher],
#         published_date="2010-07-16",
#         actors=[leo],
#         genres=[sci_fi],
#         country_of_production=usa,
#     )
    
#     # -------------------
#     # Act
#     # -------------------
#     movie_repository.add(movie)
#     session.flush()
    
#     # -------------------
#     # Assert
#     # -------------------
#     assert movie_repository.find_by_title(title="Inception") == movie