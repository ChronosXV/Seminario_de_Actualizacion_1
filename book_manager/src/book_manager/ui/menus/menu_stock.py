# Creacion del menu de stock

from book_manager.entities.entities import Stock
from book_manager.services.services import ServicioBase, ServicioStock


class MenuStock:
    """Interfaz de consola para la gestión de stock."""

    def __init__(
        self,
        servicio_stock: ServicioStock,
        servicio_libros: ServicioBase,
    ) -> None:
        """Inicializa los servicios necesarios para gestionar stock."""

        self.servicio_stock = servicio_stock
        self.servicio_libros = servicio_libros

    def ejecutar(self) -> None:
        """Ejecuta el menú de gestión de stock."""

        while True:
            self.mostrar_menu()

            opcion = input("Seleccione una opción: ").strip()

            if opcion == "1":
                self.buscar_stock()
            elif opcion == "2":
                self.crear_stock()
            elif opcion == "3":
                self.modificar_stock()
            elif opcion == "4":
                self.eliminar_stock()
            elif opcion == "0":
                break
            else:
                print("\nOpción inválida. Intente nuevamente.")

    @staticmethod
    def mostrar_menu() -> None:
        """Muestra las opciones de gestión de stock."""

        print("\n" + "=" * 40)
        print("          GESTIÓN DE STOCK")
        print("=" * 40)
        print("1. Buscar stock por libro")
        print("2. Crear stock")
        print("3. Modificar stock")
        print("4. Eliminar stock")
        print("0. Volver")
        print("=" * 40)

    def buscar_stock(self) -> None:
        """Busca el stock correspondiente a un libro."""

        try:
            libro_id = int(input("Ingrese el ID del libro: "))

            stock = self.servicio_stock.obtener_por_libro(libro_id)

            if stock is None:
                print("\nNo se encontró stock para ese libro.")
                return

            print("\n--- STOCK ENCONTRADO ---")
            print(f"Libro ID: {stock.libro.id}")
            print(f"Título: {stock.libro.titulo}")
            print(f"Cantidad: {stock.cantidad}")

        except ValueError:
            print("\nEl ID debe ser un número entero.")

    def crear_stock(self) -> None:
        """Crea un registro de stock para un libro."""

        try:
            print("\n--- CREAR STOCK ---")

            libro_id = int(input("ID del libro: "))
            cantidad = int(input("Cantidad: "))

            libro = self.servicio_libros.obtener_por_id(libro_id)

            if libro is None:
                print("\nEl libro indicado no existe.")
                return

            stock = Stock(
                libro=libro,
                cantidad=cantidad,
            )

            self.servicio_stock.crear(stock)

            print("\nStock creado correctamente.")

        except ValueError as error:
            print(f"\nError: {error}")

    def modificar_stock(self) -> None:
        """Modifica el stock de un libro."""

        try:
            print("\n--- MODIFICAR STOCK ---")

            libro_id = int(input("ID del libro: "))

            stock_actual = self.servicio_stock.obtener_por_libro(
                libro_id
            )

            if stock_actual is None:
                print("\nNo se encontró stock para ese libro.")
                return

            print(f"Libro: {stock_actual.libro.titulo}")
            print(f"Cantidad actual: {stock_actual.cantidad}")

            cantidad = int(input("Nueva cantidad: "))

            stock_modificado = Stock(
                libro=stock_actual.libro,
                cantidad=cantidad,
            )

            self.servicio_stock.actualizar(stock_modificado)

            print("\nStock modificado correctamente.")

        except ValueError as error:
            print(f"\nError: {error}")

    def eliminar_stock(self) -> None:
        """Elimina el stock correspondiente a un libro."""

        try:
            print("\n--- ELIMINAR STOCK ---")

            libro_id = int(input("ID del libro: "))

            stock = self.servicio_stock.obtener_por_libro(libro_id)

            if stock is None:
                print("\nNo se encontró stock para ese libro.")
                return

            print(f"\nLibro: {stock.libro.titulo}")
            print(f"Cantidad actual: {stock.cantidad}")

            confirmacion = input(
                "¿Confirma la eliminación? (s/n): "
            ).strip().lower()

            if confirmacion != "s":
                print("\nEliminación cancelada.")
                return

            self.servicio_stock.eliminar(libro_id)

            print("\nStock eliminado correctamente.")

        except ValueError:
            print("\nEl ID debe ser un número entero.")