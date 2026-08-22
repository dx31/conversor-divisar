from decimal import Decimal

import pytest

from conversor.catalogo import CatalogoDivisas, Divisa
from conversor.convertidor import ConvertidorDivisas
from conversor.excepciones import DivisaNoSoportadaError, TasaCeroError
from conversor.historial import HistorialConversiones


def catalogo_con_tasa_cero() -> CatalogoDivisas:
    return CatalogoDivisas(
        {
            "USD": Divisa("USD", "Dólar", Decimal("1"), 2),
            "ZZZ": Divisa("ZZZ", "Tasa inválida", Decimal("0"), 2),
        }
    )


@pytest.mark.unit
def test_divisa_destino_no_soportada():
    convertidor = ConvertidorDivisas()
    with pytest.raises(DivisaNoSoportadaError, match="XYZ") as exc:
        convertidor.convertir(Decimal("10"), "USD", "XYZ")
    assert exc.value.codigo == "XYZ"


@pytest.mark.unit
def test_divisa_origen_no_soportada():
    convertidor = ConvertidorDivisas()
    with pytest.raises(DivisaNoSoportadaError, match="BTC"):
        convertidor.convertir(Decimal("10"), "BTC", "USD")


@pytest.mark.unit
def test_divisa_no_soportada_no_guarda_historial():
    historial = HistorialConversiones()
    convertidor = ConvertidorDivisas(historial=historial)
    with pytest.raises(DivisaNoSoportadaError):
        convertidor.convertir(Decimal("10"), "USD", "AAA")
    assert len(historial) == 0


@pytest.mark.unit
def test_catalogo_soporta_solo_codigos_conocidos():
    catalogo = CatalogoDivisas()
    assert catalogo.soporta("mxn")
    assert not catalogo.soporta("XYZ")


@pytest.mark.unit
def test_division_por_cero_al_convertir_con_tasa_origen_cero():
    convertidor = ConvertidorDivisas(catalogo=catalogo_con_tasa_cero())
    with pytest.raises(ZeroDivisionError):
        convertidor.convertir(Decimal("50"), "ZZZ", "USD")


@pytest.mark.unit
def test_tasa_cero_expone_el_codigo_de_divisa():
    convertidor = ConvertidorDivisas(catalogo=catalogo_con_tasa_cero())
    with pytest.raises(TasaCeroError, match="ZZZ") as exc:
        convertidor.convertir("50", "ZZZ", "USD")
    assert exc.value.codigo == "ZZZ"


@pytest.mark.unit
def test_tasa_cero_no_guarda_historial():
    historial = HistorialConversiones()
    convertidor = ConvertidorDivisas(
        catalogo=catalogo_con_tasa_cero(),
        historial=historial,
    )
    with pytest.raises(TasaCeroError):
        convertidor.convertir(Decimal("50"), "ZZZ", "USD")
    assert len(historial) == 0
