# Creación de la consola/interfaz de interacción

from book_manager.ui.menus.menu_cotizaciones import MenuCotizaciones
from book_manager.ui.menus.menu_libros import MenuLibros
from book_manager.ui.menus.menu_precios import MenuPrecios
from book_manager.ui.menus.menu_stock import MenuStock


class Consola:
    """Interfaz principal de usuario por consola para Book Manager."""

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
        """Inicializa los menús de la aplicación."""

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

            elif opcion == "0":
                print("\nSaliendo de Book Manager...")
                break

            else:
                print("\nOpción inválida. Intente nuevamente.")

    @staticmethod
    def mostrar_menu_principal() -> None:
        """Muestra las opciones principales."""

        print("\n" + "=" * 40)
        print("  BOOK MANAGER")
        print("=" * 40)
        print("1. Gestión de libros")
        print("2. Gestión de precios")
        print("3. Gestión de stock")
        print("4. Gestión de cotizaciones")
        print("0. Salir")
        print("=" * 40)