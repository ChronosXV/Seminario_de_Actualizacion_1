
"""
Módulo encargado de la conexión y gestión de transacciones.

Utiliza SQLAlchemy para configurar la conexión a PostgreSQL
(Supabase) y administrar sesiones mediante un Context Manager.
"""

import os
from contextlib import contextmanager
from typing import Iterator

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker


class ConexionDB:
    """
    Administra la conexión y las transacciones de la base de datos.

    Gestiona automáticamente commit, rollback y cierre
    de sesiones.
    """

    def __init__(self, url_db: str | None = None) -> None:
        """
        Inicializa el motor y la fábrica de sesiones.

        Args:
            url_db: URL de conexión. Si no se proporciona,
                    utiliza DATABASE_URL del entorno.
        """

        self.url_db = url_db or os.getenv("DATABASE_URL")

        if not self.url_db:
            raise ValueError(
                "No se encontró DATABASE_URL. "
                "Configurá la conexión a Supabase."
            )

        self.engine: Engine = create_engine(
            self.url_db,
            echo=False,
            pool_pre_ping=True
        )

        self.Session = sessionmaker(
            bind=self.engine,
            autoflush=False,
            expire_on_commit=False
        )

    def crear_sesion(self) -> Session:
        """Crea una nueva sesión de SQLAlchemy."""
        return self.Session()

    @contextmanager
    def obtener_sesion(self) -> Iterator[Session]:
        """
        Administra una transacción.

        Confirma los cambios si finalizan correctamente,
        revierte los cambios ante errores y cierra la sesión.
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
