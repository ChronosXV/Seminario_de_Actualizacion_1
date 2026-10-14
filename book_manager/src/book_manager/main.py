
"""
Punto de entrada del sistema Book Manager.

Inicializa SQLite, los repositorios, los servicios
y la interfaz de consola.
"""

from book_manager.database.connection import ConexionDB

from book_manager.models.models import (
    Base,
    GeneroModel,
    EditorialModel,
    MonedaModel,
    TipoCotizacionModel,
    LibroModel,
    PrecioModel,
)

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
from pathlib import Path

def main(import_default_data: bool = False) -> None:
    """
    Inicializa y ejecuta Book Manager.

    Args:
        import_default_data: Si es True, importa los datos
            iniciales desde los archivos CSV cuando la
            base de datos está vacía.
    """

    # -------------------------------------------
    # 1. Inicialización de base de datos
    # -------------------------------------------

    conexion = ConexionDB()

    Base.metadata.create_all(conexion.engine)

    print(f"Base de datos utilizada: {conexion.engine.dialect.name}")

    # -------------------------------------------
    # 2. Carga opcional de datos iniciales
    # -------------------------------------------

    if import_default_data:
        cargar_datos(conexion)

    # -------------------------------------------
    # 3. Inicialización de repositorios
    # -------------------------------------------

    repositorios = {
        "generos": Repositorio(conexion, GeneroModel),
        "editoriales": Repositorio(conexion, EditorialModel),
        "monedas": Repositorio(conexion, MonedaModel),
        "tipos_cotizacion": Repositorio(
            conexion, TipoCotizacionModel
        ),
        "libros": Repositorio(conexion, LibroModel),
        "precios": Repositorio(conexion, PrecioModel),
        "stock": RepositorioStock(conexion),
        "cotizaciones": RepositorioCotizacionDolar(conexion),
    }

    # -------------------------------------------
    # 4. Inicialización de servicios
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
    # 5. Inicialización de la consola
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
    # 6. Ejecución
    # -------------------------------------------

    consola.ejecutar()


if __name__ == "__main__":
    main()
