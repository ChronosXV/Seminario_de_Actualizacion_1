
"""
Decorador para auditar operaciones de Book Manager.

Registra la acción, fecha y detalles de cada operación
en la tabla auditoria de la base de datos.
"""

from datetime import datetime
from functools import wraps

from book_manager.database.connection import ConexionDB
from book_manager.models.models import AuditoriaModel


def registrar_auditoria(accion: str, detalles: str) -> None:
    """Guarda un registro de auditoría en la base de datos."""

    conexion = ConexionDB()

    with conexion.obtener_sesion() as sesion:
        registro = AuditoriaModel(
            accion=accion,
            fecha=datetime.now(),
            detalles=detalles,
        )

        sesion.add(registro)


def auditar(accion: str):
    """
    Decorador que registra el resultado de una operación.

    Si la operación falla, registra el error y vuelve
    a lanzar la excepción original.
    """

    def decorador(funcion):

        @wraps(funcion)
        def envoltura(*args, **kwargs):

            try:
                resultado = funcion(*args, **kwargs)

            except Exception as error:

                try:
                    registrar_auditoria(
                        accion=accion,
                        detalles=(
                            f"Error en {funcion.__qualname__}: "
                            f"{type(error).__name__}: {error}"
                        ),
                    )
                except Exception as error_auditoria:
                    print(
                        "No se pudo registrar la auditoría: "
                        f"{error_auditoria}"
                    )

                raise

            registrar_auditoria(
                accion=accion,
                detalles=(
                    f"Operación {funcion.__qualname__} "
                    "completada correctamente."
                ),
            )

            return resultado

        return envoltura

    return decorador
