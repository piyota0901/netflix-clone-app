class MovieAlreadyExistError(Exception):
    """Exception raised when a movie already exists."""
    pass

class InvalidGenreError(Exception):
    """Exception raised when a genre is invalid."""
    pass

class InvalidCountryOfProductionError(Exception):
    """Exception raised when a country of production is invalid."""
    pass