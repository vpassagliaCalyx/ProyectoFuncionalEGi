# Resumen de casos de uso: integración Metrics ↔ Odoo (EG)

**Fuentes leídas (completas):**
- **[CU]** `XMLs2/cu/casos-uso-integracion-metrics-odoo.md`: v1.0, 2026-11-06, 140 casos en 12 prefijos.
- **[TEC]** `XMLs2/cu/cu integracion tecnico modulo.txt`: diseño técnico del módulo, basado en el de Rofina.
- **[HU]** `XMLs2/HU Integración Odoo ↔ METRICS (1).md`: HU-01 a HU-16, solo del circuito de compras (muestras 07 a 11).

**Referencias de otras fuentes:** [CU] cita reglas R01–R23 (`generar_excel_metrics.py`), RR/RN (`resumen_flujo_compras_metrics_odoo.md`), la "Minuta funcional §n" (`resumen_meet_integracion_funcional.txt`) y AGENTS.md (§17 Trazabilidad documental). No leí esas fuentes.

---

## 1. Índice de casos de uso / HUs

**Sentido.** M→O = Metrics → Odoo. O→M = Odoo → Metrics.

**Fixtures.** Los números (01–16) son los XML de `ejemplo completo/`.

### 1.1 [CU] §3 Transversales `CU-INF` (10)

| ID | Nombre | Sentido / disparador | Modelos Odoo | Propósito |
|---|---|---|---|---|
| INF-01 | Credenciales y entorno | Config | `res.config.settings`, `ir.config_parameter` | URL WSDL, usuario, contraseña cifrada, entorno, cursor delta |
| INF-02/03 | Testear conexión OK / error | Handshake SOAP | settings (notification / UserError) | Banner verde o diálogo con código HTTP |
| INF-04 | Lectura por lotes + cursor | M→O, lote de 100 | log, settings | El cursor avanza solo si el lote termina completo |
| INF-05 | Idempotencia por TransactionID | Cualquiera | log | Una transacción repetida se descarta |
| INF-06 | Bitácora y reproceso | Entrante/saliente | log | Filtrar por error y reprocesar |
| INF-07 | Aislamiento de logs ("prueba del ácido") | Cualquiera | log + queue_job/savepoint | Rollback del negocio sin perder el log |
| INF-08 | Equivalencias de maestros | Validación previa | tablas de equivalencia | Si falta un código: error claro, nada creado a medias |
| INF-09 | Informar resultado | `SetTransactionResult` | log | HasError 0/1 + mensaje, una operación por llamada |
| INF-10 | Orden de llegada y reintentos | Dependencias (STK antes que REC) | queue_job | Reintento con espera hasta un máximo, después error |

### 1.2 [CU] §4 CRM `CU-CRM` (13). M→O, contexto CRM, fixtures 01/02

**Modelo:** todos los casos tocan `res.partner`.

| ID | Nombre | Propósito |
|---|---|---|
| CRM-01 | Alta cliente activo | `customer_rank>0`; `code` como referencia externa; dirección y contacto |
| CRM-02 | Alta proveedor | `supplier_rank>0`; datos fiscales; condición de pago |
| CRM-03 | Actor mixto | Una sola ficha con ambos ranks |
| CRM-04 | Persona física/jurídica/gobierno/exportación | `persontype` 0→person, 1/2/3→company |
| CRM-05 | Documento fiscal por país | `countrydocumentnumber`→`vat` + tipo de identificación; país por código BACEN (639) |
| CRM-06 | Direcciones múltiples | `isbilling`→invoice, `isdelivery`→delivery, `ischarging`→other (contactos hijos) |
| CRM-07 | Contactos del actor | `sdilcrmactorcontact` → contacto hijo |
| CRM-08 | Condición de pago, crédito, vendedor | Busca el término de pago por nombre y lo crea si no existe (`account.payment.term`); límite de crédito; vendedor |
| CRM-09 | Prospecto o inactivo | No se crea; la bitácora lo registra como "omitido" |
| CRM-10 | Update sin duplicar | Busca por `code` |
| CRM-11 | AFIP e IIBB | `broptingsimplenational=3` → Responsable Inscripto (l10n_ar) |
| CRM-12 | País o moneda desconocidos | Error, nada creado |
| CRM-13 | Baja o desactivación | `isactv=0` → archivar, conservar historial |

### 1.3 [CU] §5 Ítems `CU-ITM` (13). M→O, contexto STKITEM, fixtures 03/04

**Modelos:** `product.product`/`product.template`, `product.category`, `uom.uom`.

| ID | Nombre | Propósito |
|---|---|---|
| ITM-01 | Alta PT | `materialtype=6`, `itemtype=1`→`type=product`; `default_code=stockcode`; tracking |
| ITM-02 | Alta MP | FL (stock/demanda) y KG (costo); categoría 02→02.01 |
| ITM-03 | Intermedio, servicio, consumible | `itemtype` 2→product, 3→service, 4→consu |
| ITM-04 | Clasificación de producto | `productclassification` (p. ej. "Láminas"); flags de separación |
| ITM-05 | Jerarquía de categorías | Raíz "Metrics" → master (02 Sustratos) → group (02.01); el producto cuelga del nivel group |
| ITM-06 | UOM y conversiones | `sdistkunitconversion`; crea la UOM si no existe |
| ITM-07 | Trazabilidad | `uselot`/`controltraceability` → lot/serial/none (R09) |
| ITM-08 | NCM, EAN, FSC, pesos | Datos fiscales y logísticos |
| ITM-09 | Bobina madre/hija (`originitem`) | Vínculo y herencia o prorrateo de costo (muestra pendiente) |
| ITM-10 | Control por volúmenes | `usesctrlvolume`, diámetro, pesos |
| ITM-11 | Modificación | Update por `default_code` |
| ITM-12 | UOM o categoría faltante | Error |
| ITM-13 | Discrepancia de `materialtype` STKItem vs WO | Tablas distintas según contexto (ver §3) |

### 1.4 [CU] §6 Producción `CU-WO` (21). M→O, contexto WO (fixture 05, "OP compartida") + STK

**Modelos:** `mrp.production`, `mrp.bom`/`mrp.bom.line`, `mrp.workorder`, `mrp.routing.workcenter`, `mrp.workcenter`.

| ID | Nombre | Propósito |
|---|---|---|
| WO-01 | Alta de MO | `origin=wonumber`, producto, cantidad, `date_deadline` |
| WO-02 | Cabecera, estados, fechas | `status` 0–6 → `state` según R13 |
| WO-03 | MP a la BOM | `sdiworawmaterial` → `mrp.bom.line`; guarda `idativ` |
| WO-04 | Componentes a la BOM | `sdiwocomponent`; detecta un componente que repite el PT (BOM circular) |
| WO-05 | Operaciones | `sdiwooperation` → workcenter/workorder, `idativ` |
| WO-06 | Centros de trabajo, tiempos, mermas | Crea el centro o da error "según política" |
| WO-07 | OP simple | Una MO |
| WO-08 | OP compartida | Una MO por PT con el mismo `wonumber` (OFC00008: 2 PT) |
| WO-09 | % por cantidad planificada | qty_i / Σqty |
| WO-10 | Redondeo y residuo | El último PT absorbe el residuo |
| WO-11 | Tercerización | Solo costo; ni OC ni subcontratación |
| WO-12 | Reserva de componentes | Faltantes visibles |
| WO-13 | Consumo real STK TType 0 | Descuenta el lote y registra el consumo en la MO |
| WO-14 | Conciliación WIP | `ProcessID`↔`idativ`; sin movimientos |
| WO-15 | Entrega PT STK TType 1 y cierre | "Cerrar o actualizar la MO"; evitar doble descuento |
| WO-16 | Pedido de venta ↔ MO | Vínculo por `wonumber` |
| WO-17 | Modificación y cancelación | `status=4` → cancelar |
| WO-18 | Costeo promedio | MP + operaciones + tercerización; comparar con Metrics |
| WO-19 | Errores de estructura | No crea una MO parcial |
| WO-20 | Consumibles no medibles | Tintas y pegamentos al centro de costo, fuera de la BOM |
| WO-21 | BOM multinivel | Muestra pendiente |

### 1.5 [CU] §7 Ventas `CU-SOR` (9). M→O, contexto SOR, fixture 06

**Modelos:** `sale.order`, `sale.order.line`.

| ID | Propósito |
|---|---|
| SOR-01 | Alta de pedido (`saleordernumber=5Q-1`, `status=2`→confirmado) |
| SOR-02 | Líneas con referencias a `wonumber` y `quotenumber` |
| SOR-03 | Condición de pago y vencimientos |
| SOR-04 | Moneda y tipo de cambio |
| SOR-05 | Entregas parciales y direcciones (`sdisoritemdelivery`, transportista) |
| SOR-06 | Estados: 0/1→draft, 2→sale, 3→sent, 4→done, 5→cancel |
| SOR-07 | Update y cancelación |
| SOR-08 | Cliente o producto inexistente |
| SOR-09 | Disparo o vínculo de MO por `wonumber`, sin duplicar |

### 1.6 [CU] §8 Compras `CU-POR` (9). M→O, contexto POR, fixture 07, operaciones INSERT/UPDATE/DELETE

**Modelo:** `purchase.order`.

| ID | Propósito |
|---|---|
| POR-01 | Alta de OC nacional; `purchaseordernumber` como referencia única |
| POR-02 | Moneda extranjera (`idcurrency=2`, TC 1450, `*_foreigncurrency`) |
| POR-03 | Condición "45 dias" y vencimientos |
| POR-04 | Un INSERT repetido actualiza en vez de duplicar |
| POR-05 | DELETE/CANCEL: cancelar o eliminar "según la regla" si no hay recepciones ni facturas |
| POR-06 | OC no aprobada (`situation`) |
| POR-07 | OC de solo lectura (solo el **usuario bot** modifica) |
| POR-08 | Maestro inexistente |
| POR-09 | Total de cabecera con IVA 21% vs base |

### 1.7 [CU] §9 Remitos de compra `CU-REC` (6). M→O, contexto REC, fixture 08

**Modelo:** `stock.picking` (recepción).

| ID | Propósito |
|---|---|
| REC-01 | Crea la recepción **en borrador**, vinculada a la OC |
| REC-02 | Update (clave: proveedor + serie + número) |
| REC-03 | Cancelación con reversión de stock |
| REC-04 | Remito duplicado |
| REC-05 | STK llega antes que REC: reintento |
| REC-06 | Remito con ítems (bloqueado: la muestra viene con el ítem vacío) |

### 1.8 [CU] §10 Movimientos `CU-STK` (31). Contexto STK

**Modelos:** `stock.move`/`stock.move.line`, `stock.lot`, `stock.quant`, `mrp.production`, `account.move`.

| ID | TType / sentido | Propósito |
|---|---|---|
| STK-01..08 | TType 2, op 0, M→O (09) | Ingreso por compra en KG, lote y lote de proveedor, FL→KG, vínculo REC/OC por `docnumber`, `totalvalue` como base del ajuste, CANCEL, errores, residuo de redondeo |
| STK-09..14 | TType 0, op 1, M→O (11) | Consumo vs MO, saldo de lote, CANCEL, WIP, valorización |
| **STK-15..17** | **TType 9, op 1, M→O (12)** | **Ajuste de cantidad de stock** (500 FL = 30,192 KG, lote 00000017), lote y vencimiento, idempotencia y CANCEL |
| STK-18..22 | TType 1, op 0, M→O (13) | Entrega de PT, UN vs PZ, parcial (50.000 de 100.000 → no cierra), lote y vencimiento (1899 = sin vencimiento), CANCEL |
| STK-23/24 | TType 5, M→O | Transferencia de un ítem a varios (99.0014 → 99.0004/99.0005); pares por `relatedtransactioncodeextref` |
| STK-25..30 | TType 9, **O→M** (10) | Ajuste de valor por factura de proveedor: cálculo, envío `ProcessTransaction`, tolerancia, moneda extranjera, CANCEL, reintento con el mismo código |
| STK-31 | Validación | `stockmovementtype` de las muestras contradice R12; bloquea la implementación |

### 1.9 [CU] §11 Separación `CU-PCK` (5). M→O, contexto PCK, fixture 15

**Modelo:** separación/picking (no precisado).

| ID | Propósito |
|---|---|
| PCK-01 | Alta de separación |
| PCK-02 | Ítems, lotes y bultos (100.000 UN / 2.000 CX = 50 bultos) |
| PCK-03 | Pesos neto y bruto |
| PCK-04 | `status=3` → liberada para remito |
| PCK-05 | Stock o lote insuficiente |

### 1.10 [CU] §12 Remisión y facturación `CU-BIL` (13). M→O, contexto BIL, fixtures 14 (remisión) y 16 (facturación)

**Modelos:** `account.move`, `stock.picking`.

| ID | Propósito |
|---|---|
| BIL-01 | Solicitud de remisión (`delivery=1`, `billing=0`) |
| BIL-02 | Solicitud de facturación (`billing=1`, `delivery=0`) |
| BIL-03 | Vínculo con pedido, línea y MO |
| BIL-04 | Direcciones |
| BIL-05 | Emisión de remito (`local=PADRON`) |
| BIL-06 | Rama "¿Es remisión?" |
| BIL-07 | Numeración AR: `invoicecompl` = punto de venta; `invoicenumber=0` = solicitud previa; `l10n_latam_document_number` |
| BIL-08 | Tipo de comprobante (`invoicetype=1`→`out_invoice`) y **CFOP** |
| BIL-09 | Impuestos (vacíos en el XML: se aplican los configurados) |
| BIL-10 | Nota de crédito (`invoicetype=3`, `out_refund`) |
| BIL-11 | Condición de pago |
| BIL-12 | Moneda |
| BIL-13 | Maestro inexistente |

### 1.11 [CU] §13 WIP `CU-WIP` (6). M→O (solo exportación de Metrics), manual 11.16–11.17

| ID | Propósito |
|---|---|
| WIP-01 | Etiqueta |
| WIP-02 | WIP_TR por tipo (1, 2, 3, 4, 7, 10, 11, 16, 17, 18, 20, 24, 27) |
| WIP-03 | `ProcessID`↔`idativ` |
| WIP-04 | `IdPalletLabel` |
| WIP-05 | Conciliación del consumo real |
| WIP-06 | Rechazo de un envío de WIP O→M |

**Regla:** WIP solo concilia, no mueve stock.

### 1.12 [CU] §14 End-to-end `CU-E2E` (4)

- E2E-01: producto nuevo.
- E2E-02: producto repetido.
- E2E-03: compra completa (07→10).
- E2E-04: trazabilidad WO→WIP→STK.

### 1.13 [HU] Historias de usuario (16)

**Alcance:** solo compras. El HU no nombra modelos de Odoo porque no conocía la versión.

| HU | Sentido | Propósito |
|---|---|---|
| HU-01 | — | Conexión WS: `GetPendingTransaction`, `SetTransactionResult`, `ProcessTransaction` |
| HU-02 | M→O | Lectura periódica, `SetTransactionResult`, idempotencia |
| HU-03 | — | Bitácora y reproceso |
| HU-04 | — | Equivalencias (`suppliercode`, `stockcode`, KG/FL, `idcurrency`, `idcompany`, `stockplacecode`) |
| HU-05 | M→O POR (07) | OC solo lectura; `situation`/`status`; fecha límite informativa (cabecera y línea) |
| HU-06 | — | Condición de pago por nombre; crear si falta; mostrar diferencias de vencimiento |
| HU-07 | — | OC en moneda extranjera |
| HU-08 | M→O REC (08) | Remito; clave proveedor + serie + número |
| HU-09 | M→O STK TType 2 (09) | Ingreso en KG con lote; CANCEL solo sin consumos |
| HU-10 | — | FL↔KG, factor por producto, residuo |
| HU-11 | M→O STK TType 0 (11) | Consumo por lote; ¿REQ? |
| HU-12 | — | Factura de proveedor editable; precio solo para un grupo autorizado |
| HU-13 | — | Ajuste = factura sin impuestos − `totalvalue` del ingreso − ajustes ya enviados; tolerancia |
| HU-14 | O→M STK TType 9 (10) | Envío del ajuste; campos fijos |
| HU-15 | O→M | CANCEL del ajuste con el mismo `transactioncodeextref` y la fecha original |
| HU-16 | — | Pruebas del circuito 07–11 |

---

## 2. Arquitectura técnica propuesta ([TEC] + [CU] §3 + [HU] Épica 1)

### Nombre del módulo
No está definido. [TEC] es una copia del módulo Calyx–Rofina ("cambiar nombres para EGI, lógica igual a rofina"). El modelo se llama `rofina.log` y hay que renombrarlo (p. ej. `egi.log`). **No hay nombre técnico de módulo en ninguna fuente.**

### Modelo log (`rofina.log`, [TEC] §1)

| Campo | Definición |
|---|---|
| `transaction_id` | Char indexado, **UNIQUE** (`_sql_constraints`) |
| `context_type` | Selection con **7 valores**: CRM, STKItem, STK, WO, SOR, BIL, WIP |
| `xml_operation`, `xml_data` | Text |
| `has_error` | Boolean indexado |
| `return_code` | Integer (200/500/409) |
| `xml_return` | Text |
| `dt_processing` | Datetime UTC |

### Settings ([TEC] §2)
`res.config.settings` persiste en `ir.config_parameter` cinco claves:
- URL del WSDL
- Usuario
- Contraseña (cifrado nativo)
- Entorno (Sandbox/Homologación o Producción)
- Cursor delta (solo lectura)

El botón "Testear conexión" hace un handshake SOAP y muestra una notification verde o un `UserError` con el código.

### Flujo entrante ([TEC] §3)
1. Leer el cursor.
2. Llamar con la fecha y un **límite de 100**.
3. Por cada registro, buscar `transaction_id` en el log: si existe, se ignora; si no, va a **`queue_job`**.
4. Si el lote termina completo, el cursor toma la fecha del último registro.

### Flujo "saliente" ([TEC] §3)
Ciclo: consultar pendientes → procesar → confirmar el estado a Metrics antes de seguir con el siguiente.

En realidad describe el ack de la entrada. El envío O→M real (ajuste por `ProcessTransaction`) aparece solo en HU-14 y CU-STK-26/30.

### Aislamiento ([TEC] §4)
Está marcado "**sugerencia IA — ver qué es lo mejor**".
- **A (recomendado):** commit del log y después `queue_job` para el negocio.
- **B:** savepoint o cursor independiente, más una micro-transacción para marcar el error.

### Endpoints / WS ([HU] HU-01)
- `GetPendingTransaction`
- `SetTransactionResult` (HasError 0/1 + mensaje)
- `ProcessTransaction` (envíos O→M)

Supuesto: Odoo consume el WebService directo, porque la DLL del manual es de Windows. La URL y el WSDL están pendientes.

### Reintentos
- **CU-INF-10** y CU-REC-05: reintento encolado "con espera" hasta un "máximo configurado", después error accionable y sin bucles infinitos. No se fijan cantidad, backoff ni frecuencia del cron.
- **CU-STK-30:** el reintento del envío reutiliza el mismo `transactioncodeextref`.
- La frecuencia de lectura está pendiente (HU-02).

### Usuario Bot
Solo aparece en **CU-POR-07** ("crear la OC con el bot… el bot sí puede modificar"). No hay definición de grupo, permisos ni record rules.

### Otras reglas transversales ([CU] §1.1)
- Los documentos de Metrics son de solo lectura, salvo la factura de proveedor.
- Si falta un maestro, error sin registros parciales.
- El log se confirma de forma independiente.
- Un error no frena las transacciones siguientes.

---

## 3. Diferencias contra la lista maestra (H2/H3/H5/H6)

### 3.1 Presentes acá y ausentes en la maestra
1. **Maestros CRM (clientes/proveedores), 13 casos.** La maestra solo tiene "cliente+SOR" dentro de 2082. Faltan el alta de proveedor, el actor mixto, CUIT/AFIP/IIBB, direcciones y contactos, prospectos/inactivos y la baja.
2. **Maestro de productos STKITEM, 13 casos.** Incluye itemtype→type, UOM y conversiones, tracking, NCM/EAN, bobina madre/hija, volúmenes. La maestra solo cubre categoría (2367) y analítica (2368).
3. **Ajuste de cantidad de stock M→O (CU-STK-15/16/17, TType 9, op 1, fixture 12).** No figura en la maestra.
4. **Infraestructura CU-INF-01..10** (credenciales, cursor, idempotencia, log, reintentos, `SetTransactionResult`). Sin CU propio en la maestra.
5. **WIP (CU-WIP-01..06, CU-WO-14, CU-STK-13):** conciliación de consumo, sin movimientos.
6. **Producción, temas extra:**
   - BOM armada desde MP + componentes (WO-03/04), workorders y centros de trabajo (WO-05/06).
   - Tercerización solo como costo (WO-11).
   - Consumibles no medibles al centro de costo (WO-20).
   - Costeo promedio (WO-18), BOM multinivel (WO-21), cancelación de MO (WO-17).
7. **Transferencias TType 5 genéricas (STK-23/24) y bobina madre/hija (ITM-09):** relacionadas con 2366 pero más amplias.
8. **Ventas, temas extra:**
   - Estados del pedido (SOR-06), moneda y entregas parciales (SOR-04/05).
   - Disparo de MO desde el pedido (SOR-09).
   - **Nota de crédito y devolución (BIL-10).**
   - Separación PCK como documento propio (PCK-01..05: bultos y pesos).
9. **Compras, temas extra:**
   - OC no aprobada (POR-06), solo lectura (POR-07), impuestos de cabecera (POR-09).
   - Tolerancia (STK-27), moneda extranjera (STK-28), CANCEL (STK-29) y reintento (STK-30) del ajuste.
   - Restricción de edición del precio de la factura (HU-12).
   - Cancelaciones STK de ingreso, consumo y entrega (STK-06/12/22).
10. **E2E (4) y criterios de salida (§18).**

### 3.2 En la maestra y ausentes o débiles acá
- **2368 distribución analítica por rama de categoría:** no aparece. Lo más cercano es WO-20 (centro de costo de consumibles).
- **2085 remito oficial / COT desde PCK:** no se menciona COT/ARBA. BIL-05 emite el remito desde la *solicitud de remisión* (BIL), no desde PCK. PCK-04 solo "libera para remito".
- **2084 talonario por planta:** no hay concepto de planta. BIL-07 toma el punto de venta de `invoicecompl`.
- **2086 cancelación de ventas:** solo SOR-06/07 (`status=5`). No hay cancelación de BIL, remito ni factura.
- **2255 backorder:** STK-20 y SOR-05 cubren la entrega parcial, pero no se habla de backorder de `stock.picking`/MO.
- **2245 `button_mark_done`:** no se nombra. WO-15 dice "cerrar o actualizar la MO". STK-20 dice que no cierra en una entrega parcial.

### 3.3 Contradicciones y tensiones en reglas y mapeos
1. **`context_type` del log ([TEC]):** tiene 7 valores (CRM, STKItem, STK, WO, SOR, BIL, WIP). **Faltan POR, REC y PCK**, que [CU] y [HU] procesan.
2. **TType 9 tiene dos usos:**
   - O→M ajuste de valor: op 0, `quantity=0`, `lot=UNICO` (STK-26).
   - M→O ajuste de cantidad: op 1, lote real (STK-15).

   El módulo necesita discriminar por sentido y cantidad. Ademas, para STK-26 [CU] §16 #20 deja abierto si se envía "al confirmar o al publicar".
3. **`stockmovementtype` vs R12 (STK-31):** las muestras no coinciden con R12 (09: smt=2/op 0; 11: smt=0/op 1; 10: smt=1). Implementación **bloqueada** hasta tener la tabla de Metrics.
4. **`materialtype` (ITM-13):**
   - STKItem: 1 Tinta, 2 Plancha, 3 Otros, 4 Papel Hoja, 5 Papel Bobina, 6 Personalizado.
   - WO: 0 Papel, 1 Tinta, 2 Plancha, 3 Otros.

   No se puede reutilizar una tabla en el otro contexto.
5. **`itemtype`→`type=product` (ITM-01/02/03):** en Odoo 17+ / 19 no existe `type='product'` (se usa `consu` + `is_storable`). El mapeo R07 está escrito con la semántica vieja. **Esto es observación mía, no de las fuentes.** [HU] además dice que no conocía la versión de Odoo.
6. **Estado de la MO:** CU-WO-02 dice que `status=3` → "cerrado o terminado", pero el fixture 05 de *alta* (WO-01) viene con `status=3`. Si fuera así, una MO nueva nacería cerrada, y eso choca con la maestra (cierre por `button_mark_done` al entregar el PT).
7. **Estados SOR (SOR-06):** 2→`sale` pero 3→`sent`. Es un retroceso de estado, inconsistente en el orden de Odoo.
8. **CFOP (BIL-08):** es un concepto brasileño en un proyecto argentino (l10n_ar). Viene de R16/R18.
9. **Consumo con o sin MO:** HU-11 lo deja pendiente ("órdenes de producción de Odoo o solo movimiento de stock"). [CU] ya asume MO (WO-13, STK-09), en línea con la maestra 2244. HU está desactualizado.
10. **Valorización del consumo:** HU-11 y STK-14 dejan abierto si se usa el valor de Metrics o el costo promedio de Odoo. WO-18 asume costo promedio.
11. **Inactivos CRM:** CRM-09 dice que `isactv=0` no se crea ("omitido"). CRM-13 dice que `isactv=0` archiva un partner existente. Es coherente solo si se distingue alta de update; no está explicitado.
12. **Recepción:** REC-01 crea la recepción "en borrador" y STK-01 la valida. Coincide con la maestra 2361, pero HU-08 la define sin modelo y con la muestra sin ítems (REC-06 bloqueado).
13. **Categorías (ITM-05):** raíz "Metrics" → master → group, con el producto en el group. Coincide con "categoría hoja" de 2367, pero la maestra no menciona la raíz "Metrics".
14. **OP compartida:** WO-08/09/10 coinciden con 2237 (una MO por PT y prorrateo por cantidad planificada). Agregan la regla de que el último PT absorbe el residuo, y su prorrateo también aplica a la tercerización.
15. **Bot:** solo aparece en POR-07. La maestra probablemente lo da por sentado; no hay definición de permisos.

---

## 4. Puntos abiertos / decisiones pendientes

### [CU] §16 Pendientes consolidados (20)

| # | Pendiente | Responsable |
|---|---|---|
| 1 | Endpoint y WSDL | Metrics |
| 2 | Tabla `idcurrency` (no se puede confirmar que 2 = USD) | Metrics |
| 3 | Regla de vencimiento "45 dias" (hipótesis: fin de mes + 45; la muestra da 14/09 y no 06/09) | Metrics / negocio |
| 4 | Muestra REC con ítems y número de OC | Metrics |
| 5 | STKItem `02.01.0003` con UOM y `WeightKg` | Metrics |
| 6 | ¿Se importa REQ? | Metrics |
| 7 | Ajustes negativos y contenido de `docnumber` | Metrics |
| 8 | Política de OC no aprobada | Negocio |
| 9 | Tolerancia, tipo de cambio y fecha del ajuste | Negocio |
| 10 | Residuo de kilos (0,24 KG en 600 consumos de 100 FL) | Negocio |
| 11 | Valorización del consumo: Metrics vs Odoo | Negocio |
| 12 | Semántica de `stockmovementtype` | Metrics |
| 13 | `sdiwocomponent`: ¿insumo o PT? | Metrics |
| 14 | Muestra con `originitem` (bobina madre/hija) | Metrics |
| 15 | Muestra de BOM multinivel | Metrics |
| 16 | Versión de Odoo y módulos | Proyecto |
| 17 | Destino de `productclassification` | Proyecto |
| 18 | Absorción del residuo porcentual | Negocio |
| 19 | PT con `controltraceability=1` | Negocio |
| 20 | ¿El ajuste se envía al confirmar o al publicar la factura? | Negocio |

### [HU] Pendientes consolidados (11)
Repite los #1–11 de arriba, incluido "Versión de Odoo", que ya está resuelta: Odoo 19 Enterprise.

Agrega estos pendientes de detalle:
- Comportamiento de Metrics si Odoo no responde el resultado, y frecuencia de lectura (HU-02).
- Significado de los atributos `*_foreigncurrency` (HU-07).
- Si `docnumbercompl` trae el código de proveedor (HU-09).
- Si con la OC en solo lectura se puede generar la factura de proveedor (HU-05).
- Si el total de la OC incluye 21% de IVA (supuesto).
- Si `transactiondt` del ajuste toma la fecha de la factura o de la recepción, y si `transactioncode` repite `transactioncodeextref` (HU-14).
- Cómo restringir la edición del precio de la factura (HU-12).

### Decisiones "según política", sin definir, dentro de los CU
- WO-06: crear el centro de trabajo o dar error.
- POR-05: cancelar o eliminar la OC.
- STK-11: falla o consumo parcial con saldo insuficiente.
- BIL-05: descontar o reservar stock en el remito.
- BIL-06: documento mixto con `billing=1` y `delivery=1`.
- WO-12: producir con faltantes.
- STK-21: vencimiento 1899 interpretado como "sin vencimiento".

### [TEC]
- El patrón de aislamiento A/B está marcado como sugerencia de IA a validar.
- Falta el renombre `rofina` → EGI.
- No define cantidad de reintentos, backoff ni el cron.
