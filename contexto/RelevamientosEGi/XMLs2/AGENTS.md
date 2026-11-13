# Proyecto: Integración Metrics → Odoo (XMLs2)

## Arquitectura

- **Flujo unidireccional**: Metrics publica XML → Odoo consume. Odoo NO tiene GET/pull.
- Metrics envía XMLs con cada evento (creación/modificación). Para carga inicial, Metrics genera un XML batch completo.
- No hay endpoints REST; la integración es basada en archivos XML.

## Archivos del proyecto

| Archivo | Propósito |
|---------|-----------|
| `WO - Orden de Producción.xml` | Ejemplo WO UD36440 |
| `STK - Consumo.xml` | Ejemplo STK TransactionType=9 (ajuste) |
| `STK - Entrega Producción 01.xml` | Ejemplo STK TransactionType=1 (entrega PT.FOL.FEI.4665) |
| `STK - Entrega Producción 02.xml` | Ejemplo STK TransactionType=1 (entrega PT.FOL.FEI.4666) |
| `generar_excel_metrics.py` | Genera Excel con mapeo completo Metrics ↔ Odoo |
| `xml_to_excel.py` | Utilidad para extraer XML a Excel |
| `investigacion.md` | Documentación de investigación previa |
| `Metrics Integración XML - Revisión 93 (1).pdf` | Manual de integración Metrics (174 pág.) |
| `video/` | Grabaciones de reuniones + transcripciones |

## Entidades XML

### 1. CRM — Relaciones (Clientes/Proveedores)

| Elemento XML | Modelo Odoo | Descripción |
|---|---|---|
| `<sdiCrmActor>` | `res.partner` | Actor principal (cliente/proveedor) |
| `<sdiCrmActorContact>` | `res.partner` | Contactos (child) |
| `<sdiCrmAddress>` | `res.partner` | Direcciones (child) |
| `<sdiCrmCustomer>` | `res.partner` | Datos específicos de cliente |
| `<sdiCrmSupplier>` | `res.partner` | Datos específicos de proveedor |

### 2. STKItem — Ítems de Stock

| Elemento XML | Modelo Odoo | Descripción |
|---|---|---|
| `<sdiStkItem>` | `product.product` | Ítem de stock (material/PT) |

Campos clave: `StockCode` (default_code), `MaterialType` (categ), `ItemType` (type), `UnitCode` (uom_id), `MaterialGroupCode` (categ_id), `NCM` (l10n_latam_product_ncm), `EAN` (barcode), `UseLot`/`ControlTraceability` (tracking).

**Siempre se envían desde Metrics vía XML.** No hay GET. Metrics envía cada alta/modificación como XML individual.

### 3. STK — Movimientos de Stock

| Elemento XML | Modelo Odoo | Descripción |
|---|---|---|
| `<sdistktransactiongroup>` | `stock.picking` | Agrupación de transacciones |
| `<sdistktransaction>` | `stock.move` | Movimiento individual |

**TransactionType (manual pág 81-82):**

| TType | Descripción |
|---|---|
| 0 | Atención/devolución Solicitud MP |
| 1 | **Entrega de producción** |
| 2 | Compras |
| 3 | Ventas |
| 4 | Inventario |
| 5 | Transferencia entre ítems |
| 6 | Volúmenes |
| 7 | Transferencia entre empresas |
| 8 | Transferencia |
| **9** | **Ajuste de saldo** (NO es consumo de producción) |
| 10 | Otro |

### 4. WO — Órdenes de Producción

| Elemento XML | Modelo Odoo | Descripción |
|---|---|---|
| `<sdiwoworkorder>` | `mrp.production` | Orden de producción |
| `<sdiwoworkorderinfo>` | `mrp.production` | Cabecera (wonumber, status, fechas) |
| `<sdiwocustomerinfo>` | `res.partner` | Cliente |
| `<sdiwofinisheditem>` | `mrp.production` | Producto terminado |
| `<sdiworawmaterial>` | `stock.move` | Materia prima (vinculada por `idativ`) |
| `<sdiwooperation>` | `mrp.workorder` | Operación (vinculada por `idativ`) |
| `<sdiwocomponent>` | `mrp.bom.line` | Componente |

**MaterialType:**
- 0 = Papel/sustrato
- 1 = Tintas/consumibles
- 2 = Planchas/herramientas

### 5. SOR — Pedidos de Venta

| Elemento XML | Modelo Odoo | Descripción |
|---|---|---|
| `<sdiSorHeader>` | `sale.order` | Cabecera |
| `<sdiSorInfo>` | `sale.order` | Info (OrderNumber, CustomerCode, Status) |
| `<sdiSorItem>` | `sale.order.line` | Línea de pedido |
| `<sdiSorCustomer>` | `res.partner` | Cliente |

### 6. BIL — Facturas

| Elemento XML | Modelo Odoo | Descripción |
|---|---|---|
| `<sdiBilInvoice>` | `account.move` | Factura |
| `<sdiBilItemInfo>` | `account.move.line` | Línea de factura |
| `<sdiBilPayCondDueDate>` | `account.move.line` | Vencimientos |

### 7. WIP — Work in Progress

| Elemento XML | Modelo Odoo | Descripción |
|---|---|---|
| `<sdiWIPLabel>` | `mrp.workorder` | Etiqueta WIP |
| `<sdiWIPTransaction>` | `stock.move` | Transacción WIP |

**Solo exportación** (no se puede importar a Metrics).

**TransactionType WIP_TR:**
- 1 = Nuevo, 2 = Validación, 3 = Movimiento, 10 = Entrada en stock
- 17 = Totalmente consumida, 18 = Parcialmente consumida

## Vinculaciones clave

```
WO.idativ ↔ WIP.ProcessID (vincula WO con WIP)
WIP.IdPalletLabel ↔ WIP_TR.IdPalletLabel
WO → STK Entrega (TransactionType=1) via wonumber
ItemHija.OriginItem ↔ ItemMadre.StockCode (bobina madre/hija, herencia de costo)
```

## Reuniones grabadas

| Archivo | Temas cubiertos |
|---------|-----------------|
| `meet integracion funcional.srt` | CRM, ventas/cotizaciones, costos, materiales, bobina madre/hija (OriginItem), UOM, consumos reales vía WIP, remito/factura, logística, cierre stock |
| `video/` (otras grabaciones) | Ver transcripciones individuales |

Ver `resumen_meet_integracion_funcional.txt` para resumen completo de la meet funcional.

## Decisiones de diseño

1. **Moneda**: Metrics opera en USD, Odoo en ARS. Conversión al tipo de cambio de la factura de compra.
2. **Consumos no medibles** (tintas, pegamentos): se cargan contra centro de costo, no contra WO.
3. **Materiales productivos**: se crean en Metrics. **Materiales no productivos**: pueden crearse en Odoo.
4. **Carga inicial**: Metrics debe generar XML con todos los items. Una vez en marcha, cada alta/modificación se envía individualmente.
5. **Método valuación**: Costo promedio. Cotización usa tabla paralela (NO costo promedio de stock).
6. **Bobina madre/hija**: Item comprado (madre) tiene el costo. Item consumido (hija) hereda costo prorrateado. Vínculo via `OriginItem`.
7. **Unidades**: UOM distintas para compra, stock, consumo e ingeniería. Ideal: stock = consumo = ingeniería.
8. **Remito vs Factura**: Remito (entrega física) y Factura (documento fiscal) pueden ir separados.
9. **Clientes**: Solo activos se envían a Odoo. Proveedores se crean en ambos sistemas.
10. **Entrega producción**: Incluye solo PT, no materiales.
11. **Cierre stock**: Necesario para costos. Odoo no maneja cierre de costos financiero.
12. **Volúmenes**: Sistema de control individual de bobinas (código único). Materiales volumétricos solo se mueven via colector o sistema de volúmenes.

## Problemas identificados

1. STK Consumo (TType=9) es un **ajuste de saldo**, NO consumo de producción. No tiene wonumber.
2. WO planea 1150 FL de PF.2094, pero el ajuste registra 2500 FL — cantidades inconsistentes.
3. Entregas muy por debajo de lo planeado (8% y 0.2%).
4. Unidades inconsistentes entre WO (UN) y STK Entrega (PZ).
5. WIP y WIP_TR no tienen WONumber directo — el vínculo WO→consumo es por `ProcessID` ↔ `idativ`.

## Reglas de transformación complejas (R01-R23)

Ver `generar_excel_metrics.py:884-954` para 23 reglas detalladas que incluyen:
- R01: Mapeo de unidades (UnitCode → uom.uom)
- R07: Mapeo ItemType (0-4 → product/consu/service)
- R08: Creación de jerarquía de categorías por MaterialType
- R09: UseLot + ControlTraceability → tracking (lot/serial/none)
- R11: Mapeo transactiontype → picking_type_id
- R13: Mapeo WO status (0-6 → state)
- R17: Formato invoice number argentino (PV + número)
