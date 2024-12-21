from datetime import date

from app.core.entities import Movie
from app.persistence.repositories import MovieRepository, PosterRepository


class MovieService:
    
    def __init__(
        self,
        movie_repository: MovieRepository,
        poster_repository: PosterRepository,
    ):
        self.movie_repository = movie_repository
        self.poster_repository = poster_repository
    
    def save(self, movie: Movie):
        self.movie_repository.add(movie)
        
    def find_all(self):
        movies = self.movie_repository.find_all()
        posters = [self.poster_repository.find_by_id(movie_id=movie.poster.id) for movie in movies]
        
        # Movieオブジェクトは、プロパティの値を変更できないため、新しいMovieオブジェクトを作成する
        return [
            Movie(
                id=movie.id, 
                title=movie.title, 
                description=movie.description, 
                published_date=movie.published_date, 
                directors=movie.directors, 
                actors=movie.actors, 
                genres=movie.genres, 
                country_of_production=movie.country_of_production, 
                poster=poster
            ) for movie, poster in zip(movies, posters)
        ]

    def find_by_title_and_year(self, title: str, published_date: date) -> Movie:
        movie = self.movie_repository.find_by_title_and_year(title=title, published_date=published_date)
        poster = self.poster_repository.find_by_id(movie_id=movie.poster.id)
        
        # Movieオブジェクトは、プロパティの値を変更できないため、新しいMovieオブジェクトを作成する
        return Movie(
                    id=movie.id, 
                    title=movie.title, 
                    description=movie.description, 
                    published_date=movie.published_date, 
                    directors=movie.directors, 
                    actors=movie.actors, 
                    genres=movie.genres, 
                    country_of_production=movie.country_of_production, 
                    poster=poster
                )