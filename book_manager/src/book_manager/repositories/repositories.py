
import abc
import csv
import os
import tempfile
from datetime import date
from pathlib import Path
from typing import Dict, Generic, List, Optional, TypeVar

from book_manager.entities.entities import (
    CotizacionDolar,
    EntidadBase,
    Stock,
)


T = TypeVar("T", bound=EntidadBase)


# ==========================================================
# FUNCIONES AUXILIARES PARA PERSISTENCIA CSV
# ==========================================================

def guardar_csv(
    ruta: Path,
    columnas: List[str],
    registros: List[dict],
) -> None:
    """Guarda los registros mediante reemplazo atómico del CSV."""

    ruta.parent.mkdir(parents=True, exist_ok=True)
    temporal = None

    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            newline="",
            dir=ruta.parent,
            suffix=".tmp",
            delete=False,
        ) as archivo:

            temporal = Path(archivo.name)

            escritor = csv.DictWriter(
                archivo,
                fieldnames=columnas,
            )

            escritor.writeheader()
            escritor.writerows(registros)

        os.replace(temporal, ruta)

    finally:
        if temporal is not None and temporal.exists():
            temporal.unlink()


def convertir_entidad(entidad: EntidadBase) -> dict:
    """Convierte una entidad en un registro compatible con CSV."""

    registro = {"id": entidad.id}

    for atributo, valor in vars(entidad).items():

        if atributo == "_id":
            continue

        columna = atributo.lstrip("_")

        if isinstance(valor, EntidadBase):
            registro[f"{columna}_id"] = valor.id

        elif isinstance(valor, date):
            registro[columna] = valor.isoformat()

        else:
            registro[columna] = valor

    return registro


# ==========================================================
# INTERFAZ DEL REPOSITORIO GENÉRICO
# ==========================================================

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


# ==========================================================
# REPOSITORIO GENÉRICO
# ==========================================================

class Repositorio(IRepositorio[T]):
    """Repositorio genérico con persistencia CSV y rollback."""

    def __init__(
        self,
        ruta_csv: Optional[str] = None,
    ) -> None:

        self._datos: Dict[int, T] = {}

        self._ruta_csv = (
            Path(ruta_csv)
            if ruta_csv is not None
            else None
        )

    def _guardar(self) -> None:
        """Guarda el estado actual del repositorio en CSV."""

        if self._ruta_csv is None:
            return

        registros = [
            convertir_entidad(entidad)
            for entidad in self._datos.values()
        ]

        if registros:
            columnas = list(registros[0].keys())

        else:
            columnas = ["id"]

            if self._ruta_csv.exists():
                with self._ruta_csv.open(
                    encoding="utf-8",
                    newline="",
                ) as archivo:

                    columnas = (
                        csv.DictReader(archivo).fieldnames
                        or ["id"]
                    )

        guardar_csv(
            self._ruta_csv,
            columnas,
            registros,
        )

    def _guardar_con_rollback(self, datos_anteriores) -> None:
        """Restaura el diccionario si falla la escritura."""

        try:
            self._guardar()

        except Exception:
            self._datos = datos_anteriores
            raise

    def crear(self, entidad: T) -> T:

        if entidad.id in self._datos:
            raise ValueError(
                f"Ya existe una entidad con ID {entidad.id}."
            )

        datos_anteriores = self._datos.copy()

        self._datos[entidad.id] = entidad

        self._guardar_con_rollback(datos_anteriores)

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

        datos_anteriores = self._datos.copy()

        self._datos[entidad.id] = entidad

        self._guardar_con_rollback(datos_anteriores)

        return entidad

    def eliminar(self, id: int) -> bool:

        if id not in self._datos:
            return False

        datos_anteriores = self._datos.copy()

        del self._datos[id]

        self._guardar_con_rollback(datos_anteriores)

        return True


# ==========================================================
# INTERFAZ DEL REPOSITORIO DE STOCK
# ==========================================================

class IRepositorioStock(abc.ABC):
    """Interfaz para administrar registros de stock."""

    @abc.abstractmethod
    def crear(self, stock: Stock) -> Stock:
        pass

    @abc.abstractmethod
    def leer_por_libro(
        self,
        libro_id: int,
    ) -> Optional[Stock]:
        pass

    @abc.abstractmethod
    def actualizar(self, stock: Stock) -> Stock:
        pass

    @abc.abstractmethod
    def eliminar(self, libro_id: int) -> bool:
        pass


# ==========================================================
# REPOSITORIO DE STOCK
# ==========================================================

class RepositorioStock(IRepositorioStock):
    """Repositorio de stock con persistencia CSV y rollback."""

    def __init__(
        self,
        ruta_csv: Optional[str] = None,
    ) -> None:

        self._datos: Dict[int, Stock] = {}

        self._ruta_csv = (
            Path(ruta_csv)
            if ruta_csv is not None
            else None
        )

    def _guardar(self) -> None:
        """Guarda los registros de stock en CSV."""

        if self._ruta_csv is None:
            return

        registros = [
            convertir_entidad(stock)
            for stock in self._datos.values()
        ]

        guardar_csv(
            self._ruta_csv,
            ["id", "libro_id", "cantidad"],
            registros,
        )

    def _guardar_con_rollback(self, datos_anteriores) -> None:
        """Restaura los datos si falla la escritura."""

        try:
            self._guardar()

        except Exception:
            self._datos = datos_anteriores
            raise

    def crear(self, stock: Stock) -> Stock:

        libro_id = stock.libro.id

        if libro_id in self._datos:
            raise ValueError(
                f"Ya existe stock para el libro {libro_id}."
            )

        datos_anteriores = self._datos.copy()

        self._datos[libro_id] = stock

        self._guardar_con_rollback(datos_anteriores)

        return stock

    def leer_por_libro(
        self,
        libro_id: int,
    ) -> Optional[Stock]:

        return self._datos.get(libro_id)

    def actualizar(self, stock: Stock) -> Stock:

        libro_id = stock.libro.id

        if libro_id not in self._datos:
            raise ValueError(
                f"No existe stock para el libro {libro_id}."
            )

        datos_anteriores = self._datos.copy()

        self._datos[libro_id] = stock

        self._guardar_con_rollback(datos_anteriores)

        return stock

    def eliminar(self, libro_id: int) -> bool:

        if libro_id not in self._datos:
            return False

        datos_anteriores = self._datos.copy()

        del self._datos[libro_id]

        self._guardar_con_rollback(datos_anteriores)

        return True


# ==========================================================
# INTERFAZ DEL REPOSITORIO DE COTIZACIONES
# ==========================================================

class IRepositorioCotizacionDolar(abc.ABC):
    """Interfaz para administrar cotizaciones."""

    @abc.abstractmethod
    def crear(
        self,
        cotizacion: CotizacionDolar,
    ) -> CotizacionDolar:
        pass

    @abc.abstractmethod
    def leer_por_tipo_y_fecha(
        self,
        tipo_id: int,
        fecha: date,
    ) -> Optional[CotizacionDolar]:
        pass

    @abc.abstractmethod
    def leer_historico_por_tipo(
        self,
        tipo_id: int,
    ) -> List[CotizacionDolar]:
        pass

    @abc.abstractmethod
    def actualizar(
        self,
        cotizacion: CotizacionDolar,
    ) -> CotizacionDolar:
        pass

    @abc.abstractmethod
    def eliminar(
        self,
        tipo_id: int,
        fecha: date,
    ) -> bool:
        pass


# ==========================================================
# REPOSITORIO DE COTIZACIONES
# ==========================================================

class RepositorioCotizacionDolar(
    IRepositorioCotizacionDolar
):
    """Repositorio de cotizaciones con persistencia CSV y rollback."""

    def __init__(
        self,
        ruta_csv: Optional[str] = None,
    ) -> None:

        self._datos: Dict[
            tuple[int, date],
            CotizacionDolar,
        ] = {}

        self._ruta_csv = (
            Path(ruta_csv)
            if ruta_csv is not None
            else None
        )

    def _guardar(self) -> None:
        """Guarda las cotizaciones en CSV."""

        if self._ruta_csv is None:
            return

        registros = [
            convertir_entidad(cotizacion)
            for cotizacion in self._datos.values()
        ]

        guardar_csv(
            self._ruta_csv,
            [
                "id",
                "tipo_cotizacion_id",
                "moneda_id",
                "fecha",
                "valor_compra",
                "valor_venta",
            ],
            registros,
        )

    def _guardar_con_rollback(self, datos_anteriores) -> None:
        """Restaura los datos si falla la escritura."""

        try:
            self._guardar()

        except Exception:
            self._datos = datos_anteriores
            raise

    def crear(
        self,
        cotizacion: CotizacionDolar,
    ) -> CotizacionDolar:

        clave = (
            cotizacion.tipo_cotizacion.id,
            cotizacion.fecha,
        )

        if clave in self._datos:
            raise ValueError(
                "Ya existe una cotización para ese tipo y fecha."
            )

        datos_anteriores = self._datos.copy()

        self._datos[clave] = cotizacion

        self._guardar_con_rollback(datos_anteriores)

        return cotizacion

    def leer_por_tipo_y_fecha(
        self,
        tipo_id: int,
        fecha: date,
    ) -> Optional[CotizacionDolar]:

        return self._datos.get((tipo_id, fecha))

    def leer_historico_por_tipo(
        self,
        tipo_id: int,
    ) -> List[CotizacionDolar]:

        return [
            cotizacion
            for (id_tipo, _), cotizacion
            in self._datos.items()
            if id_tipo == tipo_id
        ]

    def actualizar(
        self,
        cotizacion: CotizacionDolar,
    ) -> CotizacionDolar:

        clave = (
            cotizacion.tipo_cotizacion.id,
            cotizacion.fecha,
        )

        if clave not in self._datos:
            raise ValueError(
                "No existe la cotización que se quiere actualizar."
            )

        datos_anteriores = self._datos.copy()

        self._datos[clave] = cotizacion

        self._guardar_con_rollback(datos_anteriores)

        return cotizacion

    def eliminar(
        self,
        tipo_id: int,
        fecha: date,
    ) -> bool:

        clave = (tipo_id, fecha)

        if clave not in self._datos:
            return False

        datos_anteriores = self._datos.copy()

        del self._datos[clave]

        self._guardar_con_rollback(datos_anteriores)

        return True
