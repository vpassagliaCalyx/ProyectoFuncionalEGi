# Digest – Manual "Metrics Integración XML – Revisión 93" (SDI)

Fuente: `contexto/RelevamientosEGi/XMLs2/Metrics Integración XML - Revisión 93 (1).pdf` (225 págs., rev. 93 del 06/02/2024, autor EProductivity Software / EPS). Las páginas citadas son las del índice del manual ("p."). Todo lo que sigue sale del manual; lo marcado **[AMBIGUO]** o **[INFERENCIA]** es interpretación nuestra.

---

## 1. Mecanismo general

### 1.1 Qué es el SDI
- "SDI" es el módulo de integración de Metrics. EPS provee el módulo SDI (monitor) y el servidor **MTCSERVER** que procesa las transacciones (§5.2, p.15).
- Tecnologías: XML + **SQL Server o WebServices** (§6, p.15). Prerrequisito: IIS del SDI en 32 bits (§4).
- Regla de formato (§2, p.14): **todos los atributos deben escribirse en minúsculas**, aunque el manual los muestre en CamelCase. Si hay divergencias entre el manual y el XML de ejemplo que entrega EPS, **manda el XML de ejemplo**.
- Atributos que no aplican pueden ir **vacíos** (ej. `idcountry=""`) (§11.5, p.39).
- Fechas: formato `AAAA-MM-DDTHH:MM:SS.MMM` (ej. `1970-12-30T00:00:00.000`) en todos los XMLData. En el WebService, `DtProcessing`/`InsDt` van como `yyyy-mm-dd hh:nn:ss` (§11.2).
- Booleanos: `"0"`=No, `"1"`=Sí.
- **Encoding: el manual no lo especifica** [AMBIGUO] – no hay mención a UTF-8/ISO-8859-1. Validar con el XML de ejemplo/EPS.

### 1.2 Cada transacción = 3 XML
| XML | Función |
|---|---|
| **XMLOperation** | Qué operación (INSERT/UPDATE/DELETE/…) y sobre qué contexto (§11.5.1) |
| **XMLData** | Los datos del registro, con estructura propia por contexto (§11.6 en adelante) |
| **XMLReturn** | Resultado del procesamiento (OK/error + mensaje) (§11.5.2) |

### 1.3 Modalidad A – Tablas de integración en la BD de Metrics (§7–9, p.15–22)
- **Importación (tercero → Metrics):** el tercero inserta una fila en `sdiTmImportData` (BD de Metrics); Metrics la procesa y completa `XMLReturn`, `HasError`, `DtProcessing` (§9.1, leyenda A–D).
- **Exportación (Metrics → tercero):** cuando Metrics detecta un cambio (ej. un teléfono de una relación), inserta una fila en `sdiTmExportData`. El tercero **hace polling** de esa tabla, procesa y **graba el XMLReturn** con el estado (§7.2, §9.2 leyenda B).
- Columnas (§8.1/8.2, p.17): `DtProcessing`, `InsDt`, `ExtRef` (varchar, libre / referencia del sistema que corresponda), `InsUser`, `XMLOperation` (text), `XMLData` (text), `XMLReturn` (text), `HasError` (int: 0 = OK, ≠0 = con error), PK `idimportdata` / `idExportdata` (autoincremental), `ContextType` (varchar: CRM, SOR, BIL, CR, …).
- [AMBIGUO] El diagrama §9.1 (importación) rotula la tabla como `sdiTMExportData`, pero la leyenda dice `sdiTMImportData`; tomamos la leyenda como correcta.

### 1.4 Modalidad B – WebService (§10–11.3, p.23–32)
Interfaz **IMetricsSDIWebService** (§11.1):
- `GetPendingTransaction(SDICredentials)` → devuelve la próxima transacción exportada por Metrics pendiente de consumir + `TotalPendingTransaction` (§11.1.1).
- `SetTransactionResult(SDICredentials, SDITransactionHeader, SDITransactionResult)` → **el tercero informa a Metrics el resultado** de procesar una transacción obtenida con GetPendingTransaction (§11.1.2). Es el "ACK".
- `ProcessTransaction(SDICredentials, SDITransactionHeader, SDITransactionData, SDITransactionOperation)` → el tercero pide a Metrics que **importe** datos (§11.1.3).
- Tipos (§11.2, tabla muy desordenada en el PDF): `SDICredentials` (User, Password); `SDIRequestResult` (ReturnCode int 0=OK/otro=error, MSG); `SDITransactionHeader` (TransactionID int, DtProcessing, InsDt, ExtRef = "código usado por el sistema tercero para identificar la transacción", InsUser, HasError 0=OK/1=error, ContextType); `SDITransactionOperation` (Operation); `SDITransactionData` (XMLData); `SDITransactionResult` (ReturnCode, Operation, MSG).

Interfaz **IMetricsSDIBasicCall** (§11.3, pensada para Java/C#; todo string):
- Parámetros comunes (§11.3.1): `pUser`, `pPsw`, `pIdTransaction` (ID de la transacción en Metrics), `pExtref` (ID en el sistema tercero), `pHasError` (**0 ok, -1 con error**).
- `GetPendingtrasctionBasic(pUser,pPsw)` (sic) → respuesta:
  `<GetPendingtrasctionBasicResponse><RequestResult ReturnCode Msg TotalPendingTransaction/><SDITransactionHeader TransactionID="12345" ContextType="CRM" Operation="INSERT"/><XMLData><![CDATA[<METRICS>…</METRICS>]]></XMLData><TransactionResult …/></…>` (§11.3.1.1, p.27).
- `SetTransactionResultBasic(pUser,pPsw,pIdTransaction,pExtref,pHasError,pResult)` → `<SetTransactionResultResponse ReturnCode Msg/>` (§11.3.1.2, p.29).
- `ProcessTransactionBasic(pUser,pPsw,pContext,pExtRef,pXmlData,pOperation)` → `<ProcessTransactionBasicResponse ReturnCode Operation Msg/>` (§11.3.1.3, p.30).
- Variantes `…Basic2`: idénticas pero **sin `<![CDATA[`** en Msg/XMLData.
- `MetricsSDIClientDLL.dll` (§11.3.1.4): DLL Windows que encapsula estas 3 llamadas (config generada con `MetricsSDIClient.exe`). No aplica directamente a Odoo (Python/Linux) [INFERENCIA].
- [AMBIGUO] El formato de `pResult` en SetTransactionResultBasic no está definido; lo lógico es enviar el XMLReturn (§11.5.2) o un mensaje. Confirmar con EPS. También hay discrepancia de códigos de error: `pHasError` usa -1, `HasError`/`Return` usan 1 o "≠0".

### 1.5 Módulo SDI (monitor, §11.4, p.33–38)
Pantalla de Metrics para ver importaciones/exportaciones: filtros por tipo de operación/contexto, situación (Todas/Esperando/Procesadas), resultado (Todas/OK/c/Error), fechas y **Código Externo** (ExtRef, ej. "código del pedido en el sistema tercero"). Grilla: ID transacción, tipo de operación, fecha ingreso, usuario, fecha y status de procesamiento; detalle con los 3 XML.

### 1.6 XMLOperation (§11.5.1, p.39–42)
```xml
<metrics><sdistandardoperation>
  <sdiloperationcontext lcount="1">
    <sdioperationcontext name="STK" sequence="1">
      <sdiloperation lcount="1"><sdioperation name="INSERT" sequence="1"/></sdiloperation>
    </sdioperationcontext>
  </sdiloperationcontext>
</sdistandardoperation></metrics>
```
- `sdiOperationContext/@Name` (String(10)) = contexto. **Una sola operación y un solo contexto por XML** (LCount=1, Sequence=1).
- `sdiOperation/@Name` = operación. El manual de OE06 lista INSERT/UPDATE/DELETE, pero los contextos usan además **CANCEL, PROCESS, UPDATESTATUS** y el histórico (rev. 43) agrega **INSERTUPDATE** (no documentada en la tabla) [AMBIGUO].
- En casi todos los contextos: "la estructura del XML es igual en todas las operaciones; sólo cambia el NAME de sdiOperation".

### 1.7 XMLReturn (§11.5.2, p.43–46) – respuesta/ACK
```xml
<metrics><sdistandardxmlreturn><sdilxmlreturn lcount="1">
  <sdixmlreturn return="0" msg="" operation="INSERT" operationsequence="1"
                context="BIL" contextsequence="1" docnumber=""/>
</sdilxmlreturn></sdistandardxmlreturn></metrics>
```
- `Return` (Int): **0 = OK, 1 = error**. `Msg` String(200): inconsistencia. `Operation`: INSERT/UPDATE/DELETE. `OperationSequence`/`ContextSequence`: siempre 1. `Context` String(10).
- `DocNumber` Varchar(32), opcional: identificador del registro importado en Metrics (STKITEM=código de ítem; SOR=nº de pedido; CRM=código de cliente; POR=nº de orden de compra).
- Lo genera Metrics al importar; **en la exportación lo genera el tercero** (§9.2-B) y lo deja en la columna XMLReturn o lo manda vía SetTransactionResult.

### 1.8 Referencias externas (ExtRef)
- Casi todos los contextos tienen `ExtRef` = código del registro en el sistema tercero (cliente, dirección, contacto, pedido, factura, OC…). En CRM, el ExtRef de relación, contacto y dirección **deben ser distintos entre sí** (§11.6).
- STK tiene tres refs específicas (§11.10.1.1, p.82–86) – ver §2.5.

---

## 2. Contextos

### 2.0 Tabla resumen (dirección según §x.1.3/x.1.4 de cada contexto)
"Imp." = tercero→Metrics (ProcessTransaction / sdiTmImportData). "Exp." = Metrics→tercero (GetPendingTransaction / sdiTmExportData).

| § (p.) | Contexto | Raíz XMLData (bajo `<metrics>`) | Imp. | Exp. |
|---|---|---|---|---|
| 11.6 (46) | CRM Relaciones (clientes/proveedores/vendedores/transportistas) | `sdiCrmActor` | INS/UPD/DEL | INS/UPD/DEL |
| 11.7 (56) | SOR Pedidos de venta | `sdiSORSalesOrder` | INS/UPD/DEL | INS/UPD/DEL |
| 11.8 (64) | BIL Facturas/Remisiones | `sdiBilInvoice` | INS/UPD/DEL/CANCEL/PROCESS | ídem |
| 11.9 (74) | STKITEM Ítems de stock | `sdiStkItem` | INS/UPD/DEL | INS/UPD/DEL |
| 11.10 (82) | STK Movimientos de stock | `sdiStkTransactionGroup` | INSERT/CANCEL | INSERT/CANCEL |
| 11.11 (87) | REQ Solicitudes de materiales | `sdiReqRequisition` | INS/UPD/DEL | INS/UPD/DEL |
| 11.12 (90) | PS Estructuras de producto | `sdiPSProductStructure` | no | INS/UPD/DEL |
| 11.13 (97) | WO Órdenes de producción | `sdiWOWorkOrder` | no | INS/UPD/DEL |
| 11.14 (104) | INT-OP OPs para JobTrack/M3 Planner | `WOMainNode` (sin `<metrics>`) | UPD/DEL/UPDATESTATUS/CANCEL | ídem |
| 11.15 (116) | WO_ESKO | `sdiWOEsko` | no | INS/UPD |
| 11.16 (137) | WIP etiquetas en proceso | `sdiWIPLabel` | no | INSERT |
| 11.17 (139) | WIP_TR transacciones etiqueta WIP | `sdiWIPTransaction` | INSERT | INSERT |
| 11.18 (142) | STK_VL ítems por volúmenes (lotes de entrada) | `sdiStkVolumeInputLot` | UPD/DEL/CANCEL | no |
| 11.19 (147) | STK_VT transacciones de volúmenes | `sdiStkVolumeTransactionLot` | PROCESS | PROCESS |
| 11.20 (151) | STK_VR solicitudes de volúmenes | `sdiStkRequestedMaterial` | no | PROCESS |
| 11.21 (153) | STK_LBL entregas de producción por etiqueta | `sdistkreportproductionlabels` | no | PROCESS/CANCEL |
| 11.22 (158) | ACR Pos cálculo (costos por OP) | `sdiACRTransactionGroup` | INSERT | no |
| 11.23 (162) | JBT fin/suspensión de trabajo JobTrack | `jbtJobFinalization` | no | INSERT (disparo manual) |
| 11.24 (163) | CR Títulos financieros (CxC/CxP) | `sdiCRGroup` | INS/UPD/DEL | INS/UPD/DEL |
| 11.25 (169) | CTB_CTA Plan de cuentas | `sdiCtbCtaContabil` | no | INS/UPD (lote manual) |
| 11.26 (171) | STK_NCM Clasificaciones fiscales | `sdiStkNCM` | no | INS/UPD/DEL (lote manual) |
| 11.27 (172) | CTB_LCTO Asientos contables | `sdiCtbLoteLactoContabil` | no | INS/UPD/DEL |
| 11.28 (174) | STK_BLC Saldos de stock | `sdiStkBalance` | no | INSERT (disparo manual) |
| 11.29 (179) | BIL_NFE_REC | layout NF-e SEFAZ (sólo Brasil) | – | – |
| 11.30 (179) | REC Facturas de compra procesadas | `SdiProviderReceipt` | no | INS/UPD/CANCEL |
| 11.31 (183) | BIL_NFE_ENV | layout NF-e SEFAZ (sólo Brasil) | – | – |
| 11.32 (183) | CTB_CTC Centros de costo | `sdiCtbCostCenter` | no | INS/UPD/DEL (lote manual) |
| 11.33 (186) | POR Órdenes de compra | `sdiPORPurchaseOrder` | INS/UPD/DEL | INS/UPD/DEL |
| 11.34 (192) | JBT_APT Apuntes JobTrack | `Ljbtjobentry`/`jbtjobentry` | PROCESS | no |
| 11.35 (194) | PCK Solicitud de picking (separación) | `SdiPCKSeparation` | UPD/PROCESS/DEL/CANCEL | INS/UPD/DEL |
| 11.36 (199) | PRQ Solicitudes de compra | `SdiPRQPurchaceRequest` (sic) | UPDATE (sólo situación) | INS/UPD/DEL |
| 11.37 (202) | OSP Lotes de pago a terceros | `SdiOSPPaymentLot` | no | INS/UPD/DEL |
| 11.38 (206) | SCHD Planificación de actividades | `sdischdplanner` | no | INS/UPD/DEL |
| 11.39 (208) | IQT Presupuesto IQuote | `sdiiqtquote` | no | INSERT |
| 11.40 (219) | QTTEP Creación de presupuesto por EP | `sdiQttInfo` | sí | no |

Nota: **No existe un contexto "CUS"**; clientes/proveedores van por **CRM**. Tampoco hay un contexto específico de "respuesta de factura/remito": la respuesta siempre es el XMLReturn genérico.

### 2.1 CRM – Relaciones (§11.6, p.46–55)
- `sdiCrmActor` (CE02): `Code` (Int, obl.), `PersonTypeCompl` (0 Matriz, 1 Sucursal, 2 Área), `PersonType` (0 Persona física, 1 Jurídica, 2 Gobierno, 3 Exportación), `CountryDocumentNumber` (RUC/RUT, obl.), `Name` (fantasía), `FullName` (razón social), `ExtRef` (obl.), `Isactv`, flags `IsCustomer`, `IsSupplier`, `IsPerson`, `IsBroker` (agencia), `isCustomerService` (vendedor), `IsTransport`; `CountryCode` (BACEN), `CountryFiscalCode`, `ConditionPaymentStandard`, `Email`, `Emailtax`, `EmailBilling`, `LimitValueCredit`, `CreditExpirationDt`, `InvoiceCFOP`/`ShippingCFOP`/`InvoiceandShippingCFOP`, `UserFieldClassic1..5`, `userfield1..8`.
- Hijos: contactos `sdiCrmActorContact`, direcciones `sdiCrmAddress` (IsBilling/IsCharging/IsMailing/IsDelivery, ExtRef obl.), `sdiCrmCustomer`, `sdiCrmSupplier`, `sdiCrmPerson`, `sdiCrmCustomerService` (vendedores), `sdiCrmProduct`, tablas `*_u`.

### 2.2 SOR – Pedidos de venta (§11.7, p.56–64)
- `sdiSORInfo` (SE03): `IdCompany`, `SaleOrderNumber` String(13), `Status` (**1 Esperando liberación, 2 Liberado, 3 Bloqueado, 4 Cerrado**), `SalesManCode`, `CustomerOrderId` (OC del cliente), `DueDt`, `ExtRef` (obl.), `IdCurrency`, `QuotationDt`, `ExchangeRate`, `SalesOrderNote`, `ShippingType` (0 Emisor, 1 Destinatario/Remitente, 2 Terceros, 9 Sin flete), `UserInfo1..6`.
- `sdiSORPayCondInfo` (ConditionCode) → `sdiSORPayCondDueDate` (DueDate, Value); `sdiSORCommissioninfo` (CommissionType 1 Vendedor/2 Agencia/3 Productor; ValueType 1 %/2 monto); `sdiSORCustomerinfo` (Code, Name, ExtRef, ContactName).
- Ítems `sdiSORItemInfo`: Seq, StockCode, ProductName, UnitValue, Quantity, TotalValue, UnitCode, WONumber, QuoteNumber, CustomerStockCode, customerpurchaseorder/customeritempurchaseorder; userinfo1..6 **sólo exportación**. Impuestos `sdiSORItemTaxInfo` (TaxId, Code, Name, ValueType, Value).
- Entregas `sdiSORItemDelivery`: DeliveryDt, DeliveryQty, CarrierCode, **`Delivery` (remisión 0/1), `Billing` (factura 0/1)**, DeliveryCustomerCode/Extref, `Status` (0 Abierto, 1 Cerrado – permite cerrar entregas), + dirección `sdiSORAddress`.
- Opcional `sdiRecOrignInfo/sdiLRecord/sdiRecord` (líneas del archivo de texto origen).

### 2.3 BIL – Facturas / Remisiones (§11.8, p.64–74)
- Operaciones: **INSERT, UPDATE, DELETE, CANCEL, PROCESS**, en importación y exportación (§11.8.1.3).
- `sdiBilInvoiceInfo` (BE03): `InvoiceReqNumber` String(10) (nº de **solicitud** de factura), `InvoiceNumber` String(10), `InvoiceCompl` String(3) (serie), **`Status` (1 No procesado, 2 Procesado, 3 Cancelado)**, `EmissionDt`, `IdCompany`, `Extref` (obl., "código en el sistema tercero"), `UserInfo1..5`, **`InvoiceType` (0 Compra, 1 Venta, 2 Devolución de compra, 3 Devolución de venta)**, `InvoiceMessage`, `IsBrokerResponsiblePayment`, `accesskey` (llave de acceso FFe).
- `sdiBilPayConInfo` (ConditionCode, ExtRef) → `sdiBilPayCondDueDate` (DueDate, Value). [AMBIGUO] el nombre aparece como `sdiBilPayConInfo` en la tabla y `sdiBilPayCondInfo` en el diagrama (corregido en rev. 36 → usar el del XML de ejemplo).
- `sdilAddress/sdiBilAddress` (IsBilling, IsCharging, IsDelivery, ExtRef), `sdiBilCustomerInfo` (Code, Name, ExtRef, ContactName).
- Ítems `sdiBilItemInfo`: ItemID (lo completa Metrics, default ""), Seq, StockCode, CustomerStockCode, ProductName, UnitValue, Quantity, TotalValue, UnitCode, `CFOP` String(5) (operación del ítem), CustomerPurchaseOrder/Item.
  - `sdiBilItemReturned` → `sdiBilItemReturnedDetail` (lotes devueltos: Lot, StockPlaceCode, StockAddress): obligatorio si InvoiceType = 2 o 3.
  - `sdiBilItemTaxInfo` (Name, Value), `sdiBilItemCommissionInfo` (CommissionType 1/2, ValueType 1/2).
  - **`sdiBilItemSorItemRef`** (vincula el ítem con el pedido): Quantity, TotalValue, WONumber, QuoteNumber, **`Billing` (es factura 0/1), `Delivery` (es remisión 0/1)**, SalesOrderNumber, SalesOrderExtRef, StockCode, ItemObs → `sdiBilItemSorItemStockLocal` (Local, Quantity, Location, Lot; vacío = "ÚNICO") y `sdiBilBrokerInfo`.
- **Tipos "F/R"**: el manual **no usa letras F/R**; la distinción factura/remisión se hace con los flags `Billing`/`Delivery` (en SOR entregas y en BIL SorItemRef) y en REC con `IsBilling`/`IsDelivery`. Si en los XML reales aparece F/R, es un valor de otro campo no documentado aquí [AMBIGUO].

### 2.4 STKITEM – Ítems de stock (§11.9, p.74–81)
- `sdiStkItem`: `idItem` (sólo exportación), `StockCode` String(20), `Status` (activo 0/1), **`MaterialType` (1 tinta, 2 plancha, 3 otros, 4 papel en hoja, 5 papel en bobina, 6 personalizado)**, **`ItemType` (0 materia prima, 1 producto terminado, 2 producto intermediario, 3 servicio, 4 consumibles)**, MaterialName, `UnitCode` (stock), `UnitCodeDemand` (consumo), `UnitCodeCost` (costo); Height/Width/Grammage obligatorios si MaterialType=4; CustomMaterialTypeCode/Description si =6; MaterialGroupCode/Description y MasterMaterialGroupCode/Description (obl.); NCM, EAN, WeightKg, IsFSC, UseLot, UseAddress, IsInventoried, ControlTraceability, TipoItemSped (00…99), userfield1..8, PackagingQty/Unit, BillingDescription, InvoiceItemType/ShippingItemType/InvoiceShippingItemType (0 Estándar, 1 Producto, 2 Servicio), NeedSeparation, etc.
- Opcional `sdistkitemvolumeinfo` (bobinas: pesos, diámetro).
- Regla (§11.9.1.3): **INSERT sobre StockCode existente ejecuta UPDATE; UPDATE sobre inexistente ejecuta INSERT** (upsert).

### 2.5 STK – Movimientos de stock (§11.10, p.82–86) – el más relevante
Estructura: `<metrics><sdiStkTransactionGroup><sdiLStkTransaction LCount="n"><sdiStkTransaction …/>…`
- **`TransactionType`** (Int, obl.):
  | Valor | Significado |
  |---|---|
  | 0 | Atención o devolución de solicitud de materia prima (OperationType distingue atención=salida / devolución=entrada) |
  | 1 | Entrega de producción |
  | 2 | Compras |
  | 3 | Ventas |
  | 4 | Inventario |
  | 5 | Transferencia entre ítems de stock |
  | 6 | Volúmenes |
  | 7 | Transferencia entre empresas |
  | 8 | Transferencia |
  | 9 | **Ajuste de saldo** |
  | 10 | Otro |
  | 11 | Recálculo del costo promedio |
- **`StockMovementType`**: 0 Físico, 1 Financiero, 2 Físico/Financiero.
- **`OperationType`**: 0 Entrada, 1 Salida.
- Otros (obl. salvo indicación): `Lot` String(40), `DocNumber` String(20), `DocNumberCompl` (opc.), `StockAddress` (localización), `TransactionDt`, `StockCode` String(16), `UnitCode`, `Quantity`, `TotalValue` (valor monetario total en moneda estándar), `WONumber` (marcado obligatorio; OP origen), `StockPlaceCode` (local), `IdCompany`; opcionales `CostCenterCode/Name`, `TransactionCode` String(15) (ID de la transacción **en Metrics**), `UnitCostCode`, `QuantityUnitCost`, `ExpirationDate`/`ProductionDate`/`ProviderLot`/`UnitLot` (obligatorios si el ítem tiene trazabilidad), `GrossWeight` y `LogUser` (sólo exportación), `UserField1..5`.
- **Refs externas** (todas **Double**, o sea numéricas [ojo para Odoo: no admiten strings]):
  - `TransactionCodeExtRef`: ID único de la transacción en el sistema de origen; no puede repetirse. **Para CANCEL se manda el código de la transacción original** + operación CANCEL.
  - `RelatedTransactionCodeExtRef`: ID de la transacción relacionada; necesario para valorizar bien transferencias (en la entrada de transferencia identifica la salida) y devoluciones de solicitud (identifica la atención que se devuelve).
  - `TransactionOriginExtRef`: ID del registro origen **en Metrics**; en atención de solicitud debe identificar **el ítem de la solicitud** (obligatorio); en devoluciones también, si no se informa RelatedTransactionCodeExtRef.
- Reglas (§11.10.1.3): operaciones **INSERT y CANCEL** (imp. y exp.). En CANCEL, `TransactionDt` = fecha de la transacción original. INSERT de importación puede crear lotes de Producto Adquirido y de Producción Interna; estos últimos si el ítem controla trazabilidad y TransactionType=1, con WONumber obligatorio (errores: "Necesario informar el número de la OP", "Orden de producción "%s" no está registrada", "Ítem de stock: %s no encontrado en la OP: %s").
- [INFERENCIA, no dicho en el manual] Un ajuste sólo de valor (revalorización) se modelaría como TransactionType=9 con StockMovementType=1 (Financiero) y TotalValue; el manual no describe semántica adicional del tipo 9 ni que el ERP deba enviarlo. Confirmar con EPS.
- [AMBIGUO] La tabla dice que `sdiStkTransaction` tiene padre STE01, pero el diagrama la ubica bajo `sdiLStkTransaction` (STE03); usar el diagrama.

### 2.6 REQ – Solicitudes de materiales (§11.11, p.87–90)
`sdiReqRequisition`: IdReq (si no viene se genera), IdCompany, RequesterName, EmissionDt, ApprovalName/Dt, `TransactionCode` (obl.), WONumber, UserField1..5 → `sdiReqRequisitionItem`: IdReqItem, StockCode, Quantity, UnitCode, QuantityUnitCost, UnitCostCode, CostCenterCode, **Status (0 Abierto, 1 Cerrado)**, Note. Importada no queda asociada a OP; DELETE se rechaza si algún ítem ya fue atendido.

### 2.7 WO – Órdenes de producción (§11.13, p.97–103) – sólo exportación
- `sdiWOWorkOrderInfo`: IdCompany, WONumber String(20), QuoteNumber, **`Status` (0 abierta, 1 finalizada, 2 cancelada, 3 bloqueada, 4 evaluación de carga)**, InsertDt, WODescription, ProjectCode/Title, Userinfo1..5.
- `sdiWOCustomerInfo` (Code, ExtRef, Name); `sdiWOFinishedItem` (StockCode, ProductName, UnitCode, Quantity, DeliveryDt, IsFSC); `sdiWORawMaterial` (**MaterialType 0 Papel, 1 Tinta, 2 Plancha, 3 Otro** – ojo, distinto del enum de STKITEM), StockCode, Quantity, ProcessGroupCode, ActivityCode); `sdiWOOperation` (ResourceCode/Name, TotalTime, SetupTime, ProductionTime, Sequence, IdAtiv…); `sdiWOOutsourcing` (servicios tercerizados con TotalValue, CostAccountCode, Currency); `sdiWOComponent` / `sdiWOInputComponent`.

### 2.8 CR – Títulos financieros (§11.24, p.163–168)
`sdiCRGroup/sdiLCR/sdiCR`: CrId, InvoiceNumber/InvoiceCompl (obl. si OriginDocumentType≠7), IdTitulo, IdCompany, CurrentValue, CurrentPaidValue, Discount, Interest, InsDate, DueDate, PayDate, **CrStatus (1 Abierto, 2 Bajado/pagado, 3 Cancelado)**, ValuePaymentCommission (0 valor del título, 1 valor del pago), IdCurrency, ExtRef, ExchangeRate, **OriginDocumentType (0 usuario, 1 Facturación, 2 Compras, 3 Comisiones, 5 flete, 6 Control de terceros, 7 anticipo de pedido de venta)**, ForeignValue, ActorCode/ExtRefActor, SalesOrderNumber (obl. si 7), IdDoctoType, IdBankAccount, **financialtype (0 CxC, 1 CxP)**, PaymentFormCode → prorrateo `sdicrallocation` (CostCenterID, FinancialAccountingID, BusinessUnitID, Percentage).

### 2.9 STK_BLC – Saldos de stock (§11.28, p.174–179) – sólo exportación, disparo manual
`sdiStkBalance` (IdCompany, Company, BalanceDate, StockPlaceCode) → `sdiStkBalanceItem` (StockCode, StockCodeExt, Description, UnitCode, **PhysicalBalance, FinancialBalance, AverageCost**) + listas de ítems propios en poder de terceros y de terceros en poder de la gráfica. Se genera desde Controlar Materiales › Stock › Informes › SDI › Exportación de Saldos de Stock vía SDI.

### 2.10 REC – Facturas de compra procesadas (§11.30, p.179–183) – sólo exportación
Automático si en Integraciones › SDI › Configuraciones está tildado "Facturas Fiscales (Compras)". Ops INSERT/UPDATE/CANCEL. `SdiProviderReceipt`: ReceiptNumber/Serie, ReceiptDate, ReceiptProcessing, ProviderCode/Name/CountryDocument + dirección, PayCondition, moneda/tasa → ítems `SdiProviderItemReceipt` (ItemCode, Quantity, Unit, UnitPrice, TotalPrice, Discount, **IsBilling/IsDelivery**, Tax1Percentage/Value (IVA), costos de flete/seguro) → `SdiReceiptPurchaseOrder` (PurchaseOrder, cantidad/valor atendido).

### 2.11 POR – Órdenes de compra (§11.33, p.186–192)
`sdiPORPurchaseOrderInfo`: IDCompany, PurchaseOrderNumber (Int), EmissionDt, SupplierCode, ContactName, LimitReceiptDt, TotalValue, **Situation (0 No aprobada, 1 Aprobada, 2 Rechazada, 3 En aprobación)**, **Status (0 Abierta, 1 Cerrada)**, IDCurrency, TransporterCode, ExtRef. Pago (`sdiPORPayCondInfo`/DueDate). Ítems `sdiPORItemInfo`: StockCode, Quantity, TotalReceiptQty, UnitCode, UnitValue, TransportCost, TotalValue, LimitReceiptDt, **Status (0 Pendiente, 1 Parcialmente entregado, 2 Totalmente entregado)**, OtherCosts, IdCurrency, ExchangeRate, UserField1..5 → `sdiPORItemReceiptInfo` (recepciones: DocumentNumber de la factura de entrada, cantidades/valores) **sólo exportado, no se procesa en la importación**.

### 2.12 PCK – Solicitud de picking / separación (§11.35, p.194–199)
`SdiPCKSeparation`: IDSeparation, IDCompany, CustomerCode, InvoiceReqNumber, **Status (0 Pendiente, 1 Atendida, 2 Procesada, 3 Liberada para emisión, 4 Factura emitida)**, pesos, volúmenes → `SdiPCKProcessInfo` (StockPlaceCode/StockAddressCode, obligatorios para PROCESS) → `SdiPCKSeparationItem` (Status 0 No atendido, 1 Parcial, 2 Atendido) → `SdiPCKTrackOutputEntry` (lotes separados: Quantity, Lot, Stockplacecode, StockAddress).
Reglas de importación: UPDATE sólo cambia situación si no está Pendiente/Atendida; PROCESS sólo si todos los ítems atendidos; DELETE sólo en ABIERTO y sin ítems atendidos; CANCEL sólo si Procesado o Liberado para emisión y sin factura emitida.

### 2.13 Otros (breve)
- **ACR (§11.22)**: importa costos por OP. `ACRTransactionType` 1 Previsto, 2 Previsto extorno, 3 Real, 4 Real extorno; `ACRAccountType` 1 materiales, 2 mano de obra, 3 terceros, 4 impuestos, 5 comisiones, 6 costo financiero, 7 otros; `SourceID` = origen en el tercero. **No se puede borrar**: se corrige mandando el mismo movimiento con valor negativo.
- **PRQ (§11.36)**: Situation 0 Abierto, 1 En cotización, 2 En OC, 3 Abierto aprobado, 4 Rechazada, 5 Pendiente aprobación, 7 Atendido parcial, 8 Atendido total. Import UPDATE valida 1, 2, 6, 7 u 8 [AMBIGUO: el 6 no figura en la enumeración].
- **WIP_TR (§11.17)**: TransactionType distinto por dirección: import 2 Validación, 3 Movimiento, 4 Registro peso, 7 Finalización, 24 Reapertura de pallet; export 1 Nuevo, 2, 3, 4, 7, 10 Entrada en stock, 11 Cancelación entrada, 16 Etiqueta dividida, 17/18 Total/Parcialmente consumida, 20/21 Entrega de producción por volúmenes / cancelación, 24, 27 Pallet cancelado (p.141–142).
- **CTB_CTA / STK_NCM / CTB_CTC**: exportación en lote, disparada por el usuario desde el menú SDI ("no basta grabar"). **CTB_LCTO**: cada registro (`Lacto`) es una línea de un archivo de texto de asientos.
- **INT-OP (§11.14)**: raíz `WOMainNode`; UPDATESTATUS lleva sólo `WOChangeStatus`.

---

## 3. Qué tiene que devolver el ERP (Odoo) a Metrics

1. **ACK de cada transacción exportada por Metrics** (BIL, SOR, CRM, STK, WO, REC, POR, etc.): tras procesarla, el ERP debe informar el resultado:
   - WebService: `SetTransactionResult` / `SetTransactionResultBasic(pIdTransaction=TransactionID recibido, pExtref=ID en Odoo, pHasError=0 ó -1, pResult=…)` (§11.1.2, §11.3.1.2).
   - BD: grabar `XMLReturn` (estructura §11.5.2: `Return` 0/1, `Msg`, `Operation`, `Context`, `DocNumber`) en la fila de `sdiTmExportData` (§9.2-B).
   - El estado queda visible en el monitor SDI (§11.4).
2. **No existe en el manual un XML de "respuesta de factura/remito"** específico. Si el ERP es quien emite la factura (fiscal) y Metrics debe enterarse del número/estado, la vía documentada sería **importar BIL** (ops UPDATE/PROCESS/CANCEL con `InvoiceNumber`, `InvoiceCompl`, `Status` 2=Procesado/3=Cancelado, `accesskey`) con ExtRef propio [INFERENCIA – el manual sólo dice que BIL admite esas operaciones en ambos sentidos, sin detallar el flujo].
3. **Movimientos de stock hacia Metrics** (STK import, INSERT/CANCEL): con `TransactionCodeExtRef` único numérico por movimiento; para anular, CANCEL con el mismo `TransactionCodeExtRef` y la `TransactionDt` original. Tipo **9 = Ajuste de saldo** y **11 = Recálculo del costo promedio** existen en el enum; el manual no especifica un "XML de ajuste de valor" aparte [ver §2.5, INFERENCIA].
4. **Títulos (CR)**: el ERP puede importar títulos/pagos (CrStatus 2 = Bajado, PayDate, CurrentPaidValue) – p.ej. bajas de cobranza o anticipos (OriginDocumentType 7).
5. **Costos reales por OP (ACR)**: importación INSERT, correcciones con valor negativo.
6. Para importaciones el ERP recibe a su vez el resultado de Metrics: `ProcessTransactionResponse` (ReturnCode 0/otro, Operation, Msg) o `XMLReturn`/`HasError` en `sdiTmImportData`; `DocNumber` devuelve el código Metrics creado (ítem, pedido, cliente, OC).

## 4. Puntos abiertos para validar con EPS/EG
- Encoding de los XML (no especificado).
- Formato exacto de `pResult` y códigos (`-1` vs `1`).
- Existencia/uso de INSERTUPDATE.
- Si se usará WebService o tablas (`sdiTmImportData`/`sdiTmExportData`) – el manual soporta ambos.
- Semántica de TransactionType 9 y 11 y quién los origina.
- Atributos en minúsculas y nombres de tags: usar los XML de ejemplo reales como fuente de verdad (§2).
