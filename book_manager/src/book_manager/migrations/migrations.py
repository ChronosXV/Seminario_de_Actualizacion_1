
"""
Módulo de migración de datos del sistema Book Manager.

Convierte los registros almacenados en archivos CSV
en sentencias SQL INSERT para las tablas del sistema.
"""

import csv
from pathlib import Path
from datetime import date
from decimal import Decimal


def migrar_datos(carpeta_csvs: str, carpeta_sqls: str) -> Path:
    """
    Genera un archivo SQL con los datos de los archivos CSV.

    Procesa las tablas en un orden que respeta las dependencias
    entre claves primarias y foráneas.

    Args:
        carpeta_csvs (str): Ruta de la carpeta que contiene los CSV.
        carpeta_sqls (str): Ruta donde se guardará el archivo SQL.

    Returns:
        Path: Ruta del archivo SQL generado.

    Raises:
        FileNotFoundError: Si falta alguno de los CSV requeridos.
        ValueError: Si un registro contiene datos inválidos.
    """

    ruta_csvs = Path(carpeta_csvs)
    ruta_sqls = Path(carpeta_sqls)

    ruta_sqls.mkdir(parents=True, exist_ok=True)

    archivo_salida = ruta_sqls / "migracion_datos.sql"

    tablas = [
        "generos",
        "editoriales",
        "monedas",
        "tipos_cotizacion",
        "libros",
        "precios",
        "stock",
        "cotizaciones_dolar",
    ]

    columnas_enteras = {
        "id",
        "editorial_id",
        "genero_id",
        "libro_id",
        "moneda_id",
        "tipo_cotizacion_id",
        "cantidad",
    }

    columnas_decimales = {
        "valor",
        "valor_compra",
        "valor_venta",
    }

    sentencias: list[str] = [
        "-- Migración de datos de Book Manager",
        "BEGIN TRANSACTION;",
    ]

    for tabla in tablas:
        archivo_csv = ruta_csvs / f"{tabla}.csv"

        if not archivo_csv.is_file():
            raise FileNotFoundError(
                f"No se encontró el archivo: {archivo_csv}"
            )

        with archivo_csv.open(
            "r", encoding="utf-8-sig", newline=""
        ) as archivo:

            lector = csv.DictReader(archivo)

            if not lector.fieldnames:
                raise ValueError(
                    f"El archivo {archivo_csv.name} no tiene encabezados"
                )

            columnas = lector.fieldnames

            sentencias.append(f"\n-- Tabla: {tabla}")

            for numero_fila, fila in enumerate(lector, start=2):

                valores_sql: list[str] = []

                for columna in columnas:
                    valor = fila[columna]

                    if valor is None or valor == "":
                        valores_sql.append("NULL")

                    elif columna in columnas_enteras:
                        valores_sql.append(str(int(valor)))

                    elif columna in columnas_decimales:
                        valores_sql.append(str(Decimal(valor)))

                    elif columna == "fecha":
                        fecha = date.fromisoformat(valor)
                        valores_sql.append(f"'{fecha.isoformat()}'")

                    else:
                        valor_escapado = valor.replace("'", "''")
                        valores_sql.append(f"'{valor_escapado}'")

                nombres_columnas = ", ".join(columnas)
                valores = ", ".join(valores_sql)

                sentencia = (
                    f"INSERT INTO {tabla} ({nombres_columnas}) "
                    f"VALUES ({valores});"
                )

                sentencias.append(sentencia)

    sentencias.append("\nCOMMIT;")

    archivo_salida.write_text(
        "\n".join(sentencias) + "\n",
        encoding="utf-8",
    )

    return archivo_salida
