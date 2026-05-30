# Prompt: revisar anomalias (lo unico que juzga el agente)

Recibis `outputs/anomalias.json`. Para cada producto marcado:

- Explica en una linea la causa probable de la variacion.
- Clasifica: [ESPERADA] / [REVISAR] / [ERROR].
- Redacta el cuerpo del resumen para el humano: que cambio en general y que
  conviene mirar puntualmente.

NO modifiques precios. NO inventes numeros. Solo explicas y resumis a partir de
lo que el script ya calculo. Si necesitas un numero, sale del output del script.

Formato del resumen esperado:

> **Resumen de recalculo**
> Subio todo ~X% por <causa>. Revisar puntualmente: <SKUs y motivo>.
> Resto dentro de lo normal. Listo para aprobar.
