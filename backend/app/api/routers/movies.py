from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from app.api.schemas.movies import MovieCreate, MovieResponse
from app.persistence.repositories import MovieRepository


router = APIRouter(
    prefix="/movies",
    tags=["movies"],
)
engine = create_engine("sqlite:////home/tatsuro/workspaces/netflix-clone-app/backend/netflix.db", echo=True)

def get_db():    
    db = scoped_session(
                sessionmaker(
                    bind=engine,
                    autocommit=False,
                    autoflush=False
                )
            )
    try:
        yield db
    finally:
        db.close()


@router.get("", response_model=list[MovieResponse])
async def read_movies(db=Depends(get_db)):
    repository = MovieRepository(session=db)
    movies = repository.find_all()
    return movies