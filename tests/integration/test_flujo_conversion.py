from decimal import Decimal

import pytest

from conversor.catalogo import CatalogoDivisas
from conversor.convertidor import ConvertidorDivisas
from conversor.historial import HistorialConversiones, Transaccion


@pytest.fixture
def convertidor() -> ConvertidorDivisas:
    return ConvertidorDivisas(
        catalogo=CatalogoDivisas(),
        historial=HistorialConversiones(),
    )


@pytest.mark.integration
def test_flujo_conversion_guarda_transaccion(convertidor: ConvertidorDivisas):
    resultado = convertidor.convertir(Decimal("100"), "USD", "MXN")

    assert resultado == Decimal("1715.00")
    historial = convertidor.historial_transacciones()
    assert len(historial) == 1

    tx = historial[0]
    assert isinstance(tx, Transaccion)
    assert tx.origen == "USD"
    assert tx.destino == "MXN"
    assert tx.monto == Decimal("100")
    assert tx.resultado == Decimal("1715.00")
    assert tx.marca_tiempo is not None


@pytest.mark.integration
def test_flujo_varias_conversiones_acumulan_historial(
    convertidor: ConvertidorDivisas,
):
    convertidor.convertir("10", "EUR", "USD")
    convertidor.convertir("200", "MXN", "USD")
    convertidor.convertir("1", "USD", "JPY")

    historial = convertidor.historial_transacciones()
    assert len(historial) == 3
    assert [tx.destino for tx in historial] == ["USD", "USD", "JPY"]


@pytest.mark.integration
def test_conversion_inversa_aproxima_el_monto_original(
    convertidor: ConvertidorDivisas,
):
    ida = convertidor.convertir(Decimal("100"), "USD", "EUR")
    vuelta = convertidor.convertir(ida, "EUR", "USD")
    assert abs(vuelta - Decimal("100")) <= Decimal("0.02")


@pytest.mark.integration
def test_yen_redondea_sin_decimales(convertidor: ConvertidorDivisas):
    resultado = convertidor.convertir(Decimal("1"), "USD", "JPY")
    assert resultado == Decimal("150")
    assert convertidor.historial_transacciones()[0].resultado == Decimal("150")


@pytest.mark.integration
def test_convertir_sin_registrar_deja_historial_vacio(
    convertidor: ConvertidorDivisas,
):
    convertidor.convertir(Decimal("5"), "USD", "CAD", registrar=False)
    assert len(convertidor.historial) == 0
