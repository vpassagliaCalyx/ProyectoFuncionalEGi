# H3-VENTAS — Etapa 1 — Gestión de Clientes y Pedido de Venta (SOR)

- Origen: Metrics → Destino: Odoo.
- Disparador: aprobación de una cotización en Metrics.
- Al aprobarse la cotización, Metrics genera en paralelo la WO (Orden de Producción, destinada a planta) y el SOR (Pedido de Venta, destinado a administración y enviado a Odoo).
- RN-01 — Conversión de Prospecto a Cliente Fiscal: validar CUIT válido, responsabilidad fiscal/condición ante IVA, estado/provincia y país. Si la validación es correcta, Odoo crea o actualiza res.partner, remueve la etiqueta de prospecto y permite la operación. Si falla, se retorna error.
- RN-02 — Unicidad del Pedido: el identificador del SOR actúa como external_id único en Odoo y evita la creación de pedidos duplicados.
- Idempotencia contable: ante una solicitud de remisión/facturación con un SOR único, Odoo debe verificar que no exista previamente el pedido asociado al SOR.
- Pendiente: definir la tabla de equivalencias entre unidades de venta de Metrics y unidades de medida de Odoo.
