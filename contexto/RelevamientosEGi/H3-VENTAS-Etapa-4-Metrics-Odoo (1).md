# H3-VENTAS — Etapa 4 — Emisión de Remito Oficial / COT

- Origen: Odoo → Metrics.
- Disparador: separación de material en Metrics (PCK).
- RN-01 — Idempotencia por PCK_ID: Odoo verifica si ya existe comprobante/remito asociado al PCK_ID. Si existe, devuelve los datos previamente emitidos sin duplicar registros.
- RN-02 — Permisos para empleados de depósito: los usuarios de depósito no deben modificar datos contables. Para completar transporte (camión, patente, peso), el acceso se limita al modelo arba.cot.wizard.
- RN-03 — Sincronización del comprobante: cuando el comprobante queda posted y obtiene COT, Odoo envía asíncronamente a Metrics número de comprobante, fecha, montos totales y estado. Metrics actualiza el pedido a Entregado.
