from contextlib import contextmanager

"""
Módulo de conexión a la base de datos mediante SQLAlchemy.
"""

import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from typing import Iterator
from sqlalchemy.orm import Session


class ConexionDB:
    """
    Administra la conexión y las sesiones de la base de datos.
    """

    def __init__(self, url_db: str | None = None) -> None:
        """
        Inicializa la conexión.

        Prioriza una URL explícita, luego DATABASE_URL
        y finalmente SQLite como alternativa local.
        """
        self.url_db = (
            url_db
            or os.getenv("DATABASE_URL")
            or "sqlite:///book_manager.db"
        )

        self.engine = create_engine(
            self.url_db,
            echo=False,
            pool_pre_ping=True
        )

        self.Session = sessionmaker(
            bind=self.engine,
            autoflush=False,
            expire_on_commit=False
        )

    def crear_sesion(self) -> "Session":
        """
        Crea y devuelve una sesión de SQLAlchemy.
        """
        return self.Session()


    @contextmanager
    def obtener_sesion(self) -> "Iterator[Session]":
        """
        Administra una sesión y su transacción.

        Realiza commit si la operación termina correctamente,
        rollback si ocurre un error y cierra la sesión.
        """
        sesion = self.crear_sesion()

        try:
            yield sesion
            sesion.commit()

        except Exception:
            sesion.rollback()
            raise

        finally:
            sesion.close()
