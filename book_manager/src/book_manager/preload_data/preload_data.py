
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


def cargar_datos_desde_sql(
    conexion: ConexionDB,
    ruta_sql: str | Path,
) -> int:
    """
    Carga datos ejecutando instrucciones SQL desde un archivo.

    Args:
        conexion: Administrador de conexión a la base de datos.
        ruta_sql: Ruta del archivo SQL que se desea ejecutar.

    Returns:
        int: Cantidad de instrucciones SQL ejecutadas.

    Raises:
        FileNotFoundError: Si el archivo SQL no existe.
        ValueError: Si el archivo no contiene instrucciones válidas.
    """
    archivo = Path(ruta_sql)

    if not archivo.is_file():
        raise FileNotFoundError(
            f"No se encontró el archivo SQL: {archivo}"
        )

    contenido = archivo.read_text(encoding="utf-8")

    instrucciones = []

    for bloque in contenido.split(";"):
        lineas = [
            linea
            for linea in bloque.splitlines()
            if linea.strip()
            and not linea.strip().startswith("--")
        ]

        instruccion = "\n".join(lineas).strip()

        if not instruccion:
            continue

        if instruccion.upper() in (
            "BEGIN",
            "BEGIN TRANSACTION",
            "COMMIT",
        ):
            continue

        instrucciones.append(instruccion)

    if not instrucciones:
        raise ValueError(
            "El archivo SQL no contiene instrucciones para ejecutar."
        )

    with conexion.obtener_sesion() as sesion:
        for instruccion in instrucciones:
            sesion.execute(text(instruccion))

    print(
        f"Carga SQL finalizada: "
        f"{len(instrucciones)} instrucciones ejecutadas."
    )

    return len(instrucciones)
