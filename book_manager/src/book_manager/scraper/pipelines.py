"""
Validación de libros extraídos mediante Scrapy.

Sprint 3 - Ejercicio 03.
"""

from decimal import Decimal, InvalidOperation

from scrapy.exceptions import DropItem
from scrapy.item import Item


class ValidacionLibroPipeline:
    """Valida los datos obligatorios de cada libro extraído."""

    def process_item(self, item: Item) -> Item:
        """Valida el libro y lo devuelve si cumple las condiciones."""

        titulo = item.get("titulo")
        precio = item.get("precio")
        url = item.get("url")

        if not isinstance(titulo, str) or not titulo.strip():
            raise DropItem("Libro descartado: título vacío.")

        if not isinstance(url, str) or not url.strip():
            raise DropItem("Libro descartado: URL vacía.")

        if precio is None:
            raise DropItem("Libro descartado: precio inexistente.")

        try:
            precio_decimal = Decimal(str(precio))
        except (InvalidOperation, ValueError, TypeError) as error:
            raise DropItem(
                f"Libro descartado: precio inválido ({precio})."
            ) from error

        if not precio_decimal.is_finite() or precio_decimal <= 0:
            raise DropItem(
                "Libro descartado: el precio debe ser positivo."
            )

        item["precio"] = precio_decimal

        return item
