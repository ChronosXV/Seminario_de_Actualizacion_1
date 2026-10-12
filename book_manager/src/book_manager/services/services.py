
"""
Servicios del sistema Book Manager.

Contiene la lógica de negocio y las validaciones necesarias
para operar con los modelos ORM mediante los repositorios.
"""

from datetime import date
from typing import Generic, TypeVar

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
        """Inicializa el servicio con su repositorio."""
        self._repositorio = repositorio

    def crear(self, entidad: M) -> M:
        """Crea una entidad en la base de datos."""
        return self._repositorio.crear(entidad)

    def obtener_por_id(self, id: int) -> M | None:
        """Obtiene una entidad mediante su identificador."""
        return self._repositorio.leer_por_id(id)

    def obtener_todos(self) -> list[M]:
        """Obtiene todas las entidades."""
        return self._repositorio.leer_todos()

    def actualizar(self, entidad: M) -> M:
        """Actualiza una entidad existente."""
        return self._repositorio.actualizar(entidad)

    def eliminar(self, id: int) -> bool:
        """Elimina una entidad mediante su identificador."""
        return self._repositorio.eliminar(id)


class ServicioLibro(ServicioBase[LibroModel]):
    """Servicio de gestión de libros."""

    def crear(self, libro: LibroModel) -> LibroModel:
        """Valida y registra un libro."""
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
        """Valida y registra un precio."""
        if precio.valor is None or precio.valor <= 0:
            raise ValueError("El precio debe ser mayor que cero.")

        return self._repositorio.crear(precio)


class ServicioStock:
    """Servicio de gestión de existencias."""

    def __init__(self, repositorio: RepositorioStock) -> None:
        """Inicializa el servicio con el repositorio de stock."""
        self._repositorio = repositorio

    def crear(self, stock: StockModel) -> StockModel:
        """Valida y registra el stock de un libro."""
        if stock.cantidad is None or stock.cantidad < 0:
            raise ValueError("El stock no puede ser negativo.")

        return self._repositorio.crear(stock)

    def obtener_por_libro(self, libro_id: int) -> StockModel | None:
        """Obtiene el stock de un libro."""
        return self._repositorio.leer_por_libro(libro_id)

    def actualizar(self, stock: StockModel) -> StockModel:
        """Valida y actualiza el stock de un libro."""
        if stock.cantidad is None or stock.cantidad < 0:
            raise ValueError("El stock no puede ser negativo.")

        return self._repositorio.actualizar(stock)

    def eliminar(self, libro_id: int) -> bool:
        """Elimina el stock asociado a un libro."""
        return self._repositorio.eliminar_por_libro(libro_id)


class ServicioCotizacionDolar:
    """Servicio de gestión de cotizaciones del dólar."""

    def __init__(
        self,
        repositorio: RepositorioCotizacionDolar,
    ) -> None:
        """Inicializa el servicio con el repositorio de cotizaciones."""
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
                "El valor de venta no puede ser menor "
                "que el valor de compra."
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
        """Obtiene una cotización por tipo y fecha."""
        return self._repositorio.leer_por_tipo_y_fecha(
            tipo_id,
            fecha,
        )

    def obtener_historico(
        self,
        tipo_id: int,
    ) -> list[CotizacionDolarModel]:
        """Obtiene el historial de cotizaciones de un tipo."""
        return self._repositorio.leer_historico_por_tipo(tipo_id)

    def actualizar(
        self,
        cotizacion: CotizacionDolarModel,
    ) -> CotizacionDolarModel:
        """Valida y actualiza una cotización."""
        self._validar(cotizacion)
        return self._repositorio.actualizar(cotizacion)

    def eliminar(
        self,
        tipo_id: int,
        fecha: date,
    ) -> bool:
        """Elimina una cotización por tipo y fecha."""
        return self._repositorio.eliminar_por_tipo_y_fecha(
            tipo_id,
            fecha,
        )
