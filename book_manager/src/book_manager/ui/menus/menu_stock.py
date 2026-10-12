
"""
Interfaz de consola para la gestión de stock con SQLAlchemy.
"""

from sqlalchemy.exc import IntegrityError

from book_manager.models.models import StockModel
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
                self.listar_stock()
            elif opcion == "2":
                self.buscar_stock()
            elif opcion == "3":
                self.crear_stock()
            elif opcion == "4":
                self.modificar_stock()
            elif opcion == "5":
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
        print("1. Listar stock")
        print("2. Buscar stock por libro")
        print("3. Crear stock")
        print("4. Modificar stock")
        print("5. Eliminar stock")
        print("0. Volver")
        print("=" * 40)

    @staticmethod
    def mostrar_stock(stock: StockModel) -> None:
        """Muestra los datos del stock y del libro relacionado."""
        print(f"Stock ID: {stock.id}")
        print(f"Libro ID: {stock.libro_id}")
        print(f"Título: {stock.libro.titulo}")
        print(f"Cantidad: {stock.cantidad}")

    @staticmethod
    def validar_cantidad(cantidad: int) -> None:
        """Verifica que la cantidad de stock no sea negativa."""
        if cantidad < 0:
            raise ValueError(
                "La cantidad de stock no puede ser negativa."
            )

    def listar_stock(self) -> None:
        """Lista todos los registros de stock."""

        print("\n--- LISTADO DE STOCK ---")

        stocks = self.servicio_stock.listar()

        if not stocks:
            print("\nNo hay registros de stock.")
            return

        for stock in stocks:
            print("\n" + "-" * 40)
            self.mostrar_stock(stock)

        print("\n" + "-" * 40)
        print(f"Total de registros: {len(stocks)}")

    def buscar_stock(self) -> None:
        """Busca el stock correspondiente a un libro."""
        try:
            libro_id = int(input("Ingrese el ID del libro: "))
            stock = self.servicio_stock.obtener_por_libro(libro_id)

            if stock is None:
                print("\nNo se encontró stock para ese libro.")
                return

            print("\n--- STOCK ENCONTRADO ---")
            self.mostrar_stock(stock)

        except ValueError as error:
            print(f"\nError: {error}")

    def crear_stock(self) -> None:
        """Crea un registro de stock para un libro."""
        try:
            print("\n--- CREAR STOCK ---")

            stock_id = int(input("ID del stock: "))
            libro_id = int(input("ID del libro: "))
            cantidad = int(input("Cantidad: "))

            self.validar_cantidad(cantidad)

            libro = self.servicio_libros.obtener_por_id(libro_id)

            if libro is None:
                print("\nEl libro indicado no existe.")
                return

            if self.servicio_stock.obtener_por_libro(libro_id) is not None:
                print("\nEl libro ya tiene un registro de stock.")
                return

            stock = StockModel(
                id=stock_id,
                libro_id=libro_id,
                cantidad=cantidad,
            )

            self.servicio_stock.crear(stock)
            print("\nStock creado correctamente.")

        except (ValueError, IntegrityError) as error:
            print(f"\nError al crear el stock: {error}")

    def modificar_stock(self) -> None:
        """Modifica la cantidad de stock de un libro."""
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
            self.validar_cantidad(cantidad)

            stock_modificado = StockModel(
                id=stock_actual.id,
                libro_id=stock_actual.libro_id,
                cantidad=cantidad,
            )

            self.servicio_stock.actualizar(stock_modificado)
            print("\nStock modificado correctamente.")

        except (ValueError, IntegrityError) as error:
            print(f"\nError al modificar el stock: {error}")

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

            eliminado = self.servicio_stock.eliminar(libro_id)

            if eliminado:
                print("\nStock eliminado correctamente.")
            else:
                print("\nNo se encontró stock para eliminar.")

        except (ValueError, IntegrityError) as error:
            print(f"\nError al eliminar el stock: {error}")
