
"""
Funciones de creación, visualización y modificación
de los catálogos del sistema Book Manager.
"""

from book_manager.models.models import (
    EditorialModel,
    GeneroModel,
    MonedaModel,
    TipoCotizacionModel,
)


# =========================================================
# GÉNEROS
# =========================================================

def crear_genero() -> GeneroModel:
    """Solicita los datos para crear un género."""
    genero_id = int(input("ID: "))
    nombre = input("Nombre: ").strip()

    return GeneroModel(id=genero_id, nombre=nombre)


def mostrar_genero(genero: GeneroModel) -> None:
    """Muestra los datos de un género."""
    print(f"ID: {genero.id} | Nombre: {genero.nombre}")


def modificar_genero(genero: GeneroModel) -> GeneroModel:
    """Solicita los nuevos datos de un género."""
    nombre = input("Nuevo nombre: ").strip()

    return GeneroModel(id=genero.id, nombre=nombre)


# =========================================================
# EDITORIALES
# =========================================================

def crear_editorial() -> EditorialModel:
    """Solicita los datos para crear una editorial."""
    editorial_id = int(input("ID: "))
    nombre = input("Nombre: ").strip()

    return EditorialModel(id=editorial_id, nombre=nombre)


def mostrar_editorial(editorial: EditorialModel) -> None:
    """Muestra los datos de una editorial."""
    print(f"ID: {editorial.id} | Nombre: {editorial.nombre}")


def modificar_editorial(editorial: EditorialModel) -> EditorialModel:
    """Solicita los nuevos datos de una editorial."""
    nombre = input("Nuevo nombre: ").strip()

    return EditorialModel(id=editorial.id, nombre=nombre)


# =========================================================
# MONEDAS
# =========================================================

def crear_moneda() -> MonedaModel:
    """Solicita los datos para crear una moneda."""
    moneda_id = int(input("ID: "))
    codigo = input("Código: ").strip()
    nombre = input("Nombre: ").strip()
    simbolo = input("Símbolo: ").strip()

    return MonedaModel(
        id=moneda_id,
        codigo=codigo,
        nombre=nombre,
        simbolo=simbolo,
    )


def mostrar_moneda(moneda: MonedaModel) -> None:
    """Muestra los datos de una moneda."""
    print(
        f"ID: {moneda.id} | "
        f"Código: {moneda.codigo} | "
        f"Nombre: {moneda.nombre} | "
        f"Símbolo: {moneda.simbolo}"
    )


def modificar_moneda(moneda: MonedaModel) -> MonedaModel:
    """Solicita los nuevos datos de una moneda."""
    codigo = input("Nuevo código: ").strip()
    nombre = input("Nuevo nombre: ").strip()
    simbolo = input("Nuevo símbolo: ").strip()

    return MonedaModel(
        id=moneda.id,
        codigo=codigo,
        nombre=nombre,
        simbolo=simbolo,
    )


# =========================================================
# TIPOS DE COTIZACIÓN
# =========================================================

def crear_tipo_cotizacion() -> TipoCotizacionModel:
    """Solicita los datos para crear un tipo de cotización."""
    tipo_id = int(input("ID: "))
    nombre = input("Nombre: ").strip()

    return TipoCotizacionModel(id=tipo_id, nombre=nombre)


def mostrar_tipo_cotizacion(tipo: TipoCotizacionModel) -> None:
    """Muestra los datos de un tipo de cotización."""
    print(f"ID: {tipo.id} | Nombre: {tipo.nombre}")


def modificar_tipo_cotizacion(
    tipo: TipoCotizacionModel,
) -> TipoCotizacionModel:
    """Solicita los nuevos datos de un tipo de cotización."""
    nombre = input("Nuevo nombre: ").strip()

    return TipoCotizacionModel(id=tipo.id, nombre=nombre)
