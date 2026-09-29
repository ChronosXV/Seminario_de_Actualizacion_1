
from typing import Callable

from book_manager.services.services import ServicioBase


class MenuCatalogos:
    """Menú CRUD genérico para entidades de catálogo."""

    def __init__(
        self,
        titulo: str,
        servicio: ServicioBase,
        crear_entidad: Callable,
        mostrar_entidad: Callable,
        modificar_entidad: Callable,
    ) -> None:
        self.titulo = titulo
        self.servicio = servicio
        self.crear_entidad = crear_entidad
        self.mostrar_entidad = mostrar_entidad
        self.modificar_entidad = modificar_entidad

    def ejecutar(self) -> None:
        """Ejecuta el menú CRUD del catálogo."""

        while True:
            print("\n" + "=" * 40)
            print(f"         GESTIÓN DE {self.titulo.upper()}")
            print("=" * 40)
            print(f"1. Listar {self.titulo.lower()}")
            print(f"2. Buscar {self.titulo.lower()}")
            print(f"3. Crear {self.titulo.lower()}")
            print(f"4. Modificar {self.titulo.lower()}")
            print(f"5. Eliminar {self.titulo.lower()}")
            print("0. Volver")
            print("=" * 40)

            opcion = input("Seleccione una opción: ").strip()

            if opcion == "1":
                self.listar()
            elif opcion == "2":
                self.buscar()
            elif opcion == "3":
                self.crear()
            elif opcion == "4":
                self.modificar()
            elif opcion == "5":
                self.eliminar()
            elif opcion == "0":
                break
            else:
                print("\nOpción inválida.")

    def listar(self) -> None:
        """Lista todas las entidades del catálogo."""

        entidades = self.servicio.obtener_todos()

        print(f"\n--- LISTADO DE {self.titulo.upper()} ---")

        if not entidades:
            print("No hay registros.")
            return

        for entidad in entidades:
            self.mostrar_entidad(entidad)

    def buscar(self) -> None:
        """Busca una entidad por ID."""

        try:
            entidad_id = int(input("Ingrese el ID: "))
            entidad = self.servicio.obtener_por_id(entidad_id)

            if entidad is None:
                print("\nRegistro no encontrado.")
                return

            print("\n--- REGISTRO ENCONTRADO ---")
            self.mostrar_entidad(entidad)

        except ValueError:
            print("\nEl ID debe ser numérico.")

    def crear(self) -> None:
        """Crea una nueva entidad."""

        try:
            entidad = self.crear_entidad()
            self.servicio.crear(entidad)
            print("\nRegistro creado correctamente.")

        except ValueError as error:
            print(f"\nError: {error}")

    def modificar(self) -> None:
        """Modifica una entidad existente."""

        try:
            entidad_id = int(input("Ingrese el ID a modificar: "))
            entidad = self.servicio.obtener_por_id(entidad_id)

            if entidad is None:
                print("\nRegistro no encontrado.")
                return

            entidad_modificada = self.modificar_entidad(entidad)
            self.servicio.actualizar(entidad_modificada)

            print("\nRegistro modificado correctamente.")

        except ValueError as error:
            print(f"\nError: {error}")

    def eliminar(self) -> None:
        """Elimina una entidad por ID."""

        try:
            entidad_id = int(input("Ingrese el ID a eliminar: "))
            entidad = self.servicio.obtener_por_id(entidad_id)

            if entidad is None:
                print("\nRegistro no encontrado.")
                return

            confirmacion = input(
                "¿Confirma la eliminación? (s/n): "
            ).strip().lower()

            if confirmacion == "s":
                self.servicio.eliminar(entidad_id)
                print("\nRegistro eliminado correctamente.")
            else:
                print("\nOperación cancelada.")

        except ValueError:
            print("\nEl ID debe ser numérico.")
