# Spec: Procesamiento de Work Orders (WO) — `mrp.production`

 se usa el modelo nativo `mrp.production`, heredado, **una instancia por producto terminado**. Todo lo que sigue está tomado tal cual del diseño que pasaste; donde agrego una observación o un punto sin cerrar, lo marco explícitamente como tal — no es parte de tu texto original.

---

## 0. Problema y enfoque general

**Problema de origen:** la interfaz estándar de Odoo permite que usuarios finales manipulen las WOs, y `mrp.production` no soporta de forma nativa:
- asignar una WO de Metrics con múltiples productos terminados sin duplicar la orden,
- restringir la imputación de consumos a que dependa de disponibilidad de stock y facturación previa de lotes.

**Enfoque:** desacoplar la recepción del XML de Metrics generando internamente **una `mrp.production` por cada producto terminado** de la WO, y mover el control de consumo/cierre a nivel de código Python, restringiendo el acceso de la vista al usuario Bot integrador.

### Cambios de modelo transversales (aplican a todas las etapas)

| Elemento | Detalle |
|---|---|
| Campo nuevo | `x_metrics_wo_number` (Char, indexado) en `mrp.production` — guarda el `wonumber` de Metrics |
| Vista | `x_metrics_wo_number` visible en la vista lista (tree view) de `mrp.production` |
| Permisos | Solo el usuario Bot de integración puede crear, editar y confirmar `mrp.production`. Usuarios normales: solo lectura/reportes. |

**Nota (no es parte de tu texto, es una observación mía):** como una misma WO (`wonumber`) puede generar **varias** `mrp.production` (una por producto terminado), `x_metrics_wo_number` deja de ser único por registro — va a haber múltiplas filas con el mismo valor. Esto está bien para trazabilidad, pero cualquier búsqueda/validación por `wonumber` debe devolver una lista, no un único registro. Marco esto como punto a tener en cuenta en el código, no como gap funcional.

---

## Etapa 1 — Recepción de la WO

### Objetivo
Al llegar el XML de WO (`sdiwoworkorder`), crear en Odoo una `mrp.production` por cada producto terminado, con las materias primas ya prorrateadas, sin bloquear la confirmación por falta de stock.

### Trigger
XML `sdiwoworkorder` con uno o más `sdiwofinisheditem`.

### Lógica

1. Si la WO trae **más de un** producto terminado (`sdilwofinisheditem.lcount > 1`), crear **una `mrp.production` por producto**, todas con el mismo `x_metrics_wo_number`.
2. Distribuir cada materia prima (`sdiworawmaterial`) entre las `mrp.production` generadas, en proporción a la cantidad planificada de cada producto terminado sobre el total de la WO (regla de tres simple — ya definida como regla cerrada en `metrics_compras_spec.md`, sección 5.3):

$$\text{Cantidad MP Asignada} = \frac{\text{Cantidad MP Total} \times \text{Cantidad Producto WO Current}}{\text{Cantidad Total Productos WO Metrics}}$$

3. Redondeo: aplicar `round()` según la precisión decimal de la UOM del componente. El **residuo de redondeo se asigna al último registro procesado** (última WO/producto generado), para que la suma total del prorrateo cierre exacto contra la cantidad total de materia prima informada por Metrics.
4. La WO debe poder **guardarse y confirmarse** aunque las materias primas no tengan stock disponible (no se bloquea por disponibilidad en esta etapa).

### Mapeo de campos

| Campo Metrics | Campo Odoo |
|---|---|
| `wonumber` | `x_metrics_wo_number` |

### Criterios de aceptación

- [ ] El campo `x_metrics_wo_number` es visible en la vista de lista (tree view) de `mrp.production`.
- [ ] Al ingresar un XML de WO con 2+ productos terminados, se crea una `mrp.production` independiente por cada producto, conservando el mismo `x_metrics_wo_number`.
- [ ] La distribución de materias primas entre las WOs generadas respeta la proporción de cada producto; los residuos de redondeo se asignan a la última WO/producto generado.
- [ ] La WO puede guardarse y confirmarse aun si las materias primas no tienen stock disponible.
- [ ] Un usuario regular (no Bot) no puede crear, editar ni confirmar `mrp.production` — solo visualizar y extraer reportes.

---

## Etapa 2 — Consumo de materia prima

### Objetivo
Que el consumo real de materia prima en Odoo quede condicionado a: (a) disponibilidad de stock, y (b) si el producto valúa por lote, a que la factura de esa materia prima esté contabilizada. El consumo **no** debe autocompletarse por defecto — solo debe reflejarse cuando llega el XML de consumo correspondiente.

### Trigger
XML `sdistktransaction` con `transactiontype="0"` (**"Atención/devolución de Solicitud de materia prima"** — este es el mismo código que ya está documentado en la tabla de `TransactionType` de `AGENTS.md`/manual, no es un valor nuevo inventado para este flujo).

### Lógica

1. Al recibir el XML de consumo, **validar antes de procesar**:
   - que la materia prima tenga stock disponible;
   - si el producto valúa por lote, que la materia prima tenga factura registrada en estado `posted`.
2. Si falta stock, o el lote de materia prima no está facturado (en valuación por lote), **la transacción se frena y devuelve un error controlado de validación** — no se procesa parcialmente.
3. **Manejo del error (confirmado):** la transacción **queda en cola para reintento**, hasta que se resuelva el inconveniente (llegue el stock, o se contabilice la factura). No se descarta ni requiere reproceso manual.
4. Evitar el comportamiento por defecto de Odoo de marcar automáticamente los componentes como "Consumido" al confirmar/procesar la orden (ver conversación anterior sobre el campo "Consumido" y la opción de Consumo manual de la BoM). El consumo solo se actualiza formalmente cuando llega este XML.

### Mapeo de campos

| Campo Metrics | Campo Odoo |
|---|---|
| `wonumber` | `x_metrics_wo_number` |
| `lot` | Lote del componente (`stock.lot`) |
| `quantity` | Cantidad a consumir en la línea de componentes (`stock.move`) |

**Punto sin cerrar (observación mía, no es parte de tu texto):** como una misma `wonumber` puede corresponder a varias `mrp.production` (una por producto, desde la Etapa 1), el mapeo `wonumber → x_metrics_wo_number` por sí solo no alcanza para identificar en cuál de esas producciones hay que imputar el consumo cuando llega el XML de esta etapa. Supongo que el criterio adicional es cruzar por `stockcode` de la materia prima contra las líneas de componente ya creadas en cada `mrp.production` del grupo — pero esto no está explicitado en tu diseño y prefiero que lo confirmes antes de que quede como regla implícita.

### Criterios de aceptación

- [ ] Al recibir el XML de consumo, el sistema valida que el stock esté disponible; si falta stock o el lote de materia prima no está facturado (en valuación por lote), la transacción frena y devuelve un error controlado de validación.
- [ ] Ante ese error, la transacción queda en cola para reintento automático (no se descarta ni requiere reproceso manual), hasta que se resuelva el inconveniente de stock o facturación.
- [ ] El consumo de materia prima no se marca como ejecutado/consumido en Odoo hasta que no se procesa explícitamente el XML de consumo correspondiente.

---

## Etapa 3 — Producto terminado

### Objetivo
Al recibir el XML de producto terminado, actualizar la cantidad realmente producida, asignar el lote recibido, y cerrar la WO.

### Trigger
XML `sdistktransaction` con `transactiontype="1"` (**"Entrega de producción"** — coincide con el valor ya documentado y usado en el resto del proyecto, ej. `STK - Entrega Producción`).

### Lógica

1. Actualizar la cantidad producida.
2. Asignar/crear el número de lote recibido en el XML.
3. Ejecutar la acción del botón `button_mark_done` para finalizar la WO (deja la `mrp.production` en estado `done`).

### Mapeo de campos

| Campo Metrics | Campo Odoo |
|---|---|
| `wonumber` | `x_metrics_wo_number` |
| `quantity` | `qty_producing` |
| `lot` | `lot_producing_id` |

**Misma observación que en Etapa 2**, aplicada acá: si hay varias `mrp.production` con el mismo `x_metrics_wo_number` (una por producto terminado), hace falta un criterio adicional (probablemente `stockcode` del producto terminado) para identificar a cuál de ellas corresponde este XML puntual. No lo doy por resuelto solo, lo marco para que lo confirmes.

### Criterios de aceptación

- [ ] Al procesar el XML de producto terminado, se actualiza la cantidad real producida, se asigna/crea el lote indicado, y se invoca con éxito `button_mark_done`, dejando la WO en estado `done`.

---

## Resumen de puntos a confirmar (no resueltos por tu texto original)

| # | Punto | Etapa afectada | Estado |
|---|---|---|---|
| 1 | Múltiples `mrp.production` comparten el mismo `x_metrics_wo_number` — ¿cómo se identifica la instancia correcta al llegar el XML de consumo o de producto terminado? Supuesto: por `stockcode` cruzado contra las líneas ya creadas. | Etapa 2 y 3 | Abierto |
| 2 | El manejo de errores de validación en Etapa 2 (stock insuficiente / factura no `posted`) | Etapa 2 | **Cerrado: queda en cola para reintento hasta resolver el inconveniente** |
