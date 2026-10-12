
"""
Carga inicial de datos del sistema Book Manager.

Utiliza la migración SQL generada a partir de los CSV
para poblar una base de datos SQLite mediante SQLAlchemy.
"""

from pathlib import Path

from sqlalchemy import text

from book_manager.database.connection import ConexionDB
from book_manager.migrations.migrations import migrar_datos
from book_manager.models.models import Base, GeneroModel


def cargar_datos(
    conexion: ConexionDB,
    ruta_base: str | Path | None = None,
) -> None:
    """
    Carga los registros iniciales en SQLite si la base está vacía.

    Args:
        conexion (ConexionDB): Administrador de conexiones SQLite.
        ruta_base (str | Path | None): Carpeta de archivos CSV.

    Raises:
        FileNotFoundError: Si no existen los archivos necesarios.
        ValueError: Si la base contiene una carga parcial.
    """
    ruta_migrations = Path(__file__).resolve().parent.parent / "migrations"

    ruta_csv = (
        Path(ruta_base)
        if ruta_base is not None
        else ruta_migrations / "csv"
    )

    ruta_sql = ruta_migrations / "sql"

    Base.metadata.create_all(conexion.engine)

    # Verificar el estado de las ocho tablas.
    with conexion.obtener_sesion() as sesion:
        tablas = list(Base.metadata.sorted_tables)

        cantidades = {
            tabla.name: sesion.execute(
                text(f'SELECT COUNT(*) FROM "{tabla.name}"')
            ).scalar_one()
            for tabla in tablas
        }

    if all(cantidad > 0 for cantidad in cantidades.values()):
        print("La base ya contiene datos. No se repite la carga.")
        return

    if any(cantidad > 0 for cantidad in cantidades.values()):
        raise ValueError(
            "La base contiene datos parciales. "
            "Se cancela la carga inicial para evitar duplicados."
        )

    # Generar el archivo SQL utilizando la migración existente.
    archivo_sql = migrar_datos(
        str(ruta_csv),
        str(ruta_sql),
    )

    contenido_sql = archivo_sql.read_text(encoding="utf-8")

    # Ejecutar el script completo dentro de una transacción SQLite.
    # La migración existente contiene instrucciones de transacción.
    conexion_sqlite = conexion.engine.raw_connection()

    try:
        conexion_sqlite.executescript(contenido_sql)
        conexion_sqlite.commit()
    except Exception:
        conexion_sqlite.rollback()
        raise
    finally:
        conexion_sqlite.close()

    print("Datos iniciales cargados correctamente en SQLite.")
