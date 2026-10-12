"""
Menú de gestión de cotizaciones del dólar.

Permite consultar, crear, modificar y eliminar cotizaciones
utilizando los servicios y modelos SQLAlchemy.
"""

from datetime import date
from decimal import Decimal, InvalidOperation

from sqlalchemy.exc import IntegrityError

from book_manager.models.models import CotizacionDolarModel


class MenuCotizaciones:
    """Interfaz de consola para gestionar cotizaciones."""

    def __init__(
        self,
        servicio_cotizaciones,
        servicio_tipos_cotizacion,
        servicio_monedas,
    ) -> None:
        """Inicializa el menú con sus servicios."""
        self.servicio = servicio_cotizaciones
        self.servicio_tipos_cotizacion = servicio_tipos_cotizacion
        self.servicio_monedas = servicio_monedas

    @staticmethod
    def leer_id(mensaje: str) -> int:
        """Solicita un identificador positivo."""
        try:
            identificador = int(input(mensaje))
        except ValueError as error:
            raise ValueError("El ID debe ser numérico.") from error

        if identificador <= 0:
            raise ValueError("El ID debe ser mayor que cero.")

        return identificador

    @staticmethod
    def leer_fecha(mensaje: str) -> date:
        """Solicita una fecha en formato AAAA-MM-DD."""
        try:
            return date.fromisoformat(input(mensaje).strip())
        except ValueError as error:
            raise ValueError(
                "La fecha debe tener formato AAAA-MM-DD."
            ) from error

    @staticmethod
    def validar_decimal(valor: str) -> Decimal:
        """Valida un importe positivo con hasta dos decimales."""
        try:
            numero = Decimal(valor.strip().replace(",", "."))
        except (InvalidOperation, AttributeError) as error:
            raise ValueError(
                "El importe debe ser numérico."
            ) from error

        if not numero.is_finite() or numero <= 0:
            raise ValueError(
                "El importe debe ser mayor que cero."
            )

        if numero.as_tuple().exponent < -2:
            raise ValueError(
                "El importe puede tener como máximo dos decimales."
            )

        if numero > Decimal("9999999999999.99"):
            raise ValueError(
                "El importe supera el máximo permitido."
            )

        return numero

    @staticmethod
    def validar_valores(
        valor_compra: Decimal,
        valor_venta: Decimal,
    ) -> None:
        """Valida la coherencia de los valores de cotización."""
        if valor_compra <= 0 or valor_venta <= 0:
            raise ValueError(
                "Los valores deben ser mayores que cero."
            )

        if valor_compra > valor_venta:
            raise ValueError(
                "El valor de compra no puede superar al de venta."
            )

    def validar_referencias(
        self,
        tipo_id: int,
        moneda_id: int,
    ) -> None:
        """Comprueba que el tipo de cotización y la moneda existan."""
        tipo = self.servicio_tipos_cotizacion.obtener_por_id(
            tipo_id
        )

        if tipo is None:
            raise ValueError(
                "El tipo de cotización no existe."
            )

        moneda = self.servicio_monedas.obtener_por_id(
            moneda_id
        )

        if moneda is None:
            raise ValueError(
                "La moneda no existe."
            )

    def ejecutar(self) -> None:
        """Ejecuta el menú de gestión de cotizaciones."""
        opciones = {
            "1": self.listar,
            "2": self.buscar,
            "3": self.crear,
            "4": self.modificar,
            "5": self.eliminar,
        }

        while True:
            print("\n--- GESTIÓN DE COTIZACIONES ---")
            print("1. Listar historial por tipo")
            print("2. Buscar por tipo y fecha")
            print("3. Crear cotización")
            print("4. Modificar cotización")
            print("5. Eliminar cotización")
            print("0. Volver")

            opcion = input(
                "Seleccione una opción: "
            ).strip()

            if opcion == "0":
                return

            accion = opciones.get(opcion)

            if accion is None:
                print("\nOpción inválida.")
                continue

            try:
                accion()

            except ValueError as error:
                print(f"\nDatos inválidos: {error}")

            except IntegrityError:
                print(
                    "\nNo se pudo completar la operación. "
                    "Verificá que no exista una cotización "
                    "duplicada y que las referencias sean válidas."
                )

    def listar(self) -> None:
        """Lista el historial de cotizaciones de un tipo."""
        tipos = self.servicio_tipos_cotizacion.obtener_todos()

        if not tipos:
            print("\nNo hay tipos de cotización registrados.")
            return

        print("\n--- TIPOS DE COTIZACIÓN ---")

        for tipo in tipos:
            print(f"{tipo.id}. {tipo.nombre}")

        tipo_id = self.leer_id(
            "\nID del tipo de cotización: "
        )

        tipo = self.servicio_tipos_cotizacion.obtener_por_id(
            tipo_id
        )

        if tipo is None:
            print("\nTipo de cotización inexistente.")
            return

        cotizaciones = self.servicio.obtener_historico(
            tipo_id
        )

        if not cotizaciones:
            print("\nNo hay cotizaciones registradas.")
            return

        print(f"\n--- HISTORIAL: {tipo.nombre} ---")

        for cotizacion in cotizaciones:
            self.mostrar_cotizacion(cotizacion)

    def buscar(self) -> None:
        """Busca una cotización por tipo y fecha."""
        tipo_id = self.leer_id(
            "ID del tipo de cotización: "
        )

        fecha = self.leer_fecha(
            "Fecha (AAAA-MM-DD): "
        )

        cotizacion = self.servicio.obtener_por_tipo_y_fecha(
            tipo_id,
            fecha,
        )

        if cotizacion is None:
            print("\nCotización no encontrada.")
            return

        self.mostrar_cotizacion(cotizacion)

    def crear(self) -> None:
        """Registra una nueva cotización."""
        print("\n--- NUEVA COTIZACIÓN ---")

        tipo_id = self.leer_id(
            "ID del tipo de cotización: "
        )

        moneda_id = self.leer_id(
            "ID de la moneda: "
        )

        self.validar_referencias(
            tipo_id,
            moneda_id,
        )

        fecha = self.leer_fecha(
            "Fecha (AAAA-MM-DD): "
        )

        valor_compra = self.validar_decimal(
            input("Valor compra: ")
        )

        valor_venta = self.validar_decimal(
            input("Valor venta: ")
        )

        self.validar_valores(
            valor_compra,
            valor_venta,
        )

        existente = self.servicio.obtener_por_tipo_y_fecha(
            tipo_id,
            fecha,
        )

        if existente is not None:
            print(
                "\nYa existe una cotización para "
                "ese tipo y fecha."
            )
            return

        cotizacion = CotizacionDolarModel(
            tipo_cotizacion_id=tipo_id,
            moneda_id=moneda_id,
            fecha=fecha,
            valor_compra=valor_compra,
            valor_venta=valor_venta,
        )

        self.servicio.crear(cotizacion)

        print("\nCotización creada correctamente.")

    def modificar(self) -> None:
        """Modifica una cotización existente."""
        print("\n--- MODIFICAR COTIZACIÓN ---")

        tipo_id = self.leer_id(
            "ID del tipo de cotización: "
        )

        fecha = self.leer_fecha(
            "Fecha (AAAA-MM-DD): "
        )

        cotizacion = self.servicio.obtener_por_tipo_y_fecha(
            tipo_id,
            fecha,
        )

        if cotizacion is None:
            print("\nCotización no encontrada.")
            return

        self.mostrar_cotizacion(cotizacion)

        moneda_id = self.leer_id(
            "\nNuevo ID de moneda: "
        )

        self.validar_referencias(
            tipo_id,
            moneda_id,
        )

        valor_compra = self.validar_decimal(
            input("Nuevo valor compra: ")
        )

        valor_venta = self.validar_decimal(
            input("Nuevo valor venta: ")
        )

        self.validar_valores(
            valor_compra,
            valor_venta,
        )

        cotizacion.moneda_id = moneda_id
        cotizacion.valor_compra = valor_compra
        cotizacion.valor_venta = valor_venta

        self.servicio.actualizar(cotizacion)

        print("\nCotización modificada correctamente.")

    def eliminar(self) -> None:
        """Elimina una cotización por tipo y fecha."""
        print("\n--- ELIMINAR COTIZACIÓN ---")

        tipo_id = self.leer_id(
            "ID del tipo de cotización: "
        )

        fecha = self.leer_fecha(
            "Fecha (AAAA-MM-DD): "
        )

        cotizacion = self.servicio.obtener_por_tipo_y_fecha(
            tipo_id,
            fecha,
        )

        if cotizacion is None:
            print("\nCotización no encontrada.")
            return

        self.mostrar_cotizacion(cotizacion)

        confirmacion = input(
            "\n¿Confirmar eliminación? (s/n): "
        ).strip().lower()

        if confirmacion != "s":
            print("\nOperación cancelada.")
            return

        eliminado = self.servicio.eliminar(
            tipo_id,
            fecha,
        )

        if eliminado:
            print("\nCotización eliminada correctamente.")
        else:
            print("\nNo se pudo eliminar la cotización.")

    @staticmethod
    def mostrar_cotizacion(
        cotizacion: CotizacionDolarModel,
    ) -> None:
        """Muestra los datos de una cotización."""
        print("\n--- COTIZACIÓN ---")
        print(f"ID: {cotizacion.id}")
        print(
            f"Tipo: {cotizacion.tipo_cotizacion.nombre}"
        )
        print(
            f"Moneda: {cotizacion.moneda.nombre}"
        )
        print(f"Fecha: {cotizacion.fecha}")
        print(
            f"Valor compra: {cotizacion.valor_compra:.2f}"
        )
        print(
            f"Valor venta: {cotizacion.valor_venta:.2f}"
        )
