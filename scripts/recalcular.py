#!/usr/bin/env python3
"""Recalcula precios segun reglas.md. Deterministico y testeable.

Lee:   data/costos.csv, data/parametros.json
Emite: outputs/nueva_lista.csv, outputs/anomalias.json
Imprime un diff legible por consola. No publica nada.
"""
import csv
import json
import math
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
DATA = BASE / "data"
OUT = BASE / "outputs"


def redondear_arriba_100(valor: float) -> int:
    return int(math.ceil(valor / 100.0) * 100)


def cargar_parametros() -> dict:
    return json.loads((DATA / "parametros.json").read_text(encoding="utf-8"))


def cargar_costos() -> list[dict]:
    with (DATA / "costos.csv").open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def calcular(p: dict) -> tuple[list[dict], list[dict]]:
    tc = p["tipo_cambio"]
    arancel = p["arancel"]
    margenes = p["margenes"]
    umbral_var = p["umbral_variacion"]
    umbral_margen = p["umbral_margen_minimo"]
    factor_ml = p["factor_mercadolibre"]

    filas, anomalias = [], []
    for prod in cargar_costos():
        costo_usd = float(prod["costo_usd"])
        cat = prod["categoria"].strip().upper()
        precio_actual = float(prod["precio_actual"])
        margen = margenes[cat]

        costo_ars = costo_usd * tc * (1 + arancel)
        precio_bruto = costo_ars / (1 - margen)
        precio_venta = redondear_arriba_100(precio_bruto)
        precio_ml = redondear_arriba_100(precio_venta * factor_ml)

        variacion = (precio_venta - precio_actual) / precio_actual if precio_actual else 0.0
        margen_efectivo = (precio_venta - costo_ars) / precio_venta

        flags = []
        if abs(variacion) > umbral_var:
            flags.append("VARIACION")
        if margen_efectivo < umbral_margen:
            flags.append("MARGEN_BAJO")

        fila = {
            "sku": prod["sku"],
            "nombre": prod["nombre"],
            "categoria": cat,
            "costo_ars": round(costo_ars, 2),
            "precio_actual": int(precio_actual),
            "precio_venta": precio_venta,
            "precio_ml": precio_ml,
            "variacion_pct": round(variacion * 100, 1),
            "margen_efectivo_pct": round(margen_efectivo * 100, 1),
        }
        filas.append(fila)
        if flags:
            anomalias.append({**fila, "flags": flags})
    return filas, anomalias


def escribir_outputs(filas: list[dict], anomalias: list[dict]) -> None:
    OUT.mkdir(exist_ok=True)
    campos = ["sku", "nombre", "categoria", "costo_ars", "precio_actual",
              "precio_venta", "precio_ml", "variacion_pct", "margen_efectivo_pct"]
    with (OUT / "nueva_lista.csv").open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=campos)
        w.writeheader()
        w.writerows(filas)
    (OUT / "anomalias.json").write_text(
        json.dumps(anomalias, ensure_ascii=False, indent=2), encoding="utf-8")


def imprimir_diff(p: dict, filas: list[dict], anomalias: list[dict]) -> None:
    print(f"Tipo de cambio: {p['tipo_cambio']}  |  Arancel: {p['arancel']*100:.0f}%")
    print("-" * 78)
    print(f"{'SKU':<7}{'PRODUCTO':<28}{'ACTUAL':>10}{'NUEVO':>10}{'VAR%':>8}{'':>5}")
    print("-" * 78)
    for r in filas:
        marca = " <-" if any(a["sku"] == r["sku"] for a in anomalias) else ""
        print(f"{r['sku']:<7}{r['nombre'][:27]:<28}"
              f"{r['precio_actual']:>10,}{r['precio_venta']:>10,}"
              f"{r['variacion_pct']:>7.1f}%{marca:>5}")
    print("-" * 78)
    print(f"Productos: {len(filas)}  |  Anomalias (revisar): {len(anomalias)}")
    print("Archivos: outputs/nueva_lista.csv  outputs/anomalias.json")


def main() -> None:
    p = cargar_parametros()
    filas, anomalias = calcular(p)
    escribir_outputs(filas, anomalias)
    imprimir_diff(p, filas, anomalias)


if __name__ == "__main__":
    main()
