"""
Definición de los datos extraídos mediante Scrapy.

Sprint 3 - Ejercicio 03.
"""

import scrapy


class LibroItem(scrapy.Item):
    """Representa la información de un libro extraído de Cúspide."""

    titulo = scrapy.Field()
    precio = scrapy.Field()
    imagen_url = scrapy.Field()
    medios_pago = scrapy.Field()
    descripcion = scrapy.Field()
    url = scrapy.Field()
