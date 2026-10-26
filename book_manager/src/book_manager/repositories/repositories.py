
"""
Repositorios del sistema Book Manager.

Implementa las operaciones de persistencia mediante SQLAlchemy,
utilizando los modelos ORM y el administrador de conexiones.
"""

from datetime import date
from typing import Generic, TypeVar

from sqlalchemy import select
from sqlalchemy.orm import DeclarativeBase, selectinload

from book_manager.database.connection import ConexionDB
from book_manager.models.models import (
    CotizacionDolarModel,
    StockModel,
)
from typing import Any


M = TypeVar("M", bound=DeclarativeBase)


class Repositorio(Generic[M]):
    """
    Repositorio genérico para operaciones CRUD con SQLAlchemy.

    Attributes:
        conexion (ConexionDB): Administrador de conexiones.
        modelo (type[M]): Clase del modelo ORM.
    """

    def __init__(
        self,
        conexion: ConexionDB,
        modelo: type[M],
    ) -> None:
        """Inicializa el repositorio con su conexión y modelo ORM."""
        self._conexion = conexion
        self._modelo = modelo

    def _opciones_relaciones(self) -> list[Any]:
        """
        Prepara la carga anticipada de relaciones del modelo ORM.

        Permite acceder a las relaciones después de cerrar
        la sesión de SQLAlchemy.
        """
        return [
            selectinload(getattr(self._modelo, relacion.key))
            for relacion in self._modelo.__mapper__.relationships
        ]

    def crear(self, entidad: M) -> M:
        """Inserta un registro en la base de datos."""
        with self._conexion.obtener_sesion() as sesion:
            if entidad.id is not None:
                if sesion.get(self._modelo, entidad.id) is not None:
                    raise ValueError(
                        f"Ya existe un registro con ID {entidad.id}."
                    )

            sesion.add(entidad)
            sesion.flush()
            sesion.refresh(entidad)

        return entidad

    def leer_por_id(self, id: int) -> M | None:
        """Obtiene un registro con sus relaciones cargadas."""
        with self._conexion.obtener_sesion() as sesion:
            consulta = (
                select(self._modelo)
                .options(*self._opciones_relaciones())
                .where(self._modelo.id == id)
            )

            return sesion.scalar(consulta)

    def leer_todos(self) -> list[M]:
        """Obtiene todos los registros con sus relaciones cargadas."""
        with self._conexion.obtener_sesion() as sesion:
            consulta = (
                select(self._modelo)
                .options(*self._opciones_relaciones())
                .order_by(self._modelo.id)
            )

            return list(sesion.scalars(consulta).all())

    def actualizar(self, entidad: M) -> M:
        """Actualiza un registro existente."""
        with self._conexion.obtener_sesion() as sesion:
            if entidad.id is None:
                raise ValueError(
                    "La entidad debe tener un ID para actualizarse."
                )

            if sesion.get(self._modelo, entidad.id) is None:
                raise ValueError(
                    f"No existe un registro con ID {entidad.id}."
                )

            entidad_actualizada = sesion.merge(entidad)
            sesion.flush()

            return entidad_actualizada

    def eliminar(self, id: int) -> bool:
        """Elimina un registro por su identificador."""
        with self._conexion.obtener_sesion() as sesion:
            entidad = sesion.get(self._modelo, id)

            if entidad is None:
                return False

            sesion.delete(entidad)
            sesion.flush()

            return True


class RepositorioStock(Repositorio[StockModel]):
    """
    Repositorio especializado en la gestión de stock.

    Permite consultar y administrar las existencias
    utilizando el identificador del libro.
    """

    def __init__(self, conexion: ConexionDB) -> None:
        """Inicializa el repositorio con el modelo de stock."""
        super().__init__(conexion, StockModel)

    def leer_por_libro(self, libro_id: int) -> StockModel | None:
        """Obtiene el stock correspondiente a un libro."""
        with self._conexion.obtener_sesion() as sesion:
            consulta = (
                select(StockModel)
                .options(*self._opciones_relaciones())
                .where(StockModel.libro_id == libro_id)
            )

            return sesion.scalar(consulta)

    def eliminar_por_libro(self, libro_id: int) -> bool:
        """Elimina el registro de stock correspondiente a un libro."""
        with self._conexion.obtener_sesion() as sesion:
            consulta = select(StockModel).where(
                StockModel.libro_id == libro_id
            )

            stock = sesion.scalar(consulta)

            if stock is None:
                return False

            sesion.delete(stock)
            sesion.flush()

            return True


class RepositorioCotizacionDolar(
    Repositorio[CotizacionDolarModel]
):
    """
    Repositorio especializado en cotizaciones del dólar.

    Permite consultar cotizaciones por tipo y fecha,
    además de recuperar su historial.
    """

    def __init__(self, conexion: ConexionDB) -> None:
        """Inicializa el repositorio con el modelo de cotizaciones."""
        super().__init__(conexion, CotizacionDolarModel)

    def leer_por_tipo_y_fecha(
        self,
        tipo_id: int,
        fecha: date,
    ) -> CotizacionDolarModel | None:
        """Obtiene una cotización por tipo y fecha."""
        with self._conexion.obtener_sesion() as sesion:
            consulta = (
                select(CotizacionDolarModel)
                .options(*self._opciones_relaciones())
                .where(
                    CotizacionDolarModel.tipo_cotizacion_id == tipo_id,
                    CotizacionDolarModel.fecha == fecha,
                )
            )

            return sesion.scalar(consulta)

    def leer_historico_por_tipo(
        self,
        tipo_id: int,
    ) -> list[CotizacionDolarModel]:
        """Obtiene el historial de cotizaciones de un tipo."""
        with self._conexion.obtener_sesion() as sesion:
            consulta = (
                select(CotizacionDolarModel)
                .options(*self._opciones_relaciones())
                .where(
                    CotizacionDolarModel.tipo_cotizacion_id == tipo_id
                )
                .order_by(CotizacionDolarModel.fecha)
            )

            return list(sesion.scalars(consulta).all())

    def eliminar_por_tipo_y_fecha(
        self,
        tipo_id: int,
        fecha: date,
    ) -> bool:
        """Elimina una cotización identificada por tipo y fecha."""
        with self._conexion.obtener_sesion() as sesion:
            consulta = select(CotizacionDolarModel).where(
                CotizacionDolarModel.tipo_cotizacion_id == tipo_id,
                CotizacionDolarModel.fecha == fecha,
            )

            cotizacion = sesion.scalar(consulta)

            if cotizacion is None:
                return False

            sesion.delete(cotizacion)
            sesion.flush()

            return True
