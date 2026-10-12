
"""
Módulo encargado de la conexión y gestión de transacciones.

Utiliza SQLAlchemy para configurar la conexión a SQLite
y administrar sesiones mediante un Context Manager.
"""

from contextlib import contextmanager
from typing import Iterator

from sqlalchemy import create_engine, event
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker


class ConexionDB:
    """
    Administra la conexión y las transacciones de la base de datos.

    Habilita las restricciones de claves foráneas para SQLite
    y gestiona automáticamente commit, rollback y cierre.
    """

    def __init__(
        self,
        url_db: str = "sqlite:///book_manager.db"
    ) -> None:
        """
        Inicializa el motor y la fábrica de sesiones.

        Args:
            url_db: URL de conexión a la base de datos.
        """

        self.url_db = url_db

        self.engine: Engine = create_engine(
            self.url_db,
            echo=False
        )

        if self.engine.dialect.name == "sqlite":

            @event.listens_for(self.engine, "connect")
            def activar_claves_foraneas(
                conexion_dbapi,
                registro_conexion
            ) -> None:
                """Activa las restricciones en cada conexión SQLite."""

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
