

class MovieService:
    
        
        
    
    def exists(self, movie: Movie):
        return self.repository.find_by_title_and_year(title=movie.title, published_date=movie.published_date)