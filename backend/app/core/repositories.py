import abc


class MovieRepository(abc.ABC):
    @abc.abstractmethod
    def find_all(self):
        raise NotImplementedError
    
    @abc.abstractmethod
    def find_by_id(self, id: str):
        raise NotImplementedError
    
    @abc.abstractmethod
    def create(self, movie: dict):
        raise NotImplementedError