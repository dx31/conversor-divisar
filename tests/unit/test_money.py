from decimal import Decimal

import pytest

from conversor.excepciones import TasaCeroError
from conversor.money import dividir_por_tasa, multiplicar_por_tasa, redondear_monto


@pytest.mark.unit
@pytest.mark.parametrize(
    ("monto", "tasa", "esperado"),
    [
        (Decimal("100"), Decimal("17.15"), Decimal("1715.00")),
        (Decimal("0"), Decimal("17.15"), Decimal("0.00")),
        (Decimal("50"), Decimal("1"), Decimal("50")),
        (Decimal("10.50"), Decimal("0.92"), Decimal("9.660")),
        (Decimal("1"), Decimal("149.50"), Decimal("149.50")),
    ],
)
def test_multiplicar_por_tasa(monto, tasa, esperado):
    assert multiplicar_por_tasa(monto, tasa) == esperado


@pytest.mark.unit
def test_multiplicar_no_modifica_entradas():
    monto = Decimal("25")
    tasa = Decimal("2")
    multiplicar_por_tasa(monto, tasa)
    assert monto == Decimal("25")
    assert tasa == Decimal("2")


@pytest.mark.unit
@pytest.mark.parametrize(
    ("monto", "decimales", "esperado"),
    [
        (Decimal("10.125"), 2, Decimal("10.13")),
        (Decimal("10.124"), 2, Decimal("10.12")),
        (Decimal("10.5"), 0, Decimal("11")),
        (Decimal("10.4"), 0, Decimal("10")),
        (Decimal("1.225"), 2, Decimal("1.23")),
        (Decimal("100"), 2, Decimal("100.00")),
        (Decimal("149.6"), 0, Decimal("150")),
    ],
)
def test_redondear_monto(monto, decimales, esperado):
    assert redondear_monto(monto, decimales) == esperado


@pytest.mark.unit
def test_redondear_rechaza_decimales_negativos():
    with pytest.raises(ValueError, match="negativos"):
        redondear_monto(Decimal("1"), -1)


@pytest.mark.unit
def test_dividir_por_tasa_normal():
    assert dividir_por_tasa(Decimal("1715"), Decimal("17.15")) == Decimal("100")


@pytest.mark.unit
def test_dividir_por_tasa_cero_lanza_zero_division():
    with pytest.raises(ZeroDivisionError):
        dividir_por_tasa(Decimal("100"), Decimal("0"), "MXN")


@pytest.mark.unit
def test_dividir_por_tasa_cero_es_tasa_cero_error():
    with pytest.raises(TasaCeroError, match="MXN"):
        dividir_por_tasa(Decimal("100"), Decimal("0"), "MXN")
