
from book_manager.entities.entities import Libro
from book_manager.services.services import ServicioBase, ServicioLibro


class MenuLibros:
    """Interfaz de consola para la gestión de libros."""

    def __init__(
        self,
        servicio_libros: ServicioLibro,
        servicio_editoriales: ServicioBase,
        servicio_generos: ServicioBase,
    ) -> None:
        """Inicializa los servicios necesarios para gestionar libros."""

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
        """Muestra las opciones de gestión de libros."""

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

    def listar_libros(self) -> None:
        """Lista todos los libros."""

        libros = self.servicio_libros.obtener_todos()

        if not libros:
            print("\nNo hay libros cargados.")
            return

        print("\n--- LISTADO DE LIBROS ---")

        for libro in libros:
            print(
                f"ID: {libro.id} | "
                f"ISBN: {libro.isbn} | "
                f"Título: {libro.titulo} | "
                f"Autor: {libro.autor} | "
                f"Editorial: {libro.editorial.nombre} | "
                f"Género: {libro.genero.nombre}"
            )

    def buscar_libro(self) -> None:
        """Busca un libro por su ID."""

        try:
            libro_id = int(input("Ingrese el ID del libro: "))

            libro = self.servicio_libros.obtener_por_id(libro_id)

            if libro is None:
                print("\nLibro no encontrado.")
                return

            print("\n--- LIBRO ENCONTRADO ---")
            print(f"ID: {libro.id}")
            print(f"ISBN: {libro.isbn}")
            print(f"Título: {libro.titulo}")
            print(f"Autor: {libro.autor}")
            print(f"Editorial: {libro.editorial.nombre}")
            print(f"Género: {libro.genero.nombre}")

        except ValueError:
            print("\nEl ID debe ser un número entero.")

    def crear_libro(self) -> None:
        """Crea un nuevo libro."""

        try:
            print("\n--- CREAR LIBRO ---")

            libro_id = int(input("ID: "))
            isbn = input("ISBN: ").strip()
            titulo = input("Título: ").strip()
            autor = input("Autor: ").strip()
            editorial_id = int(input("ID de la editorial: "))
            genero_id = int(input("ID del género: "))

            editorial = self.servicio_editoriales.obtener_por_id(
                editorial_id
            )

            genero = self.servicio_generos.obtener_por_id(
                genero_id
            )

            if editorial is None:
                print("\nLa editorial indicada no existe.")
                return

            if genero is None:
                print("\nEl género indicado no existe.")
                return

            libro = Libro(
                id=libro_id,
                isbn=isbn,
                titulo=titulo,
                autor=autor,
                editorial=editorial,
                genero=genero,
            )

            self.servicio_libros.crear(libro)

            print("\nLibro creado correctamente.")

        except ValueError as error:
            print(f"\nError: {error}")

    def modificar_libro(self) -> None:
        """Modifica un libro existente."""

        try:
            print("\n--- MODIFICAR LIBRO ---")

            libro_id = int(input("ID del libro a modificar: "))

            libro_actual = self.servicio_libros.obtener_por_id(
                libro_id
            )

            if libro_actual is None:
                print("\nLibro no encontrado.")
                return

            isbn = input(
                f"ISBN [{libro_actual.isbn}]: "
            ).strip()

            titulo = input(
                f"Título [{libro_actual.titulo}]: "
            ).strip()

            autor = input(
                f"Autor [{libro_actual.autor}]: "
            ).strip()

            if not isbn:
                isbn = libro_actual.isbn

            if not titulo:
                titulo = libro_actual.titulo

            if not autor:
                autor = libro_actual.autor

            libro_modificado = Libro(
                id=libro_actual.id,
                isbn=isbn,
                titulo=titulo,
                autor=autor,
                editorial=libro_actual.editorial,
                genero=libro_actual.genero,
            )

            self.servicio_libros.actualizar(libro_modificado)

            print("\nLibro modificado correctamente.")

        except ValueError as error:
            print(f"\nError: {error}")

    def eliminar_libro(self) -> None:
        """Elimina un libro por su ID."""

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

        except ValueError:
            print("\nEl ID debe ser un número entero.")
