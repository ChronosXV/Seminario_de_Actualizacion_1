
from book_manager.preload_data.preload_data import cargar_datos

from book_manager.repositories.repositories import (
    Repositorio,
    RepositorioStock,
    RepositorioCotizacionDolar,
)

from book_manager.services.services import (
    ServicioBase,
    ServicioCotizacionDolar,
    ServicioLibro,
    ServicioPrecio,
    ServicioStock,
)

from book_manager.ui.console import Consola


def main(import_default_data: bool = True) -> None:
    """Inicializa y ejecuta el sistema Book Manager."""

    # -------------------------------------------
    # Inicialización de repositorios
    # -------------------------------------------

    if import_default_data:

        # Cargar los datos existentes desde CSV
        # y habilitar persistencia.
        repositorios = cargar_datos(
            persistir=True
        )

        print("Datos iniciales cargados correctamente.")

    else:

        # Crear repositorios vacíos, sin importar
        # los datos iniciales.
        repositorios = {
            "generos": Repositorio(),
            "editoriales": Repositorio(),
            "monedas": Repositorio(),
            "tipos_cotizacion": Repositorio(),
            "libros": Repositorio(),
            "precios": Repositorio(),
            "stock": RepositorioStock(),
            "cotizaciones": RepositorioCotizacionDolar(),
        }

        print("Sistema iniciado sin datos iniciales.")

    # -------------------------------------------
    # Creación de servicios
    # -------------------------------------------

    servicio_generos = ServicioBase(
        repositorios["generos"]
    )

    servicio_editoriales = ServicioBase(
        repositorios["editoriales"]
    )

    servicio_monedas = ServicioBase(
        repositorios["monedas"]
    )

    servicio_tipos_cotizacion = ServicioBase(
        repositorios["tipos_cotizacion"]
    )

    servicio_libros = ServicioLibro(
        repositorios["libros"]
    )

    servicio_precios = ServicioPrecio(
        repositorios["precios"]
    )

    servicio_stock = ServicioStock(
        repositorios["stock"]
    )

    servicio_cotizaciones = ServicioCotizacionDolar(
        repositorios["cotizaciones"]
    )

    # -------------------------------------------
    # Creación de la consola
    # -------------------------------------------

    consola = Consola(
        servicio_libros=servicio_libros,
        servicio_editoriales=servicio_editoriales,
        servicio_generos=servicio_generos,
        servicio_precios=servicio_precios,
        servicio_monedas=servicio_monedas,
        servicio_stock=servicio_stock,
        servicio_cotizaciones=servicio_cotizaciones,
        servicio_tipos_cotizacion=servicio_tipos_cotizacion,
    )

    # -------------------------------------------
    # Ejecución del sistema
    # -------------------------------------------

    consola.ejecutar()


if __name__ == "__main__":
    main()
