# Conversor de divisas

Convierte montos entre divisas de un catálogo fijo, redondea el resultado y guarda cada operación en un historial. Incluye pruebas unitarias, de integración, cobertura con pytest-cov y un workflow de GitHub Actions.

## Requisitos cubiertos

| Tipo | Qué cubre |
| --- | --- |
| Pruebas unitarias | Funciones puras `multiplicar_por_tasa` y `redondear_monto` |
| Pruebas de integración | Flujo `convertir` → transacción guardada en historial |
| Cobertura (pytest-cov) | División por cero (tasa origen = 0) y divisas fuera del catálogo |
| CI | GitHub Actions: unitarias, integración y `cov-fail-under=90` |

## Instalación

```bash
cd conversor-divisas
python -m pip install -e ".[dev]"
```

## Uso

```bash
python -m conversor convertir 100 USD MXN
python -m conversor divisas
```

Tasas del catálogo (unidades de cada divisa por 1 USD): USD 1, MXN 17.15, EUR 0.92, GBP 0.78, JPY 149.50, CAD 1.36.

La conversión es `(monto / tasa_origen) * tasa_destino`, redondeada con HALF_UP. El yen no usa decimales.

## Pruebas

```bash
pytest tests/unit -v -m unit
pytest tests/integration -v -m integration
pytest --cov=conversor --cov-report=term-missing --cov-fail-under=90
```

Los casos de cobertura están en `tests/unit/test_casos_borde.py`: `TasaCeroError` / `ZeroDivisionError` y `DivisaNoSoportadaError`.

## GitHub Actions

El workflow `.github/workflows/ci.yml` corre en cada push y pull request (Python 3.11 y 3.12). Para activarlo, inicializa git **dentro de esta carpeta** (para que `.github/` quede en la raíz del repositorio) y súbelo a GitHub:

```bash
cd conversor-divisas
git init
git add .
git commit -m "Conversor de divisas con pruebas y CI"
git branch -M main
git remote add origin <url-de-tu-repo>
git push -u origin main
```
