"""
Módulo encargado de la conexión y gestión de transacciones.

Utiliza SQLAlchemy para configurar la conexión a la base
de datos y administrar sesiones mediante un Context Manager.
"""

from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class ConexionDB:
    """
    Administra la conexión y las transacciones de la base de datos.

    Permite configurar el motor de SQLAlchemy, crear sesiones
    y administrar automáticamente las transacciones.

    Attributes:
        url_db (str): URL de conexión a la base de datos.
        engine (Engine): Motor de conexión de SQLAlchemy.
        Session (sessionmaker): Fábrica de sesiones.
    """

    def __init__(self, url_db="sqlite:///book_manager.db"):
        """
        Inicializa la configuración de conexión a la base de datos.

        Args:
            url_db (str): URL de conexión. Por defecto utiliza
                una base de datos SQLite local.
        """
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
        """
        Crea y devuelve una nueva sesión de SQLAlchemy.

        Returns:
            Session: Nueva sesión asociada al motor de conexión.
        """
        return self.Session()

    @contextmanager
    def obtener_sesion(self):
        """
        Gestiona automáticamente una sesión y su transacción.

        Confirma los cambios mediante commit si las operaciones
        finalizan correctamente. Si ocurre un error, ejecuta
        rollback para revertir la transacción.

        La sesión se cierra siempre al finalizar el bloque.

        Yields:
            Session: Sesión activa para operar con la base de datos.

        Raises:
            Exception: Propaga cualquier error ocurrido durante
                las operaciones de la transacción.
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
