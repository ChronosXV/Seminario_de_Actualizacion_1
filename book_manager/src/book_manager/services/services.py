
"""
Servicios del sistema Book Manager.

Contiene la lógica de negocio y las validaciones necesarias
para operar con los modelos ORM mediante los repositorios.
"""

import os
from datetime import date, datetime
from decimal import Decimal
from pathlib import Path
from typing import Generic, TypeVar
from zoneinfo import ZoneInfo

import requests
from dotenv import load_dotenv
from sqlalchemy.orm import DeclarativeBase

from book_manager.models.models import (
    LibroModel,
    PrecioModel,
    StockModel,
    CotizacionDolarModel,
)

from book_manager.repositories.repositories import (
    Repositorio,
    RepositorioStock,
    RepositorioCotizacionDolar,
)


M = TypeVar("M", bound=DeclarativeBase)


class ServicioBase(Generic[M]):
    """Servicio genérico para operaciones CRUD."""

    def __init__(self, repositorio: Repositorio[M]) -> None:
        self._repositorio = repositorio

    def crear(self, entidad: M) -> M:
        return self._repositorio.crear(entidad)

    def obtener_por_id(self, id: int) -> M | None:
        return self._repositorio.leer_por_id(id)

    def obtener_todos(self) -> list[M]:
        return self._repositorio.leer_todos()

    def actualizar(self, entidad: M) -> M:
        return self._repositorio.actualizar(entidad)

    def eliminar(self, id: int) -> bool:
        return self._repositorio.eliminar(id)


class ServicioLibro(ServicioBase[LibroModel]):
    """Servicio de gestión de libros."""

    def crear(self, libro: LibroModel) -> LibroModel:

        if not libro.isbn or not libro.isbn.strip():
            raise ValueError("El ISBN no puede estar vacío.")

        if not libro.titulo or not libro.titulo.strip():
            raise ValueError("El título no puede estar vacío.")

        if not libro.autor or not libro.autor.strip():
            raise ValueError("El autor no puede estar vacío.")

        return self._repositorio.crear(libro)


class ServicioPrecio(ServicioBase[PrecioModel]):
    """Servicio de gestión de precios."""

    def crear(self, precio: PrecioModel) -> PrecioModel:

        if precio.valor is None or precio.valor <= 0:
            raise ValueError("El precio debe ser mayor que cero.")

        return self._repositorio.crear(precio)


class ServicioStock:
    """Servicio de gestión de existencias."""

    def __init__(self, repositorio: RepositorioStock) -> None:
        self._repositorio = repositorio

    def listar(self) -> list[StockModel]:
        """Obtiene todos los registros de stock."""
        return self._repositorio.leer_todos()

    def crear(self, stock: StockModel) -> StockModel:

        if stock.cantidad is None or stock.cantidad < 0:
            raise ValueError("El stock no puede ser negativo.")

        return self._repositorio.crear(stock)

    def obtener_por_libro(self, libro_id: int) -> StockModel | None:
        return self._repositorio.leer_por_libro(libro_id)

    def actualizar(self, stock: StockModel) -> StockModel:

        if stock.cantidad is None or stock.cantidad < 0:
            raise ValueError("El stock no puede ser negativo.")

        return self._repositorio.actualizar(stock)

    def eliminar(self, libro_id: int) -> bool:
        return self._repositorio.eliminar_por_libro(libro_id)


class ServicioCotizacionDolar:
    """Servicio de gestión de cotizaciones del dólar."""

    def __init__(
        self,
        repositorio: RepositorioCotizacionDolar,
    ) -> None:
        self._repositorio = repositorio

    def _validar(
        self,
        cotizacion: CotizacionDolarModel,
    ) -> None:
        """Valida los valores de compra y venta."""

        if cotizacion.valor_compra is None or cotizacion.valor_compra <= 0:
            raise ValueError(
                "El valor de compra debe ser mayor que cero."
            )

        if cotizacion.valor_venta is None or cotizacion.valor_venta <= 0:
            raise ValueError(
                "El valor de venta debe ser mayor que cero."
            )

        if cotizacion.valor_venta < cotizacion.valor_compra:
            raise ValueError(
                "El valor de venta no puede ser menor que el valor de compra."
            )

    def crear(
        self,
        cotizacion: CotizacionDolarModel,
    ) -> CotizacionDolarModel:
        """Valida y registra una cotización."""

        self._validar(cotizacion)
        return self._repositorio.crear(cotizacion)

    def obtener_por_tipo_y_fecha(
        self,
        tipo_id: int,
        fecha: date,
    ) -> CotizacionDolarModel | None:

        return self._repositorio.leer_por_tipo_y_fecha(
            tipo_id,
            fecha,
        )

    def obtener_historico(
        self,
        tipo_id: int,
    ) -> list[CotizacionDolarModel]:

        return self._repositorio.leer_historico_por_tipo(tipo_id)

    def actualizar(
        self,
        cotizacion: CotizacionDolarModel,
    ) -> CotizacionDolarModel:

        self._validar(cotizacion)
        return self._repositorio.actualizar(cotizacion)

    def eliminar(
        self,
        tipo_id: int,
        fecha: date,
    ) -> bool:

        return self._repositorio.eliminar_por_tipo_y_fecha(
            tipo_id,
            fecha,
        )

    def obtener_cotizaciones(self) -> dict[str, int]:
        """
        Descarga cotizaciones desde DolarAPI.

        Crea nuevas cotizaciones y actualiza las existentes
        según el tipo de dólar y la fecha.
        """

        # 1. Leer configuración del archivo .env

        ruta_env = Path(__file__).resolve().parents[3] / ".env"

        load_dotenv(ruta_env)

        api_url = os.getenv("API_URL")

        if not api_url:
            raise ValueError(
                "No se encontró API_URL en el archivo .env."
            )

        # 2. Consultar la API

        respuesta = requests.get(api_url, timeout=15)
        respuesta.raise_for_status()

        datos = respuesta.json()

        if not isinstance(datos, list):
            raise ValueError(
                "La API no devolvió una lista de cotizaciones."
            )

        # 3. Relacionar los tipos de dólar con nuestra BD

        tipos = {
            "oficial": 1,
            "blue": 2,
            "bolsa": 3,
            "contadoconliqui": 4,
            "mayorista": 5,
            "cripto": 6,
            "tarjeta": 8,
        }

        moneda_usd_id = 2

        # 4. Inicializar contadores

        creadas = 0
        actualizadas = 0
        omitidas = 0

        # 5. Procesar cada cotización

        for dato in datos:

            tipo_id = tipos.get(dato.get("casa"))

            if tipo_id is None or dato.get("moneda") != "USD":
                omitidas += 1
                continue

            # Convertir la fecha UTC a fecha argentina

            fecha_actualizacion = datetime.fromisoformat(
                dato["fechaActualizacion"].replace("Z", "+00:00")
            )

            fecha_cotizacion = fecha_actualizacion.astimezone(
                ZoneInfo("America/Argentina/Buenos_Aires")
            ).date()

            # Convertir importes a Decimal

            compra = Decimal(str(dato["compra"]))
            venta = Decimal(str(dato["venta"]))

            # Buscar cotización existente

            existente = self.obtener_por_tipo_y_fecha(
                tipo_id,
                fecha_cotizacion,
            )

            if existente is None:

                # 6. Crear una nueva cotización

                cotizacion = CotizacionDolarModel(
                    tipo_cotizacion_id=tipo_id,
                    moneda_id=moneda_usd_id,
                    fecha=fecha_cotizacion,
                    valor_compra=compra,
                    valor_venta=venta,
                )

                self.crear(cotizacion)
                creadas += 1

            else:

                # 7. Actualizar una cotización existente

                existente.moneda_id = moneda_usd_id
                existente.valor_compra = compra
                existente.valor_venta = venta

                self.actualizar(existente)
                actualizadas += 1

        # 8. Devolver resumen

        return {
            "creadas": creadas,
            "actualizadas": actualizadas,
            "omitidas": omitidas,
        }
