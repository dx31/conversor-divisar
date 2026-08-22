"""Interfaz de línea de comandos del conversor."""

from __future__ import annotations

import argparse
import sys
from decimal import Decimal, InvalidOperation

from conversor.convertidor import ConvertidorDivisas
from conversor.excepciones import ErrorConversor


def construir_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="conversor",
        description="Convierte montos entre divisas del catálogo y guarda el historial.",
    )
    sub = parser.add_subparsers(dest="comando")

    conv = sub.add_parser("convertir", help="Convertir un monto")
    conv.add_argument("monto", help="Cantidad a convertir")
    conv.add_argument("origen", help="Código ISO de origen, p. ej. USD")
    conv.add_argument("destino", help="Código ISO de destino, p. ej. PEN")

    sub.add_parser("divisas", help="Listar divisas soportadas")
    return parser


def ejecutar(argv: list[str] | None = None) -> int:
    parser = construir_parser()
    args = parser.parse_args(argv)
    convertidor = ConvertidorDivisas()

    if args.comando == "divisas":
        for codigo in sorted(convertidor.catalogo.codigos()):
            divisa = convertidor.catalogo.obtener(codigo)
            print(f"{divisa.codigo}\t{divisa.nombre}\t{divisa.unidades_por_usd} por USD")
        return 0

    if args.comando != "convertir":
        parser.print_help()
        return 1

    try:
        monto = Decimal(args.monto)
    except InvalidOperation:
        print(f"Monto inválido: {args.monto}", file=sys.stderr)
        return 2

    try:
        resultado = convertidor.convertir(monto, args.origen, args.destino)
    except (ErrorConversor, ZeroDivisionError) as exc:
        print(str(exc), file=sys.stderr)
        return 3

    print(f"{monto} {args.origen.upper()} = {resultado} {args.destino.upper()}")
    return 0


def main() -> None:
    sys.exit(ejecutar())


if __name__ == "__main__":
    main()
