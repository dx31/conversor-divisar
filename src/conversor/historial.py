"""Historial de transacciones de conversión."""

from dataclasses import dataclass
from datetime import datetime, timezone
from decimal import Decimal


@dataclass(frozen=True)
class Transaccion:
    origen: str
    destino: str
    monto: Decimal
    resultado: Decimal
    marca_tiempo: datetime


class HistorialConversiones:
    """Almacén en memoria de conversiones realizadas."""

    def __init__(self) -> None:
        self._transacciones: list[Transaccion] = []

    def guardar(self, transaccion: Transaccion) -> None:
        self._transacciones.append(transaccion)

    def registrar(
        self,
        origen: str,
        destino: str,
        monto: Decimal,
        resultado: Decimal,
        marca_tiempo: datetime | None = None,
    ) -> Transaccion:
        transaccion = Transaccion(
            origen=origen.upper(),
            destino=destino.upper(),
            monto=monto,
            resultado=resultado,
            marca_tiempo=marca_tiempo or datetime.now(timezone.utc),
        )
        self.guardar(transaccion)
        return transaccion

    def listar(self) -> tuple[Transaccion, ...]:
        return tuple(self._transacciones)

    def __len__(self) -> int:
        return len(self._transacciones)

    def vaciar(self) -> None:
        self._transacciones.clear()
