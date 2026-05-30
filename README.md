# carpeta_trabajador — Rol: Precios (prueba conceptual)

Esta es una **carpeta-agente** segun el modelo agent-native. Entra aca con tu
agente y pedile tareas en lenguaje natural. El ya sabe que hace porque su
frontera esta escrita en `contexto.md` y sus reglas en `reglas.md`.

## Estructura
```
carpeta_trabajador/
├── contexto.md      # quien soy: que hago y que NO hago
├── reglas.md        # las reglas de calculo (auditable)
├── data/
│   ├── costos.csv       # productos: costo USD, categoria, precio vigente
│   └── parametros.json  # tipo de cambio, arancel, margenes, umbrales
├── scripts/
│   └── recalcular.py    # la aritmetica determinista (corre solo)
├── prompts/
│   └── revisar_anomalias.md  # lo unico que juzga el agente
└── outputs/         # resultados: nueva_lista.csv + anomalias.json
```

## Tareas que le podes pedir
- "Recalcula los precios" → corre el script y te muestra el diff.
- "Que productos tienen anomalias y por que?" → te explico cada uno.
- "Subio el dolar a 1300, recalcula" → cambio el parametro y recalculo.
- "Agrega un producto nuevo: X, costo USD 20, categoria B" → lo sumo y recalculo.
- "Armame el resumen para aprobar" → te redacto el resumen tipo PR.

## Correr a mano (sin agente)
```
python scripts/recalcular.py
```
