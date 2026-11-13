# Investigación: Trazabilidad Metrics XML — WO, STK, WIP

## Archivos analizados

| Archivo | Descripción |
|---------|-------------|
| `WO - Orden de Producción.xml` | Orden de producción UD36440 |
| `STK - Consumo.xml` | Movimiento de stock (TransactionType=9) |
| `STK - Entrega Producción 01.xml` | Entrega PT.FOL.FEI.4665 (TransactionType=1) |
| `STK - Entrega Producción 02.xml` | Entrega PT.FOL.FEI.4666 (TransactionType=1) |
| `Metrics Integración XML - Revisión 93 (1).pdf` | Manual de integración Metrics (174 pág.) |

---

## 1. Estructura del XML de Work Order (WO)

Elemento raíz: `<METRICS><sdiwoworkorder>`

| Elemento | Descripción |
|----------|-------------|
| `sdiwoworkorderinfo` | Cabecera: `wonumber`, `wodescription`, `quotenumber`, `status`, `projectcode` |
| `sdiwocustomerinfo` | Cliente: `code`, `name` |
| `sdilwofinisheditem` > `sdiwofinisheditem` | Productos terminados: `stockcode`, `productname`, `unitcode`, `quantity`, `deliverydt` |
| `sdilworawmaterial` > `sdiworawmaterial` | Materias primas: `stockcode`, `materialname`, `unitcode`, `quantity`, `unitcode2`, `quantity2`, `materialtype`, `idativ` |
| `sdilwooperation` > `sdiwooperation` | Operaciones: `processgroupcode`, `activitycode`, `sequence`, `quantity`, `resourcecode`, `idativ` |
| `sdilwocomponent` > `sdiwocomponent` | Componentes: `name`, `stockcode`, `quantity` (vacíos en este caso) |

### MaterialType

| Valor | Significado |
|-------|-------------|
| 0 | Papel/sustrato |
| 1 | Tintas/consumibles |
| 2 | Planchas/herramientas |

---

## 2. TransactionType de Stock (STK) — Manual pág. 81-82

Los valores reales del manual (NO coinciden con lo que se pensaba):

| TType | Descripción |
|-------|-------------|
| 0 | Atención o devolución de Solicitud de materia prima |
| 1 | **Entrega de producción** |
| 2 | Compras |
| 3 | Ventas |
| 4 | Inventario |
| 5 | Transferencia entre ítems de stock |
| 6 | Volúmenes |
| 7 | Transferencia entre empresas |
| 8 | Transferencia |
| **9** | **Ajuste de saldo** ← el `STK - Consumo.xml` es un AJUSTE, NO consumo de producción |
| 10 | Otro |

**Conclusión clave:** El archivo `STK - Consumo.xml` con `TransactionType=9` no es consumo vinculado a producción. Es un ajuste de saldo genérico, por eso `wonumber=""`.

---

## 3. Datos de la WO UD36440 (Planeado)

### Productos Terminados

| StockCode | Producto | Cantidad | Unidad |
|-----------|----------|----------|--------|
| PT.FOL.FEI.4665 | 501. Flyer / Encarte / Insertos | 25.000 | UN |
| PT.FOL.FEI.4666 | Machine Test-Prod 2 | 2.000.000 | UN |

### Materias Primas

| StockCode | Material | Cantidad | Unidad | Cantidad2 | Unidad2 | Tipo |
|-----------|----------|----------|--------|-----------|---------|------|
| PF.2094 | BOND BLANCO FSC 90X64CMS 90GRS | 59,616 | KG | 1.150 | FL | 0 |
| PF.1961 | Negro - Offset Plana | 3,456 | KG | 0 | | 1 |
| PF.1130 | Bond Blanco K95, FSC 72x102cm 90grs | 4.131 | KG | 62.500 | FL | 0 |
| ME.CJA.0556 | VPI INK MAGENTA - B2 | 3,456 | KG | 0 | | 1 |
| ME.CJA.0553 | HP ELECT FOR B2 HIGH SOL INK CYAN Q4212B | 3,456 | KG | 0 | | 1 |
| ME.CJA.0590 | Cyan - Offset Plana | 3,456 | KG | 0 | | 1 |
| PL.0011 | Placa 99.6 x 119.6 cm | 4 | UN | 0 | | 2 |

---

## 4. STK Entrega Producción (Real vs Planeado)

| Producto | WO Planeado | Unidad | STK Entregado | Unidad | Diferencia | % |
|----------|------------|--------|---------------|--------|------------|---|
| PT.FOL.FEI.4665 | 25.000 | UN | **2.000** | PZ | -23.000 | 8% |
| PT.FOL.FEI.4666 | 2.000.000 | UN | **4.000** | PZ | -1.996.000 | 0,2% |

**Problemas:**
- Unidades distintas (UN vs PZ)
- Entregas muy por debajo de lo planeado

---

## 5. STK Consumo (Ajuste de saldo)

| Campo | Valor |
|-------|-------|
| transactiontype | 9 (Ajuste de saldo) |
| stockcode | pf.2094 |
| quantity | 2.500 FL |
| totalvalue | 500 |
| **wonumber** | **(vacío)** |
| stockmovementtype | 2 |
| docnumber | PF.2094 |

**No se puede vincular a ninguna WO.** El `wonumber` está vacío.

---

## 6. Contexto WIP (Work-in-Progress) — Manual pág. 137-138, Sección 11.16

Elemento raíz: `<sdiWIPLabel>`

| Atributo | Tipo | Descripción |
|----------|------|-------------|
| IdPalletLabel | Int | Código de identificación de la etiqueta del pallet |
| BarCode | String(100) | Código de barras de la etiqueta WIP |
| Quantity | Double | Cantidad de la etiqueta WIP |
| QuantityKG | Double | Cantidad en Kg |
| UnitCode | String(10) | Unidad de medida |
| IsValid | Boolean | Indica si la etiqueta está validada |
| DtValidation | TDateTime | Fecha de validación |
| UserValidation | String(32) | Usuario que validó |
| Status | Int | 1=Esperando, 2=En Uso, 3=Procesado, 4=Parcialmente, 5=No utilizado, 6=Cancelado, 7=Dividido, 8=En máquina, 9=Bloqueado, 10=En revisión |
| InsDt | TDateTime | Fecha de ingreso |
| InsUser | String(32) | Usuario que ingresó |
| IsFinalProduct | Boolean | Indica si es producto final |
| **StkCode** | String(20) | **Código del ítem de stock** |
| StkDescription | String(100) | Descripción del ítem |
| Shift | Int | Turno |
| Note | String(50) | Observación |
| PalletWeight | Double | Peso del pallet |
| IsBobbin | Boolean | Indica si es bobina |
| **ComponentId** | String(32) | **Identificación del componente** |
| Lot | String(20) | Lote del ítem |
| **ProcessID** | Int | **Código de proceso** |
| ProcessDescription | String(200) | Descripción del proceso |

**Solo exportación** (no se puede importar).

---

## 7. Contexto WIP_TR (Transacción de Etiqueta WIP) — Manual pág. 139-141, Sección 11.17

Elemento raíz: `<sdiWIPTransaction>`

| Atributo | Tipo | Descripción |
|----------|------|-------------|
| **TransactionType** | Int | Tipo de transacción (ver tabla abajo) |
| IdPalletLabel | Int | Código de identificación de la etiqueta del pallet |
| TransactionDt | TDateTime | Fecha de la transacción |
| Status | Int | Situación de la etiqueta |
| QtyBefore | Double | Cantidad antes de la transacción |
| QtyAfter | Double | Cantidad después de la transacción |
| UnitCode | String(10) | Unidad de medida |
| QtyBeforeKG | Double | Cantidad antes en Kg |
| QtyAfterKG | Double | Cantidad después en Kg |
| StockPlaceCodeBefore | String(32) | Código del local de stock antes |
| StockPlaceCodeAfter | String(32) | Código del local de stock después |
| StockAddressBefore | String(30) | Localización de stock antes |
| StockAddressAfter | String(30) | Localización de stock después |
| LogUser | String(32) | Usuario que realizó la transacción |
| Note | String(100) | Observaciones |
| Lot | String(20) | Lote del ítem |
| MachineInputCode | String(30) | Código de entrada de máquina |

### TransactionType para exportación WIP_TR

| ID | Descripción | Uso |
|----|-------------|-----|
| 1 | Nuevo | Creación de etiqueta |
| 2 | Validación | Validación de etiqueta |
| 3 | Movimiento | Movimiento de stock |
| 4 | Registro peso | Pesaje |
| 7 | Finalización | Cierre de etiqueta |
| 10 | **Entrada en stock** | Ingreso a stock (producto terminado) |
| 11 | Cancelación de entrada en stock | |
| 16 | Etiqueta dividida | Split de etiqueta |
| **17** | **Totalmente consumida** | **Consumo total de material** |
| **18** | **Parcialmente consumida** | **Consumo parcial de material** |
| 20 | Entrega de Producción (volúmenes) | |
| 24 | Reapertura de pallet | |
| 27 | Pallet Cancelado | |

---

## 8. Cómo vincular WO → Consumo → Producto Terminado

La trazabilidad completa se arma cruzando estos contextos:

```
WO XML (sdiwoworkorder)
│
├── sdiworawmaterial.idativ  ───────┐
├── sdiwooperation.idativ    ───────┤
│                                   │
│                                   ▼
│                    WIP (sdiWIPLabel)
│                    ├── StkCode = código material
│                    ├── ProcessID ── coincide con idativ ──┐
│                    ├── ComponentId                        │
│                    ├── IsFinalProduct                     │
│                    │                                      │
│                    ▼                                      ▼
│           WIP_TR (sdiWIPTransaction)         WO.idativ ↔ WIP.ProcessID
│           ├── TransactionType=17/18          WIP.IdPalletLabel ↔ WIP_TR.IdPalletLabel
│           ├── IdPalletLabel ──────────────────┘
│           ├── QtyBefore / QtyAfter
│           └── StockPlaceCode
│
└── sdilwofinisheditem.stockcode ─── STK Entrega (TransactionType=1)
                                    └── wonumber = UD36440
```

---

## 9. Problemas identificados

1. **STK Consumo (TType=9) no es consumo de producción** — es un "Ajuste de saldo" según el manual, no tiene WO
2. **WO planea 1150 FL de PF.2094** pero el ajuste registra 2500 FL — cantidades inconsistentes
3. **Entregas muy por debajo de lo planeado** — PT.FOL.FEI.4665 solo el 8%, PT.FOL.FEI.4666 solo el 0,2%
4. **Unidades inconsistentes** — WO usa UN, STK Entrega usa PZ
5. **WIP y WIP_TR no tienen WONumber** — el vínculo WO→consumo se hace por `ProcessID` ↔ `idativ`, no por número de orden

---

## 10. Lo que falta para trazabilidad completa

| Necesito | Dónde está |
|----------|-----------|
| Consumo real de materiales | WIP + WIP_TR (TransactionType 17 y 18) |
| Vinculación WO → Consumo | `WO.sdiworawmaterial.idativ` → `WIP.ProcessID` |
| Vinculación Componente → Material | `WIP.ComponentId` |
| Entregas vs Planeado | `WO.sdiwofinisheditem.quantity` vs `STK TType=1.quantity` |

**Sin los XML de WIP y WIP_TR no se puede reconstruir qué materias primas se consumieron realmente para producir cada producto terminado.**