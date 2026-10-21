
"""
Definición de los datos extraídos mediante Scrapy.

Sprint 3 - Ejercicio 03.
"""

import scrapy


class LibroItem(scrapy.Item):
    """Representa un libro encontrado en Cúspide."""

    titulo_buscado = scrapy.Field()
    titulo = scrapy.Field()
    precio = scrapy.Field()
    imagen_url = scrapy.Field()
    medios_pago = scrapy.Field()
    descripcion = scrapy.Field()
    url = scrapy.Field()
