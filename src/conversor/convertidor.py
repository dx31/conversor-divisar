"""Servicio de conversión: usa el catálogo, funciones puras e historial."""

from decimal import Decimal

from conversor.catalogo import CatalogoDivisas
from conversor.historial import HistorialConversiones, Transaccion
from conversor.money import dividir_por_tasa, multiplicar_por_tasa, redondear_monto


class ConvertidorDivisas:
    def __init__(
        self,
        catalogo: CatalogoDivisas | None = None,
        historial: HistorialConversiones | None = None,
    ) -> None:
        self.catalogo = catalogo or CatalogoDivisas()
        self.historial = historial or HistorialConversiones()

    def convertir(
        self,
        monto: Decimal | int | str | float,
        origen: str,
        destino: str,
        registrar: bool = True,
    ) -> Decimal:
        """Convierte un monto. Fórmula: (monto / tasa_origen) * tasa_destino, redondeado."""
        cantidad = Decimal(str(monto))
        divisa_origen = self.catalogo.obtener(origen)
        divisa_destino = self.catalogo.obtener(destino)

        en_usd = dividir_por_tasa(
            cantidad, divisa_origen.unidades_por_usd, divisa_origen.codigo
        )
        bruto = multiplicar_por_tasa(en_usd, divisa_destino.unidades_por_usd)
        resultado = redondear_monto(bruto, divisa_destino.decimales)

        if registrar:
            self.historial.registrar(
                origen=divisa_origen.codigo,
                destino=divisa_destino.codigo,
                monto=cantidad,
                resultado=resultado,
            )
        return resultado

    def historial_transacciones(self) -> tuple[Transaccion, ...]:
        return self.historial.listar()
