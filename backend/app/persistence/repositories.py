import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.entities import (
    Actor,
    Director,
    CountryOfProduction,
    Genre,
    Movie, 
)
from app.persistence.models import (
    ActorModel,
    CountryOfProductionModel,
    DirectorModel,
    GenreModel,
    MovieModel,
)


class ActorRepository:
    def __init__(self, session: Session):
        self.session = session
        
    def add(self, actor: Actor):
        """Add an actor to the database

        Args:
            actor (Actor): Domain model
        """
        actor_model = self._entity_to_model(actor_entity=actor)
        self.session.add(actor_model)
    
    def find_by_name(self, name: str) -> Actor | None:
        """Find an actor by name in the database

        Args:
            name (str): name of the actor

        Returns:
            Actor | None: an actor or None
                "None" is returned if the actor is not found
        """
        stmt = select(ActorModel).where(ActorModel.name == name)
        actor_model = self.session.scalars(stmt).first()
        
        if actor_model is None:
            return None
        
        return self._model_to_entity(actor_model=actor_model)
    
    def find_movies_by_actor_name(self, name: str) -> list[Movie] | None:
        """Find movies by actor name in the database

        Args:
            name (str): Domain model

        Returns:
            list[Movie] | None: Domain model
        """
        stmt = select(ActorModel).where(ActorModel.name == name)
        actor_model = self.session.scalars(stmt).first()
        
        if actor_model is None:
            return None
        
        movies = [
                    Movie(
                        id=movie.id,
                        title=movie.title,
                        description=movie.description,
                        published_date=movie.published_date,
                        country_of_production=CountryOfProduction(
                            id=movie.country_of_production.id,
                            name=movie.country_of_production.name
                        ),
                        genres=[
                            Genre(
                                id=genre.id,
                                name=genre.name
                            )
                            for genre in movie.genres
                        ],
                        directors=[
                            Director(
                                id=director.id,
                                name=director.name
                            )
                            for director in movie.directors
                        ],
                        actors=[
                            Actor(
                                id=actor.id,
                                name=actor.name
                            )
                            for actor in movie.actors
                        ]
                    )
                    for movie in actor_model.movies
                ]
        return movies

    
    def _entity_to_model(self, actor_entity: Actor) -> ActorModel:
        """Domain model to ORM model

        Args:
            actor_entity (Actor): Domain model

        Returns:
            ActorModel: ORM model
        """
        return ActorModel(
                    id=actor_entity.id,
                    name=actor_entity.name
                )
    
    def _model_to_entity(self, actor_model: ActorModel) -> Actor:
        """ORM model to Domain model

        Args:
            actor_model (ActorModel): ORM model

        Returns:
            Actor: Domain model
        """
        return Actor(
                    id=actor_model.id,
                    name=actor_model.name
                )


class DirectorRepository:
    def __init__(self, session: Session):
        self.session = session
    
    def add(self, director: Director):
        """Add a director to the database

        Args:
            director (Director): Domain model
        """
        director_model = self._entity_to_model(director_entity=director)
        self.session.add(director_model)
    
    def find_by_name(self, name: str) -> Director | None:
        """Find a director by name in the database

        Args:
            name (str): name of the director

        Returns:
            Director | None: a director or None
                "None" is returned if the director is not found
        """
        stmt = select(DirectorModel).where(DirectorModel.name == name)
        director_model = self.session.scalars(stmt).first()
        
        if director_model is None:
            return None
        
        return self._model_to_entity(director_model=director_model)
    
    def find_movies_by_director_name(self, name: str) -> list[Movie] | None:
        """Find movies by director name in the database

        Args:
            name (str): name of the director

        Returns:
            list[Movie] | None: a list of movies or None
                "None" is returned if the director is not found
        """
        stmt = select(DirectorModel).where(DirectorModel.name == name)
        director_model = self.session.scalars(stmt).first()
        
        if director_model is None:
            return None
        
        movies = [
                    Movie(
                        id=movie.id,
                        title=movie.title,
                        description=movie.description,
                        published_date=movie.published_date,
                        country_of_production=CountryOfProduction(
                            id=movie.country_of_production.id,
                            name=movie.country_of_production.name
                        ),
                        genres=[
                            Genre(
                                id=genre.id,
                                name=genre.name
                            )
                            for genre in movie.genres
                        ],
                        directors=[
                            Director(
                                id=director.id,
                                name=director.name
                            )
                            for director in movie.directors
                        ],
                        actors=[
                            Actor(
                                id=actor.id,
                                name=actor.name
                            )
                            for actor in movie.actors
                        ]
                    )
                    for movie in director_model.movies
                ]
        return movies
    
    def _entity_to_model(self, director_entity: Director) -> DirectorModel:
        """Domain model to ORM model

        Args:
            director_entity (Director): Domain model

        Returns:
            DirectorModel: ORM model
        """
        return DirectorModel(
                    id=director_entity.id,
                    name=director_entity.name
                )
    
    def _model_to_entity(self, director_model: DirectorModel) -> Director:
        """ORM model to Domain model

        Args:
            director_model (DirectorModel): ORM model

        Returns:
            Director: Domain model
        """
        return Director(
                    id=director_model.id,
                    name=director_model.name
                )


class CountryOfProductionRepository:
    def __init__(self, session: Session):
        self.session = session
    
    def add(self, country_of_production: CountryOfProduction):
        """Add a country of production to the database

        Args:
            country_of_production (CountryOfProduction): Domain model
        """
        country_of_production_model = self._entity_to_model(country_of_production_entity=country_of_production)
        self.session.add(country_of_production_model)
    
    def find_by_name(self, name: str) -> CountryOfProduction | None:
        """Find a country of production by name in the database

        Args:
            name (str): name of the country of production

        Returns:
            CountryOfProduction | None: a country of production or None
                "None" is returned if the country of production is not found
        """
        stmt = select(CountryOfProductionModel).where(CountryOfProductionModel.name == name)
        country_of_production_model = self.session.scalars(stmt).first()
        
        if country_of_production_model is None:
            return None
        
        return self._model_to_entity(country_of_production_model=country_of_production_model)
    
    def _entity_to_model(self, country_of_production_entity: CountryOfProduction) -> CountryOfProductionModel:
        """Domain model to ORM model

        Args:
            country_of_production_entity (CountryOfProduction): Domain model

        Returns:
            CountryOfProductionModel: ORM model
        """
        return CountryOfProductionModel(
                    id=country_of_production_entity.id,
                    name=country_of_production_entity.name
                )
    
    def _model_to_entity(self, country_of_production_model: CountryOfProductionModel) -> CountryOfProduction:
        """ORM model to Domain model

        Args:
            country_of_production_model (CountryOfProductionModel): ORM model

        Returns:
            CountryOfProduction: Domain model
        """
        return CountryOfProduction(
                    id=country_of_production_model.id,
                    name=country_of_production_model.name
                )


class GenreRepository:
    def __init__(self, session: Session):
        self.session = session
    
    def add(self, genre: Genre):
        """Add a genre to the database

        Args:
            genre (Genre): Domain model
        """
        genre_model = self._entity_to_model(genre_entity=genre)
        self.session.add(genre_model)
    
    def find_by_name(self, name: str) -> Genre | None:
        """Find a genre by name in the database

        Args:
            name (str): name of the genre

        Returns:
            Genre | None: a genre or None
                "None" is returned if the genre is not found
        """
        stmt = select(GenreModel).where(GenreModel.name == name)
        genre_model = self.session.scalars(stmt).first()
        
        if genre_model is None:
            return None
        
        return self._model_to_entity(genre_model=genre_model)
    
    def find_movies_by_genre_name(self, name: str) -> list[Movie] | None:
        """Find movies by genre name in the database

        Args:
            name (str): name of the genre

        Returns:
            list[Movie] | None: a list of movies or None
                "None" is returned if the genre is not found
        """
        stmt = select(GenreModel).where(GenreModel.name == name)
        genre_model = self.session.scalars(stmt).first()
        
        if genre_model is None:
            return None
        
        movies = [
                    Movie(
                        id=movie.id,
                        title=movie.title,
                        description=movie.description,
                        published_date=movie.published_date,
                        country_of_production=CountryOfProduction(
                            id=movie.country_of_production.id,
                            name=movie.country_of_production.name
                        ),
                        genres=[
                            Genre(
                                id=genre.id,
                                name=genre.name
                            )
                            for genre in movie.genres
                        ],
                        directors=[
                            Director(
                                id=director.id,
                                name=director.name
                            )
                            for director in movie.directors
                        ],
                        actors=[
                            Actor(
                                id=actor.id,
                                name=actor.name
                            )
                            for actor in movie.actors
                        ]
                    )
                    for movie in genre_model.movies
                ]
        return movies
    
    def _entity_to_model(self, genre_entity: Genre) -> GenreModel:
        """Domain model to ORM model

        Args:
            genre_entity (Genre): Domain model

        Returns:
            GenreModel: ORM model
        """
        return GenreModel(
                    id=genre_entity.id,
                    name=genre_entity.name
                )
    
    def _model_to_entity(self, genre_model: GenreModel) -> Genre:
        """ORM model to Domain model

        Args:
            genre_model (GenreModel): ORM model

        Returns:
            Genre: Domain model
        """
        return Genre(
                    id=genre_model.id,
                    name=genre_model.name
                )


class MovieRepository:
    def __init__(self, session: Session):
        self.session = session
        
    def add(
        self, 
        movie: Movie,
        genres: list[Genre],
        actors: list[Actor],
        directors: list[Director],
    ):
        """Add a movie to the database

        Args:
            movie (Movie): Domain model
            genres (list[Genre]): Domain model
            actors (list[Actor]): Domain model
            directors (list[Director]): Domain model
        """
        movie_model = self._entity_to_model(movie_entity=movie)
        
        for genre in genres:
            genre_model = self.session.query(GenreModel).get(genre.id)
            movie_model.genres.append(genre_model)
        
        for actor in actors:
            actor_model = self.session.query(ActorModel).get(actor.id)
            movie_model.actors.append(actor_model)
        
        for director in directors:
            director_model = self.session.query(DirectorModel).get(director.id)
            movie_model.directors.append(director_model)
        
        self.session.add(movie_model)
    
    def find_all(self) -> list[Movie]:
        """Find all movies in the database

        Returns:
            list[Movie]: a list of movies
        """
        stmt = select(MovieModel)
        movie_models = self.session.scalars(stmt).all()
        
        return [
                    self._model_to_entity(movie_model=movie_model)
                    for movie_model in movie_models
                ]
        

    def _entity_to_model(self, movie_entity: Movie) -> MovieModel:
        """Domain model to ORM model

        Args:
            movie_entity (Movie): Domain model

        Returns:
            MovieModel: ORM model
        """
        return MovieModel(
                    id=movie_entity.id,
                    title=movie_entity.title,
                    description=movie_entity.description,
                    published_date=movie_entity.published_date,
                    country_of_production_id=movie_entity.country_of_production.id
                )
    
    def _model_to_entity(self, movie_model: MovieModel) -> Movie:
        """ORM model to Domain model

        Args:
            movie_model (MovieModel): ORM model

        Returns:
            Movie: Domain model
        """
        return Movie(
                    id=movie_model.id,
                    title=movie_model.title,
                    description=movie_model.description,
                    published_date=movie_model.published_date,
                    country_of_production=CountryOfProduction(
                        id=movie_model.country_of_production.id,
                        name=movie_model.country_of_production.name
                    ),
                    genres=[
                        Genre(
                            id=genre.id,
                            name=genre.name
                        )
                        for genre in movie_model.genres
                    ],
                    directors=[
                        Director(
                            id=director.id,
                            name=director.name
                        )
                        for director in movie_model.directors
                    ],
                    actors=[
                        Actor(
                            id=actor.id,
                            name=actor.name
                        )
                        for actor in movie_model.actors
                    ]
                )