
import os
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class ConexionDB:
    """
    Administra la conexión y las transacciones de la base de datos.

    Utiliza DATABASE_URL cuando está configurada.
    En caso contrario, utiliza SQLite como alternativa local.
    """

    def __init__(self, url_db=None):
        """
        Inicializa la conexión a la base de datos.

        Args:
            url_db (str | None): URL explícita de conexión.
                Si no se proporciona, utiliza DATABASE_URL
                o SQLite como alternativa.
        """
        self.url_db = (
            url_db
            or os.getenv("DATABASE_URL")
            or "sqlite:///book_manager.db"
        )

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
        """
        Crea y devuelve una nueva sesión de SQLAlchemy.
        """
        return self.Session()

    @contextmanager
    def obtener_sesion(self):
        """
        Administra una transacción con commit, rollback
        y cierre automático de sesión.
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
