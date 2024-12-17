from sqlalchemy.orm import Session

from app.api.schemas.movies import MovieCreate
from app.core.exceptions import InvalidCountryOfProductionError, InvalidGenreError, MovieAlreadyExistError
from app.core.factories import (
    create_movie,
    create_actor,
    create_director,
    create_country_of_production,
)
from app.persistence.repositories import (
    MovieRepository,
    ActorRepository,
    DirectorRepository,
    GenreRepository,
    CountryOfProductionRepository,
)

class MovieUseCase:
    def __init__(
        self, 
        session: Session,
        movie_repository: MovieRepository,
        actor_repository: ActorRepository,
        director_repository: DirectorRepository,
        genre_repository: GenreRepository,
        country_of_production_repository: CountryOfProductionRepository,
    ):
        self.session = session
        self.movie_repository = movie_repository
        self.actor_repository = actor_repository
        self.director_repository = director_repository
        self.genre_repository = genre_repository
        self.country_of_production_repository = country_of_production_repository
    
    def get_all(self):
        """Get all movies.
        """
        return self.movie_repository.find_all()

    def register(self, movie_create: MovieCreate):
        """Register a movie.

        Args:
            movie (Movie): Domain model
        """
        if self.movie_repository.find_by_title_and_year(title=movie_create.title, published_date=movie_create.published_date):
            raise MovieAlreadyExistError("The movie already exists.")
        
        actors = []
        for actor in movie_create.actors:
            # 俳優を名前で検索
            existing_actor = self.actor_repository.find_by_name(name=actor.name)
            
            if existing_actor:
                actors.append(existing_actor)
            else:
                # 新しい俳優を作成してリポジトリに追加
                new_actor = create_actor(name=actor.name)
                actors.append(new_actor)
        
        directors = []
        for director in movie_create.directors:
            existing_director = self.director_repository.find_by_name(name=director.name)
            if existing_director:
                directors.append(existing_director)
            else:
                new_director = create_director(name=director.name)
                directors.append(new_director)
        
        genres = []
        for genre in movie_create.genres:
            existing_genre = self.genre_repository.find_by_name(name=genre.name)
            # NOTE: 登録されているジャンルのみ登録可能とする仕様
            if existing_genre:
                genres.append(existing_genre)
            else:
                all_genres = self.genre_repository.find_all()
                raise InvalidGenreError(f"Invalid genre: {genre.name}. Available genres are {', '.join([genre.name for genre in all_genres])}")
        
        country_of_production = self.country_of_production_repository.find_by_name(name=movie_create.country_of_production.name)
        if country_of_production is None:
            raise InvalidCountryOfProductionError(f"Invalid country of production: {movie_create.country_of_production.name}. \
                                                    Available countries are {', '.join([country.name for country in self.country_of_production_repository.find_all()])}")
        
        movie = create_movie(
            title=movie_create.title,
            description=movie_create.description,
            published_date=movie_create.published_date,
            country_of_production=country_of_production,
            genres=genres,
            actors=actors,
            directors=directors,
        )
        
        self.movie_repository.add(movie)
        self.session.commit()
        
        return movie