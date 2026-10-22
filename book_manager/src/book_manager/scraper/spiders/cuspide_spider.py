
"""
Spider para buscar libros del catálogo de Book Manager en Cúspide.

Sprint 3 - Ejercicio 03.
"""

import json
import re
from urllib.parse import urlencode

import scrapy

from book_manager.scraper.loaders import LibroLoader


class CuspideSpider(scrapy.Spider):
    """Busca hasta diez resultados de Cúspide por cada título recibido."""

    name = "cuspide"

    allowed_domains = ["cuspide.com"]

    custom_settings = {
        "ROBOTSTXT_OBEY": True,
        "DOWNLOAD_DELAY": 1,
        "CONCURRENT_REQUESTS_PER_DOMAIN": 1,
        "ITEM_PIPELINES": {
            "book_manager.scraper.pipelines.ValidacionLibroPipeline": 300
        },
    }

    def __init__(self, titulos_json=None, *args, **kwargs):
        """Recibe los títulos de los libros de nuestro catálogo."""

        super().__init__(*args, **kwargs)

        if not titulos_json:
            raise ValueError(
                "Debe proporcionar los títulos del catálogo."
            )

        titulos = json.loads(titulos_json)

        if not isinstance(titulos, list):
            raise ValueError(
                "Los títulos deben proporcionarse como una lista JSON."
            )

        self.titulos = [
            titulo.strip()
            for titulo in titulos
            if isinstance(titulo, str) and titulo.strip()
        ]

        if not self.titulos:
            raise ValueError(
                "No se recibieron títulos válidos."
            )

    async def start(self):
        """Genera una búsqueda por cada título del catálogo.
        Nota: En la clase vimos start_requests(), pero nosotros utilizamos async def start() porque es el recomendado con Scrapy 2.19, para generar las solicitudes iniciales."""

        for titulo in self.titulos:

            parametros = urlencode({
                "s": titulo,
                "post_type": "product"
            })

            url_busqueda = (
                f"https://cuspide.com/?{parametros}"
            )

            yield scrapy.Request(
                url=url_busqueda,
                callback=self.parse,
                cb_kwargs={
                    "titulo_buscado": titulo
                },
                dont_filter=True
            )

    def parse(self, response, titulo_buscado):
        """Obtiene hasta diez resultados de una búsqueda por título."""

        productos = response.css("div.product")

        encontrados = 0

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
                callback=self.parse_libro,
                cb_kwargs={
                    "titulo_buscado": titulo_buscado
                }
            )

            encontrados += 1

            if encontrados >= 10:
                break

    def parse_libro(self, response, titulo_buscado):
        """Extrae los datos de cada resultado encontrado."""

        loader = LibroLoader(response=response)

        # ------------------------------------------
        # Título
        # ------------------------------------------

        titulo = response.css(
            "h1.product_title"
        ).xpath("string(.)").get()

        # ------------------------------------------
        # Precio
        # ------------------------------------------

        precio = response.css(
            ".summary .price"
        ).xpath("string(.)").get()

        # ------------------------------------------
        # Descripción
        # ------------------------------------------

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

        # ------------------------------------------
        # Imagen del libro
        # ------------------------------------------

        imagen = response.css(
            "div.product img::attr(src)"
        ).get()

        # ------------------------------------------
        # Cargar los datos mediante ItemLoader
        # ------------------------------------------

        if titulo:
            loader.add_value(
                "titulo",
                titulo
            )

        if precio:
            loader.add_value(
                "precio",
                precio
            )

        # Limpiar la descripción antes de cargarla
        if descripcion:

            descripcion = self.limpiar_descripcion(
                descripcion,
                titulo
            )

            if descripcion:
                loader.add_value(
                    "descripcion",
                    descripcion
                )

        if imagen:
            loader.add_value(
                "imagen_url",
                response.urljoin(imagen)
            )

        loader.add_value(
            "url",
            response.url
        )

        # ------------------------------------------
        # Formas de pago
        # ------------------------------------------

        medios_pago = []

        for lista in response.css("ul"):

            opciones = lista.xpath("./li")

            textos = [
                " ".join(
                    opcion.xpath("string(.)").get(default="").split()
                )
                for opcion in opciones
            ]

            # Identificar el listado de medios de pago
            if any(
                "depósito o transferencia" in texto.lower()
                for texto in textos
            ):

                for texto in textos:

                    forma_pago = texto.lstrip("> ").strip()

                    if forma_pago:
                        medios_pago.append({
                            "forma_pago": forma_pago,
                            "precio": None
                        })

                break

        # Incorporar las formas de pago al ItemLoader
        if medios_pago:
            loader.add_value(
                "medios_pago",
                medios_pago
            )

        # ------------------------------------------
        # Construir el Item
        # ------------------------------------------

        item = loader.load_item()

        # Asociar el resultado al título de nuestro catálogo
        item["titulo_buscado"] = titulo_buscado

        # Enviar el resultado al Pipeline
        yield item

    @staticmethod
    def limpiar_descripcion(descripcion, titulo):
        """
        Limpia la sinopsis del producto.

        Elimina:
        - Encabezado 'Sinopsis del producto'.
        - Título repetido al final.
        - Posible ISBN-13 al final.
        """

        texto = descripcion.strip()

        # Eliminar encabezado
        texto = re.sub(
            r"^Sinopsis del producto\s*",
            "",
            texto,
            flags=re.IGNORECASE
        )

        # Normalizar espacios del título
        titulo_limpio = (
            " ".join(titulo.split())
            if titulo
            else ""
        )

        # Eliminar título repetido al final
        if titulo_limpio:

            patron_titulo = re.escape(titulo_limpio)

            texto = re.sub(
                rf"\s*{patron_titulo}\s*$",
                "",
                texto,
                flags=re.IGNORECASE
            ).rstrip()

        # Eliminar posible ISBN-13 al final
        texto = re.sub(
            r"(?<!\d)97[89]\d{10}$",
            "",
            texto
        ).rstrip()

        return texto

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
