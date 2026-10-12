
"""
Interfaz principal de consola del sistema Book Manager.
"""

import csv
from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

from book_manager.ui.menus.catalogos_config import (
    crear_editorial,
    crear_genero,
    crear_moneda,
    crear_tipo_cotizacion,
    modificar_editorial,
    modificar_genero,
    modificar_moneda,
    modificar_tipo_cotizacion,
    mostrar_editorial,
    mostrar_genero,
    mostrar_moneda,
    mostrar_tipo_cotizacion,
)
from book_manager.ui.menus.menu_catalogos import MenuCatalogos
from book_manager.ui.menus.menu_cotizaciones import MenuCotizaciones
from book_manager.ui.menus.menu_libros import MenuLibros
from book_manager.ui.menus.menu_precios import MenuPrecios
from book_manager.ui.menus.menu_stock import MenuStock


class Consola:
    """Interfaz principal de usuario para Book Manager."""

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

        self.servicio_libros = servicio_libros
        self.servicio_precios = servicio_precios
        self.servicio_monedas = servicio_monedas
        self.servicio_cotizaciones = servicio_cotizaciones
        self.servicio_tipos_cotizacion = servicio_tipos_cotizacion

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

        self.menu_generos = MenuCatalogos(
            titulo="Géneros",
            servicio=servicio_generos,
            crear_entidad=crear_genero,
            mostrar_entidad=mostrar_genero,
            modificar_entidad=modificar_genero,
        )

        self.menu_editoriales = MenuCatalogos(
            titulo="Editoriales",
            servicio=servicio_editoriales,
            crear_entidad=crear_editorial,
            mostrar_entidad=mostrar_editorial,
            modificar_entidad=modificar_editorial,
        )

        self.menu_monedas = MenuCatalogos(
            titulo="Monedas",
            servicio=servicio_monedas,
            crear_entidad=crear_moneda,
            mostrar_entidad=mostrar_moneda,
            modificar_entidad=modificar_moneda,
        )

        self.menu_tipos_cotizacion = MenuCatalogos(
            titulo="Tipos de cotización",
            servicio=servicio_tipos_cotizacion,
            crear_entidad=crear_tipo_cotizacion,
            mostrar_entidad=mostrar_tipo_cotizacion,
            modificar_entidad=modificar_tipo_cotizacion,
        )

    # ======================================================
    # OPCIÓN 9 - OBTENER COTIZACIONES POR API
    # ======================================================

    def obtener_cotizaciones_api(self) -> None:
        """Actualiza cotizaciones desde la API y muestra los valores."""

        print("\n=== OBTENER COTIZACIONES POR API ===")
        print("Consultando cotizaciones del dólar...")

        try:
            resultado = self.servicio_cotizaciones.obtener_cotizaciones()

            print("\nCotizaciones procesadas correctamente.")
            print(f"Creadas: {resultado['creadas']}")
            print(f"Actualizadas: {resultado['actualizadas']}")
            print(f"Omitidas: {resultado['omitidas']}")

        except Exception as error:
            print(f"\nError al consultar la API: {error}")
            return

        # Recuperar las últimas cotizaciones guardadas.
        tipos = self.servicio_tipos_cotizacion.obtener_todos()

        print("\n=== ÚLTIMAS COTIZACIONES REGISTRADAS ===")

        print(
            "{:<22} {:<14} {:>15} {:>15}".format(
                "TIPO",
                "FECHA",
                "COMPRA",
                "VENTA",
            )
        )

        print("-" * 70)

        cantidad = 0

        for tipo in tipos:

            try:
                historico = (
                    self.servicio_cotizaciones.obtener_historico(
                        tipo.id
                    )
                )

                if not historico:
                    continue

                ultima = max(
                    historico,
                    key=lambda cotizacion: cotizacion.fecha,
                )

                compra = (
                    f"{ultima.valor_compra:.2f}"
                    if ultima.valor_compra is not None
                    else "N/D"
                )

                venta = (
                    f"{ultima.valor_venta:.2f}"
                    if ultima.valor_venta is not None
                    else "N/D"
                )

                print(
                    "{:<22} {:<14} {:>15} {:>15}".format(
                        tipo.nombre[:22],
                        str(ultima.fecha),
                        compra,
                        venta,
                    )
                )

                cantidad += 1

            except Exception as error:
                print(
                    f"No se pudo consultar {tipo.nombre}: {error}"
                )

        if cantidad == 0:
            print("\nNo hay cotizaciones registradas.")

        print(f"\nTipos de cotización mostrados: {cantidad}")

    # ======================================================
    # MÉTODOS AUXILIARES
    # ======================================================

    @staticmethod
    def redondear(valor: Decimal) -> Decimal:
        """Redondea importes a dos decimales."""

        return valor.quantize(
            Decimal("0.01"),
            rounding=ROUND_HALF_UP,
        )

    def obtener_ultima_cotizacion(self, tipo_id: int):
        """Recupera la cotización más reciente de un tipo."""

        cotizaciones = (
            self.servicio_cotizaciones.obtener_historico(tipo_id)
        )

        if not cotizaciones:
            return None

        return max(
            cotizaciones,
            key=lambda cotizacion: cotizacion.fecha,
        )

    def seleccionar_tipo_cotizacion(self):
        """Permite seleccionar un tipo de cotización."""

        tipos = self.servicio_tipos_cotizacion.obtener_todos()

        if not tipos:
            print("\nNo hay tipos de cotización registrados.")
            return None

        print("\nTipos de cotización disponibles:")

        for tipo in tipos:
            print(f"{tipo.id}. {tipo.nombre}")

        try:
            tipo_id = int(
                input(
                    "\nSeleccione el ID del tipo de cotización: "
                ).strip()
            )
        except ValueError:
            print("\nDebe ingresar un número entero.")
            return None

        tipo = next(
            (t for t in tipos if t.id == tipo_id),
            None,
        )

        if tipo is None:
            print("\nEl tipo de cotización no existe.")
            return None

        cotizacion = self.obtener_ultima_cotizacion(tipo_id)

        if cotizacion is None:
            print(
                "\nNo hay cotizaciones registradas para ese tipo."
            )
            return None

        return tipo, cotizacion

    def seleccionar_moneda(self):
        """
        Permite seleccionar una moneda por:
        - ID
        - Código
        - Nombre completo
        """

        monedas = self.servicio_monedas.obtener_todos()

        if not monedas:
            print("\nNo hay monedas registradas.")
            return None

        print("\nMonedas disponibles:")

        for moneda in monedas:
            print(
                f"{moneda.id}. "
                f"{moneda.codigo} - {moneda.nombre}"
            )

        seleccion = input(
            "\nIngrese el ID, código o nombre de la moneda: "
        ).strip().casefold()

        moneda_seleccionada = next(
            (
                moneda
                for moneda in monedas
                if str(moneda.id) == seleccion
                or moneda.codigo.strip().casefold() == seleccion
                or moneda.nombre.strip().casefold() == seleccion
            ),
            None,
        )

        if moneda_seleccionada is None:
            print("\nLa moneda seleccionada no existe.")
            return None

        return moneda_seleccionada

    # ======================================================
    # OPCIÓN 10 - PRECIOS BIMONETARIOS
    # ======================================================

    def ver_precios_bimonetarios(self) -> None:
        """
        Muestra precios en ARS y otra moneda seleccionada.

        Para USD calcula conversiones utilizando la
        cotización de venta seleccionada.

        Para otras monedas muestra los precios registrados.
        """

        print("\n=== PRECIOS BIMONETARIOS ===")

        moneda = self.seleccionar_moneda()

        if moneda is None:
            return

        codigo = moneda.codigo.upper()

        if codigo == "ARS":
            print(
                "\nSeleccione una moneda distinta de ARS."
            )
            return

        valor_dolar = None

        # Solicitar cotización solamente para USD.
        if codigo == "USD":

            seleccion = self.seleccionar_tipo_cotizacion()

            if seleccion is None:
                return

            tipo, cotizacion = seleccion

            if cotizacion.valor_venta is None:
                print("\nLa cotización de venta no está disponible.")
                return

            valor_dolar = Decimal(
                str(cotizacion.valor_venta)
            )

            if valor_dolar <= 0:
                print(
                    "\nLa cotización seleccionada no es válida."
                )
                return

            print(
                f"\nTipo: {tipo.nombre}"
                f" | Fecha: {cotizacion.fecha}"
                f" | Venta: {valor_dolar:.2f} ARS/USD"
            )

        precios = self.servicio_precios.obtener_todos()

        if not precios:
            print("\nNo hay precios registrados.")
            return

        # Agrupar precios por libro y moneda.
        precios_por_libro = {}

        for precio in precios:

            libro_id = precio.libro_id

            if libro_id not in precios_por_libro:
                precios_por_libro[libro_id] = {
                    "titulo": precio.libro.titulo,
                    "monedas": {},
                }

            codigo_origen = precio.moneda.codigo.upper()

            precios_por_libro[libro_id]["monedas"][
                codigo_origen
            ] = Decimal(str(precio.valor))

        print(
            "\n{:<35} {:>16} {:>16}".format(
                "LIBRO",
                "PRECIO ARS",
                f"PRECIO {codigo}",
            )
        )

        print("-" * 70)

        for datos in precios_por_libro.values():

            precio_ars = datos["monedas"].get("ARS")
            precio_destino = datos["monedas"].get(codigo)

            # Completar precios faltantes mediante conversión.
            if codigo == "USD" and valor_dolar is not None:

                if (
                    precio_ars is not None
                    and precio_destino is None
                ):
                    precio_destino = (
                        precio_ars / valor_dolar
                    )

                elif (
                    precio_destino is not None
                    and precio_ars is None
                ):
                    precio_ars = (
                        precio_destino * valor_dolar
                    )

            texto_ars = (
                f"{self.redondear(precio_ars):.2f}"
                if precio_ars is not None
                else "Sin precio"
            )

            texto_destino = (
                f"{self.redondear(precio_destino):.2f}"
                if precio_destino is not None
                else "Sin precio"
            )

            print(
                "{:<35} {:>16} {:>16}".format(
                    datos["titulo"][:35],
                    texto_ars,
                    texto_destino,
                )
            )

        if codigo == "USD":
            print(
                "\nNota: los precios faltantes en ARS/USD "
                "se calcularon usando la cotización seleccionada."
            )
        else:
            print(
                "\nNota: para esta moneda se muestran únicamente "
                "los precios registrados en la base de datos."
            )

    # ======================================================
    # OPCIÓN 11 - EXPORTAR PRECIOS A CSV
    # ======================================================
    def exportar_precios_csv(self) -> None:
        """
        Exporta todos los precios registrados en la base
        de datos, respetando la moneda original.
        """

        print("\n=== EXPORTAR PRECIOS A CSV ===")

        precios = self.servicio_precios.obtener_todos()

        if not precios:
            print("\nNo hay precios registrados para exportar.")
            return

        # Preparar los datos del archivo
        filas = []

        for precio in precios:
            filas.append({
                "libro_id": precio.libro_id,
                "isbn": precio.libro.isbn,
                "titulo": precio.libro.titulo,
                "moneda": precio.moneda.codigo,
                "precio": str(precio.valor),
            })

        # Definir la ubicación del archivo CSV
        ruta_proyecto = Path(__file__).resolve().parents[3]
        carpeta_exportaciones = ruta_proyecto / "exportaciones"

        try:
            carpeta_exportaciones.mkdir(
                parents=True,
                exist_ok=True,
            )

            fecha_archivo = datetime.now().strftime(
                "%Y%m%d_%H%M%S"
            )

            ruta_csv = (
                carpeta_exportaciones
                / f"precios_{fecha_archivo}.csv"
            )

            columnas = [
                "libro_id",
                "isbn",
                "titulo",
                "moneda",
                "precio",
            ]

            with open(
                ruta_csv,
                mode="w",
                newline="",
                encoding="utf-8-sig",
            ) as archivo:

                escritor = csv.DictWriter(
                    archivo,
                    fieldnames=columnas,
                )

                escritor.writeheader()
                escritor.writerows(filas)

            print("\nArchivo CSV generado correctamente.")
            print(f"Registros exportados: {len(filas)}")
            print(f"Ubicación: {ruta_csv}")

        except OSError as error:
            print(f"\nError al exportar el archivo: {error}")


    # ======================================================
    # MENÚ PRINCIPAL
    # ======================================================

    def ejecutar(self) -> None:
        """Ejecuta el menú principal de la aplicación."""

        while True:

            self.mostrar_menu_principal()

            opcion = input(
                "Seleccione una opción: "
            ).strip()

            if opcion == "1":
                self.menu_libros.ejecutar()

            elif opcion == "2":
                self.menu_precios.ejecutar()

            elif opcion == "3":
                self.menu_stock.ejecutar()

            elif opcion == "4":
                self.menu_cotizaciones.ejecutar()

            elif opcion == "5":
                self.menu_generos.ejecutar()

            elif opcion == "6":
                self.menu_editoriales.ejecutar()

            elif opcion == "7":
                self.menu_monedas.ejecutar()

            elif opcion == "8":
                self.menu_tipos_cotizacion.ejecutar()

            elif opcion == "9":
                self.obtener_cotizaciones_api()

            elif opcion == "10":
                self.ver_precios_bimonetarios()

            elif opcion == "11":
                self.exportar_precios_csv()

            elif opcion == "0":
                print("\nSaliendo de Book Manager...")
                break

            else:
                print(
                    "\nOpción inválida. Intente nuevamente."
                )

    @staticmethod
    def mostrar_menu_principal() -> None:
        """Muestra las opciones principales del sistema."""

        print("\n" + "=" * 45)
        print("              BOOK MANAGER")
        print("=" * 45)

        print("1. Gestión de libros")
        print("2. Gestión de precios")
        print("3. Gestión de stock")
        print("4. Gestión de cotizaciones")
        print("5. Gestión de géneros")
        print("6. Gestión de editoriales")
        print("7. Gestión de monedas")
        print("8. Gestión de tipos de cotización")
        print("9. Obtener cotizaciones por API")
        print("10. Ver precios bimonetarios")
        print("11. Exportar precios a CSV")
        print("0. Salir")

        print("=" * 45)
