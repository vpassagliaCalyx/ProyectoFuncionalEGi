# EG — Contexto del proyecto (resumen para nuevas sesiones)

> Actualizado: 13/11/2026. **Leer esto antes que las fuentes originales.** Abrir una fuente solo si hace falta un detalle que no está acá; usar la tabla "Dónde está cada cosa".

## Proyecto
- Cliente: **Establecimiento Grafico Impresores** (EG = EGI). Consultora: Calyx (+ PGK/TGS).
- Integración **Metrics → Odoo 19 Enterprise** (localización argentina ADHOC). Metrics = sistema de planta (gráfica: Offset, Flexo, Recuperadora de solventes).
- Integración por **WebService SOAP** de Metrics (manual rev. 93 §11.1–11.3): `GetPendingTransaction` (ERP trae pendientes), `SetTransactionResult` (ERP informa resultado), `ProcessTransaction` (ERP envía a Metrics). Alternativa: tablas `sdiTmExportData` / `sdiTmImportData`. **No es por archivos.**
- Un XML = una operación y un contexto; atributos en minúsculas; respuesta genérica XMLReturn (Return 0 OK / 1 error, Msg).

## CU Odoo a probar (lista maestra: `cucontectoproyecto15-11-2026.docx`)
| CU | Tema | Modelo |
|---|---|---|
| 2082 | H3 Ventas E1: SOR, SOR = external_id único | sale.order |
| 2083 | H3 E2: facturación (billing=1), ARS, qty_invoiced, BIL_ID, respuesta CAE | account.move |
| 2084 | H3 E3: solicitud remisión (delivery=1) → entrega borrador bloqueada, talonario por planta | stock.picking |
| 2085 | H3 E4: PCK → lotes, emite remito + COT (`arba.cot.wizard`), idempotencia PCK_ID | stock.picking |
| 2086 | H3 E5: cancelación (solo si no facturado/entregado; factura solo borrador) | sale/account/picking |
| 2238 | H5 PO desde POR (INSERT/UPDATE/DELETE), clave `x_metrics_po_key`, INSERT duplicado se rechaza | purchase.order |
| 2361 | H5 recepción REC (08) + STK TType 2 (09), sin sobre-recepción, ubicación única | stock.picking |
| 2364 | H5 factura proveedor confirmada → XML ajuste valor (STK TType 9, financiero, qty 0) a Metrics | account.move |
| 2366 | H5 conversión rollo→pliego (STK TType 5, origen op=1, destinos op=0), costo prorrateado | stock.move |
| 2237 | H6 E1 WO → una `mrp.production` por PT, `x_metrics_wo_number`, MP prorrateada por cantidad, residuo al último, confirma sin stock, solo Bot | mrp.production |
| 2244 | H6 E2 consumo STK TType 0, atómico, sin stock → pendiente de reintento, MP compartida con misma proporción | mrp.production |
| 2245 | H6 E3 PT STK TType 1: valida consumos en proceso y OC pendientes (MP con lote), `button_mark_done` | mrp.production |
| 2255 | H6 E3.1 entregas parciales con backorder | mrp.production |
| 2367 | H2 categoría hoja (árbol precargado, no se crean categorías) | product.category |
| 2368 | H2 cuenta analítica por categoría → `account.analytic.distribution.model` con toda la rama | product.category |

## Decisiones (minutas 02/07 y 03/07/2026; detalle en `memoria/decisiones.md`)
- Clientes/proveedores: los crea **solo Administración en Odoo** (no se integra CRM).
- Materiales, PT y categorías nacen en Metrics. Compras productivas en Metrics; recepciones solo en Metrics → Odoo.
- UoM: la integración usa **solo la unidad de costo**; Odoo registra en kg.
- Valuación: ARS, TC de la OC ajustado a factura, ajuste por inflación; **PT a costo real de MP directa, PEPS/FIFO**.
- Consumos no medibles (tinta, pegamento) → centro de costo de la máquina.
- Talonario por planta (Recuperadora = remito 9, depósito externo = remito 11). WIP **no** se integra.

## Hechos técnicos verificados
- **Manual Metrics:** STK TransactionType 0 consumo, 1 entrega producción, 2 compra, 3 venta, 4 inventario, 5 transferencia entre ítems, 6 volúmenes, 7 entre empresas, 8 transferencia, 9 ajuste de saldo, 10 otro, 11 recálculo costo promedio. StockMovementType 0 físico / 1 financiero / 2 ambos. OperationType 0 entrada / 1 salida. STK solo INSERT y CANCEL. Referencias ExtRef son **numéricas (Double)**.
- BIL: no existen "tipo F/R"; factura vs remito por flags `billing`/`delivery` (invoicetype 1 = venta). WO status 0 abierta, 1 finalizada, 2 cancelada, 3 bloqueada, 4 evaluación (solo interesa 0).
- MaterialType distinto en STKITEM (1 tinta, 2 plancha, 3 otros, 4 papel hoja, 5 bobina, 6 personalizado) y WO (0 papel, 1 tinta, 2 plancha, 3 otro).
- **Odoo 19:** PT lote = `lot_producing_ids` (no `_id`); no existe `action_backorder` (backorder = `button_mark_done` con `mo_ids_to_backorder` → `_split_productions`, usa `copy_data`); almacenable = `type='consu'` + `is_storable`; advertencia de consumo depende de `consumption` de la BoM.
- **Localización:** COT en `l10n_ar_stock_ux` (ADHOC, repo `argentina-sale`) → `arba.cot.wizard` (sin campo peso). Tipo de documento del remito en `stock.picking.type.l10n_ar_document_type_id`. Lista completa de módulos: `contexto/L10N_AR_v19 (3).xlsx`.

## Pendientes principales
WSDL/endpoint; tabla UoM venta; fuente de la planta (WO/producto/prefijo SKU 90-91); mecanismo de respuesta con CAE/N° (manual solo define XMLReturn); contexto de la cancelación; muestras: WO status 0 con stockcode en MP, REC con ítems, conversión con costo; docnumber/docnumbercompl; CU-2244 CA03 en revisión con EG; regla de consumos tras entrega parcial ("QUEDAN MAL LOS CONSUMIDOS"); doc técnico del módulo copiado de otro proyecto (`rofina.log`).

## Dónde está cada cosa
| Necesito | Archivo |
|---|---|
| Detalle del manual Metrics | `salidas/2026-11-13_referencia_EG_manual-metrics-xml-rev93.md` |
| Resumen de los 140 casos de uso originales | `salidas/2026-11-13_referencia_EG_casos-uso-integracion.md` |
| Resumen de reuniones | `salidas/2026-11-13_referencia_EG_reuniones-julio-2026.md` |
| Revisión de casos (197, por modelo, con hallazgos) | `salidas/2026-11-13_revision-casos-uso_EG_integracion-metrics-odoo.xlsx` |
| Plan de pruebas para marcar (157 casos) | `salidas/2026-11-13_plan-pruebas_EG_integracion-metrics-odoo.xlsx` (+ `.spec.json`) |
| Texto de las CU Odoo | `contexto/RelevamientosEGi/cucontectoproyecto15-11-2026.docx` |
| Alcance WO | `contexto/RelevamientosEGi/Alcance funcional — Gestión de Work Orders ... .pdf` |
| XML de ejemplo 01–16 | `contexto/RelevamientosEGi/XMLs2/ejemplo completo/` (ISO-8859-1) |
| Manual Metrics original (174 pág.) | `contexto/RelevamientosEGi/XMLs2/Metrics Integración XML - Revisión 93 (1).pdf` |

Notas: duplicados idénticos `Manual_..._H3_Ventas (1)/(3).docx` y `Mapeo_XML (1)/(2).xlsx`; `metrics_wo_etapas_spec (3).md` es la versión vigente. El `.mp4` (845 MB) no se abre.

## Herramientas en esta PC
- Python: `py -I` (3.14, con openpyxl; sin Pillow → los Excel salen sin logos, el usuario lo aceptó). `pdftotext` disponible en Git Bash. Para imprimir UTF-8: `sys.stdout.reconfigure(encoding='utf-8')`.
- Plan de pruebas: sale en **Excel** con `.claude/skills/plan-de-pruebas/scripts/build_xlsx.py`.
