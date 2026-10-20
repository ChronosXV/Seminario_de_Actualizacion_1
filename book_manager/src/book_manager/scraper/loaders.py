"""
Procesamiento y limpieza de los datos extraídos con Scrapy.

Sprint 3 - Ejercicio 03.
"""

import re
from decimal import Decimal, InvalidOperation

from itemloaders import ItemLoader
from itemloaders.processors import Identity, Join, MapCompose, TakeFirst

from book_manager.scraper.items import LibroItem


def limpiar_texto(valor: str) -> str:
    """Elimina espacios innecesarios de un texto."""
    return " ".join(valor.split())


def limpiar_precio(valor: str) -> Decimal:
    """Convierte un precio argentino a Decimal."""
    texto = re.sub(r"[^0-9,.-]", "", str(valor).strip())

    if not texto:
        raise ValueError("El precio está vacío.")

    # Formato argentino: 15.000,50
    if "," in texto:
        texto = texto.replace(".", "").replace(",", ".")
    elif texto.count(".") > 1:
        texto = texto.replace(".", "")
    elif "." in texto:
        parte_entera, parte_decimal = texto.split(".")
        if len(parte_decimal) == 3:
            texto = parte_entera + parte_decimal

    try:
        return Decimal(texto)
    except InvalidOperation as error:
        raise ValueError(f"Precio inválido: {valor}") from error


class LibroLoader(ItemLoader):
    """Limpia y organiza la información extraída de cada libro."""

    default_item_class = LibroItem

    titulo_in = MapCompose(limpiar_texto)
    titulo_out = TakeFirst()

    precio_in = MapCompose(limpiar_precio)
    precio_out = TakeFirst()

    imagen_url_in = MapCompose(str.strip)
    imagen_url_out = TakeFirst()

    medios_pago_out = Identity()

    descripcion_in = MapCompose(limpiar_texto)
    descripcion_out = Join(" ")

    url_in = MapCompose(str.strip)
    url_out = TakeFirst()
