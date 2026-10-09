
from datetime import date
from math import isfinite


class EntidadBase:
    """Clase base que proporciona un identificador a las entidades."""

    def __init__(self, id: int) -> None:
        self._id = None
        self.id = id

    @property
    def id(self) -> int:
        """Devuelve el identificador de la entidad."""
        return self._id

    @id.setter
    def id(self, valor: int) -> None:
        """Valida y establece el identificador."""
        if type(valor) is not int or valor <= 0:
            raise ValueError(
                "El ID debe ser un número entero positivo."
            )

        self._id = valor

    def __str__(self) -> str:
        """Devuelve una representación de la entidad."""
        return f"{self.__class__.__name__}(id={self.id})"


class Genero(EntidadBase):
    """Representa un género literario."""

    def __init__(self, id: int, nombre: str) -> None:
        super().__init__(id)
        self.nombre = nombre

    @property
    def nombre(self) -> str:
        """Devuelve el nombre del género."""
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        """Valida y establece el nombre del género."""
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError(
                "El nombre del género no puede estar vacío."
            )

        self._nombre = valor.strip()

    def __str__(self) -> str:
        """Devuelve una representación del género."""
        return f"Género: {self.nombre} (ID: {self.id})"


class Editorial(EntidadBase):
    """Representa una editorial de libros."""

    def __init__(self, id: int, nombre: str) -> None:
        super().__init__(id)
        self.nombre = nombre

    @property
    def nombre(self) -> str:
        """Devuelve el nombre de la editorial."""
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        """Valida y establece el nombre de la editorial."""
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError(
                "El nombre de la editorial no puede estar vacío."
            )

        self._nombre = valor.strip()

    def __str__(self) -> str:
        """Devuelve una representación de la editorial."""
        return f"Editorial: {self.nombre} (ID: {self.id})"


class Moneda(EntidadBase):
    """Representa una moneda utilizada en el sistema."""

    def __init__(
        self,
        id: int,
        codigo: str,
        nombre: str,
        simbolo: str,
    ) -> None:
        super().__init__(id)
        self.codigo = codigo
        self.nombre = nombre
        self.simbolo = simbolo

    @property
    def codigo(self) -> str:
        """Devuelve el código de la moneda."""
        return self._codigo

    @codigo.setter
    def codigo(self, valor: str) -> None:
        """Valida y establece el código de la moneda."""
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError(
                "El código de la moneda no puede estar vacío."
            )

        self._codigo = valor.strip().upper()

    @property
    def nombre(self) -> str:
        """Devuelve el nombre de la moneda."""
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        """Valida y establece el nombre de la moneda."""
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError(
                "El nombre de la moneda no puede estar vacío."
            )

        self._nombre = valor.strip()

    @property
    def simbolo(self) -> str:
        """Devuelve el símbolo de la moneda."""
        return self._simbolo

    @simbolo.setter
    def simbolo(self, valor: str) -> None:
        """Valida y establece el símbolo de la moneda."""
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError(
                "El símbolo de la moneda no puede estar vacío."
            )

        self._simbolo = valor.strip()

    def __str__(self) -> str:
        """Devuelve una representación de la moneda."""
        return (
            f"Moneda: {self.nombre} "
            f"({self.codigo}) - {self.simbolo}"
        )


class TipoCotizacion(EntidadBase):
    """Representa un tipo de cotización del dólar."""

    def __init__(self, id: int, nombre: str) -> None:
        super().__init__(id)
        self.nombre = nombre

    @property
    def nombre(self) -> str:
        """Devuelve el nombre del tipo de cotización."""
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        """Valida y establece el nombre del tipo de cotización."""
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError(
                "El nombre del tipo de cotización no puede estar vacío."
            )

        self._nombre = valor.strip()

    def __str__(self) -> str:
        """Devuelve una representación del tipo de cotización."""
        return (
            f"Tipo de cotización: {self.nombre} "
            f"(ID: {self.id})"
        )


class Libro(EntidadBase):
    """Representa un libro asociado a una editorial y un género."""

    def __init__(
        self,
        id: int,
        isbn: str,
        titulo: str,
        autor: str,
        editorial: Editorial,
        genero: Genero,
    ) -> None:
        super().__init__(id)
        self.isbn = isbn
        self.titulo = titulo
        self.autor = autor
        self.editorial = editorial
        self.genero = genero

    @property
    def isbn(self) -> str:
        """Devuelve el ISBN del libro."""
        return self._isbn

    @isbn.setter
    def isbn(self, valor: str) -> None:
        """Valida y establece el ISBN."""
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError(
                "El ISBN no puede estar vacío."
            )

        self._isbn = valor.strip()

    @property
    def titulo(self) -> str:
        """Devuelve el título del libro."""
        return self._titulo

    @titulo.setter
    def titulo(self, valor: str) -> None:
        """Valida y establece el título."""
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError(
                "El título del libro no puede estar vacío."
            )

        self._titulo = valor.strip()

    @property
    def autor(self) -> str:
        """Devuelve el autor del libro."""
        return self._autor

    @autor.setter
    def autor(self, valor: str) -> None:
        """Valida y establece el autor."""
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError(
                "El autor del libro no puede estar vacío."
            )

        self._autor = valor.strip()

    @property
    def editorial(self) -> Editorial:
        """Devuelve la editorial asociada."""
        return self._editorial

    @editorial.setter
    def editorial(self, valor: Editorial) -> None:
        """Valida y establece la editorial."""
        if not isinstance(valor, Editorial):
            raise ValueError(
                "La editorial debe ser un objeto Editorial."
            )

        self._editorial = valor

    @property
    def genero(self) -> Genero:
        """Devuelve el género asociado."""
        return self._genero

    @genero.setter
    def genero(self, valor: Genero) -> None:
        """Valida y establece el género."""
        if not isinstance(valor, Genero):
            raise ValueError(
                "El género debe ser un objeto Genero."
            )

        self._genero = valor

    def __str__(self) -> str:
        """Devuelve una representación del libro."""
        return (
            f"Libro: {self.titulo} - {self.autor} "
            f"(ISBN: {self.isbn})"
        )


class Precio(EntidadBase):
    """Representa el precio de un libro en una moneda."""

    def __init__(
        self,
        id: int,
        libro: Libro,
        moneda: Moneda,
        valor: float,
    ) -> None:
        super().__init__(id)
        self.libro = libro
        self.moneda = moneda
        self.valor = valor

    @property
    def libro(self) -> Libro:
        """Devuelve el libro asociado."""
        return self._libro

    @libro.setter
    def libro(self, valor: Libro) -> None:
        """Valida y establece el libro."""
        if not isinstance(valor, Libro):
            raise ValueError(
                "El libro debe ser un objeto Libro."
            )

        self._libro = valor

    @property
    def moneda(self) -> Moneda:
        """Devuelve la moneda asociada."""
        return self._moneda

    @moneda.setter
    def moneda(self, valor: Moneda) -> None:
        """Valida y establece la moneda."""
        if not isinstance(valor, Moneda):
            raise ValueError(
                "La moneda debe ser un objeto Moneda."
            )

        self._moneda = valor

    @property
    def valor(self) -> float:
        """Devuelve el valor del precio."""
        return self._valor

    @valor.setter
    def valor(self, nuevo_valor: float) -> None:
        """Valida que el precio sea positivo y finito."""
        if (
            isinstance(nuevo_valor, bool)
            or not isinstance(nuevo_valor, (int, float))
            or not isfinite(nuevo_valor)
            or nuevo_valor <= 0
        ):
            raise ValueError(
                "El precio debe ser un número mayor que cero."
            )

        self._valor = float(nuevo_valor)

    def __str__(self) -> str:
        """Devuelve una representación del precio."""
        return (
            f"Precio: {self.libro.titulo} - "
            f"{self.moneda.simbolo}{self.valor:.2f}"
        )


class Stock(EntidadBase):
    """Representa la cantidad disponible de un libro."""

    def __init__(
        self,
        id: int,
        libro: Libro,
        cantidad: int,
    ) -> None:
        super().__init__(id)
        self.libro = libro
        self.cantidad = cantidad

    @property
    def libro(self) -> Libro:
        """Devuelve el libro asociado al stock."""
        return self._libro

    @libro.setter
    def libro(self, valor: Libro) -> None:
        """Valida y establece el libro."""
        if not isinstance(valor, Libro):
            raise ValueError(
                "El libro debe ser un objeto Libro."
            )

        self._libro = valor

    @property
    def cantidad(self) -> int:
        """Devuelve la cantidad disponible."""
        return self._cantidad

    @cantidad.setter
    def cantidad(self, valor: int) -> None:
        """Valida que la cantidad sea un entero no negativo."""
        if type(valor) is not int or valor < 0:
            raise ValueError(
                "La cantidad de stock no puede ser negativa "
                "y debe ser un número entero."
            )

        self._cantidad = valor

    def __str__(self) -> str:
        """Devuelve una representación del stock."""
        return (
            f"Stock: {self.libro.titulo} - "
            f"Cantidad: {self.cantidad}"
        )


class CotizacionDolar(EntidadBase):
    """Representa una cotización del dólar para una fecha."""

    def __init__(
        self,
        id: int,
        tipo_cotizacion: TipoCotizacion,
        moneda: Moneda,
        fecha: date,
        valor_compra: float,
        valor_venta: float,
    ) -> None:
        super().__init__(id)
        self.tipo_cotizacion = tipo_cotizacion
        self.moneda = moneda
        self.fecha = fecha
        self.valor_compra = valor_compra
        self.valor_venta = valor_venta

    @property
    def tipo_cotizacion(self) -> TipoCotizacion:
        """Devuelve el tipo de cotización."""
        return self._tipo_cotizacion

    @tipo_cotizacion.setter
    def tipo_cotizacion(
        self,
        valor: TipoCotizacion,
    ) -> None:
        """Valida y establece el tipo de cotización."""
        if not isinstance(valor, TipoCotizacion):
            raise ValueError(
                "Debe proporcionar un objeto TipoCotizacion."
            )

        self._tipo_cotizacion = valor

    @property
    def moneda(self) -> Moneda:
        """Devuelve la moneda asociada."""
        return self._moneda

    @moneda.setter
    def moneda(self, valor: Moneda) -> None:
        """Valida y establece la moneda."""
        if not isinstance(valor, Moneda):
            raise ValueError(
                "Debe proporcionar un objeto Moneda."
            )

        self._moneda = valor

    @property
    def fecha(self) -> date:
        """Devuelve la fecha de cotización."""
        return self._fecha

    @fecha.setter
    def fecha(self, valor: date) -> None:
        """Valida y establece la fecha."""
        if not isinstance(valor, date):
            raise ValueError(
                "La fecha debe ser un objeto date."
            )

        self._fecha = valor

    @property
    def valor_compra(self) -> float:
        """Devuelve el valor de compra."""
        return self._valor_compra

    @valor_compra.setter
    def valor_compra(self, valor: float) -> None:
        """Valida y establece el valor de compra."""
        if (
            isinstance(valor, bool)
            or not isinstance(valor, (int, float))
            or not isfinite(valor)
            or valor <= 0
        ):
            raise ValueError(
                "El valor de compra debe ser mayor que cero."
            )

        if (
            hasattr(self, "_valor_venta")
            and valor > self._valor_venta
        ):
            raise ValueError(
                "El valor de compra no puede superar "
                "el valor de venta."
            )

        self._valor_compra = float(valor)

    @property
    def valor_venta(self) -> float:
        """Devuelve el valor de venta."""
        return self._valor_venta

    @valor_venta.setter
    def valor_venta(self, valor: float) -> None:
        """Valida y establece el valor de venta."""
        if (
            isinstance(valor, bool)
            or not isinstance(valor, (int, float))
            or not isfinite(valor)
            or valor <= 0
        ):
            raise ValueError(
                "El valor de venta debe ser mayor que cero."
            )

        if (
            hasattr(self, "_valor_compra")
            and valor < self._valor_compra
        ):
            raise ValueError(
                "El valor de venta no puede ser menor "
                "que el valor de compra."
            )

        self._valor_venta = float(valor)

    def __str__(self) -> str:
        """Devuelve una representación de la cotización."""
        return (
            f"Cotización: {self.tipo_cotizacion.nombre} - "
            f"Fecha: {self.fecha} - "
            f"Compra: {self.valor_compra:.2f} - "
            f"Venta: {self.valor_venta:.2f}"
        )
