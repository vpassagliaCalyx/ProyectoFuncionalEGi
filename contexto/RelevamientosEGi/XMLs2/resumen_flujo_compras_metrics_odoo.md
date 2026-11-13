# Resumen del Flujo de Compras: Integración Metrics → Odoo

## 1. Visión General de la Arquitectura
- **Flujo Unidireccional:** Metrics publica eventos en XML y Odoo los procesa automáticamente.
- **Rol del Usuario Bot:** Las Órdenes de Compra y Recepciones creadas por la integración son de **solo lectura para usuarios en la UI**; únicamente el Bot de integración puede crearlas y modificarlas.
- **Unidades y Valuación:** 

  - Cotización/Metrics opera en USD y Odoo contabiliza en ARS (la conversión final de costo se ajusta mediante la factura de compra).

---

## 2. Componentes del Flujo de Compras

```
 [POR - Órdenes de Compra]
            │
            ▼
 [REC - Remito de Proveedor]  ──(Llama a la OC)──┐
            │                                    │
            ▼                                    ▼
 [STK - Ingreso Físico (Type 2)] ────► [Recepción en Odoo Validada]
   - Lote / Lote Proveedor               - Cantidad Real (KG)
   - Vencimiento / Ubicación             - Trazabilidad Asignada
```

---

## 3. Desglose de Historias de Usuario (HU)

### A. Orden de Compra — Contexto `POR` (XML 07)
* **Objetivo:** Crear y mantener órdenes de compra (`purchase.order`) en Odoo a partir de los XMLs enviados por Metrics.
* **Clave Única de Integración:** `idcompany` + `purchaseordernumber`.
* **Mapeo Principal:**
  * Cabecera: Proveedor (`res.partner`), Términos de Pago (`payment_term_id`), Fecha Prevista, Moneda.
  * Líneas: Producto (`product_id` por `stockcode`), Cantidad (`product_qty`), Precio Unitario (`price_unit`).
* **Reglas Destacadas:**
  * **RN-02 / RN-03:** Inserción limpia y control de duplicados por clave única.
  * **RN-04:** Si una línea de la OC ya tiene factura, el `UPDATE` queda pendiente hasta que la factura sea anulada.
  * **RN-08:** Manejo de reintentos automáticos si faltan maestros (proveedor, producto o moneda inactiva).
  * **RN-12 / RN-13:** Manejo multimoneda aplicando la tasa (`exchangerate`) provista por Metrics o la tabla de cotizaciones de Odoo.

---

### B. Recepción de Mercadería — Contexto `REC` (XML 08) + `STK Compras` (XML 09)
* **Objetivo:** Reflejar el ingreso físico de la mercadería y su trazabilidad vinculándola a la Orden de Compra.

#### 1. Mantenimiento Documental (`REC` - Muestra 08)
* Asigna la clave del remito (`providercode` + `receiptserie` + `receiptnumber`).
* Vincula los ítems recibidos con la línea de la OC (`purchaseorder`).
* Determina qué ítems son de entrega física (`isdelivery=1`).

#### 2. Ingreso Físico e Inventario (`STK` - Muestra 09 / `TransactionType=2`)
* Otorga la cantidad real recibida en KG (`quantityunitcost`).
* Asigna datos obligatorios de trazabilidad: **Lote (`lot`)**, **Lote del Proveedor (`providerlot`)**, **Fechas de Fabricación/Vencimiento** y **Ubicación/Almacén**.
* Valida e impacta el inventario en Odoo.

* **Reglas Destacadas:**
  * **RR-01 / RR-02:** El REC crea la recepción borrador vinculada a la OC; el STK asigna lotes/cantidades y **valida** la recepción.
  * **RR-04:** Manejo de desfasajes en orden de llegada (si llega primero el STK que el REC, la transacción espera reintento automático).
  * **RR-08:** Cancelaciones (`CANCEL`) revierten el stock siempre y cuando el lote no haya sido consumido en producción.

---

## 4. Estado de Pendientes y Próximos Pasos

| Contexto | Pendiente Clave | Responsable |
| :--- | :--- | :--- |
| **REC (08)** | Solicitar a Metrics muestra XML con el tag `<sdiprovideritemreceipt>` poblado. | Metrics |
| **STK (09)** | Confirmar si `receiptserie` puede incluirse en el STK para evitar colisiones entre remitos repetidos. | Metrics |
| **POR / REC** | Homologación exacta de ubicaciones (`PADRON`, `UNICO`) hacia los almacenes de Odoo. | Proyecto |
| **Siguiente HU** | **Facturas de Proveedor (`BIL` / Archivo 10):** Cierre de flujo, ajuste de diferencias de precio y variaciones de tipo de cambio. | Equipo |