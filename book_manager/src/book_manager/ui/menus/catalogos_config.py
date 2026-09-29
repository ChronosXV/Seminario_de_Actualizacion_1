
from book_manager.entities.entities import (
    Editorial,
    Genero,
    Moneda,
    TipoCotizacion,
)


# =========================================================
# GÉNEROS
# =========================================================

def crear_genero() -> Genero:
    """Solicita los datos necesarios para crear un género."""

    genero_id = int(input("ID: "))
    nombre = input("Nombre: ").strip()

    return Genero(
        id=genero_id,
        nombre=nombre,
    )


def mostrar_genero(genero: Genero) -> None:
    """Muestra los datos de un género."""

    print(
        f"ID: {genero.id} | "
        f"Nombre: {genero.nombre}"
    )


def modificar_genero(genero: Genero) -> Genero:
    """Solicita los nuevos datos de un género."""

    nombre = input("Nuevo nombre: ").strip()

    return Genero(
        id=genero.id,
        nombre=nombre,
    )


# =========================================================
# EDITORIALES
# =========================================================

def crear_editorial() -> Editorial:
    """Solicita los datos necesarios para crear una editorial."""

    editorial_id = int(input("ID: "))
    nombre = input("Nombre: ").strip()

    return Editorial(
        id=editorial_id,
        nombre=nombre,
    )


def mostrar_editorial(editorial: Editorial) -> None:
    """Muestra los datos de una editorial."""

    print(
        f"ID: {editorial.id} | "
        f"Nombre: {editorial.nombre}"
    )


def modificar_editorial(editorial: Editorial) -> Editorial:
    """Solicita los nuevos datos de una editorial."""

    nombre = input("Nuevo nombre: ").strip()

    return Editorial(
        id=editorial.id,
        nombre=nombre,
    )


# =========================================================
# MONEDAS
# =========================================================

def crear_moneda() -> Moneda:
    """Solicita los datos necesarios para crear una moneda."""

    moneda_id = int(input("ID: "))
    codigo = input("Código: ").strip()
    nombre = input("Nombre: ").strip()
    simbolo = input("Símbolo: ").strip()

    return Moneda(
        id=moneda_id,
        codigo=codigo,
        nombre=nombre,
        simbolo=simbolo,
    )


def mostrar_moneda(moneda: Moneda) -> None:
    """Muestra los datos de una moneda."""

    print(
        f"ID: {moneda.id} | "
        f"Código: {moneda.codigo} | "
        f"Nombre: {moneda.nombre} | "
        f"Símbolo: {moneda.simbolo}"
    )


def modificar_moneda(moneda: Moneda) -> Moneda:
    """Solicita los nuevos datos de una moneda."""

    codigo = input("Nuevo código: ").strip()
    nombre = input("Nuevo nombre: ").strip()
    simbolo = input("Nuevo símbolo: ").strip()

    return Moneda(
        id=moneda.id,
        codigo=codigo,
        nombre=nombre,
        simbolo=simbolo,
    )


# =========================================================
# TIPOS DE COTIZACIÓN
# =========================================================

def crear_tipo_cotizacion() -> TipoCotizacion:
    """Solicita los datos para crear un tipo de cotización."""

    tipo_id = int(input("ID: "))
    nombre = input("Nombre: ").strip()

    return TipoCotizacion(
        id=tipo_id,
        nombre=nombre,
    )


def mostrar_tipo_cotizacion(
    tipo: TipoCotizacion,
) -> None:
    """Muestra los datos de un tipo de cotización."""

    print(
        f"ID: {tipo.id} | "
        f"Nombre: {tipo.nombre}"
    )


def modificar_tipo_cotizacion(
    tipo: TipoCotizacion,
) -> TipoCotizacion:
    """Solicita los nuevos datos de un tipo de cotización."""

    nombre = input("Nuevo nombre: ").strip()

    return TipoCotizacion(
        id=tipo.id,
        nombre=nombre,
    )
