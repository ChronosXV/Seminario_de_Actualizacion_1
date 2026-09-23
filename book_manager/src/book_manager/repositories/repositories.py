
import abc
from datetime import date
from typing import Dict, Generic, List, Optional, TypeVar

from book_manager.entities.entities import (
    EntidadBase,
    Stock,
    CotizacionDolar,
)


T = TypeVar("T", bound=EntidadBase)


class IRepositorio(abc.ABC, Generic[T]):
    """Interfaz para operaciones CRUD."""

    @abc.abstractmethod
    def crear(self, entidad: T) -> T:
        pass

    @abc.abstractmethod
    def leer_por_id(self, id: int) -> Optional[T]:
        pass

    @abc.abstractmethod
    def leer_todos(self) -> List[T]:
        pass

    @abc.abstractmethod
    def actualizar(self, entidad: T) -> T:
        pass

    @abc.abstractmethod
    def eliminar(self, id: int) -> bool:
        pass


class Repositorio(IRepositorio[T]):
    """Repositorio genérico para administrar entidades."""

    def __init__(self) -> None:
        self._datos: Dict[int, T] = {}

    def crear(self, entidad: T) -> T:
        if entidad.id in self._datos:
            raise ValueError(
                f"Ya existe una entidad con ID {entidad.id}."
            )

        self._datos[entidad.id] = entidad
        return entidad

    def leer_por_id(self, id: int) -> Optional[T]:
        return self._datos.get(id)

    def leer_todos(self) -> List[T]:
        return list(self._datos.values())

    def actualizar(self, entidad: T) -> T:
        if entidad.id not in self._datos:
            raise ValueError(
                f"No existe una entidad con ID {entidad.id}."
            )

        self._datos[entidad.id] = entidad
        return entidad

    def eliminar(self, id: int) -> bool:
        if id not in self._datos:
            return False

        del self._datos[id]
        return True


class IRepositorioStock(abc.ABC):
    """Interfaz para administrar registros de stock."""

    @abc.abstractmethod
    def crear(self, stock: Stock) -> Stock:
        pass

    @abc.abstractmethod
    def leer_por_libro(
        self, libro_id: int
    ) -> Optional[Stock]:
        pass

    @abc.abstractmethod
    def actualizar(self, stock: Stock) -> Stock:
        pass

    @abc.abstractmethod
    def eliminar(self, libro_id: int) -> bool:
        pass


class RepositorioStock(IRepositorioStock):
    """Repositorio especializado para el stock."""

    def __init__(self) -> None:
        self._datos: Dict[int, Stock] = {}

    def crear(self, stock: Stock) -> Stock:
        libro_id = stock.libro.id

        if libro_id in self._datos:
            raise ValueError(
                f"Ya existe stock para el libro {libro_id}."
            )

        self._datos[libro_id] = stock
        return stock

    def leer_por_libro(
        self, libro_id: int
    ) -> Optional[Stock]:
        return self._datos.get(libro_id)

    def actualizar(self, stock: Stock) -> Stock:
        libro_id = stock.libro.id

        if libro_id not in self._datos:
            raise ValueError(
                f"No existe stock para el libro {libro_id}."
            )

        self._datos[libro_id] = stock
        return stock

    def eliminar(self, libro_id: int) -> bool:
        if libro_id not in self._datos:
            return False

        del self._datos[libro_id]
        return True


class IRepositorioCotizacionDolar(abc.ABC):
    """Interfaz para administrar cotizaciones."""

    @abc.abstractmethod
    def crear(
        self, cotizacion: CotizacionDolar
    ) -> CotizacionDolar:
        pass

    @abc.abstractmethod
    def leer_por_tipo_y_fecha(
        self, tipo_id: int, fecha: date
    ) -> Optional[CotizacionDolar]:
        pass

    @abc.abstractmethod
    def leer_historico_por_tipo(
        self, tipo_id: int
    ) -> List[CotizacionDolar]:
        pass

    @abc.abstractmethod
    def actualizar(
        self, cotizacion: CotizacionDolar
    ) -> CotizacionDolar:
        pass

    @abc.abstractmethod
    def eliminar(
        self, tipo_id: int, fecha: date
    ) -> bool:
        pass


class RepositorioCotizacionDolar(
    IRepositorioCotizacionDolar
):
    """Repositorio especializado para cotizaciones."""

    def __init__(self) -> None:
        self._datos: Dict[
            tuple[int, date], CotizacionDolar
        ] = {}

    def crear(
        self, cotizacion: CotizacionDolar
    ) -> CotizacionDolar:
        clave = (
            cotizacion.tipo_cotizacion.id,
            cotizacion.fecha,
        )

        if clave in self._datos:
            raise ValueError(
                "Ya existe una cotización para ese tipo y fecha."
            )

        self._datos[clave] = cotizacion
        return cotizacion

    def leer_por_tipo_y_fecha(
        self, tipo_id: int, fecha: date
    ) -> Optional[CotizacionDolar]:
        return self._datos.get((tipo_id, fecha))

    def leer_historico_por_tipo(
        self, tipo_id: int
    ) -> List[CotizacionDolar]:
        return [
            cotizacion
            for (id_tipo, _), cotizacion
            in self._datos.items()
            if id_tipo == tipo_id
        ]

    def actualizar(
        self, cotizacion: CotizacionDolar
    ) -> CotizacionDolar:
        clave = (
            cotizacion.tipo_cotizacion.id,
            cotizacion.fecha,
        )

        if clave not in self._datos:
            raise ValueError(
                "No existe la cotización que se quiere actualizar."
            )

        self._datos[clave] = cotizacion
        return cotizacion

    def eliminar(
        self, tipo_id: int, fecha: date
    ) -> bool:
        clave = (tipo_id, fecha)

        if clave not in self._datos:
            return False

        del self._datos[clave]
        return True
