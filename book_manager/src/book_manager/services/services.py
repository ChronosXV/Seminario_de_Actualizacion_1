
from datetime import date
from typing import Generic, List, Optional, TypeVar

from book_manager.entities.entities import (
    CotizacionDolar,
    EntidadBase,
    Libro,
    Precio,
    Stock,
)
from book_manager.repositories.repositories import (
    IRepositorio,
    IRepositorioCotizacionDolar,
    IRepositorioStock,
)

T = TypeVar("T", bound=EntidadBase)


class ServicioBase(Generic[T]):
    """Servicio genérico para operaciones CRUD."""

    def __init__(self, repositorio: IRepositorio[T]) -> None:
        self._repositorio = repositorio

    def crear(self, entidad: T) -> T:
        return self._repositorio.crear(entidad)

    def obtener_por_id(self, id: int) -> Optional[T]:
        return self._repositorio.leer_por_id(id)

    def obtener_todos(self) -> List[T]:
        return self._repositorio.leer_todos()

    def actualizar(self, entidad: T) -> T:
        return self._repositorio.actualizar(entidad)

    def eliminar(self, id: int) -> bool:
        return self._repositorio.eliminar(id)


class ServicioLibro(ServicioBase[Libro]):
    """Lógica de negocio relacionada con libros."""

    def crear(self, libro: Libro) -> Libro:
        if not libro.isbn.strip():
            raise ValueError("El ISBN no puede estar vacío.")

        if not libro.titulo.strip():
            raise ValueError("El título no puede estar vacío.")

        if not libro.autor.strip():
            raise ValueError("El autor no puede estar vacío.")

        return self._repositorio.crear(libro)


class ServicioPrecio(ServicioBase[Precio]):
    """Lógica de negocio relacionada con precios."""

    def crear(self, precio: Precio) -> Precio:
        if precio.valor <= 0:
            raise ValueError("El precio debe ser mayor que cero.")

        return self._repositorio.crear(precio)


class ServicioStock:
    """Lógica de negocio relacionada con el stock."""

    def __init__(self, repositorio: IRepositorioStock) -> None:
        self._repositorio = repositorio

    def crear(self, stock: Stock) -> Stock:
        if stock.cantidad < 0:
            raise ValueError("El stock no puede ser negativo.")

        return self._repositorio.crear(stock)

    def obtener_por_libro(self, libro_id: int) -> Optional[Stock]:
        return self._repositorio.leer_por_libro(libro_id)

    def actualizar(self, stock: Stock) -> Stock:
        if stock.cantidad < 0:
            raise ValueError("El stock no puede ser negativo.")

        return self._repositorio.actualizar(stock)

    def eliminar(self, libro_id: int) -> bool:
        return self._repositorio.eliminar(libro_id)


class ServicioCotizacionDolar:
    """Lógica de negocio relacionada con cotizaciones."""

    def __init__(
        self,
        repositorio: IRepositorioCotizacionDolar,
    ) -> None:
        self._repositorio = repositorio

    def crear(
        self,
        cotizacion: CotizacionDolar,
    ) -> CotizacionDolar:

        if cotizacion.valor_compra <= 0:
            raise ValueError(
                "El valor de compra debe ser mayor que cero."
            )

        if cotizacion.valor_venta <= 0:
            raise ValueError(
                "El valor de venta debe ser mayor que cero."
            )

        if cotizacion.valor_venta < cotizacion.valor_compra:
            raise ValueError(
                "El valor de venta no puede ser menor "
                "que el valor de compra."
            )

        return self._repositorio.crear(cotizacion)

    def obtener_por_tipo_y_fecha(
        self,
        tipo_id: int,
        fecha: date,
    ) -> Optional[CotizacionDolar]:
        return self._repositorio.leer_por_tipo_y_fecha(
            tipo_id,
            fecha,
        )

    def obtener_historico(
        self,
        tipo_id: int,
    ) -> List[CotizacionDolar]:
        return self._repositorio.leer_historico_por_tipo(tipo_id)

    def actualizar(
        self,
        cotizacion: CotizacionDolar,
    ) -> CotizacionDolar:
        if cotizacion.valor_compra <= 0:
            raise ValueError(
                "El valor de compra debe ser mayor que cero."
            )

        if cotizacion.valor_venta <= 0:
            raise ValueError(
                "El valor de venta debe ser mayor que cero."
            )

        return self._repositorio.actualizar(cotizacion)

    def eliminar(
        self,
        tipo_id: int,
        fecha: date,
    ) -> bool:
        return self._repositorio.eliminar(tipo_id, fecha)
