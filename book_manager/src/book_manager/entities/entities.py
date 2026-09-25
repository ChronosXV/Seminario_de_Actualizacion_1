from datetime import date
from typing import Optional

# Creacion de identidades
class EntidadBase:
    """Clase base para las entidades."""

    def __init__(self, id: int) -> None:
        self._id = id

    @property
    def id(self) -> int:
        return self._id


class Genero(EntidadBase):
    def __init__(self, id: int, nombre: str) -> None:
        super().__init__(id)
        self._nombre = nombre

    @property
    def nombre(self) -> str:
        return self._nombre


class Editorial(EntidadBase):
    def __init__(self, id: int, nombre: str) -> None:
        super().__init__(id)
        self._nombre = nombre

    @property
    def nombre(self) -> str:
        return self._nombre


class Moneda(EntidadBase):
    def __init__(
        self, id: int, codigo: str, nombre: str, simbolo: str
    ) -> None:
        super().__init__(id)
        self._codigo = codigo
        self._nombre = nombre
        self._simbolo = simbolo

    @property
    def codigo(self) -> str:
        return self._codigo

    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def simbolo(self) -> str:
        return self._simbolo


class TipoCotizacion(EntidadBase):
    def __init__(self, id: int, nombre: str) -> None:
        super().__init__(id)
        self._nombre = nombre

    @property
    def nombre(self) -> str:
        return self._nombre


class Libro(EntidadBase):
    def __init__(
        self,
        id: int,
        isbn: str,
        titulo: str,
        autor: str,
        editorial: Editorial,
        genero: Genero,
    ) -> None:
        super().__init__(id)
        self._isbn = isbn
        self._titulo = titulo
        self._autor = autor
        self._editorial = editorial
        self._genero = genero

    @property
    def isbn(self) -> str:
        return self._isbn

    @property
    def titulo(self) -> str:
        return self._titulo

    @property
    def autor(self) -> str:
        return self._autor

    @property
    def editorial(self) -> Editorial:
        return self._editorial

    @property
    def genero(self) -> Genero:
        return self._genero


class Precio(EntidadBase):
    def __init__(
        self, id: int, libro: Libro, moneda: Moneda, valor: float
    ) -> None:
        super().__init__(id)
        self._libro = libro
        self._moneda = moneda
        self._valor = valor

    @property
    def libro(self) -> Libro:
        return self._libro

    @property
    def moneda(self) -> Moneda:
        return self._moneda

    @property
    def valor(self) -> float:
        return self._valor


class Stock(EntidadBase):
    def __init__(
        self, id: int, libro: Libro, cantidad: int
    ) -> None:
        super().__init__(id)
        self._libro = libro
        self._cantidad = cantidad

    @property
    def libro(self) -> Libro:
        return self._libro

    @property
    def cantidad(self) -> int:
        return self._cantidad


class CotizacionDolar(EntidadBase):
    def __init__(
        self,
        id: int,
        tipo_cotizacion: TipoCotizacion,
        moneda: Moneda,
        fecha: date,
        valor_compra: float,
        valor_venta: float,
    ) -> None:
        super().__init__(id)
        self._tipo_cotizacion = tipo_cotizacion
        self._moneda = moneda
        self._fecha = fecha
        self._valor_compra = valor_compra
        self._valor_venta = valor_venta

    @property
    def tipo_cotizacion(self) -> TipoCotizacion:
        return self._tipo_cotizacion

    @property
    def moneda(self) -> Moneda:
        return self._moneda

    @property
    def fecha(self) -> date:
        return self._fecha

    @property
    def valor_compra(self) -> float:
        return self._valor_compra

    @property
    def valor_venta(self) -> float:
        return self._valor_venta