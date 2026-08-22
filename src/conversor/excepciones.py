"""Errores de dominio del conversor."""


class ErrorConversor(Exception):
    """Error base del conversor de divisas."""


class DivisaNoSoportadaError(ErrorConversor):
    """La divisa no existe en el catálogo."""

    def __init__(self, codigo: str) -> None:
        self.codigo = codigo
        super().__init__(f"Divisa no soportada en el catálogo: {codigo}")


class TasaCeroError(ZeroDivisionError, ErrorConversor):
    """La tasa de la divisa origen es cero; no se puede convertir."""

    def __init__(self, codigo: str) -> None:
        self.codigo = codigo
        super().__init__(
            f"División por cero: la tasa de {codigo} no puede ser 0"
        )
