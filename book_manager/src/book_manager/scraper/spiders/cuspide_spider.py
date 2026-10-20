
"""
Spider para extraer libros del catálogo de Cúspide.

Sprint 3 - Ejercicio 03.
"""

import json

import scrapy

from book_manager.scraper.loaders import LibroLoader


class CuspideSpider(scrapy.Spider):
    """Extrae los primeros diez libros del catálogo de Cúspide."""

    name = "cuspide"

    allowed_domains = ["cuspide.com"]

    start_urls = [
        "https://cuspide.com/tienda/"
    ]

    custom_settings = {
        "ROBOTSTXT_OBEY": True,
        "DOWNLOAD_DELAY": 1,
        "CONCURRENT_REQUESTS_PER_DOMAIN": 1,
        "ITEM_PIPELINES": {
            "book_manager.scraper.pipelines.ValidacionLibroPipeline": 300
        },
    }

    def parse(self, response):
        """Obtiene los enlaces de los primeros diez libros."""

        productos = response.css("div.product")

        libros_encontrados = 0

        for producto in productos:

            titulo = producto.css(
                ".woocommerce-loop-product__title"
            ).xpath("string(.)").get()

            if not titulo:
                continue

            titulo = titulo.strip()

            # Excluir tarjetas de regalo
            if "GIFT CARD" in titulo.upper():
                continue

            url = producto.css(
                "a.woocommerce-LoopProduct-link::attr(href)"
            ).get()

            if not url:
                continue

            yield response.follow(
                url,
                callback=self.parse_libro
            )

            libros_encontrados += 1

            if libros_encontrados >= 10:
                break

    def parse_libro(self, response):
        """Extrae los datos de la página individual del libro."""

        loader = LibroLoader(response=response)

        # Título
        titulo = response.css(
            "h1.product_title"
        ).xpath("string(.)").get()

        # Precio
        precio = response.css(
            ".summary .price"
        ).xpath("string(.)").get()

        # Descripción desde HTML
        descripcion = response.css(
            ".description"
        ).xpath("string(.)").get()

        # Si no existe descripción HTML, buscar en JSON-LD
        if not descripcion or not descripcion.strip():

            scripts = response.css(
                'script[type="application/ld+json"]::text'
            ).getall()

            for script in scripts:

                try:
                    datos = json.loads(script)

                except json.JSONDecodeError:
                    continue

                descripcion = self.buscar_descripcion(datos)

                if descripcion:
                    break

        # URL de la imagen del libro
        imagen = response.css(
            "div.product img::attr(src)"
        ).get()

        # Cargar los datos mediante ItemLoader
        if titulo:
            loader.add_value("titulo", titulo)

        if precio:
            loader.add_value("precio", precio)

        if descripcion:
            loader.add_value("descripcion", descripcion)

        if imagen:
            loader.add_value(
                "imagen_url",
                response.urljoin(imagen)
            )

        loader.add_value(
            "url",
            response.url
        )

        # Medios de pago
        # Obtener dinámicamente la imagen desde el HTML
        imagen_pago = response.css(
            ".payment-icons img::attr(src)"
        ).get()

        medios_pago = {
            "imagen_url": (
                response.urljoin(imagen_pago)
                if imagen_pago else None
            ),
            "precios_diferenciados": None
        }

        loader.add_value(
            "medios_pago",
            medios_pago
        )

        # Enviar el libro al Pipeline
        yield loader.load_item()

    @staticmethod
    def buscar_descripcion(datos):
        """
        Busca una descripción dentro de una estructura JSON-LD.

        Admite diccionarios y listas anidadas.
        """

        if isinstance(datos, dict):

            descripcion = datos.get("description")

            if isinstance(descripcion, str) and descripcion.strip():
                return descripcion

            for valor in datos.values():

                encontrada = CuspideSpider.buscar_descripcion(
                    valor
                )

                if encontrada:
                    return encontrada

        elif isinstance(datos, list):

            for elemento in datos:

                encontrada = CuspideSpider.buscar_descripcion(
                    elemento
                )

                if encontrada:
                    return encontrada

        return None
