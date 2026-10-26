from typing import Any

"""
Ejercicio 04 - Book Manager.

Ejecuta el scraping del catálogo, convierte precios USD a ARS
y genera un reporte CSV con comparaciones y alertas.
"""

import csv
import json
import os
import re
import subprocess
import sys
import unicodedata

from datetime import datetime
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from pathlib import Path

from sqlalchemy import select

from book_manager.database.connection import ConexionDB
from book_manager.models.models import (
    LibroModel,
    PrecioModel,
    MonedaModel,
    CotizacionDolarModel,
    TipoCotizacionModel,
)

from book_manager.auditoria.auditoria import auditar


# ============================================================
# COLUMNAS DEL REPORTE
# ============================================================

COLUMNAS_CSV = [
    "fecha_ejecucion",
    "libro_id",
    "titulo",
    "precio_original",
    "moneda_original",
    "cotizacion_oficial",
    "fecha_cotizacion",
    "precio_interno_ars",
    "precio_web_ars",
    "diferencia_ars",
    "diferencia_porcentaje",
    "umbral_porcentaje",
    "estado",
    "url",
]


# ============================================================
# NORMALIZACIÓN DE TÍTULOS
# ============================================================

def normalizar_titulo(titulo: str) -> str:
    """
    Normaliza títulos para comparar sin distinguir
    mayúsculas, tildes, puntuación ni espacios extra.
    """

    texto = unicodedata.normalize(
        "NFKD",
        titulo or ""
    )

    texto = "".join(
        caracter
        for caracter in texto
        if not unicodedata.combining(caracter)
    )

    texto = re.sub(
        r"[^a-z0-9]+",
        " ",
        texto.casefold()
    )

    return " ".join(texto.split())


# ============================================================
# SOLICITAR PORCENTAJE DE ALERTA
# ============================================================

def solicitar_umbral() -> Decimal:
    """
    Solicita al usuario el porcentaje mínimo
    de diferencia para generar una alerta.
    """

    while True:

        entrada = input(
            "Ingresá el porcentaje de alerta: "
        ).strip().replace(",", ".")

        try:

            umbral = Decimal(entrada)

            if not umbral.is_finite() or umbral < 0:
                raise ValueError

            return umbral

        except (InvalidOperation, ValueError):

            print(
                "Ingresá un porcentaje válido "
                "mayor o igual a cero."
            )


# ============================================================
# OBTENER CATÁLOGO DESDE SUPABASE
# ============================================================

def obtener_catalogo(conexion: ConexionDB) -> list[dict[str, Any]]:
    """
    Obtiene los libros y sus precios desde la base de datos.
    """

    consulta = (
        select(
            LibroModel.id,
            LibroModel.titulo,
            PrecioModel.valor,
            MonedaModel.codigo,
        )
        .join(
            PrecioModel,
            PrecioModel.libro_id == LibroModel.id,
        )
        .join(
            MonedaModel,
            MonedaModel.id == PrecioModel.moneda_id,
        )
        .order_by(
            LibroModel.id,
            PrecioModel.id,
        )
    )

    with conexion.obtener_sesion() as sesion:
        filas = sesion.execute(consulta).all()

    catalogo = [
        {
            "id": libro_id,
            "titulo": titulo,
            "precio_original": Decimal(str(precio)),
            "moneda": moneda.upper(),
        }
        for libro_id, titulo, precio, moneda in filas
    ]

    return catalogo


# ============================================================
# OBTENER COTIZACIÓN OFICIAL DEL DÓLAR
# ============================================================

def obtener_dolar_oficial(conexion: ConexionDB) -> dict[str, Any] | None:
    """
    Obtiene la última cotización oficial de venta
    del dólar registrada en Supabase.
    """

    consulta = (
        select(
            CotizacionDolarModel.fecha,
            CotizacionDolarModel.valor_venta,
        )
        .join(
            TipoCotizacionModel,
            CotizacionDolarModel.tipo_cotizacion_id
            == TipoCotizacionModel.id,
        )
        .join(
            MonedaModel,
            CotizacionDolarModel.moneda_id
            == MonedaModel.id,
        )
        .where(
            TipoCotizacionModel.nombre == "Oficial",
            MonedaModel.codigo == "USD",
        )
        .order_by(
            CotizacionDolarModel.fecha.desc(),
            CotizacionDolarModel.id.desc(),
        )
        .limit(1)
    )

    with conexion.obtener_sesion() as sesion:
        fila = sesion.execute(consulta).first()

    if fila is None:
        return None

    fecha, valor_venta = fila

    cotizacion = Decimal(str(valor_venta))

    if not cotizacion.is_finite() or cotizacion <= 0:
        return None

    return {
        "fecha": fecha,
        "venta": cotizacion,
    }


# ============================================================
# CONVERTIR PRECIOS A PESOS ARGENTINOS
# ============================================================

def convertir_precios(catalogo: list[dict[str, Any]], dolar_oficial: dict[str, Any] | None) -> list[dict[str, Any]]:
    """
    Convierte los precios USD a ARS utilizando
    la cotización oficial de venta.

    Los precios en ARS se conservan sin cambios.
    """

    for libro in catalogo:

        moneda = libro["moneda"]
        precio = libro["precio_original"]

        libro["precio_ars"] = None
        libro["cotizacion"] = None
        libro["fecha_cotizacion"] = None
        libro["estado_conversion"] = "OK"

        if moneda == "ARS":

            libro["precio_ars"] = precio

        elif moneda == "USD":

            if dolar_oficial is None:

                libro["estado_conversion"] = "SIN COTIZACIÓN"
                continue

            libro["cotizacion"] = dolar_oficial["venta"]

            libro["fecha_cotizacion"] = dolar_oficial["fecha"]

            libro["precio_ars"] = (
                precio * dolar_oficial["venta"]
            ).quantize(
                Decimal("0.01"),
                rounding=ROUND_HALF_UP,
            )

        else:

            libro["estado_conversion"] = (
                "MONEDA NO SOPORTADA"
            )

    return catalogo


# ============================================================
# EJECUTAR EL SPIDER
# ============================================================

def ejecutar_spider(proyecto: Path, titulos: list[str], ruta_json: Path) -> list[dict[str, Any]]:
    """
    Ejecuta CuspideSpider utilizando los títulos
    obtenidos desde el catálogo de Supabase.
    """

    ruta_spider = (
        proyecto
        / "src/book_manager/scraper/spiders/cuspide_spider.py"
    )

    entorno = os.environ.copy()

    entorno["PYTHONPATH"] = (
        str(proyecto / "src")
        + os.pathsep
        + entorno.get("PYTHONPATH", "")
    )

    comando = [
        sys.executable,
        "-m",
        "scrapy",
        "runspider",
        str(ruta_spider),
        "-a",
        "titulos_json=" + json.dumps(
            titulos,
            ensure_ascii=False,
        ),
        "-O",
        str(ruta_json),
        "-s",
        "LOG_LEVEL=ERROR",
    ]

    print(
        f"\nEjecutando Spider para {len(titulos)} títulos..."
    )

    resultado = subprocess.run(
        comando,
        cwd=proyecto,
        env=entorno,
        capture_output=True,
        text=True,
    )

    if resultado.returncode != 0:

        print(resultado.stderr[-5000:])

        raise RuntimeError(
            "No se pudo completar la ejecución del Spider."
        )

    if not ruta_json.is_file():

        raise FileNotFoundError(
            "No se generó el archivo JSON del scraping."
        )

    with ruta_json.open(
        "r",
        encoding="utf-8"
    ) as archivo:

        datos = json.load(archivo)

    if not isinstance(datos, list):

        raise ValueError(
            "El JSON del scraping no contiene una lista."
        )

    return datos


# ============================================================
# GENERAR COMPARACIONES Y ALERTAS
# ============================================================

def generar_reporte(catalogo: list[dict[str, Any]], resultados_web: list[dict[str, Any]], umbral: Decimal, fecha: str) -> list[dict[str, Any]]:
    """
    Compara los precios internos con los precios web.

    Incluye:
    - ALERTA
    - SIN ALERTA
    - SIN COINCIDENCIA
    - SIN COTIZACIÓN
    - MONEDA NO SOPORTADA
    - SIN PRECIO WEB VÁLIDO
    """

    resultados_por_busqueda = {}

    for resultado in resultados_web:

        clave = normalizar_titulo(
            resultado.get("titulo_buscado", "")
        )

        resultados_por_busqueda.setdefault(
            clave,
            []
        ).append(resultado)

    reporte = []

    for libro in catalogo:

        titulo = libro["titulo"]

        clave = normalizar_titulo(titulo)

        coincidencias = [
            resultado
            for resultado in resultados_por_busqueda.get(
                clave,
                []
            )
            if normalizar_titulo(
                resultado.get("titulo", "")
            ) == clave
        ]

        # Evitar productos duplicados por URL.
        coincidencias_unicas = {}

        for resultado in coincidencias:

            url = resultado.get("url", "")

            if url:
                coincidencias_unicas[url] = resultado

        coincidencias = list(
            coincidencias_unicas.values()
        )

        # Datos comunes a todas las filas del libro.
        fila_base = {
            "fecha_ejecucion": fecha,
            "libro_id": libro["id"],
            "titulo": titulo,
            "precio_original": str(
                libro["precio_original"]
            ),
            "moneda_original": libro["moneda"],
            "cotizacion_oficial": (
                str(libro["cotizacion"])
                if libro["cotizacion"] is not None
                else ""
            ),
            "fecha_cotizacion": (
                str(libro["fecha_cotizacion"])
                if libro["fecha_cotizacion"] is not None
                else ""
            ),
            "precio_interno_ars": (
                str(libro["precio_ars"])
                if libro["precio_ars"] is not None
                else ""
            ),
            "precio_web_ars": "",
            "diferencia_ars": "",
            "diferencia_porcentaje": "",
            "umbral_porcentaje": str(umbral),
            "estado": "",
            "url": "",
        }

        # Validar conversión monetaria.
        if libro["estado_conversion"] != "OK":

            fila = fila_base.copy()

            fila["estado"] = libro["estado_conversion"]

            reporte.append(fila)

            continue

        # Si no encontramos el título exacto.
        if not coincidencias:

            fila = fila_base.copy()

            fila["estado"] = "SIN COINCIDENCIA"

            reporte.append(fila)

            continue

        comparaciones_validas = 0

        for resultado in coincidencias:

            try:

                precio_web = Decimal(
                    str(resultado.get("precio"))
                )

                if (
                    not precio_web.is_finite()
                    or precio_web <= 0
                ):
                    continue

            except (
                InvalidOperation,
                TypeError,
                ValueError,
            ):
                continue

            precio_interno = libro["precio_ars"]

            if (
                precio_interno is None
                or not precio_interno.is_finite()
                or precio_interno <= 0
            ):
                continue

            # Diferencia absoluta en pesos.
            diferencia = (
                precio_web - precio_interno
            )

            # Diferencia porcentual.
            porcentaje = (
                diferencia / precio_interno
            ) * Decimal("100")

            fila = fila_base.copy()

            fila["precio_web_ars"] = str(
                precio_web
            )

            fila["diferencia_ars"] = str(
                diferencia.quantize(
                    Decimal("0.01")
                )
            )

            fila["diferencia_porcentaje"] = (
                f"{porcentaje:.2f}"
            )

            # Se considera tanto aumento como disminución.
            fila["estado"] = (
                "ALERTA"
                if abs(porcentaje) >= umbral
                else "SIN ALERTA"
            )

            fila["url"] = resultado.get(
                "url",
                ""
            )

            reporte.append(fila)

            comparaciones_validas += 1

        if comparaciones_validas == 0:

            fila = fila_base.copy()

            fila["estado"] = (
                "SIN PRECIO WEB VÁLIDO"
            )

            reporte.append(fila)

    return reporte


# ============================================================
# GUARDAR CSV
# ============================================================

def guardar_csv(ruta_csv: Path, reporte: list[dict[str, Any]]) -> None:
    """
    Guarda todas las comparaciones en un CSV,
    incluyendo los libros sin alerta o coincidencia.
    """

    ruta_csv.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with ruta_csv.open(
        "w",
        newline="",
        encoding="utf-8-sig",
    ) as archivo:

        escritor = csv.DictWriter(
            archivo,
            fieldnames=COLUMNAS_CSV,
            delimiter=";",
        )

        escritor.writeheader()

        escritor.writerows(reporte)


# ============================================================
# PROCESO PRINCIPAL
# ============================================================

@auditar("EJECUTAR_SCRAPER")
def main() -> Path:
    """
    Ejecuta el proceso completo del Ejercicio 04.
    """

    proyecto = Path(__file__).resolve().parents[3]

    print("=== BOOK MANAGER - EJERCICIO 04 ===")

    # Solicitar porcentaje antes de ejecutar el Spider.
    umbral = solicitar_umbral()

    # Conectar con Supabase.
    conexion = ConexionDB()

    # Consultar catálogo.
    catalogo = obtener_catalogo(conexion)

    if not catalogo:

        raise ValueError(
            "No hay libros con precios para comparar."
        )

    # Obtener última cotización oficial.
    dolar_oficial = obtener_dolar_oficial(
        conexion
    )

    # Convertir precios a ARS.
    convertir_precios(
        catalogo,
        dolar_oficial
    )

    if dolar_oficial:

        print(
            "\nDólar oficial venta:",
            dolar_oficial["venta"],
            "ARS",
        )

        print(
            "Fecha de cotización:",
            dolar_oficial["fecha"],
        )

    else:

        print(
            "\nNo se encontró una cotización oficial válida."
        )

    # Títulos únicos del catálogo.
    titulos = list(
        dict.fromkeys(
            libro["titulo"].strip()
            for libro in catalogo
            if (
                libro["titulo"]
                and libro["titulo"].strip()
            )
        )
    )

    # Identificador único de ejecución.
    fecha_archivo = datetime.now().strftime(
        "%Y%m%d_%H%M%S_%f"
    )

    fecha_reporte = datetime.now().isoformat(
        timespec="seconds"
    )

    # Carpeta de reportes.
    carpeta_reportes = (
        proyecto / "src/book_manager/reportes"
    )

    carpeta_reportes.mkdir(
        parents=True,
        exist_ok=True,
    )

    # JSON intermedio del scraping.
    ruta_json = (
        carpeta_reportes
        / f"scraping_ejercicio04_{fecha_archivo}.json"
    )

    # CSV final de alertas.
    ruta_csv = (
        carpeta_reportes
        / f"alertas_precios_{fecha_archivo}.csv"
    )

    print(
        "\nLibros del catálogo:",
        len(titulos)
    )

    print(
        "Porcentaje de alerta:",
        f"{umbral}%"
    )

    # Ejecutar Spider.
    resultados_web = ejecutar_spider(
        proyecto,
        titulos,
        ruta_json,
    )

    # Comparar precios.
    reporte = generar_reporte(
        catalogo,
        resultados_web,
        umbral,
        fecha_reporte,
    )

    # Generar CSV.
    guardar_csv(ruta_csv,reporte )

    # Resumen de estados.
    estados = {}

    for fila in reporte:

        estado = fila["estado"]

        estados[estado] = (
            estados.get(estado, 0) + 1
        )

    print("\n=== RESUMEN ===")

    print(
        "Resultados web:",
        len(resultados_web)
    )

    print(
        "Filas del reporte:",
        len(reporte)
    )

    for estado, cantidad in sorted(
        estados.items()
    ):

        print(
            f"{estado}: {cantidad}"
        )

    print(
        "\nArchivo CSV:",
        ruta_csv
    )

    return ruta_csv


# ============================================================
# EJECUCIÓN DIRECTA DEL MÓDULO
# ============================================================

if __name__ == "__main__":
    main()

