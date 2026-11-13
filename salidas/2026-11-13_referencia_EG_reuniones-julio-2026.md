# Resumen de reuniones de relevamiento: integración Metrics ↔ Odoo (EG)

Fuentes: `XMLs2/meet integracion funcional.srt` (+ `resumen_meet_integracion_funcional.txt`), `XMLs2/video/EGI - integración ODOO-20260702_091005...txt`, `XMLs2/video/EGI - Integración ODOO-20260703_110329...srt`, `Minuta de Reunión -Flujos Integracion 1.pdf` y `...2.pdf`.

Aclaraciones generales:
- Las transcripciones son automáticas y de muy mala calidad: no tienen etiquetas de hablante, mezclan portugués y español, tienen bucles ("no, no, no…") y nombres deformados ("Metrix/Matrix/métricis" = Metrics; "o du/Odu/YouTube" = Odoo; "el exánder/Alexandre" = Alexander). Por eso casi nunca se puede atribuir una frase a una persona. Las atribuciones de este resumen salen solo de las minutas o de casos donde el texto deja claro quién habla.
- En las transcripciones a la empresa del cliente se la nombra varias veces como "impresores" ("la base de impresores", "impresores como empresa"). No se pudo confirmar si es parte de la razón social de EG [transcripción dudosa].
- Las minutas PDF parecen corresponder: **Minuta 1 → reunión del 02/07** y **Minuta 2 → reunión del 03/07**. La correspondencia se deduce por el contenido; los PDF no tienen fecha.

---

## Reunión 0: "Meet integración funcional" (demo de Metrics)

- **Fecha:** no figura. Es anterior al 02/07/2026, porque al final se dice "el 2 y 3 de julio tenemos sesiones con [Alexander]". El `.txt` de resumen dice "~Junio/Julio 2026".
- **Participantes (según aparecen):** Vanessa (presente: "¿Tenés un ratito más Vanessa? Yo sí"), Selene/"Selen"/"Silen" (todo indica que hace la demo de Metrics). Se menciona a Magalí ("la de costos"), Paula ("es comercial"), Marcelo (se le dirige una pregunta) y Francisco (se habla de llevarle temas). El `.txt` de resumen lista también a "Alexander", pero en la transcripción solo se lo nombra para reuniones futuras [no confirmado que haya estado].
- **Temas:** CRM y clientes, cotización → pedido de venta → OP, impuestos, planificación/job tracking, stock y valuación, compras, sistema de volúmenes (bobinas), tipos y grupos de ítem, unidades de medida, bobina madre/hija, consumos, entrega de producción, separación y remito, cierre de stock.

### Decisiones / acuerdos explícitos
- Lo único que queda como propuesta compartida: los clientes prospecto se manejan en Metrics y solo pasan a Odoo cuando son clientes activos. Proveedores: "los vamos a tener que cargar nosotros". Ojo: esto se revisó después; ver reunión del 02/07.
- La entrega de producción integra solo el producto terminado (PT), no los materiales.
- Producto en proceso (WIP): "no está previsto" integrarlo. Un intermedio solo genera transacción de entrada si vuelve a stock.
- Se prefiere conectar el remito con la **separación** (cuando está procesada/"liberada para emisión") y no con la solicitud de remito ("Yo creo que el ideal sería por la separación").

### Preguntas abiertas / acciones
- ¿Quién emite el remito: logística o comercial? Hoy comercial (Paula) decide qué se despacha y cómo. Se plantea llevar el tema a Francisco y a las chicas de administración, y dar perfil/licencia Odoo a logística ("pedimos licencia de Odoo para el objetivo… se planteó también para la gente de logística").
- Clientes prospecto: administración "no quiere" que comercial cree clientes. Se propone mostrarles en la próxima reunión cómo funciona. Alguien se anota configurar en Odoo una regla/alerta de cliente incompleto [hablante no identificable].
- Bobina madre/hija: ¿Metrics manda la madre o la hija? Hay confusión con los códigos ("13", "274", "12 de 4") [transcripción dudosa]. Quien pregunta se lo lleva "para analizar" cuando le pasen la OP.
- Datos de transportista: se pueden cargar en Odoo o en Metrics, a definir.
- Quedan dudas sobre compras no consumidas, conversiones a intermedios y saldos. Se derivan a las sesiones del 2 y 3/7 con Alexander.
- Se pide que la grabación quede disponible para armar un resumen.

### Hechos de negocio / sistema aprendidos
- **CRM Metrics:** ficha de cliente con NIT/RUC, transportista, matriz/sucursal, vendedor, moneda de cotización, direcciones (administrativa/entrega), contactos, datos de tamaño/potencial, datos fiscales y contables, condición de pago, crédito y alertas (pop-ups). Los campos obligatorios se definen por estado (prospecto vs cliente). La oportunidad sirve para costear desarrollos y pruebas de preprensa antes de cotizar.
- **Cotización:** por producto, con varias cantidades. La evaluación se puede hacer por proyecto. Al aprobar para producción se genera la copia del producto con su **SKU**, y automáticamente **la OP** (ingeniería: máquinas, tiempos) y **el pedido de venta**. El pedido de venta es "donde empiezan las integraciones".
- **Impuestos:** ingresos brutos va dentro del precio. El IVA no: es solo una "previsión".
- **Pedido de venta:** puede tener entregas (remito) y facturas separadas, por ejemplo facturar 10.000 y entregar 5.000 ahora. La solicitud de factura/remito indica fecha, OP, SKU, cantidad y tipo (remito o factura).
- **Producción:** planificación por máquina. El operador apunta en job track y se imprime una etiqueta con la cantidad producida. La entrega de producción se hace leyendo las etiquetas WIP de la OP. La OP se cierra al entregar el 100%.
- **Stock Metrics:** no admite saldo negativo, solo "saldo futuro negativo", que dispara la señal de compra. Las solicitudes de materiales de la OP generan "empeños" (reservas) según ingeniería. Hay sugerencia de compra por stock mínimo + empeños y fecha planificada de consumo, y solicitudes de compra no ligadas a OP (con centro de costo).
- **Valuación Metrics:** costo promedio por compra (precio de factura), recalculado con cada compra. Hay cierres de stock mensuales para cerrar costos. La cotización **no** usa el costo promedio, sino una **tabla de costos paralela**.
- **Sistema de volúmenes:** bobinas controladas individualmente, cada una con código y peso. Lo integrado debe traer cantidad total y costo total; la división en bobinas la hace Metrics. Los materiales controlados por volúmenes solo se mueven por ese sistema o por colector.
- **Ítems:** una misma ficha para intermedio, terminado, servicio, consumible y materia prima. Jerarquía Grupo master → Grupo → Ítem (ej.: master Papel; grupo 01 sustrato). Admite campos adicionales configurables (ej. código externo).
- **UoM:** hay unidades distintas de compra/costo, stock, consumo e ingeniería, con factor de conversión. Lo crítico es que stock = consumo = ingeniería. Ejemplo: bobina comprada en m² y controlada en kg. Estuches se venden en unidades; "bobinas en metros".
- **Bobina madre/hija:** se compra la bobina grande (madre, la que se factura) y el proveedor la entrega cortada (hija, otro código de ítem). Un dato en el ítem indica "material de bobina máster".
- **Consumos:** reales (no estimados), vía atención de solicitudes o job track, desde un local de stock por máquina. Algunos materiales (cajas, pallets) los baja el operador manualmente.
- **Separación (expedición):** por producto. Indica pallets, ubicaciones, embalajes, transportista, peso, placa del camión. Solo se puede remitir lo separado y lo pendiente queda para después. Antes de remitir se requiere aprobar un **lote de calidad** del PT.
- Sin la parte financiera en Metrics, el proceso "finaliza en la separación" y el cierre de stock.

---

## Reunión 1: 02/07/2026 (09:10), "EGI - integración ODOO" (~3 h 40 min)

- **Participantes (según aparecen):** Alexander (Metrics: "soy el [Alexander] de Metrics"), Vanessa ("van esa"), Macarena ("Maca"), Marcelo ("Marce"), "Fran" (entra a ~01:02; también se nombra a Francisco), Daniel (mencionado). Se nombran como ausentes a Selene ("la chica de Metrics") y a Matías. Una persona dice centralizar la información ("manda a mí y a Alexander y yo lo distribuyo"), pero no se puede identificar quién es [transcripción dudosa].
- **Temas:** flujo de producto nuevo (alta de maestros), compras y recepciones, categorías, UoM, centros de costo, moneda/valuación, tipos de movimiento de stock, remisión/facturación (SOR/BILL/PCK), talonarios por planta.

### Decisiones / acuerdos explícitos (Minuta 1 + transcripción)
1. **Clientes y proveedores:** Administración es la única dueña del dato y la única que los crea, en Odoo. En Odoo se usarán marcas/etiquetas ("prospecto"/"activo") para registrar clientes "en frío" sin ensuciar reportes.
2. **Materiales y productos terminados** se crean en Metrics.
3. **Compras productivas:** todo el flujo nace y se gestiona en Metrics. Odoo recibe copia de la OC solo para facturación y registro contable. **Compras no productivas:** las recurrentes que gestiona el sector de Compras (ej. honorarios contables mensuales) también nacen en Metrics. Las excepcionales de administración (ej. cambio de camioneta) van directo por Odoo y no se informan a Metrics.
4. **Recepciones (remito de ingreso):** solo en Metrics, unidireccional Metrics → Odoo. Se aceptan entregas parciales y remitos sin impuestos. Los impuestos se cargan en la factura, en Odoo. Alexander: "tenemos que cambiar este flujo de integración".
5. **UoM:** Metrics hace las conversiones internas (papel con gramaje, ancho y largo). La integración usa **solo la unidad de costo** (campo de cantidad en unidad de costo de los movimientos). **Odoo registra en kilos**.
6. **Categorías:** nacen en Metrics (grupo master / grupo de material). Las existentes se sincronizan con el producto. Para las nuevas hay un **punto de control manual en Odoo** donde el usuario asigna la cuenta contable antes de habilitar movimientos. En Metrics se limita por perfil quién puede crear categorías.
7. **Despacho:** se adopta **SOR** (pedido de venta) como agrupador de todas las solicitudes de remisión y facturación. Con la solicitud de remisión (BILL), Odoo crea un **remito borrador bloqueado** sin numeración. Cuando logística hace el picking y confirma el lote en Metrics, llega el **PCK**: Odoo adjunta los lotes, desbloquea y permite emitir e imprimir el remito oficial. Odoo devuelve a Metrics el BILL con número, serie, estado y fecha de emisión. Series distintas para remito y factura.
8. **Talonarios de remito separados por planta** (Offset, Flexo, Recuperadora de solventes, etc.), según el tipo de producto.

### Preguntas abiertas / acciones
- **Auto-impresores** (responsable según minuta: Administración): averiguar requisitos fiscales y volúmenes para emitir remitos en papel blanco desde Odoo.
- **Automatizar la asignación de talonario** según tipo de producto y planta (responsable según minuta: Calyx TI/Integraciones). Opciones mencionadas: prefijo de código de producto por planta (ver más abajo) o un campo "tipo de orden de venta". Falta configurarlo con Selene.
- **Frecuencia de integración de inventario:** se planteó mandar cada movimiento o un saldo mensual. EG dice que necesita ver los movimientos "todo el tiempo". Queda para analizar en otra reunión.
- **Diferencia de precio/tipo de cambio entre OC y factura:** Alexander propone que Odoo envíe a Metrics una revaluación ("recálculo de costo promedio") al recibir cada factura. Dijo que lo iba a probar ("Eso es lo que voy a probar ahora y después les contesto"). Queda abierto si la revaluación aplica a todo el stock o solo a esa entrada.
- **Moneda:** la moneda estándar de Metrics es el dólar. Odoo lleva pesos. Para compras en pesos hay que mandar el tipo de cambio; ¿de dónde sale (tabla de monedas / web service)? Hay que probar todo el flujo de monedas.
- **Centros de costo:** ¿cómo viajan los consumos por centro de costo (repuestos, consumibles de máquina) y cómo se reflejan en las cuentas analíticas de Odoo? Abierto.
- **Valuación de WIP y PT:** se cortó el tema ("hacer un parate") para tratarlo al día siguiente (03/07, 11–13 h) con el estudio contable.
- **Transportista:** Metrics no lo envía en el PCK [transcripción dudosa]; se completaría en Odoo.
- **COT** ("el tema del code… web service… Excel") [transcripción dudosa: parece referirse al código de traslado]: no se cerró.
- Una persona del lado Calyx se compromete a revisar la documentación de Alexander y a hablar con Macarena y Matías sobre la integración [quién exactamente: no claro].
- Alexander comparte XML de movimientos de stock y el documento de la integración SOR. Se pide compartir el video.

### Hechos de negocio aprendidos
- **Plantas y talonarios:** físicamente todo está en un mismo predio. Hay depósitos ficticios en Metrics para ubicar MP/PT. El remito se usa para diferenciar plantas: talonario para Offset, otro para Flexo, "remito 9" para Recuperadora de solventes y "remito 11" para un depósito fuera del predio. Los números de Offset y Flexo no se entienden [transcripción dudosa].
- Un producto terminado pertenece siempre a una sola planta (Offset **o** Flexo). Hay clientes compartidos entre plantas. La nota de pedido no debería mezclar plantas: se acuerda como procedimiento interno.
- **Códigos de producto por planta** (idea en discusión): prefijos tipo "90.x" / "91.x". Para Flexo se mencionan subcódigos ("921.01 bobinas, 921.02…, 921.03…") [transcripción dudosa]. Hoy se está parametrizando Offset en Metrics; Flexo viene "muy cerquita".
- **Grupos de material:** master "Sustrato" con grupos cuché, offset y PET (para flexografía). Hace unos 5-6 años se creó un grupo nuevo por tintas UV ("tinta subé" [transcripción dudosa]). Las categorías nuevas son raras.
- **UoM reales en EG:** el papel de Offset se compra **en pliegos** (OC en pliegos, precio por pliego). Solo las bobinas de cartulina de Offset se compran en kilos y se transforman a pliegos. Tintas, barnices y adhesivos entran y se consumen en kg. Flexo: kilos de bobina de entrada y de salida. El remito del proveedor declara kilos, pliegos y pallets. Alexander: en Metrics el estándar para papel/cartón es unidad de costo/compra = kg y stock = pliegos. Campos del ítem: "UnitCodeMan", "UnitCodeCost" y otro más [transcripción dudosa].
- **STKITEM** envía la madre y la hija (campo de "material máster").
- **Tipos de transacción en movimientos** (`TransactionType`): consumo y estorno de consumo; venta (no se usa); transferencia entre ítems (conversión de bobina, probablemente no); volúmenes (probablemente no); transferencia entre almacenes (probablemente no: un solo almacén); **ajuste manual (Odoo debería tomarlo)**; recálculo de costo. `StockMovementType`: físico, financiero (ej. flete agregado al costo) o físico-financiero (ej. entrega de producción).
- **Facturación EG:** siempre nace de una nota de pedido (moneda, condición de venta, ítems). El tipo de cambio lo pone EG al facturar. Se puede facturar antes y remitir después, o al revés. Los remitos de EG muestran el número de lote. Usan cualquier impresora con formulario preimpreso.
- **Contabilidad Odoo explicada:** la OC no toca la contabilidad. La recepción genera un asiento de mercadería contra "facturas a recibir". La factura genera "facturas a recibir" contra proveedores, y las diferencias de precio o de cambio ajustan el stock. Odoo no lleva contabilidad bimonetaria.
- Producto repetido: no integra los registros maestros (STKITEM, etc.); producto nuevo sí. El resto del flujo es igual. Al principio se dijo que "no sería necesario transmitir el pedido de venta a Odoo", pero después se acordó la integración SOR.
- EG quiere poder ver el costo por centro de costo/máquina para actualizar periódicamente el costo de cada máquina ("cada seis meses") [transcripción dudosa]. Hoy es un proceso manual.

---

## Reunión 2: 03/07/2026 (11:03), "EGI - Integración ODOO" (~1 h 54 min)

- **Participantes (según aparecen):** Alexander (Metrics), Vanessa, "Maca" (se va antes del final), Pablo (se le agradece), alguien que dice "soy Glenda" [transcripción dudosa], estudio contable ("Verino" según la Minuta 2). Minuta 2: "Alexandre, Calyx, Verino, Eg".
- **Temas:** valuación de compras y del PT, moneda, consumos individualizables vs globales, OP multiproducto, costo real de Metrics, WIP contable, XML de ejemplo.

### Decisiones / acuerdos explícitos (Minuta 2 + transcripción)
- **Inventario en Odoo en pesos**, al tipo de cambio de la OC y ajustado al valor de la factura. Sin bimonetaria nativa: si se quiere el inventario en USD, se saca de Metrics. **El ajuste por inflación está incluido** (confirmado).
- **PT valuado a costo real**, no al teórico de la receta de Metrics. Se lo da de alta sumando los consumos reales de **materias primas directas** (papel/sustrato, empaque) al costo de factura de compra en pesos. Hoy las horas máquina, amortizaciones y sueldos van a gasto. Quizás en el futuro se sume la mano de obra.
- **Método de valuación: PEPS/FIFO** para el consumo de materiales.
- **Consumos globales** (tinta, pegamento, adhesivos, no medibles por OP) se imputan al **centro de costo de la máquina**. Los individualizables (papel, sustrato, cajas, paquetes de empaque) van contra la OP.
- **OP multiproducto:** solo se agrupan productos del mismo formato y tamaño (mismo troquel; ej. cajas de gelatina de distintos sabores en un mismo pliego). El costo de materiales se reparte **proporcional a la cantidad** de cada producto en la OP.
- **Evaluar** un paso intermedio contable: consumos de MP a una cuenta "Productos en Proceso" y alta del PT al cierre de la OP.

### Preguntas abiertas / acciones
- ~~Alexander: habilitar la integración de OP y enviar XML de ejemplo (OP + movimiento de stock + entrega de producción del mismo producto).~~ La Minuta 2 lo marca **[COMPLETADO]**. En la reunión se pidió además un ejemplo con una OP de 2 productos y sus consumos. Alexander no encontró uno en el momento (ambiente "Machine Test").
- **Calyx:** analizar los XML y definir cómo mapear consumos y alta del PT según lo que necesitan las usuarias y el estudio contable.
- **Equipo general:** nueva reunión de seguimiento (con Alexander si hace falta) después de las pruebas manuales.
- **Abierto:** Metrics manda valores en USD a un tipo de cambio, pero cada insumo se compró a otro (ej. 1400 vs 1500). ¿Cómo se cruza eso con la valuación en pesos de Odoo? ("tengo que pensarlo").
- **Abierto:** el módulo "Costo real" de Metrics prorratea gastos a fin de mes. Por eso Odoo no puede tener la valuación exacta del PT online y haría falta recalcular después del cierre. En la reunión del 02/07 se dijo que EG no tiene ese módulo ("no compraron") [transcripción dudosa].
- **Abierto:** ¿el consumo informado al cerrar la OP coincidirá con los consumos reales enviados a WIP? Los consumos se pueden cargar hasta que se cierra la OP.
- Alexander menciona otras integraciones posibles que figuran en el manual: horas máquina ("TAPT" [transcripción dudosa]), producción y asientos contables. Recomienda consultar antes de decidir.
- Queda pendiente "el tema de los [show]" [transcripción dudosa], a ver con "Jeffers" [transcripción dudosa].

### Hechos de negocio aprendidos
- **Tinta y adhesivos** (Flexo) y **pegamentos** (pegadoras de Offset): hoy no se puede medir el consumo por OP. La tinta se va reponiendo en la máquina entre trabajos; medirla obligaría a parar la máquina, y eso cuesta más.
- La OP recibe costos de materiales y apuntes de horas (con centro de costo) y genera uno o más PT. Cada OP está vinculada al lote del PT y una OP puede tener varios lotes.
- Al PT se lo controla en la unidad del producto (unidades, metros o kilos). Cuando el PT entra a stock (entrega de producción) desde Metrics, viene valorado al **costo previsto** (estimado de la cotización/OP), no al real.
- Hoy EG no tiene relación entre productos terminados y su costo real ("La idea es hacer la mejora justamente por eso").
- Productos de distinto formato (ej. caja de gelatina y caja de torta) llevan presupuestos y OP distintos, porque cada uno tiene su papel, su impresión y su troquel.
