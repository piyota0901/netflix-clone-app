from pathlib import Path

import pytest
from alembic import command
from alembic.config import Config
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from app.api.main import app
from app.api.routers.movies import get_db
from app.api.schemas.movies import (
    ActorBase,
    DirectorBase,
    GenreBase,
    CountryOfProductionBase,
    MovieCreate,
)
from app.core.factories import (
    create_genre,
    create_country_of_production,
)
from app.core.usecase.movies import MovieUseCase
from app.persistence.repositories import (
    ActorRepository,
    DirectorRepository,
    GenreRepository,
    CountryOfProductionRepository,
    MovieRepository
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

@pytest.fixture(scope="function")
def client(session):
    """テストクライアントを提供するフィクスチャ。"""
    def get_db_override():
        """テスト用のDB依存関数を返す。"""
        try:
            yield session
        finally:
            session.remove()

    # 依存関係を上書き
    app.dependency_overrides[get_db] = get_db_override

    # テストクライアントを返す
    with TestClient(app) as client:
        yield client

def test_health(client):
    """ヘルスチェックのテスト
    """
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_get_all_movies(session, client):
    """全映画情報取得APIのテスト
    """
    # -------------------
    # Arrange
    # -------------------
    genre_repo = GenreRepository(session)
    country_repo = CountryOfProductionRepository(session)
    
    genre_repo.add(create_genre(name="Action"))
    genre_repo.add(create_genre(name="Adventure"))
    genre_repo.add(create_genre(name="Sci-Fi"))
    genre_repo.add(create_genre(name="Fantasy"))
    
    country_repo.add(create_country_of_production(name="USA"))
    country_repo.add(create_country_of_production(name="UK"))
    session.commit()
    
    movie_create = MovieCreate(
                    title="Avengers1",
                    published_date="2012-04-11",
                    description="Avengers1 description",
                    country_of_production=CountryOfProductionBase(name="USA"),
                    actors=[
                        ActorBase(name="Robert Downey Jr."),
                        ActorBase(name="Chris Evans"),
                        ActorBase(name="Mark Ruffalo"),
                    ],
                    directors=[
                        DirectorBase(name="Joss Whedon")
                    ],
                    genres=[
                        GenreBase(name="Action"),
                        GenreBase(name="Adventure"),
                        GenreBase(name="Sci-Fi"),
                    ]
                )
    
    movie_usecase = MovieUseCase(
        session=session,
        movie_repository=MovieRepository(session),
        actor_repository=ActorRepository(session),
        director_repository=DirectorRepository(session),
        genre_repository=GenreRepository(session),
        country_of_production_repository=CountryOfProductionRepository(session),
    )
    
    movie_usecase.register(movie_create)
    
    # -------------------
    # Act
    # -------------------
    response = client.get("/movies")
    
    # -------------------
    # Assert
    # -------------------    
    assert response.status_code == 200
    
    movies: list[dict] = response.json()
    assert len(movies) == 1
    
    movie = movies[0]
    assert movie["title"] == "Avengers1"
    assert movie["published_date"] == "2012-04-11"
    assert movie["description"] == "Avengers1 description"
    assert movie["country_of_production"]["name"] == "USA"
    assert sorted([actor["name"]    for actor    in movie["actors"]])    == ["Chris Evans", "Mark Ruffalo", "Robert Downey Jr."]
    assert sorted([director["name"] for director in movie["directors"]]) == ["Joss Whedon"]
    assert sorted([genre["name"]    for genre    in movie["genres"]])    == ["Action", "Adventure", "Sci-Fi"]

def test_get_all_movies_when_no_movies(client):
    """全映画情報取得APIのテスト
    
    映画情報が登録されていない場合のテスト
    """
    # -------------------
    # Act
    # -------------------
    response = client.get("/movies")
    
    # -------------------
    # Assert
    # -------------------    
    assert response.status_code == 200
    assert response.json() == []