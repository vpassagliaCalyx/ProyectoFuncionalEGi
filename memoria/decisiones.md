# Decisiones

<!-- Una fila por decisión confirmada. Se actualiza con confirmación. -->

| Fecha | Cliente / Proyecto | Decisión | Fuente (documento o reunión) |
| :-: | :--- | :--- | :--- |
| 02/07/2026 | EG / Integración Metrics-Odoo | Clientes y proveedores los crea solo Administración, en Odoo, con etiquetas "prospecto"/"activo". | Minuta 1 (reunión 02/07) |
| 02/07/2026 | EG / Integración Metrics-Odoo | Materiales, productos terminados y categorías nacen en Metrics. Las categorías nuevas tienen un control manual en Odoo para asignar la cuenta contable. | Minuta 1 (reunión 02/07) |
| 02/07/2026 | EG / Integración Metrics-Odoo | Compras productivas y recurrentes de Compras nacen en Metrics; las excepcionales de Administración van directo por Odoo y no se informan a Metrics. | Minuta 1 (reunión 02/07) |
| 02/07/2026 | EG / Integración Metrics-Odoo | Recepciones solo en Metrics, unidireccional hacia Odoo. Se aceptan parciales y sin impuestos (los impuestos van en la factura en Odoo). | Minuta 1 (reunión 02/07) |
| 02/07/2026 | EG / Integración Metrics-Odoo | La integración usa solo la unidad de costo; Odoo registra en kg. Metrics hace las conversiones. | Minuta 1 (reunión 02/07) |
| 02/07/2026 | EG / Integración Metrics-Odoo | SOR agrupa las solicitudes. La solicitud de remisión crea un remito borrador bloqueado; el PCK trae los lotes y habilita la emisión. Odoo devuelve número, serie, estado y fecha. | Minuta 1 (reunión 02/07) |
| 02/07/2026 | EG / Integración Metrics-Odoo | Talonarios de remito separados por planta. | Minuta 1 (reunión 02/07) |
| 03/07/2026 | EG / Integración Metrics-Odoo | Inventario en Odoo en pesos, al tipo de cambio de la OC y ajustado a la factura; sin bimonetaria. Ajuste por inflación incluido. | Minuta 2 (reunión 03/07) |
| 03/07/2026 | EG / Integración Metrics-Odoo | Producto terminado a costo real (materias primas directas), valuación PEPS/FIFO. | Minuta 2 (reunión 03/07) |
| 03/07/2026 | EG / Integración Metrics-Odoo | Consumos no medibles por OP (tintas, pegamentos, adhesivos) van al centro de costo de la máquina. | Minuta 2 (reunión 03/07) |
| 03/07/2026 | EG / Integración Metrics-Odoo | OP multiproducto (mismo formato): materiales repartidos en proporción a la cantidad de cada producto. | Minuta 2 (reunión 03/07); Alcance funcional WO (PDF) |
| [COMPLETAR] | EG / Integración Metrics-Odoo | Una `mrp.production` por producto terminado, todas con el mismo `x_metrics_wo_number`; el consumo compartido se reparte con la misma proporción. | Alcance funcional WO (PDF); `metrics_wo_etapas_spec (3).md` |
