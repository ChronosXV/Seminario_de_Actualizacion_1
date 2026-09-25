# Menú de gestión de precios

from book_manager.entities.entities import Precio
from book_manager.services.services import ServicioBase, ServicioPrecio


class MenuPrecios:
    """Interfaz de consola para la gestión de precios."""

    def __init__(
        self,
        servicio_precios: ServicioPrecio,
        servicio_libros: ServicioBase,
        servicio_monedas: ServicioBase,
    ) -> None:
        """Inicializa los servicios necesarios para gestionar precios."""

        self.servicio_precios = servicio_precios
        self.servicio_libros = servicio_libros
        self.servicio_monedas = servicio_monedas

    def ejecutar(self) -> None:
        """Ejecuta el menú de gestión de precios."""

        while True:
            self.mostrar_menu()

            opcion = input("Seleccione una opción: ").strip()

            if opcion == "1":
                self.listar_precios()
            elif opcion == "2":
                self.buscar_precio()
            elif opcion == "3":
                self.crear_precio()
            elif opcion == "4":
                self.modificar_precio()
            elif opcion == "5":
                self.eliminar_precio()
            elif opcion == "0":
                break
            else:
                print("\nOpción inválida. Intente nuevamente.")

    @staticmethod
    def mostrar_menu() -> None:
        """Muestra las opciones de gestión de precios."""

        print("\n" + "=" * 40)
        print("         GESTIÓN DE PRECIOS")
        print("=" * 40)
        print("1. Listar precios")
        print("2. Buscar precio")
        print("3. Crear precio")
        print("4. Modificar precio")
        print("5. Eliminar precio")
        print("0. Volver")
        print("=" * 40)

    def listar_precios(self) -> None:
        """Lista todos los precios."""

        precios = self.servicio_precios.obtener_todos()

        if not precios:
            print("\nNo hay precios cargados.")
            return

        print("\n--- LISTADO DE PRECIOS ---")

        for precio in precios:
            print(
                f"ID: {precio.id} | "
                f"Libro: {precio.libro.titulo} | "
                f"Moneda: {precio.moneda.codigo} | "
                f"Valor: {precio.moneda.simbolo}{precio.valor:.2f}"
            )

    def buscar_precio(self) -> None:
        """Busca un precio por su ID."""

        try:
            precio_id = int(input("Ingrese el ID del precio: "))

            precio = self.servicio_precios.obtener_por_id(precio_id)

            if precio is None:
                print("\nPrecio no encontrado.")
                return

            print("\n--- PRECIO ENCONTRADO ---")
            print(f"ID: {precio.id}")
            print(f"Libro: {precio.libro.titulo}")
            print(f"Moneda: {precio.moneda.nombre}")
            print(f"Valor: {precio.moneda.simbolo}{precio.valor:.2f}")

        except ValueError:
            print("\nEl ID debe ser un número entero.")

    def crear_precio(self) -> None:
        """Crea un nuevo precio."""

        try:
            print("\n--- CREAR PRECIO ---")

            precio_id = int(input("ID: "))
            libro_id = int(input("ID del libro: "))
            moneda_id = int(input("ID de la moneda: "))
            valor = float(input("Valor: "))

            libro = self.servicio_libros.obtener_por_id(libro_id)
            moneda = self.servicio_monedas.obtener_por_id(moneda_id)

            if libro is None:
                print("\nEl libro indicado no existe.")
                return

            if moneda is None:
                print("\nLa moneda indicada no existe.")
                return

            precio = Precio(
                id=precio_id,
                libro=libro,
                moneda=moneda,
                valor=valor,
            )

            self.servicio_precios.crear(precio)

            print("\nPrecio creado correctamente.")

        except ValueError as error:
            print(f"\nError: {error}")

    def modificar_precio(self) -> None:
        """Modifica un precio existente."""

        try:
            print("\n--- MODIFICAR PRECIO ---")

            precio_id = int(input("ID del precio a modificar: "))

            precio_actual = self.servicio_precios.obtener_por_id(
                precio_id
            )

            if precio_actual is None:
                print("\nPrecio no encontrado.")
                return

            valor_ingresado = input(
                f"Valor [{precio_actual.valor}]: "
            ).strip()

            if valor_ingresado:
                valor = float(valor_ingresado)
            else:
                valor = precio_actual.valor

            precio_modificado = Precio(
                id=precio_actual.id,
                libro=precio_actual.libro,
                moneda=precio_actual.moneda,
                valor=valor,
            )

            self.servicio_precios.actualizar(precio_modificado)

            print("\nPrecio modificado correctamente.")

        except ValueError as error:
            print(f"\nError: {error}")

    def eliminar_precio(self) -> None:
        """Elimina un precio por su ID."""

        try:
            print("\n--- ELIMINAR PRECIO ---")

            precio_id = int(input("ID del precio a eliminar: "))

            precio = self.servicio_precios.obtener_por_id(precio_id)

            if precio is None:
                print("\nPrecio no encontrado.")
                return

            print(
                f"\nPrecio encontrado: "
                f"{precio.libro.titulo} - "
                f"{precio.moneda.simbolo}{precio.valor:.2f}"
            )

            confirmacion = input(
                "¿Confirma la eliminación? (s/n): "
            ).strip().lower()

            if confirmacion != "s":
                print("\nEliminación cancelada.")
                return

            self.servicio_precios.eliminar(precio_id)

            print("\nPrecio eliminado correctamente.")

        except ValueError:
            print("\nEl ID debe ser un número entero.")