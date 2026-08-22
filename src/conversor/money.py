"""Funciones puras de multiplicación de cambio, división y redondeo."""

from decimal import Decimal, ROUND_HALF_UP

from conversor.excepciones import TasaCeroError


def multiplicar_por_tasa(monto: Decimal, tasa: Decimal) -> Decimal:
    """Aplica una tasa de cambio por multiplicación. No tiene efectos laterales."""
    return monto * tasa


def dividir_por_tasa(monto: Decimal, tasa: Decimal, codigo: str = "") -> Decimal:
    """Convierte a la moneda base dividiendo por la tasa de origen.

    Lanza TasaCeroError (también es ZeroDivisionError) si la tasa es 0.
    """
    if tasa == 0:
        raise TasaCeroError(codigo or "?")
    return monto / tasa


def redondear_monto(monto: Decimal, decimales: int = 2) -> Decimal:
    """Redondea un monto monetario con HALF_UP (1.225 -> 1.23)."""
    if decimales < 0:
        raise ValueError("Los decimales de redondeo no pueden ser negativos")
    unidad = Decimal("1").scaleb(-decimales)
    return monto.quantize(unidad, rounding=ROUND_HALF_UP)
