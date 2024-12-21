import pathlib
from typing import Callable

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker, scoped_session

from app.core.entities import Poster


class PosterFileStorageSession:
    """ファイルを操作するリポジトリクラス用のセッションクラス
    """
    def __init__(self, base_dir: pathlib.Path):
        self.base_dir = base_dir
        self.posters: list[Poster] = []
    
    def add(self, poster: Poster):
        """_summary_

        Args:
            poster (Poster): _description_
        """
        self.posters.append(poster)
    
    def commit(self):
        """_summary_
        """
        
        for poster in self.posters:
            save_path = self.base_dir / poster.filename
            if save_path.exists():
                raise FileExistsError(f"{str(save_path)} already exists.")
            
            if save_path.parent != self.base_dir:
                raise ValueError("Access outside the base directory is not allowed.") # TODO: 例外クラスを作成
            
            with open(save_path, "wb") as f:
                f.write(poster.binary)
        
        self.posters = []
    
    def rollback(self):
        """_summary_
        """
        self.posters = []
    
    def close(self):
        """_summary_
        """
        self.posters = []


class UnitOfWork:
    """_summary_
    """
    def __init__(
        self,
        db_session_factory: Callable[[], Session],
        poster_file_storage_session_factory: Callable[[], PosterFileStorageSession]
    ):
        self.db_session_factory = db_session_factory
        self.poster_file_storage_session_factory = poster_file_storage_session_factory
        self.session: Session | None = None
        self.poster_file_storage_session: PosterFileStorageSession | None = None
    
    def __enter__(self):
        self.session = self.db_session_factory()
        self.poster_file_storage_session = self.poster_file_storage_session_factory()
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is not None:
            self.rollback()
            self.close()
        self.close()
    
    def commit(self):
        """
        """
        self.session.commit()
        self.poster_file_storage_session.commit()
    
    def rollback(self):
        """
        """
        self.session.rollback()
        self.poster_file_storage_session.rollback()
    
    def close(self):
        """
        """
        self.session.close()
        self.poster_file_storage_session.close()