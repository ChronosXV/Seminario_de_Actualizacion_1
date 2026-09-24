
from datetime import datetime

from book_manager.entities.entities import CotizacionDolar
from book_manager.services.services import (
    ServicioBase,
    ServicioCotizacionDolar,
)


class MenuCotizaciones:
    """Interfaz de consola para la gestión de cotizaciones."""

    def __init__(
        self,
        servicio_cotizaciones: ServicioCotizacionDolar,
        servicio_tipos_cotizacion: ServicioBase,
        servicio_monedas: ServicioBase,
    ) -> None:
        """Inicializa los servicios necesarios."""

        self.servicio_cotizaciones = servicio_cotizaciones
        self.servicio_tipos_cotizacion = servicio_tipos_cotizacion
        self.servicio_monedas = servicio_monedas

    def ejecutar(self) -> None:
        """Ejecuta el menú de gestión de cotizaciones."""

        while True:
            self.mostrar_menu()

            opcion = input("Seleccione una opción: ").strip()

            if opcion == "1":
                self.buscar_cotizacion()
            elif opcion == "2":
                self.ver_historico()
            elif opcion == "3":
                self.crear_cotizacion()
            elif opcion == "4":
                self.modificar_cotizacion()
            elif opcion == "5":
                self.eliminar_cotizacion()
            elif opcion == "0":
                break
            else:
                print("\nOpción inválida. Intente nuevamente.")

    @staticmethod
    def mostrar_menu() -> None:
        """Muestra las opciones de gestión de cotizaciones."""

        print("\n" + "=" * 40)
        print("       GESTIÓN DE COTIZACIONES")
        print("=" * 40)
        print("1. Buscar cotización")
        print("2. Ver histórico por tipo")
        print("3. Crear cotización")
        print("4. Modificar cotización")
        print("5. Eliminar cotización")
        print("0. Volver")
        print("=" * 40)

    @staticmethod
    def leer_fecha():
        """Solicita una fecha con formato AAAA-MM-DD."""

        fecha_texto = input("Fecha (AAAA-MM-DD): ").strip()

        return datetime.strptime(
            fecha_texto,
            "%Y-%m-%d",
        ).date()

    def buscar_cotizacion(self) -> None:
        """Busca una cotización por tipo y fecha."""

        try:
            tipo_id = int(
                input("ID del tipo de cotización: ")
            )
            fecha = self.leer_fecha()

            cotizacion = (
                self.servicio_cotizaciones.obtener_por_tipo_y_fecha(
                    tipo_id,
                    fecha,
                )
            )

            if cotizacion is None:
                print("\nCotización no encontrada.")
                return

            self.mostrar_cotizacion(cotizacion)

        except ValueError:
            print("\nDatos inválidos. Verifique ID y fecha.")

    def ver_historico(self) -> None:
        """Muestra el histórico de un tipo de cotización."""

        try:
            tipo_id = int(
                input("ID del tipo de cotización: ")
            )

            cotizaciones = (
                self.servicio_cotizaciones.obtener_historico(
                    tipo_id
                )
            )

            if not cotizaciones:
                print(
                    "\nNo hay cotizaciones para ese tipo."
                )
                return

            print("\n--- HISTÓRICO DE COTIZACIONES ---")

            for cotizacion in cotizaciones:
                print(
                    f"Fecha: {cotizacion.fecha} | "
                    f"Tipo: "
                    f"{cotizacion.tipo_cotizacion.nombre} | "
                    f"Compra: {cotizacion.valor_compra:.2f} | "
                    f"Venta: {cotizacion.valor_venta:.2f}"
                )

        except ValueError:
            print("\nEl ID debe ser un número entero.")

    def crear_cotizacion(self) -> None:
        """Crea una nueva cotización."""

        try:
            print("\n--- CREAR COTIZACIÓN ---")

            cotizacion_id = int(input("ID: "))
            tipo_id = int(
                input("ID del tipo de cotización: ")
            )
            moneda_id = int(input("ID de la moneda: "))
            fecha = self.leer_fecha()
            valor_compra = float(
                input("Valor de compra: ")
            )
            valor_venta = float(
                input("Valor de venta: ")
            )

            tipo_cotizacion = (
                self.servicio_tipos_cotizacion.obtener_por_id(
                    tipo_id
                )
            )

            moneda = self.servicio_monedas.obtener_por_id(
                moneda_id
            )

            if tipo_cotizacion is None:
                print(
                    "\nEl tipo de cotización no existe."
                )
                return

            if moneda is None:
                print("\nLa moneda indicada no existe.")
                return

            cotizacion = CotizacionDolar(
                id=cotizacion_id,
                tipo_cotizacion=tipo_cotizacion,
                moneda=moneda,
                fecha=fecha,
                valor_compra=valor_compra,
                valor_venta=valor_venta,
            )

            self.servicio_cotizaciones.crear(
                cotizacion
            )

            print("\nCotización creada correctamente.")

        except ValueError as error:
            print(f"\nError: {error}")

    def modificar_cotizacion(self) -> None:
        """Modifica una cotización existente."""

        try:
            print("\n--- MODIFICAR COTIZACIÓN ---")

            tipo_id = int(
                input("ID del tipo de cotización: ")
            )
            fecha = self.leer_fecha()

            cotizacion_actual = (
                self.servicio_cotizaciones.obtener_por_tipo_y_fecha(
                    tipo_id,
                    fecha,
                )
            )

            if cotizacion_actual is None:
                print("\nCotización no encontrada.")
                return

            print(
                f"Compra actual: "
                f"{cotizacion_actual.valor_compra:.2f}"
            )
            print(
                f"Venta actual: "
                f"{cotizacion_actual.valor_venta:.2f}"
            )

            compra_texto = input(
                "Nuevo valor de compra "
                "(Enter para mantener): "
            ).strip()

            venta_texto = input(
                "Nuevo valor de venta "
                "(Enter para mantener): "
            ).strip()

            if compra_texto:
                valor_compra = float(compra_texto)
            else:
                valor_compra = (
                    cotizacion_actual.valor_compra
                )

            if venta_texto:
                valor_venta = float(venta_texto)
            else:
                valor_venta = (
                    cotizacion_actual.valor_venta
                )

            cotizacion_modificada = CotizacionDolar(
                id=cotizacion_actual.id,
                tipo_cotizacion=(
                    cotizacion_actual.tipo_cotizacion
                ),
                moneda=cotizacion_actual.moneda,
                fecha=cotizacion_actual.fecha,
                valor_compra=valor_compra,
                valor_venta=valor_venta,
            )

            self.servicio_cotizaciones.actualizar(
                cotizacion_modificada
            )

            print(
                "\nCotización modificada correctamente."
            )

        except ValueError as error:
            print(f"\nError: {error}")

    def eliminar_cotizacion(self) -> None:
        """Elimina una cotización por tipo y fecha."""

        try:
            print("\n--- ELIMINAR COTIZACIÓN ---")

            tipo_id = int(
                input("ID del tipo de cotización: ")
            )
            fecha = self.leer_fecha()

            cotizacion = (
                self.servicio_cotizaciones.obtener_por_tipo_y_fecha(
                    tipo_id,
                    fecha,
                )
            )

            if cotizacion is None:
                print("\nCotización no encontrada.")
                return

            self.mostrar_cotizacion(cotizacion)

            confirmacion = input(
                "\n¿Confirma la eliminación? (s/n): "
            ).strip().lower()

            if confirmacion != "s":
                print("\nEliminación cancelada.")
                return

            self.servicio_cotizaciones.eliminar(
                tipo_id,
                fecha,
            )

            print(
                "\nCotización eliminada correctamente."
            )

        except ValueError:
            print(
                "\nDatos inválidos. Verifique ID y fecha."
            )

    @staticmethod
    def mostrar_cotizacion(cotizacion) -> None:
        """Muestra los datos de una cotización."""

        print("\n--- COTIZACIÓN ---")
        print(f"ID: {cotizacion.id}")
        print(
            f"Tipo: {cotizacion.tipo_cotizacion.nombre}"
        )
        print(f"Moneda: {cotizacion.moneda.nombre}")
        print(f"Fecha: {cotizacion.fecha}")
        print(
            f"Valor compra: "
            f"{cotizacion.valor_compra:.2f}"
        )
        print(
            f"Valor venta: "
            f"{cotizacion.valor_venta:.2f}"
        )
