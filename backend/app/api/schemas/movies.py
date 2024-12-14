import datetime

from pydantic import BaseModel, ConfigDict

from app.core.entities import CountryOfProduction, Director, Actor, Genre

class ActorBase(BaseModel):
    name: str

class ActorCreate(ActorBase):
    pass

class ActorResponse(ActorBase):
    id: str

    model_config: ConfigDict = ConfigDict(from_attributes=True)

class DirectorBase(BaseModel):
    name: str

class DirectorCreate(BaseModel):
    name: str

class DirectorResponse(BaseModel):
    id: str
    
    model_config: ConfigDict = ConfigDict(from_attributes=True)

class CountryOfProductionBase(BaseModel):
    name: str

class CountryOfProductionCreate(CountryOfProductionBase):
    pass

class CountryOfProductionResponse(CountryOfProductionBase):
    id: str
    
    model_config: ConfigDict = ConfigDict(from_attributes=True)

class GenreBase(BaseModel):
    name: str

class GenreCreate(GenreBase):
    pass

class GenreResponse(GenreBase):
    id: str
    
    model_config: ConfigDict = ConfigDict(from_attributes=True)

class MovieBase(BaseModel):
    title: str
    published_date: datetime.date
    description: str


class MovieCreate(MovieBase):
    country_of_production: CountryOfProductionBase
    actors: list[ActorBase]
    directors: list[DirectorBase]
    genres: list[GenreBase]


class MovieResponse(MovieBase):
    id: str
    country_of_production: CountryOfProductionResponse
    actors: list[ActorResponse]
    directors: list[DirectorResponse]
    genres: list[GenreResponse]
    
    model_config: ConfigDict = ConfigDict(from_attributes=True)

    