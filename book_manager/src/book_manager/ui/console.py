
from book_manager.ui.menus.catalogos_config import (
    crear_editorial,
    crear_genero,
    crear_moneda,
    crear_tipo_cotizacion,
    modificar_editorial,
    modificar_genero,
    modificar_moneda,
    modificar_tipo_cotizacion,
    mostrar_editorial,
    mostrar_genero,
    mostrar_moneda,
    mostrar_tipo_cotizacion,
)
from book_manager.ui.menus.menu_catalogos import MenuCatalogos
from book_manager.ui.menus.menu_cotizaciones import MenuCotizaciones
from book_manager.ui.menus.menu_libros import MenuLibros
from book_manager.ui.menus.menu_precios import MenuPrecios
from book_manager.ui.menus.menu_stock import MenuStock


class Consola:
    """Interfaz principal de usuario para Book Manager."""

    def __init__(
        self,
        servicio_libros,
        servicio_editoriales,
        servicio_generos,
        servicio_precios,
        servicio_monedas,
        servicio_stock,
        servicio_cotizaciones,
        servicio_tipos_cotizacion,
    ) -> None:

        # Menús principales
        self.menu_libros = MenuLibros(
            servicio_libros,
            servicio_editoriales,
            servicio_generos,
        )

        self.menu_precios = MenuPrecios(
            servicio_precios,
            servicio_libros,
            servicio_monedas,
        )

        self.menu_stock = MenuStock(
            servicio_stock,
            servicio_libros,
        )

        self.menu_cotizaciones = MenuCotizaciones(
            servicio_cotizaciones,
            servicio_tipos_cotizacion,
            servicio_monedas,
        )

        # Menús de catálogos
        self.menu_generos = MenuCatalogos(
            titulo="Géneros",
            servicio=servicio_generos,
            crear_entidad=crear_genero,
            mostrar_entidad=mostrar_genero,
            modificar_entidad=modificar_genero,
        )

        self.menu_editoriales = MenuCatalogos(
            titulo="Editoriales",
            servicio=servicio_editoriales,
            crear_entidad=crear_editorial,
            mostrar_entidad=mostrar_editorial,
            modificar_entidad=modificar_editorial,
        )

        self.menu_monedas = MenuCatalogos(
            titulo="Monedas",
            servicio=servicio_monedas,
            crear_entidad=crear_moneda,
            mostrar_entidad=mostrar_moneda,
            modificar_entidad=modificar_moneda,
        )

        self.menu_tipos_cotizacion = MenuCatalogos(
            titulo="Tipos de cotización",
            servicio=servicio_tipos_cotizacion,
            crear_entidad=crear_tipo_cotizacion,
            mostrar_entidad=mostrar_tipo_cotizacion,
            modificar_entidad=modificar_tipo_cotizacion,
        )

    def ejecutar(self) -> None:
        """Ejecuta el menú principal de la aplicación."""

        while True:
            self.mostrar_menu_principal()

            opcion = input("Seleccione una opción: ").strip()

            if opcion == "1":
                self.menu_libros.ejecutar()

            elif opcion == "2":
                self.menu_precios.ejecutar()

            elif opcion == "3":
                self.menu_stock.ejecutar()

            elif opcion == "4":
                self.menu_cotizaciones.ejecutar()

            elif opcion == "5":
                self.menu_generos.ejecutar()

            elif opcion == "6":
                self.menu_editoriales.ejecutar()

            elif opcion == "7":
                self.menu_monedas.ejecutar()

            elif opcion == "8":
                self.menu_tipos_cotizacion.ejecutar()

            elif opcion == "0":
                print("\nSaliendo de Book Manager...")
                break

            else:
                print("\nOpción inválida. Intente nuevamente.")

    @staticmethod
    def mostrar_menu_principal() -> None:
        """Muestra las opciones principales del sistema."""

        print("\n" + "=" * 45)
        print("              BOOK MANAGER")
        print("=" * 45)
        print("1. Gestión de libros")
        print("2. Gestión de precios")
        print("3. Gestión de stock")
        print("4. Gestión de cotizaciones")
        print("5. Gestión de géneros")
        print("6. Gestión de editoriales")
        print("7. Gestión de monedas")
        print("8. Gestión de tipos de cotización")
        print("0. Salir")
        print("=" * 45)
