"""Conversor de divisas con catálogo, historial y funciones puras de cambio."""

from conversor.catalogo import CatalogoDivisas, CATALOGO_POR_DEFECTO
from conversor.convertidor import ConvertidorDivisas
from conversor.excepciones import DivisaNoSoportadaError, TasaCeroError
from conversor.historial import HistorialConversiones, Transaccion
from conversor.money import dividir_por_tasa, multiplicar_por_tasa, redondear_monto

__all__ = [
    "CATALOGO_POR_DEFECTO",
    "CatalogoDivisas",
    "ConvertidorDivisas",
    "DivisaNoSoportadaError",
    "HistorialConversiones",
    "TasaCeroError",
    "Transaccion",
    "dividir_por_tasa",
    "multiplicar_por_tasa",
    "redondear_monto",
]
