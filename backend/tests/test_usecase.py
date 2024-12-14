from pathlib import Path

import pytest
from alembic.config import Config
from alembic import command
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from app.api.schemas.movies import (
    MovieCreate,
    ActorBase,
    DirectorBase,
    GenreBase,
    CountryOfProductionBase,
)
from app.core.exceptions import (
    InvalidCountryOfProductionError, 
    InvalidGenreError, 
    MovieAlreadyExistError
)
from app.persistence.models import ActorModel, DirectorModel   
from app.core.usecase.movies import MovieUseCase
from app.core.factories import (
    create_actor,
    create_country_of_production,
    create_genre
)
from app.persistence.repositories import (
    MovieRepository,
    ActorRepository,
    DirectorRepository,
    GenreRepository,
    CountryOfProductionRepository,
)

@pytest.fixture(scope="function")
def session():
    """Create a new session for each test."""
    # テスト用のSQLiteデータベースを設定
    engine = create_engine("sqlite:///./test.db")
    session = scoped_session(
        sessionmaker(
            bind=engine,
            autocommit=False,
            autoflush=False
        )
    )

    # Alembicの設定ファイルを読み込む
    alembic_cfg_file = Path(__file__).parent.parent / "alembic.ini"
    alembic_cfg = Config(str(alembic_cfg_file))
    
    alembic_cfg.set_main_option("script_location", str(Path(__file__).parent.parent / "alembic"))
    alembic_cfg.set_main_option("sqlalchemy.url", "sqlite:///./test.db")

    # Alembicを使用してマイグレーションを適用
    command.upgrade(alembic_cfg, "head")

    try:
        yield session
    finally:
        # テスト終了後にセッションを閉じ、データベースファイルを削除
        session.close()
        engine.dispose()
        import os
        os.remove("test.db")

def test_movie_usecase_when_register(session):
    """Test MovieUseCase
    
    新規の映画を登録できることを確認するテスト
    """
    # -------------------
    # Arrange
    # -------------------
    genre_repo = GenreRepository(session=session)
    genre_repo.add(create_genre(name="Action"))
    genre_repo.add(create_genre(name="Adventure"))
    genre_repo.add(create_genre(name="Fantasy"))
    session.commit()
    
    usecase = MovieUseCase(
        session=session,
        movie_repository=MovieRepository(session=session),
        actor_repository=ActorRepository(session=session),
        director_repository=DirectorRepository(session=session),
        genre_repository=GenreRepository(session=session),
        country_of_production_repository=CountryOfProductionRepository(session=session),
    )
    
    # -------------------
    # Act
    # -------------------
    movie_create = MovieCreate(
        title="The Avengers endgame",
        description="The Avengers and their allies must be willing to sacrifice all in an attempt to defeat the powerful Thanos before his blitz of devastation and ruin puts an end to the universe.",
        published_date="2019-04-26",
        country_of_production=CountryOfProductionBase(name="USA"),
        genres=[GenreBase(name="Action"), GenreBase(name="Adventure"), GenreBase(name="Fantasy")],
        actors=[ActorBase(name="Robert Downey Jr."), ActorBase(name="Chris Evans"), ActorBase(name="Mark Ruffalo")],
        directors=[DirectorBase(name="Joss Whedon")],
    )
    usecase.register(movie_create=movie_create)
    
    # -------------------
    # Assert
    # -------------------
    movie = usecase.movie_repository.find_by_title_and_year(title=movie_create.title, published_date=movie_create.published_date)
    
    assert movie.title == movie_create.title
    assert movie.published_date == movie_create.published_date
    assert movie.description == movie_create.description
    assert movie.country_of_production.name == movie_create.country_of_production.name
    assert sorted([actor.name for actor in movie.actors]) == sorted([actor.name for actor in movie_create.actors])
    assert sorted([director.name for director in movie.directors]) == sorted([director.name for director in movie_create.directors])
    assert sorted([genre.name for genre in movie.genres]) == sorted([genre.name for genre in movie_create.genres])

def test_movie_usecase_when_actor_is_already_resistred(session):
    """Test MovieUseCase
    
    俳優のみ登録済みの場合に、新規の映画を登録できることを確認するテスト
    """
    # -------------------
    # Arrange
    # -------------------
    genre_repo = GenreRepository(session=session)
    genre_repo.add(create_genre(name="Action"))
    genre_repo.add(create_genre(name="Adventure"))
    genre_repo.add(create_genre(name="Fantasy"))
    session.commit()
    
    actor_repo = ActorRepository(session=session)
    actor_repo.add(create_actor(name="Robert Downey Jr."))
    session.commit()    
    
    usecase = MovieUseCase(
        session=session,
        movie_repository=MovieRepository(session=session),
        actor_repository=ActorRepository(session=session),
        director_repository=DirectorRepository(session=session),
        genre_repository=GenreRepository(session=session),
        country_of_production_repository=CountryOfProductionRepository(session=session),
    )    

    
    # -------------------
    # Act
    # -------------------
    movie_create = MovieCreate(
        title="Iron Man",
        description="After being held captive in an Afghan cave, billionaire engineer Tony Stark creates a unique weaponized suit of armor to fight evil.",
        published_date="2008-05-02",
        country_of_production=CountryOfProductionBase(name="USA"),
        genres=[GenreBase(name="Action"), GenreBase(name="Adventure")],
        actors=[ActorBase(name="Robert Downey Jr.")],
        directors=[DirectorBase(name="John Favreau")],
    )
    usecase.register(movie_create=movie_create)
    
    # -------------------
    # Assert
    # -------------------
    assert session.query(ActorModel).count() == 1

def test_movie_usecase_when_director_is_already_resistred(session):
    """Test MovieUseCase
    
    監督のみ登録済みの場合に、新規の映画を登録できることを確認するテスト
    """
    # -------------------
    # Arrange
    # -------------------
    genre_repo = GenreRepository(session=session)
    genre_repo.add(create_genre(name="Action"))
    genre_repo.add(create_genre(name="Adventure"))
    genre_repo.add(create_genre(name="Fantasy"))
    session.commit()
    
    actor_repo = DirectorRepository(session=session)
    actor_repo.add(create_actor(name="John Favreau"))
    session.commit()    
    
    usecase = MovieUseCase(
        session=session,
        movie_repository=MovieRepository(session=session),
        actor_repository=ActorRepository(session=session),
        director_repository=DirectorRepository(session=session),
        genre_repository=GenreRepository(session=session),
        country_of_production_repository=CountryOfProductionRepository(session=session),
    )    

    
    # -------------------
    # Act
    # -------------------
    movie_create = MovieCreate(
        title="Iron Man",
        description="After being held captive in an Afghan cave, billionaire engineer Tony Stark creates a unique weaponized suit of armor to fight evil.",
        published_date="2008-05-02",
        country_of_production=CountryOfProductionBase(name="USA"),
        genres=[GenreBase(name="Action"), GenreBase(name="Adventure")],
        actors=[ActorBase(name="Robert Downey Jr.")],
        directors=[DirectorBase(name="John Favreau")],
    )
    usecase.register(movie_create=movie_create)
    
    # -------------------
    # Assert
    # -------------------
    assert session.query(DirectorModel).count() == 1

def test_movie_usecase_when_movie_is_already_resistred(session):
    """Test MovieUseCase
    
    映画が登録済みの場合に、新規の映画を登録できないことを確認するテスト
    """
    # -------------------
    # Arrange
    # -------------------
    genre_repo = GenreRepository(session=session)
    genre_repo.add(create_genre(name="Action"))
    genre_repo.add(create_genre(name="Adventure"))
    genre_repo.add(create_genre(name="Fantasy"))
    session.commit()
    
    actor_repo = DirectorRepository(session=session)
    actor_repo.add(create_actor(name="John Favreau"))
    session.commit()    
    
    usecase = MovieUseCase(
        session=session,
        movie_repository=MovieRepository(session=session),
        actor_repository=ActorRepository(session=session),
        director_repository=DirectorRepository(session=session),
        genre_repository=GenreRepository(session=session),
        country_of_production_repository=CountryOfProductionRepository(session=session),
    )    
    movie_create = MovieCreate(
        title="Iron Man",
        description="After being held captive in an Afghan cave, billionaire engineer Tony Stark creates a unique weaponized suit of armor to fight evil.",
        published_date="2008-05-02",
        country_of_production=CountryOfProductionBase(name="USA"),
        genres=[GenreBase(name="Action"), GenreBase(name="Adventure")],
        actors=[ActorBase(name="Robert Downey Jr.")],
        directors=[DirectorBase(name="John Favreau")],
    )
    usecase.register(movie_create=movie_create)
    
    # -------------------
    # Act & Assert
    # -------------------
    movie_create = MovieCreate(
        title="Iron Man",
        description="After being held captive in an Afghan cave, billionaire engineer Tony Stark creates a unique weaponized suit of armor to fight evil.",
        published_date="2008-05-02",
        country_of_production=CountryOfProductionBase(name="USA"),
        genres=[GenreBase(name="Action"), GenreBase(name="Adventure")],
        actors=[ActorBase(name="Robert Downey Jr.")],
        directors=[DirectorBase(name="John Favreau")],
    )
    with pytest.raises(MovieAlreadyExistError):
        usecase.register(movie_create=movie_create)
    
def test_movie_usecase_when_genre_is_invalid(session):
    """Test MovieUseCase
    
    ジャンルが不正な場合に、新規の映画を登録できないことを確認するテスト
    """
    # -------------------
    # Arrange
    # -------------------
    genre_repo = GenreRepository(session=session)
    genre_repo.add(create_genre(name="Action"))
    genre_repo.add(create_genre(name="Adventure"))
    genre_repo.add(create_genre(name="Fantasy"))
    session.commit()
    
    usecase = MovieUseCase(
        session,
        movie_repository=MovieRepository(session=session),
        actor_repository=ActorRepository(session=session),
        director_repository=DirectorRepository(session=session),
        genre_repository=GenreRepository(session=session),
        country_of_production_repository=CountryOfProductionRepository(session=session),
    )
    
    # -------------------
    # Act & Assert
    # -------------------
    movie_create = MovieCreate(
        title="Iron Man",
        description="After being held captive in an Afghan cave, billionaire engineer Tony Stark creates a unique weaponized suit of armor to fight evil.",
        published_date="2008-05-02",
        country_of_production=CountryOfProductionBase(name="USA"),
        genres=[GenreBase(name="Invalid Genre")], # NOTE: Set invalid genre
        actors=[ActorBase(name="Robert Downey Jr.")],
        directors=[DirectorBase(name="John Favreau")],
    )
    with pytest.raises(InvalidGenreError):
        usecase.register(movie_create=movie_create)

def test_movie_usecase_when_countory_of_production_is_invalid(session):
    """Test MovieUseCase
    
    制作国が不正な場合に、新規の映画を登録できないことを確認するテスト
    """
    # -------------------
    # Arrange
    # -------------------
    genre_repo = GenreRepository(session=session)
    genre_repo.add(create_genre(name="Action"))
    genre_repo.add(create_genre(name="Adventure"))
    genre_repo.add(create_genre(name="Fantasy"))
    session.commit()
    
    country_repo = CountryOfProductionRepository(session=session)
    country_repo.add(create_country_of_production(name="USA"))
    
    usecase = MovieUseCase(
        session,
        movie_repository=MovieRepository(session=session),
        actor_repository=ActorRepository(session=session),
        director_repository=DirectorRepository(session=session),
        genre_repository=GenreRepository(session=session),
        country_of_production_repository=CountryOfProductionRepository(session=session),
    )
    
    # -------------------
    # Act & Assert
    # -------------------
    movie_create = MovieCreate(
        title="Iron Man",
        description="After being held captive in an Afghan cave, billionaire engineer Tony Stark creates a unique weaponized suit of armor to fight evil.",
        published_date="2008-05-02",
        country_of_production=CountryOfProductionBase(name="Invalid Country"), # NOTE: Set invalid country
        genres=[GenreBase(name="Action"), GenreBase(name="Adventure")],
        actors=[ActorBase(name="Robert Downey Jr.")],
        directors=[DirectorBase(name="John Favreau")],
    )
    with pytest.raises(InvalidCountryOfProductionError):
        usecase.register(movie_create=movie_create)
        