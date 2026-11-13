# Historias de Usuario: Integración Odoo ↔ METRICS

**Base documental:** Manual de integración XML de METRICS (revisión 93) y 5 archivos de muestra (07 a 11). **Convenciones:** *Supuesto* = lo infiero de las muestras y el manual no lo confirma. *Pendiente* = hay que confirmarlo antes de construir. No tengo la versión de Odoo ni su documentación, por eso no se nombran modelos ni pasos técnicos de Odoo.

## Alcance y reglas de negocio acordadas

| Documento | Muestra | Sentido | Contexto METRICS | Operaciones (manual) |
| --- | --- | --- | --- | --- |
| Orden de compra | 07 | METRICS → Odoo | POR | INSERT, UPDATE, DELETE |
| Remito de compra | 08 | METRICS → Odoo | REC (solo exportación) | INSERT, UPDATE, CANCEL |
| Ingreso por compra | 09 | METRICS → Odoo | STK | INSERT, CANCEL |
| Ajuste de valor por factura | 10 | **Odoo → METRICS** | STK | INSERT, CANCEL |
| Consumo de material | 11 | METRICS → Odoo | STK | INSERT, CANCEL |

Reglas definidas por el negocio:

1. Todo lo que llega de METRICS (07, 08, 09, 11) es **solo lectura en Odoo**. La OC no se edita en Odoo.
2. **Lo único editable es la factura de proveedor**. Su precio solo lo modifican usuarios autorizados.
3. Lo único que Odoo envía a METRICS es el **ajuste de valor (10)**, generado desde la factura.
4. Odoo trabaja en **kilos**. METRICS informa también la cantidad en la unidad de costo (`quantityunitcost`, KG).
5. La condición de pago se busca por nombre en Odoo y, si no existe, se crea.
6. La fecha límite de recepción es solo informativa y no bloquea nada.
7. El ajuste se calcula sobre la base **sin impuestos**.

---

## Épica 1: Conectividad y control de transacciones

### HU-01 Conexión con METRICS

**Como** administrador de la integración, **quiero** configurar la conexión con METRICS (usuario, contraseña, endpoint), **para** que Odoo lea y envíe transacciones.

Criterios de aceptación:

- Dado un usuario y contraseña válidos de METRICS, cuando pruebo la conexión, entonces veo un resultado exitoso o el mensaje de error devuelto.
- Las credenciales no se muestran en claro ni quedan en logs.
- La conexión usa el WebService de METRICS: `GetPendingTransaction`, `SetTransactionResult` y `ProcessTransaction` (manual, 11.1 y 11.3).

Notas: **Pendiente:** el manual no trae URL ni WSDL. Debe darlos el proveedor de METRICS. La DLL del manual es de Windows, por lo que Odoo debería consumir el WebService directamente (*supuesto*).

### HU-02 Lectura periódica de transacciones pendientes

**Como** sistema, **quiero** consultar periódicamente las transacciones pendientes de METRICS, **para** procesarlas en Odoo sin intervención manual.

Criterios de aceptación:

- Cada transacción se procesa según su contexto (POR, REC, STK) y su operación (INSERT, UPDATE, DELETE, CANCEL).
- Al terminar, Odoo informa el resultado a METRICS con `SetTransactionResult` (`HasError` 0 o 1 con mensaje).
- Una transacción ya procesada (mismo `TransactionID`) no se procesa dos veces.
- El manual indica una operación por transacción.

Notas: **Pendiente:** frecuencia de lectura y cómo se comporta METRICS si Odoo no responde el resultado.

### HU-03 Bitácora de integración

**Como** usuario funcional, **quiero** ver cada transacción con su estado, contexto, operación y error, **para** diagnosticar y reprocesar.

Criterios de aceptación:

- Cada transacción, entrante o saliente, guarda: id METRICS, contexto, operación, XML original, estado, mensaje y fecha.
- Puedo filtrar por estado y reprocesar manualmente una transacción con error.
- Un error en una transacción no frena las siguientes.

### HU-04 Equivalencias de maestros

**Como** administrador, **quiero** mantener las equivalencias entre códigos METRICS y registros de Odoo, **para** que los documentos se vinculen bien.

Equivalencias necesarias: proveedor (`suppliercode`), producto (`stockcode`), unidades (KG, FL), moneda (`idcurrency`), empresa (`idcompany`) y ubicación de stock (`stockplacecode`).

Criterios de aceptación:

- Si un documento trae un código sin equivalencia, la transacción queda en error con un mensaje claro y no se crea nada a medias.
- La condición de pago es la excepción: se busca por nombre y, si no existe, se crea (ver HU-06).

Notas: **Pendiente:** el manual no tiene tabla de códigos de moneda. No se puede confirmar que `idcurrency=2` sea USD. Pedirla a METRICS.

---

## Épica 2: Orden de compra (07)

### HU-05 Recibir orden de compra desde METRICS

**Como** comprador, **quiero** ver en Odoo las órdenes aprobadas en METRICS, **para** conocer qué se compró, a quién y en qué condiciones.

Criterios de aceptación:

- La OC se crea con proveedor, fecha de emisión, líneas (producto, cantidad en KG, valor unitario, total), moneda y tipo de cambio.
- Se guarda el número METRICS (`purchaseordernumber`) como referencia única. Un INSERT repetido actualiza, no duplica.
- UPDATE modifica la OC existente. DELETE la anula o elimina según la regla que se defina.
- La OC queda **solo lectura** para todos los usuarios.
- La fecha límite de recepción se guarda como informativa, a nivel cabecera y a nivel línea (el manual las define como dos fechas distintas) y no bloquea.
- Se usan los estados de METRICS: aprobación (`situation`: 0 no aprobada, 1 aprobada, 2 rechazada, 3 en aprobación) y OC abierta o cerrada (`status`).

Notas:

- *Supuesto:* el total de cabecera (12.713.247,36) incluye 21 %, porque 10.506.816 × 1,21 da ese valor. El manual no documenta impuestos en POR. Se calcula como estimación y hay que verificarlo.
- **Pendiente:** si una OC no aprobada debe crearse en Odoo o ignorarse.
- **Pendiente:** confirmar que con la OC solo lectura puede generarse la factura de proveedor en Odoo. Verificar con la versión real.

### HU-06 Condición de pago

**Como** administrador contable, **quiero** que la condición de pago de METRICS se asocie a un término de pago de Odoo, **para** que la factura y los vencimientos queden coherentes.

Criterios de aceptación:

- Se busca por nombre exacto (por ejemplo "45 dias"). Si no existe, se crea automáticamente.
- Se guardan los vencimientos informados por METRICS (`duedate`, `value`) junto a la OC.
- Si el vencimiento calculado por Odoo difiere del de METRICS, se muestra la diferencia.

Notas: **Pendiente:** el manual no explica cómo METRICS calcula el vencimiento desde "45 dias". En la muestra, 23/07/2026 + 45 días da 06/09/2026, pero METRICS informa 14/09/2026. Una hipótesis es fin de mes + 45 días (31/07 + 45 = 14/09). Con un solo ejemplo no se confirma. Se necesita la regla antes de crear el término.

### HU-07 OC en moneda extranjera

**Como** analista contable, **quiero** conservar la moneda y el tipo de cambio de cada línea, **para** valorizar correctamente en moneda estándar.

Criterios de aceptación:

- Se guardan el valor unitario y total en moneda estándar y los valores en moneda extranjera.
- Se guarda el tipo de cambio y su fecha.
- En la muestra: 2 de valor unitario en moneda extranjera × 1.450 de tipo de cambio = 2.900 por KG. Es estimación mía y hay que verificarla.

Notas: los atributos `*_foreigncurrency` aparecen en la muestra pero no en el manual. Confirmar su significado con METRICS.

---

## Épica 3: Recepción e ingreso (08 y 09)

### HU-08 Recibir remito de compra

**Como** responsable de depósito, **quiero** ver el remito del proveedor en Odoo, **para** registrar qué se recibió físicamente.

Criterios de aceptación:

- Se registran proveedor, serie, número y fecha del remito (`receiptserie`, `receiptnumber`, `receiptdate`).
- Los ítems del remito se vinculan a la OC mediante la lista de OC atendidas (`PurchaseOrder`, cantidad, valor, unidad) que el manual define para el REC.
- Soporta INSERT, UPDATE y CANCEL.
- Un remito se identifica por proveedor + serie + número. Uno repetido no duplica.

Notas: **Pendiente:** la muestra 08 viene con el ítem vacío, por lo que no se puede ver el vínculo con la OC. Pedir a METRICS una muestra con ítems.

### HU-09 Recibir ingreso de material por compra

**Como** responsable de depósito, **quiero** que el ingreso informado por METRICS se refleje en el stock de Odoo, **para** tener existencias reales con lote y vencimiento.

Criterios de aceptación:

- Se procesa `transactiontype=2` y `operationtype=0` (entrada).
- Se registran producto, **cantidad en KG** (`quantityunitcost`), lote (`lot`, `providerlot`), fecha de producción y vencimiento, ubicación y valor.
- Se vincula al remito por `docnumber` (número del remito) y a la OC por la información del REC o de la OC exportada. *Supuesto:* `docnumbercompl` trae el código del proveedor. El manual no define su contenido.
- El valor de la transacción (`totalvalue`) se guarda como valor de recepción. Queda la referencia contra la que se calcula el ajuste (HU-15).
- CANCEL revierte el ingreso si no hay consumos posteriores. Si los hay, la transacción queda en error con mensaje claro (*supuesto*).
- El ingreso es solo lectura.

Notas: en la muestra, 60.000 FL = 3.623,04 KG, que coincide con la cantidad de la OC. **Pendiente:** el 09 no trae el número de OC.

### HU-10 Conversión de unidades FL y KG

**Como** responsable de stock, **quiero** que Odoo opere en kilos y conserve la cantidad original en FL, **para** no perder trazabilidad.

Criterios de aceptación:

- Odoo usa `quantityunitcost` (KG) como cantidad cuando `unitcostcode` es KG.
- Se guarda la cantidad original en FL como dato informativo.
- Se define un factor FL→KG por producto.

Notas:

- Estimación mía: 3.623,04 ÷ 60.000 = 0,060384 kg por FL. En el consumo, 100 FL × 0,060384 = 6,0384, y METRICS informa 6,038, así que parece redondear a 3 decimales (*supuesto*).
- Si se consumen 60.000 FL en tandas de 100, la suma de kilos redondeados da 3.622,8 KG contra 3.623,04 recibidos. Quedan 0,24 KG de diferencia (estimación). **Decisión pendiente:** cómo tratar ese residuo.
- Se necesita la muestra del contexto STKITEM de `02.01.0003` (unidades y `WeightKg`).

---

## Épica 4: Consumo (11)

### HU-11 Recibir consumo de material

**Como** responsable de producción, **quiero** que los consumos informados por METRICS descuenten stock en Odoo, **para** reflejar el uso de materia prima por orden de producción.

Criterios de aceptación:

- Se procesa `transactiontype=0` y `operationtype=1` (atención de solicitud, salida).
- Se descuenta del lote indicado, en kilos (`quantityunitcost`).
- Se guarda la orden de producción (`wonumber`, por ejemplo OFC00001) y el valor informado.
- Se vincula con la recepción de origen por lote y lote del proveedor.
- Un consumo con lote inexistente o saldo insuficiente queda en error con mensaje claro.
- Soporta CANCEL.

Notas:

- Para el tipo 0, `transactionoriginextref` debe identificar el ítem de la solicitud (manual, 11.10 y 11.11). **Pendiente:** definir si se importa también el contexto REQ.
- **Decisión pendiente:** ¿Odoo toma el valor de consumo de METRICS o lo recalcula con su método de costeo? Si se recalcula, no coincidirá con METRICS.
- **Pendiente:** si el consumo se modela con órdenes de producción de Odoo o solo como movimiento de stock.

---

## Épica 5: Factura y ajuste (10)

### HU-12 Factura de proveedor editable

**Como** analista contable, **quiero** registrar la factura de proveedor en Odoo con lo recibido, **para** comparar lo facturado con lo valorizado.

Criterios de aceptación:

- La factura es el único documento editable del circuito.
- El **precio** de la línea solo puede modificarlo un grupo de usuarios autorizados. Los demás usuarios lo ven pero no lo editan.
- La factura referencia la OC y la recepción de origen.

Notas: no tengo la documentación de tu versión de Odoo, por lo que no indico cómo se restringe el campo.

### HU-13 Calcular el ajuste de valor

**Como** analista contable, **quiero** que Odoo calcule la diferencia entre lo facturado y lo valorizado en METRICS, **para** enviar solo el ajuste necesario.

Regla (base sin impuestos): **ajuste = factura sin impuestos − `totalvalue` del ingreso (09) − ajustes ya enviados para esa recepción**

Criterios de aceptación:

- Con factura de 10.556.815,98 e ingreso de 10.506.815,98 el ajuste es 50.000 (estimación sobre tus datos).
- Si hay varias facturas o ajustes parciales sobre una recepción, se descuentan los ya enviados.
- Si la diferencia es menor a una tolerancia configurable, no se envía. La OC de la muestra da una diferencia de 0,02 por redondeo de METRICS: 10.506.816 − 10.506.815,98.
- Si la factura está en moneda extranjera, se convierte a moneda estándar con el tipo de cambio que se defina.

Notas:

- **Pendiente:** valor de tolerancia, tipo de cambio de conversión y fecha del ajuste (factura o recepción).
- **Pendiente:** si METRICS acepta ajustes negativos y cómo se envían.

### HU-14 Enviar el ajuste a METRICS

**Como** sistema, **quiero** enviar el ajuste a METRICS al confirmar la factura, **para** que METRICS actualice el valor del stock.

Criterios de aceptación:

- Se envía por `ProcessTransaction` con contexto STK y operación INSERT.
- Campos fijos tomados de la muestra: `transactiontype=9`, `stockmovementtype=1`, `operationtype=0`, `quantity=0`, `lot=UNICO`, `stockaddress=UNICO`. `totalvalue` es el ajuste calculado.
- `transactioncodeextref` lo genera Odoo: numérico y único, sin repetirse en movimientos distintos (manual, 11.10). Se guarda para poder cancelar.
- Se registra la respuesta de METRICS. Si da error, queda en la bitácora y se puede reintentar sin duplicar el ajuste.
- Se envía una operación por llamada.

Notas:

- *Supuesto:* `docnumber` lleva el número de factura. El manual lo marca obligatorio y la muestra lo trae vacío, así que hay que probar.
- **Pendiente:** si `transactiondt` es la fecha de la factura o de la recepción, y si `transactioncode` debe repetir el valor de `transactioncodeextref` como en la muestra (el manual lo define como asignado por METRICS).

### HU-15 Anular un ajuste

**Como** analista contable, **quiero** que al anular o revertir la factura se cancele el ajuste en METRICS, **para** que METRICS no conserve un valor incorrecto.

Criterios de aceptación:

- Se envía la operación CANCEL con el mismo `transactioncodeextref` y la **fecha original** del ajuste (manual, 11.10).
- Odoo guarda ambos datos del ajuste original.
- Si METRICS rechaza la cancelación, queda registrado y se alerta al usuario.

---

## Épica 6: Calidad y puesta en marcha

### HU-16 Pruebas con datos de METRICS

**Como** equipo del proyecto, **quiero** probar el circuito completo con muestras reales, **para** validar antes de producción.

Criterios de aceptación:

- Circuito completo: OC → remito → ingreso → consumo → factura → ajuste, con los datos de las muestras 07 a 11.
- Casos de error: proveedor, producto o moneda sin equivalencia, lote inexistente, ajuste duplicado y UPDATE de OC.
- Prueba de CANCEL en ingreso, consumo y ajuste.

---

## Pendientes consolidados

| # | Pendiente | A quién | Impacta |
| --- | --- | --- | --- |
| 1 | Endpoint y WSDL del WebService | METRICS | HU-01 |
| 2 | Tabla de códigos de moneda (`idcurrency`) | METRICS | HU-04, HU-07 |
| 3 | Regla de vencimiento de "45 dias" | METRICS | HU-06 |
| 4 | Muestra REC con ítems y número de OC | METRICS | HU-08, HU-09 |
| 5 | Muestra STKITEM de `02.01.0003` (unidades y `WeightKg`) | METRICS | HU-10 |
| 6 | ¿Se importa REQ? Muestra de solicitud | METRICS | HU-11 |
| 7 | Ajustes negativos y significado de `docnumber` | METRICS | HU-13, HU-14 |
| 8 | Qué hacer con una OC no aprobada | Negocio | HU-05 |
| 9 | Tolerancia, tipo de cambio y fecha del ajuste | Negocio | HU-13, HU-14 |
| 10 | Tratamiento del residuo de kilos y valorización del consumo | Negocio | HU-10, HU-11 |
| 11 | Versión de Odoo y módulos usados (compras, stock, producción) | Proyecto | Todas |