
"""
Interfaz de consola para la gestión de libros mediante modelos ORM.
"""

from sqlalchemy.exc import IntegrityError

from book_manager.models.models import LibroModel
from book_manager.services.services import ServicioBase, ServicioLibro


class MenuLibros:
    """Gestiona las operaciones CRUD de libros desde la consola."""

    def __init__(
        self,
        servicio_libros: ServicioLibro,
        servicio_editoriales: ServicioBase,
        servicio_generos: ServicioBase,
    ) -> None:
        """Inicializa los servicios necesarios."""
        self.servicio_libros = servicio_libros
        self.servicio_editoriales = servicio_editoriales
        self.servicio_generos = servicio_generos

    def ejecutar(self) -> None:
        """Ejecuta el menú de gestión de libros."""
        while True:
            self.mostrar_menu()
            opcion = input("Seleccione una opción: ").strip()

            if opcion == "1":
                self.listar_libros()
            elif opcion == "2":
                self.buscar_libro()
            elif opcion == "3":
                self.crear_libro()
            elif opcion == "4":
                self.modificar_libro()
            elif opcion == "5":
                self.eliminar_libro()
            elif opcion == "0":
                break
            else:
                print("\nOpción inválida. Intente nuevamente.")

    @staticmethod
    def mostrar_menu() -> None:
        """Muestra las opciones disponibles."""
        print("\n" + "=" * 40)
        print("         GESTIÓN DE LIBROS")
        print("=" * 40)
        print("1. Listar libros")
        print("2. Buscar libro")
        print("3. Crear libro")
        print("4. Modificar libro")
        print("5. Eliminar libro")
        print("0. Volver")
        print("=" * 40)

    @staticmethod
    def mostrar_libro(libro: LibroModel) -> None:
        """Muestra los datos de un libro y sus relaciones."""
        print(
            f"ID: {libro.id} | "
            f"ISBN: {libro.isbn} | "
            f"Título: {libro.titulo} | "
            f"Autor: {libro.autor} | "
            f"Editorial: {libro.editorial.nombre} | "
            f"Género: {libro.genero.nombre}"
        )

    def listar_libros(self) -> None:
        """Lista todos los libros registrados."""
        libros = self.servicio_libros.obtener_todos()

        if not libros:
            print("\nNo hay libros cargados.")
            return

        print("\n--- LISTADO DE LIBROS ---")

        for libro in libros:
            self.mostrar_libro(libro)

    def buscar_libro(self) -> None:
        """Busca un libro por su identificador."""
        try:
            libro_id = int(input("Ingrese el ID del libro: "))
            libro = self.servicio_libros.obtener_por_id(libro_id)

            if libro is None:
                print("\nLibro no encontrado.")
                return

            print("\n--- LIBRO ENCONTRADO ---")
            self.mostrar_libro(libro)

        except ValueError:
            print("\nEl ID debe ser un número entero.")

    def crear_libro(self) -> None:
        """Crea un libro utilizando claves foráneas ORM."""
        try:
            print("\n--- CREAR LIBRO ---")

            libro_id = int(input("ID: "))
            isbn = input("ISBN: ").strip()
            titulo = input("Título: ").strip()
            autor = input("Autor: ").strip()
            editorial_id = int(input("ID de la editorial: "))
            genero_id = int(input("ID del género: "))

            if self.servicio_editoriales.obtener_por_id(editorial_id) is None:
                print("\nLa editorial indicada no existe.")
                return

            if self.servicio_generos.obtener_por_id(genero_id) is None:
                print("\nEl género indicado no existe.")
                return

            libro = LibroModel(
                id=libro_id,
                isbn=isbn,
                titulo=titulo,
                autor=autor,
                editorial_id=editorial_id,
                genero_id=genero_id,
            )

            self.servicio_libros.crear(libro)
            print("\nLibro creado correctamente.")

        except (ValueError, IntegrityError) as error:
            print(f"\nError al crear el libro: {error}")

    def modificar_libro(self) -> None:
        """Modifica los datos de un libro existente."""
        try:
            print("\n--- MODIFICAR LIBRO ---")

            libro_id = int(input("ID del libro a modificar: "))
            libro_actual = self.servicio_libros.obtener_por_id(libro_id)

            if libro_actual is None:
                print("\nLibro no encontrado.")
                return

            isbn = input(f"ISBN [{libro_actual.isbn}]: ").strip()
            titulo = input(f"Título [{libro_actual.titulo}]: ").strip()
            autor = input(f"Autor [{libro_actual.autor}]: ").strip()

            libro_modificado = LibroModel(
                id=libro_actual.id,
                isbn=isbn or libro_actual.isbn,
                titulo=titulo or libro_actual.titulo,
                autor=autor or libro_actual.autor,
                editorial_id=libro_actual.editorial_id,
                genero_id=libro_actual.genero_id,
            )

            self.servicio_libros.actualizar(libro_modificado)
            print("\nLibro modificado correctamente.")

        except (ValueError, IntegrityError) as error:
            print(f"\nError al modificar el libro: {error}")

    def eliminar_libro(self) -> None:
        """Elimina un libro previa confirmación."""
        try:
            print("\n--- ELIMINAR LIBRO ---")

            libro_id = int(input("ID del libro a eliminar: "))
            libro = self.servicio_libros.obtener_por_id(libro_id)

            if libro is None:
                print("\nLibro no encontrado.")
                return

            print(f"\nLibro encontrado: {libro.titulo}")

            confirmacion = input(
                "¿Confirma la eliminación? (s/n): "
            ).strip().lower()

            if confirmacion != "s":
                print("\nEliminación cancelada.")
                return

            self.servicio_libros.eliminar(libro_id)
            print("\nLibro eliminado correctamente.")

        except (ValueError, IntegrityError) as error:
            print(f"\nError al eliminar el libro: {error}")
