
from book_manager.preload_data.preload_data import cargar_datos
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
    # Carga de repositorios y datos iniciales
    # -------------------------------------------
    repositorios = cargar_datos()

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
