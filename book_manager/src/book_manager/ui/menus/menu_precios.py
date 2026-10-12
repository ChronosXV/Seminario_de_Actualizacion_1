
"""
Interfaz de consola para la gestión de precios con SQLAlchemy.
"""

from decimal import Decimal, InvalidOperation

from sqlalchemy.exc import IntegrityError

from book_manager.models.models import PrecioModel
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

    @staticmethod
    def mostrar_precio(precio: PrecioModel) -> None:
        """Muestra un precio junto con sus relaciones."""

        print(
            f"ID: {precio.id} | "
            f"Libro: {precio.libro.titulo} | "
            f"Moneda: {precio.moneda.codigo} | "
            f"Valor: {precio.moneda.simbolo}{precio.valor:.2f}"
        )

    @staticmethod
    def solicitar_valor(mensaje: str) -> Decimal:
        """Solicita un importe positivo con precisión decimal."""

        texto = input(mensaje).strip().replace(",", ".")

        try:
            valor = Decimal(texto)
        except InvalidOperation as error:
            raise ValueError(
                "El valor debe ser un número válido."
            ) from error

        if not valor.is_finite() or valor <= 0:
            raise ValueError(
                "El precio debe ser un número finito mayor que cero."
            )

        if valor.as_tuple().exponent < -2:
            raise ValueError(
                "El precio puede tener como máximo dos decimales."
            )

        if valor > Decimal("9999999999999.99"):
            raise ValueError(
                "El precio supera el máximo permitido."
            )

        return valor

    def listar_precios(self) -> None:
        """Lista todos los precios."""

        precios = self.servicio_precios.obtener_todos()

        if not precios:
            print("\nNo hay precios cargados.")
            return

        print("\n--- LISTADO DE PRECIOS ---")

        for precio in precios:
            self.mostrar_precio(precio)

    def buscar_precio(self) -> None:
        """Busca un precio por su ID."""

        try:
            precio_id = int(input("Ingrese el ID del precio: "))

            precio = self.servicio_precios.obtener_por_id(precio_id)

            if precio is None:
                print("\nPrecio no encontrado.")
                return

            print("\n--- PRECIO ENCONTRADO ---")

            self.mostrar_precio(precio)

        except ValueError:
            print("\nEl ID debe ser un número entero.")

    def crear_precio(self) -> None:
        """Crea un nuevo precio mediante claves foráneas ORM."""

        try:
            print("\n--- CREAR PRECIO ---")

            precio_id = int(input("ID: "))
            libro_id = int(input("ID del libro: "))
            moneda_id = int(input("ID de la moneda: "))

            valor = self.solicitar_valor("Valor: ")

            libro = self.servicio_libros.obtener_por_id(libro_id)
            moneda = self.servicio_monedas.obtener_por_id(moneda_id)

            if libro is None:
                print("\nEl libro indicado no existe.")
                return

            if moneda is None:
                print("\nLa moneda indicada no existe.")
                return

            precio = PrecioModel(
                id=precio_id,
                libro_id=libro_id,
                moneda_id=moneda_id,
                valor=valor,
            )

            self.servicio_precios.crear(precio)

            print("\nPrecio creado correctamente.")

        except (ValueError, IntegrityError) as error:
            print(f"\nError al crear el precio: {error}")

    def modificar_precio(self) -> None:
        """Modifica el importe de un precio existente."""

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
                # Reutilizamos la validación del importe.
                # Se utiliza el texto ya ingresado, sin pedirlo dos veces.
                texto = valor_ingresado.replace(",", ".")

                try:
                    valor = Decimal(texto)
                except InvalidOperation as error:
                    raise ValueError(
                        "El valor debe ser un número válido."
                    ) from error

                if not valor.is_finite() or valor <= 0:
                    raise ValueError(
                        "El precio debe ser mayor que cero."
                    )

                if valor.as_tuple().exponent < -2:
                    raise ValueError(
                        "El precio puede tener como máximo dos decimales."
                    )

                if valor > Decimal("9999999999999.99"):
                    raise ValueError(
                        "El precio supera el máximo permitido."
                    )
            else:
                valor = precio_actual.valor

            precio_modificado = PrecioModel(
                id=precio_actual.id,
                libro_id=precio_actual.libro_id,
                moneda_id=precio_actual.moneda_id,
                valor=valor,
            )

            self.servicio_precios.actualizar(precio_modificado)

            print("\nPrecio modificado correctamente.")

        except (ValueError, IntegrityError) as error:
            print(f"\nError al modificar el precio: {error}")

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

        except (ValueError, IntegrityError) as error:
            print(f"\nError al eliminar el precio: {error}")
