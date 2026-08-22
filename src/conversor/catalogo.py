"""Catálogo de divisas y tasas respecto al USD."""

from dataclasses import dataclass
from decimal import Decimal

from conversor.excepciones import DivisaNoSoportadaError


@dataclass(frozen=True)
class Divisa:
    codigo: str
    nombre: str
    unidades_por_usd: Decimal
    decimales: int = 2


CATALOGO_POR_DEFECTO = {
    "USD": Divisa("USD", "Dólar estadounidense", Decimal("1"), 2),
    "MXN": Divisa("MXN", "Peso mexicano", Decimal("17.15"), 2),
    "EUR": Divisa("EUR", "Euro", Decimal("0.92"), 2),
    "GBP": Divisa("GBP", "Libra esterlina", Decimal("0.78"), 2),
    "JPY": Divisa("JPY", "Yen japonés", Decimal("149.50"), 0),
    "CAD": Divisa("CAD", "Dólar canadiense", Decimal("1.36"), 2),
}


class CatalogoDivisas:
    """Registro de divisas soportadas. Las tasas son unidades de esa divisa por 1 USD."""

    def __init__(self, divisas: dict[str, Divisa] | None = None) -> None:
        origen = divisas if divisas is not None else CATALOGO_POR_DEFECTO
        self._divisas = {codigo.upper(): divisa for codigo, divisa in origen.items()}

    def soporta(self, codigo: str) -> bool:
        return codigo.upper() in self._divisas

    def obtener(self, codigo: str) -> Divisa:
        clave = codigo.upper()
        if clave not in self._divisas:
            raise DivisaNoSoportadaError(clave)
        return self._divisas[clave]

    def tasa(self, codigo: str) -> Decimal:
        return self.obtener(codigo).unidades_por_usd

    def decimales(self, codigo: str) -> int:
        return self.obtener(codigo).decimales

    def codigos(self) -> frozenset[str]:
        return frozenset(self._divisas)
