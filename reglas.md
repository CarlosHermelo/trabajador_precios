# Reglas de calculo (lo deterministico -> va a codigo)

Estas reglas estan implementadas en `scripts/recalcular.py`. Estan escritas aca
para que sean auditables por un humano sin leer codigo.

1. `costo_ARS = costo_USD * tipo_cambio * (1 + arancel)`
2. `precio_venta = costo_ARS / (1 - margen_categoria)`
3. Margenes por categoria: A = 0.45 · B = 0.38 · C = 0.30
4. Redondeo del precio a multiplo de 100 **hacia arriba**.
5. ALERTA si la variacion vs. el precio actual es **mayor a 15%**.
6. ALERTA si el margen efectivo (tras redondeo) queda **por debajo de 0.25**.
7. `precio_ML = precio_venta * 1.13`  (comision + envio de Mercado Libre)

El script hace ~95% del trabajo y es 100% testeable: lee inputs, aplica reglas,
compara contra el precio vigente y emite la nueva lista, las anomalias y un diff.
No publica nada: solo escribe archivos en `outputs/`.
