# Clientes

<!-- Un bloque por cliente. Solo datos confirmados. Se actualiza con confirmación. -->

## EG (EGi)
- Razón social: Establecimiento Grafico Impresores (EG = EGI = Establecimiento Grafico Impresores; también aparece así en los XML de Metrics)
- Contactos y cargos (según reuniones; cargos a confirmar):
  - Alexander: Metrics (proveedor del sistema de planta).
  - Selene: Metrics (hizo la demo funcional).
  - Paula: comercial EG.
  - Magalí: costos EG.
  - Macarena, Marcelo, Francisco: [COMPLETAR: cargo].
  - Estudio contable: "Verino" (según Minuta 2).
- Logo: [COMPLETAR] (no hay logo de EG en `contexto/logos/`)
- Proyecto(s): integración Metrics ↔ Odoo 19 Enterprise (hitos H2 Maestros, H3 Ventas, H5 Compras, H6 Producción). Tickets `ODOO_CU-XXXX`.
- Sistema(s) involucrado(s):
  - Metrics (MES/ERP gráfico de planta). Integración por XML vía WebService SOAP (`GetPendingTransaction`, `SetTransactionResult`, `ProcessTransaction`), manual de integración rev. 93.
  - Odoo 19 Enterprise con localización argentina de ADHOC (ver `contexto/L10N_AR_v19 (3).xlsx`). Remitos y COT: `l10n_ar_stock_ux` (`arba.cot.wizard`).
- Plantas: Offset, Flexo, Recuperadora de solventes; todo en un mismo predio, con un depósito fuera del predio. Talonario de remito por planta (Recuperadora = remito 9, depósito externo = remito 11).
- Notas:
  - Cada producto terminado pertenece a una sola planta; hay clientes compartidos entre plantas.
  - Offset compra papel en pliegos; solo las bobinas de cartulina se compran en kg. Bobinas madre/hija con códigos distintos.
  - Metrics opera en USD; Odoo en ARS.
  - Material de referencia: `contexto/RelevamientosEGi/` y resúmenes `salidas/2026-11-13_referencia_EG_*.md`.
