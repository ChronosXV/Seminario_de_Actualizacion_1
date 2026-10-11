from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class ConexionDB:
    def __init__(self, url_db="sqlite:///book_manager.db"):
        self.url_db = url_db

        self.engine = create_engine(
            self.url_db,
            echo=False
        )

        self.Session = sessionmaker(
            bind=self.engine,
            autoflush=False,
            expire_on_commit=False
        )

    def crear_sesion(self):
        return self.Session()
