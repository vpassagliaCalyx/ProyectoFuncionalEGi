# HU: Recepción de Órdenes de Compra desde METRICS (POR)

**Convenciones:**

- **\[DEF\]** = lo definiste vos en la conversación.
- **\[MAN\]** = viene del manual de METRICS (rev. 93, sección 11.33) o de la muestra 07.
- **\[PROP\]** = propuesta mía, a confirmar.
- **\[PEND\]** = depende de un dato que falta.

No tengo la documentación de tu versión de Odoo. Los nombres de campo del bloque 2.A son los de tu HU original. Los que agrego yo van "a confirmar".

---

## 1. Resumen funcional

Procesar mensajes XML de METRICS (contexto POR: INSERT, UPDATE, DELETE) para crear y mantener órdenes de compra en Odoo (`purchase.order`) de forma automatizada. Las OC son de **solo lectura para los usuarios en la UI**. Solo el usuario Bot de integración las crea y modifica 

Esta HU no vincula la OC con la WO mediante campos propios. La WO usa `mrp.production` nativo y consulta las compras pendientes por materia prima y lote en su propia validación de cierre 

---

## 2. Diseño técnico

### A. Mapeo de campos

**Cabecera (`purchase.order`)**

| Metrics | Odoo | Notas |
| --- | --- | --- |
| `purchaseordernumber` (Int) | Clave de integración, ver RN-01 | \ campo propio |
| `suppliercode` | `partner_id` | Búsqueda en `res.partner` por `ref`. Los proveedores existen en ambos sistemas  |
| `emissiondt` | `date_order` |  |
| `limitreceiptdt` (cabecera) | `date_planned` | Informativa, no bloquea|
| `conditioncode` | `payment_term_id` | Búsqueda por **nombre**; si no existe, se crea |
| `sdiporpaycondduedate` (`duedate`, `value`) | Vencimientos de la OC | Se guardan como informativos |
| `idcurrency` (cabecera) | Moneda de la PO (`currency_id`, a confirmar) | 
| `totalvalue` | Solo para el control RN-14 | No se carga como total |
| `situation`, `status` | Informativos | \[DEF\] Odoo no tiene "cerrada" | (ver si es recomendable agregar estados)
|

**Líneas (`purchase.order.line`)**

| Metrics | Odoo | Notas |
| --- | --- | --- |
| `stockcode` | `product_id` | Búsqueda por `default_code` |
| `quantity` | `product_qty` |  |
| `unitcode` | `product_uom` | Ver pendiente de unidades |
| `unitvalue` / `unitvalue_foreigncurrency` | `price_unit` | Ver RN-13 |
| `limitreceiptdt` (línea) | `date_planned` de la línea | Informativa  |
| `idcurrency`, `exchangerate`, `exchangeratedt` (línea) | Moneda y tasa | Ver RN-12 a RN-14 |
| `totalreceiptqty`, `status` (línea), `sdiporitemreceiptinfo` | No se procesan |  la recepción llega por REC/STK, no por la OC |
| `transportcost`, `othercosts` | Sin definir | \[PEND\] |
| Impuestos | Los del producto (stock item) | \[DEF\] |

### B. Reglas de negocio

**Identificación y operaciones**

- **RN-01 \[PROP\]** La clave de integración es `idcompany` + `purchaseordernumber`, en un campo propio con unicidad (como `x_metrics_wo_number` en WO). `name` lo asigna Odoo; `partner_ref` puede mostrar el número de METRICS.
- **RN-02 INSERT \[MAN/DEF\]** Valida proveedor, productos y moneda; crea cabecera y líneas completas. No hay creación parcial.
- **RN-03 INSERT duplicado \[PROP\]** Si el número ya existe, no duplica y registra un error en el log.
- **RN-04 UPDATE \[DEF\]** Actualiza cabecera y líneas de una OC existente. **Una línea facturada no se actualiza.** La transacción queda **pendiente hasta que se anule la factura**.
- **RN-05 Identidad de línea \[PROP\]** El manual no trae identificador de línea, solo `stockcode`. Las líneas se cruzan por `stockcode`. Si una OC trae el mismo `stockcode` más de una vez, la transacción queda en error para revisión.
- **RN-06 DELETE \[DEF\]** Ejecuta la cancelación nativa. Con líneas facturadas se aplica la misma regla que el UPDATE (queda pendiente) \[PROP\]. Con mercadería ya recibida \[PEND\].
- **RN-07 UPDATE o DELETE de una OC inexistente \[PROP\]** Si hay un INSERT pendiente de esa OC, espera detrás de él. Si no hay ninguno, error en el log.

**Excepciones y reintentos**

- **RN-08 \[DEF\]** Si falta proveedor, producto o una equivalencia necesaria (incluida una moneda inactiva), la transacción **queda pendiente para reintento** y se reprocesa cuando el dato existe. No se descarta ni requiere reproceso manual.
- **RN-09 \[PROP\]** Las transacciones de una misma OC se procesan en orden. Una pendiente bloquea las siguientes de esa OC.
- **RN-10 \[PROP\]** El motivo del bloqueo queda visible en el chatter o log de la OC.

**Condición de pago y fechas**

- **RN-11 \[DEF\]** Se busca el término de pago por nombre (por ejemplo "45 dias") y, si no existe, se crea. Los vencimientos informados por METRICS se guardan como datos informativos. La regla con que METRICS calcula el vencimiento está \[PEND\]. El parser acepta fechas con y sin zona horaria (el manual muestra `...000`, la muestra trae `-03:00`) \[MAN\].

**Moneda y tipo de cambio**

- **RN-12 \[DEF\]** La OC se toma en la moneda de la OC. La moneda debe estar activa en Odoo. Si la moneda de la línea difiere de la de cabecera (muestra: 1 y 2), manda la de la línea y se registra un aviso \[PROP\]. Supongo que una PO de Odoo tiene una sola moneda, que hay que verificar.
- **RN-13 \[DEF/PROP\]** Si la moneda de la compañía de Odoo difiere de la recibida y METRICS informa tasa (`exchangerate`, obligatoria por línea según el manual), se usa esa tasa. Si no, se usa la tabla de cotizaciones de monedas de Odoo \[DEF\]. Sin cotización disponible, la transacción queda pendiente \[PROP\]. Con moneda extranjera, el precio es `unitvalue_foreigncurrency` y no `unitvalue` \[PROP, ese atributo no figura en el manual\]. `exchangerate` y `exchangeratedt` se guardan como informativos.
- **RN-14 \[PROP\]** Se compara el total de la PO en Odoo contra `totalvalue` de METRICS y la diferencia se registra sin bloquear. Puede deberse a la tasa o a los impuestos del producto.

**Solo lectura**

- **RN-15 \[DEF\]** La restricción aplica a usuarios en la UI. El Bot no tiene restricción. Los permisos del Bot siguen el criterio del spec de WO.
- **RN-16 \[PEND\]** Qué acciones pueden hacer los usuarios sobre la PO (confirmar, recibir, generar factura) sin editar sus campos.

---

## 3. Criterios de aceptación

- [ ] **CA-01** Un INSERT crea la PO con proveedor, fechas, condición de pago, moneda y líneas (`product_id`, `product_qty`, `price_unit`, `product_uom`).
- [ ] **CA-02** La clave `idcompany` + `purchaseordernumber` es única y un INSERT repetido no duplica.
- [ ] **CA-03** Un UPDATE actualiza cabecera y líneas de una OC existente.
- [ ] **CA-04** Un UPDATE sobre una línea facturada no se aplica y queda pendiente hasta que se anule la factura. Después se reprocesa solo.
- [ ] **CA-05** Un DELETE pasa la PO a `cancel` mediante el flujo nativo.
- [ ] **CA-06** Proveedor, producto, moneda inactiva o sin cotización dejan la transacción pendiente y se reprocesa sola al resolverse.
- [ ] **CA-07** Una transacción pendiente bloquea las siguientes de la misma OC, y el motivo queda visible.
- [ ] **CA-08** Si el término de pago no existe, se crea con el nombre de METRICS.
- [ ] **CA-09** La OC se crea en la moneda de la línea. Con moneda distinta a la de la compañía se usa la tasa de METRICS o, si no hay, la de la tabla de Odoo.
- [ ] **CA-10** `exchangerate`, `exchangeratedt` y los vencimientos de METRICS quedan guardados como informativos.
- [ ] **CA-11** Los impuestos de las líneas son los del producto, y la diferencia de total contra METRICS queda registrada sin bloquear.
- [ ] **CA-12** La OC es de solo lectura para usuarios en la UI y el Bot puede crearla y modificarla.
- [ ] **CA-13** Un `status` o `situation` de METRICS no modifica estados de Odoo. Los de Odoo (entregada, facturada) salen de recepciones y facturas.

---

## 4. Pendientes

| # | Pendiente | A quién |
| --- | --- | --- |
| 1 | **Unidades:** la OC va en KG y el ingreso (09) llega en FL con `quantityunitcost` en KG. Falta definir qué cantidad se recibe contra la línea | Proyecto |
| 2 | Moneda estándar de METRICS en producción y tabla de códigos de `idcurrency`. El manual no las define. Con tus muestras (2 USD × 3.623,04 kg × 1.450 = 10.506.816) parece ARS | METRICS |
| 3 | Significado de los atributos `*_foreigncurrency` y qué trae `exchangerate` cuando la moneda es la de la compañía | METRICS |
| 4 | Si una PO de Odoo admite monedas distintas por línea y qué campo guarda la tasa | Proyecto |
| 5 | `situation`: si se crean OC no aprobadas, rechazadas o en aprobación | Negocio |
| 6 | Regla de vencimiento de METRICS (23/07 + 45 días da 06/09; METRICS informa 14/09. Hipótesis: fin de mes + 45) | METRICS |
| 7 | `transportcost` y `othercosts` (muestra en 0): cómo se tratan si vienen con valor | Negocio |
| 8 | DELETE o UPDATE con mercadería ya recibida | Negocio |
| 9 | Acciones permitidas a usuarios sobre la PO (RN-16) | Proyecto |
| 10 | Confirmar que esta HU no vincula la PO con la WO por campos propios (la validación 9.2 del alcance de WO consulta compras pendientes por materia prima y lote) | Proyecto |

## 5. Fuera de esta HU

- Precio editable solo en la factura, por usuarios autorizados \[DEF\], y cálculo del ajuste (archivo 10): HU de factura y ajuste.
- Valorización definitiva al tipo de cambio de la factura 
