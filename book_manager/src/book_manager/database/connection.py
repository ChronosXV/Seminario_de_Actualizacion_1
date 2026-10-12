
"""
Gestión de conexiones y transacciones de Book Manager.
Compatible con PostgreSQL (Supabase) y SQLite.
"""

import os
from contextlib import contextmanager
from typing import Iterator

from sqlalchemy import create_engine, event
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker


class ConexionDB:

    def __init__(self, url_db: str | None = None) -> None:

        self.url_db = (
            url_db
            or os.getenv("DATABASE_URL")
            or "sqlite:///book_manager.db"
        )

        self.engine: Engine = create_engine(
            self.url_db,
            echo=False,
            pool_pre_ping=True
        )

        if self.engine.dialect.name == "sqlite":

            @event.listens_for(self.engine, "connect")
            def activar_claves_foraneas(conexion_dbapi, registro_conexion):
                cursor = conexion_dbapi.cursor()
                try:
                    cursor.execute("PRAGMA foreign_keys=ON")
                finally:
                    cursor.close()

        self.Session = sessionmaker(
            bind=self.engine,
            autoflush=False,
            expire_on_commit=False
        )

    def crear_sesion(self) -> Session:
        return self.Session()

    @contextmanager
    def obtener_sesion(self) -> Iterator[Session]:

        sesion = self.crear_sesion()

        try:
            yield sesion
            sesion.commit()

        except Exception:
            sesion.rollback()
            raise

        finally:
            sesion.close()
