
import csv
from datetime import datetime
from pathlib import Path
from typing import Dict

from book_manager.entities.entities import (
    CotizacionDolar,
    Editorial,
    Genero,
    Libro,
    Moneda,
    Precio,
    Stock,
    TipoCotizacion,
)
from book_manager.repositories.repositories import (
    Repositorio,
    RepositorioCotizacionDolar,
    RepositorioStock,
)


def cargar_datos() -> Dict[str, object]:
    """Carga los datos iniciales desde los archivos CSV."""

    ruta_csv = (
        Path(__file__).resolve().parent.parent
        / "migrations"
        / "csv"
    )

    repo_generos = Repositorio[Genero]()
    repo_editoriales = Repositorio[Editorial]()
    repo_monedas = Repositorio[Moneda]()
    repo_tipos_cotizacion = Repositorio[TipoCotizacion]()
    repo_libros = Repositorio[Libro]()
    repo_precios = Repositorio[Precio]()
    repo_stock = RepositorioStock()
    repo_cotizaciones = RepositorioCotizacionDolar()

    # -------------------------------------------
    # Géneros
    # -------------------------------------------

    with open(
        ruta_csv / "generos.csv",
        encoding="utf-8",
        newline="",
    ) as archivo:
        lector = csv.DictReader(archivo)

        for fila in lector:
            genero = Genero(
                id=int(fila["id"]),
                nombre=fila["nombre"],
            )
            repo_generos.crear(genero)

    # -------------------------------------------
    # Editoriales
    # -------------------------------------------

    with open(
        ruta_csv / "editoriales.csv",
        encoding="utf-8",
        newline="",
    ) as archivo:
        lector = csv.DictReader(archivo)

        for fila in lector:
            editorial = Editorial(
                id=int(fila["id"]),
                nombre=fila["nombre"],
            )
            repo_editoriales.crear(editorial)

    # -------------------------------------------
    # Monedas
    # -------------------------------------------

    with open(
        ruta_csv / "monedas.csv",
        encoding="utf-8",
        newline="",
    ) as archivo:
        lector = csv.DictReader(archivo)

        for fila in lector:
            moneda = Moneda(
                id=int(fila["id"]),
                codigo=fila["codigo"],
                nombre=fila["nombre"],
                simbolo=fila["simbolo"],
            )
            repo_monedas.crear(moneda)

    # -------------------------------------------
    # Tipos de cotización
    # -------------------------------------------

    with open(
        ruta_csv / "tipos_cotizacion.csv",
        encoding="utf-8",
        newline="",
    ) as archivo:
        lector = csv.DictReader(archivo)

        for fila in lector:
            tipo = TipoCotizacion(
                id=int(fila["id"]),
                nombre=fila["nombre"],
            )
            repo_tipos_cotizacion.crear(tipo)

    # -------------------------------------------
    # Libros
    # -------------------------------------------

    with open(
        ruta_csv / "libros.csv",
        encoding="utf-8",
        newline="",
    ) as archivo:
        lector = csv.DictReader(archivo)

        for fila in lector:
            editorial = repo_editoriales.leer_por_id(
                int(fila["editorial_id"])
            )
            genero = repo_generos.leer_por_id(
                int(fila["genero_id"])
            )

            if editorial is None:
                raise ValueError(
                    f"Editorial inexistente: "
                    f"{fila['editorial_id']}"
                )

            if genero is None:
                raise ValueError(
                    f"Género inexistente: {fila['genero_id']}"
                )

            libro = Libro(
                id=int(fila["id"]),
                isbn=fila["isbn"],
                titulo=fila["titulo"],
                autor=fila["autor"],
                editorial=editorial,
                genero=genero,
            )

            repo_libros.crear(libro)

    # -------------------------------------------
    # Precios
    # -------------------------------------------

    with open(
        ruta_csv / "precios.csv",
        encoding="utf-8",
        newline="",
    ) as archivo:
        lector = csv.DictReader(archivo)

        for fila in lector:
            libro = repo_libros.leer_por_id(
                int(fila["libro_id"])
            )
            moneda = repo_monedas.leer_por_id(
                int(fila["moneda_id"])
            )

            if libro is None:
                raise ValueError(
                    f"Libro inexistente: {fila['libro_id']}"
                )

            if moneda is None:
                raise ValueError(
                    f"Moneda inexistente: {fila['moneda_id']}"
                )

            precio = Precio(
                id=int(fila["id"]),
                libro=libro,
                moneda=moneda,
                valor=float(fila["valor"]),
            )

            repo_precios.crear(precio)

    # -------------------------------------------
    # Stock
    # -------------------------------------------

    with open(
        ruta_csv / "stock.csv",
        encoding="utf-8",
        newline="",
    ) as archivo:
        lector = csv.DictReader(archivo)

        for fila in lector:
            libro = repo_libros.leer_por_id(
                int(fila["libro_id"])
            )

            if libro is None:
                raise ValueError(
                    f"Libro inexistente: {fila['libro_id']}"
                )

            stock = Stock(
                id=int(fila["id"]),
                libro=libro,
                cantidad=int(fila["cantidad"]),
            )

            repo_stock.crear(stock)

    # -------------------------------------------
    # Cotizaciones del dólar
    # -------------------------------------------

    with open(
        ruta_csv / "cotizaciones_dolar.csv",
        encoding="utf-8",
        newline="",
    ) as archivo:
        lector = csv.DictReader(archivo)

        for fila in lector:
            tipo = repo_tipos_cotizacion.leer_por_id(
                int(fila["tipo_cotizacion_id"])
            )
            moneda = repo_monedas.leer_por_id(
                int(fila["moneda_id"])
            )

            if tipo is None:
                raise ValueError(
                    "Tipo de cotización inexistente: "
                    f"{fila['tipo_cotizacion_id']}"
                )

            if moneda is None:
                raise ValueError(
                    f"Moneda inexistente: {fila['moneda_id']}"
                )

            cotizacion = CotizacionDolar(
                id=int(fila["id"]),
                tipo_cotizacion=tipo,
                moneda=moneda,
                fecha=datetime.strptime(
                    fila["fecha"],
                    "%Y-%m-%d",
                ).date(),
                valor_compra=float(fila["valor_compra"]),
                valor_venta=float(fila["valor_venta"]),
            )

            repo_cotizaciones.crear(cotizacion)

    return {
        "generos": repo_generos,
        "editoriales": repo_editoriales,
        "monedas": repo_monedas,
        "tipos_cotizacion": repo_tipos_cotizacion,
        "libros": repo_libros,
        "precios": repo_precios,
        "stock": repo_stock,
        "cotizaciones": repo_cotizaciones,
    }
