# HU – Recepción de remitos de proveedor desde METRICS

## 1. Historia de Usuario

**Como responsable de recepción de mercadería**,  
quiero que los remitos de proveedores enviados desde METRICS sean recibidos automáticamente en Odoo y vinculados con la Orden de Compra correspondiente,  
para registrar correctamente la mercadería efectivamente ingresada, sus cantidades y lotes, evitando la carga manual de información.

---

## 2. Objetivo

Permitir que Odoo reciba y procese automáticamente la información enviada por METRICS correspondiente a:

- El remito del proveedor.
- La Orden de Compra asociada.
- Los productos recibidos.
- Las cantidades efectivamente ingresadas.
- Los lotes.
- Las fechas de producción y vencimiento, cuando correspondan.
- La ubicación de recepción.

La recepción debe quedar trazada contra la Orden de Compra correspondiente y reflejar en Odoo la mercadería efectivamente ingresada.

La información generada por la integración será gestionada automáticamente y no deberá ser modificada manualmente por los usuarios.

---

# 3. Alcance

METRICS informa la recepción mediante dos tipos de información:

### 3.1. REC – Remito del proveedor

El REC informa el documento del proveedor y permite identificar la Orden de Compra que está atendiendo.

Contiene, entre otros datos:

- Proveedor.
- Serie y número de remito.
- Fecha del remito.
- Productos.
- Cantidades informadas.
- Orden de Compra asociada.
- Línea de la Orden de Compra.

El REC permite identificar y vincular el remito con la Orden de Compra.

### 3.2. STK – Ingreso físico

El STK informa el ingreso efectivo de la mercadería.

Contiene, entre otros datos:

- Producto.
- Cantidad efectivamente recibida.
- Lote.
- Lote del proveedor.
- Fecha de producción.
- Fecha de vencimiento.
- Ubicación.
- Valor informado por METRICS.

La cantidad utilizada para realizar la recepción en Odoo será la cantidad efectiva informada por STK.

---

# 4. Flujo funcional

## 4.1. Recepción del REC

Cuando Odoo recibe un REC:

1. Identifica al proveedor.
2. Identifica el remito mediante los datos enviados por METRICS.
3. Identifica la Orden de Compra asociada.
4. Identifica el producto.
5. Identifica la línea correspondiente de la Orden de Compra.
6. Genera la recepción asociada al remito.
7. Deja la recepción pendiente de completar con la información física del STK.

El REC por sí solo no valida la recepción física.

## 4.2. Recepción del STK

Cuando Odoo recibe el STK correspondiente:

1. Identifica el remito.
2. Busca la recepción previamente generada por el REC.
3. Identifica el producto.
4. Registra la cantidad efectivamente recibida.
5. Registra el lote.
6. Registra el lote del proveedor, cuando exista.
7. Registra fecha de producción y vencimiento, cuando corresponda.
8. Utiliza la ubicación única definida en Odoo para este proceso.
9. Valida la recepción.

---

# 5. Reglas de negocio

### RN-01 – Obligación de Orden de Compra

Todo REC debe tener una Orden de Compra asociada.

**No se permite procesar un remito que no tenga una Orden de Compra asociada.**

Si el REC no informa una OC válida, la recepción no debe generarse.

### RN-02 – Vinculación con la Orden de Compra

El remito debe quedar relacionado con:

- Orden de Compra.
- Línea de Orden de Compra.
- Producto correspondiente.

La recepción debe impactar sobre la cantidad pendiente de recibir de dicha línea.

### RN-03 – No duplicación

Un mismo remito no debe generar más de una recepción.

La identificación del remito se realizará utilizando los datos definidos por METRICS para proveedor, serie y número de remito.

### RN-04 – Cantidad recibida

La cantidad recibida en Odoo será la informada por STK como cantidad efectiva de ingreso.

### RN-05 – No se permite sobre-recepción

No se permite recibir una cantidad superior a la cantidad pendiente de la Orden de Compra.

Si la cantidad informada por STK supera la cantidad pendiente:

- La recepción no debe validarse.
- La transacción debe quedar rechazada/pendiente.
- Debe registrarse el motivo del rechazo.

**Ejemplo:** si la OC tiene una cantidad pendiente de recibir de 100 unidades y METRICS informa un ingreso de 110 unidades, Odoo no debe validar la recepción.

### RN-06 – Lotes

La recepción debe registrar el lote correspondiente a la mercadería recibida.

Si un mismo producto se recibe en diferentes lotes, cada lote debe registrarse con su correspondiente cantidad.

### RN-07 – Cantidad distribuida en varios lotes

Cuando un mismo producto sea recibido en varios lotes, Odoo debe registrar cada lote y su cantidad.

La suma de las cantidades recibidas no podrá superar la cantidad pendiente de la Orden de Compra.

### RN-08 – Datos inexistentes

Si Odoo no encuentra alguno de los datos necesarios para procesar la recepción, por ejemplo:

- Proveedor.
- Producto.
- Orden de Compra.
- Línea de Orden de Compra.

la recepción no debe generarse parcialmente.

La transacción debe quedar pendiente para reproceso y debe registrarse el motivo.

### RN-09 – STK recibido antes que REC

Si el STK llega antes que el REC correspondiente, Odoo debe conservar la información como pendiente.

Una vez recibido y procesado el REC, el STK podrá completar la recepción correspondiente.

### RN-10 – Ubicación

La recepción utilizará **una única ubicación definida en Odoo para este proceso**.

No se requiere realizar un mapeo entre múltiples ubicaciones de METRICS y ubicaciones de Odoo.

### RN-11 – Precio

El proceso de recepción no debe modificar el precio de la Orden de Compra.

El valor informado por METRICS se conservará como referencia para los procesos posteriores que correspondan.

### RN-12 – Cancelación

Si METRICS informa la cancelación de un REC o STK:

- Si la mercadería todavía no fue consumida, se deberá revertir la recepción.
- Si la mercadería ya fue consumida, la operación no podrá revertirse automáticamente y deberá quedar pendiente para resolución.

### RN-13 – Recepción validada

Una recepción que ya fue validada **no puede ser modificada mediante un UPDATE del REC**.

Si METRICS envía un UPDATE sobre una recepción ya validada:

- El UPDATE se considera inválido.
- No debe modificar la recepción.
- Debe registrarse el motivo del rechazo.

### RN-14 – Solo lectura

Las recepciones generadas por la integración serán de solo lectura para los usuarios.

Los usuarios no podrán:

- Crear manualmente la recepción generada por la integración.
- Modificar sus datos.
- Validarla manualmente.

La creación, modificación y validación será realizada por el proceso de integración.

### RN-15 – Odoo 19 Enterprise

La solución se implementará sobre **Odoo 19 Enterprise**.

Los campos estándar correspondientes a lotes, fechas de producción y vencimiento deberán utilizar los modelos disponibles en esta versión de Odoo.

---

# 6. Criterios de aceptación – Gherkin

## CA-01 – Crear recepción desde REC

**Dado** un REC válido enviado por METRICS  
**Y** el REC tiene una Orden de Compra asociada  
**Y** el proveedor y producto existen en Odoo  
**cuando** se procesa el REC  
**entonces** se debe crear la recepción vinculada a la Orden de Compra y a la línea correspondiente.

## CA-02 – REC sin Orden de Compra

**Dado** un REC enviado por METRICS  
**cuando** el REC no tiene una Orden de Compra asociada  
**entonces** la recepción no debe generarse  
**Y** debe registrarse el motivo del rechazo.

## CA-03 – Completar recepción mediante STK

**Dado** una recepción creada a partir de un REC  
**cuando** llega el STK correspondiente  
**entonces** Odoo debe completar la recepción con la cantidad efectivamente recibida, lote y demás datos informados  
**Y** debe validar la recepción si todas las validaciones son correctas.

## CA-04 – No permitir sobre-recepción

**Dado** una Orden de Compra con una cantidad pendiente determinada  
**cuando** STK informa una cantidad superior a la pendiente  
**entonces** Odoo no debe validar la recepción  
**Y** debe registrar el motivo del rechazo.

## CA-05 – Recepción por múltiples lotes

**Dado** un producto recibido en varios lotes  
**cuando** METRICS informa los diferentes movimientos STK  
**entonces** Odoo debe registrar cada lote con su cantidad correspondiente  
**Y** la suma de las cantidades no debe superar la cantidad pendiente de la Orden de Compra.

## CA-06 – STK recibido antes que REC

**Dado** un STK recibido sin que exista todavía el REC correspondiente  
**cuando** Odoo procese el STK  
**entonces** debe dejar la operación pendiente  
**Y** cuando llegue el REC correspondiente debe poder completar automáticamente la recepción.

## CA-07 – Datos inexistentes

**Dado** un REC o STK  
**cuando** no existe el proveedor, producto, Orden de Compra o línea correspondiente  
**entonces** no se debe generar una recepción incompleta  
**Y** la transacción debe quedar pendiente para reproceso.

## CA-08 – No duplicar recepción

**Dado** un remito ya procesado  
**cuando** METRICS envía nuevamente el mismo remito  
**entonces** Odoo no debe crear una nueva recepción.

## CA-09 – No modificar precio

**Dado** un remito válido  
**cuando** se procesa la recepción  
**entonces** el precio de la Orden de Compra no debe modificarse.

## CA-10 – Ubicación única

**Dado** una recepción válida  
**cuando** se registra el ingreso de mercadería  
**entonces** la mercadería debe ingresar en la ubicación única configurada en Odoo para este proceso.

## CA-11 – UPDATE de recepción validada

**Dado** una recepción que ya fue validada  
**cuando** METRICS envía un UPDATE del REC  
**entonces** Odoo debe rechazar el UPDATE  
**Y** la recepción validada no debe modificarse.

## CA-12 – Solo lectura

**Dado** una recepción generada por la integración  
**cuando** un usuario común accede a la recepción  
**entonces** no podrá modificar ni validar manualmente la recepción.

## CA-13 – Cancelación

**Dado** una recepción generada desde METRICS  
**cuando** METRICS informa su cancelación  
**Y** la mercadería no fue consumida  
**entonces** Odoo debe revertir la recepción.

**Y cuando** la mercadería ya fue consumida  
**entonces** Odoo no debe realizar la reversión automática  
**Y** debe dejar la operación pendiente para resolución.

---

# 7. Pendientes

Luego de las definiciones realizadas, quedan solamente los siguientes puntos funcionales/técnicos a confirmar:

1. **`docnumber` + `docnumbercompl`:** confirmar con METRICS el significado exacto de ambos campos y su utilización para identificar el remito.
2. **Fecha efectiva de recepción:** definir si Odoo debe utilizar `receiptdate` o `receiptprocessing` como fecha efectiva del ingreso.
3. **Campos de lote y vencimiento:** validar durante el desarrollo los campos estándar disponibles en Odoo 19 Enterprise para lote, fecha de producción y fecha de vencimiento.

---

# 8. Fuera de alcance

Esta HU no contempla:

- Factura de proveedor.
- Ajuste de valor de factura.
- Modificación del precio de la Orden de Compra.
- Condición de pago.
- Configuración de moneda de la Orden de Compra.
- Costos de transporte o seguro.
- Consumo de materia prima en la Orden de Fabricación.

Estos procesos corresponden a otras HUs.
