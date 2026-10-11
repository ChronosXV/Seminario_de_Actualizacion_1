"""
Modelos ORM del sistema Book Manager.

Define las tablas, sus tipos de datos, claves primarias,
claves foráneas y relaciones mediante SQLAlchemy.
"""

from datetime import date
from decimal import Decimal

from sqlalchemy import (
    CheckConstraint,
    Date,
    ForeignKey,
    Integer,
    Numeric,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
)


class Base(DeclarativeBase):
    """Clase base declarativa de los modelos ORM."""
    pass


class GeneroModel(Base):
    """Representa los géneros literarios de los libros."""

    __tablename__ = "generos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)

    libros: Mapped[list["LibroModel"]] = relationship(
        back_populates="genero"
    )


class EditorialModel(Base):
    """Representa las editoriales de los libros."""

    __tablename__ = "editoriales"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(150), nullable=False)

    libros: Mapped[list["LibroModel"]] = relationship(
        back_populates="editorial"
    )


class MonedaModel(Base):
    """Representa las monedas utilizadas por el sistema."""

    __tablename__ = "monedas"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    codigo: Mapped[str] = mapped_column(
        String(10), nullable=False, unique=True
    )
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    simbolo: Mapped[str] = mapped_column(String(10), nullable=False)

    precios: Mapped[list["PrecioModel"]] = relationship(
        back_populates="moneda"
    )

    cotizaciones: Mapped[list["CotizacionDolarModel"]] = relationship(
        back_populates="moneda"
    )


class TipoCotizacionModel(Base):
    """Representa los tipos de cotización del dólar."""

    __tablename__ = "tipos_cotizacion"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)

    cotizaciones: Mapped[list["CotizacionDolarModel"]] = relationship(
        back_populates="tipo_cotizacion"
    )


class LibroModel(Base):
    """Representa los libros y sus relaciones con género y editorial."""

    __tablename__ = "libros"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    isbn: Mapped[str] = mapped_column(
        String(20), nullable=False, unique=True
    )
    titulo: Mapped[str] = mapped_column(String(255), nullable=False)
    autor: Mapped[str] = mapped_column(String(150), nullable=False)

    editorial_id: Mapped[int] = mapped_column(
        ForeignKey("editoriales.id"), nullable=False
    )
    genero_id: Mapped[int] = mapped_column(
        ForeignKey("generos.id"), nullable=False
    )

    editorial: Mapped["EditorialModel"] = relationship(
        back_populates="libros"
    )
    genero: Mapped["GeneroModel"] = relationship(
        back_populates="libros"
    )

    precios: Mapped[list["PrecioModel"]] = relationship(
        back_populates="libro"
    )
    stock: Mapped["StockModel | None"] = relationship(
        back_populates="libro",
        uselist=False
    )


class PrecioModel(Base):
    """Representa el precio de un libro en una moneda determinada."""

    __tablename__ = "precios"

    __table_args__ = (
        CheckConstraint("valor > 0", name="ck_precio_positivo"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    libro_id: Mapped[int] = mapped_column(
        ForeignKey("libros.id"), nullable=False
    )
    moneda_id: Mapped[int] = mapped_column(
        ForeignKey("monedas.id"), nullable=False
    )

    valor: Mapped[Decimal] = mapped_column(
        Numeric(15, 2), nullable=False
    )

    libro: Mapped["LibroModel"] = relationship(
        back_populates="precios"
    )
    moneda: Mapped["MonedaModel"] = relationship(
        back_populates="precios"
    )


class StockModel(Base):
    """Representa el stock de un libro mediante una relación uno a uno."""

    __tablename__ = "stock"

    __table_args__ = (
        CheckConstraint("cantidad >= 0", name="ck_stock_no_negativo"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    libro_id: Mapped[int] = mapped_column(
        ForeignKey("libros.id"),
        nullable=False,
        unique=True
    )

    cantidad: Mapped[int] = mapped_column(
        Integer, nullable=False
    )

    libro: Mapped["LibroModel"] = relationship(
        back_populates="stock"
    )


class CotizacionDolarModel(Base):
    """Representa las cotizaciones del dólar por tipo, moneda y fecha."""

    __tablename__ = "cotizaciones_dolar"

    __table_args__ = (
        UniqueConstraint(
            "tipo_cotizacion_id",
            "fecha",
            name="uq_cotizacion_tipo_fecha"
        ),
        CheckConstraint(
            "valor_compra > 0",
            name="ck_cotizacion_compra_positiva"
        ),
        CheckConstraint(
            "valor_venta > 0",
            name="ck_cotizacion_venta_positiva"
        ),
        CheckConstraint(
            "valor_venta >= valor_compra",
            name="ck_cotizacion_valores"
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    tipo_cotizacion_id: Mapped[int] = mapped_column(
        ForeignKey("tipos_cotizacion.id"), nullable=False
    )
    moneda_id: Mapped[int] = mapped_column(
        ForeignKey("monedas.id"), nullable=False
    )

    fecha: Mapped[date] = mapped_column(Date, nullable=False)

    valor_compra: Mapped[Decimal] = mapped_column(
        Numeric(15, 2), nullable=False
    )
    valor_venta: Mapped[Decimal] = mapped_column(
        Numeric(15, 2), nullable=False
    )

    tipo_cotizacion: Mapped["TipoCotizacionModel"] = relationship(
        back_populates="cotizaciones"
    )
    moneda: Mapped["MonedaModel"] = relationship(
        back_populates="cotizaciones"
    )
