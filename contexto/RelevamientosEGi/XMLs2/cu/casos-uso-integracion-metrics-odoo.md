# Casos de uso — Integración Metrics → Odoo

**Versión:** 1.0  
**Fecha:** 2026-11-06  
**Base documental:** Manual de Integración XML Metrics (revisión 93), XML de ejemplo `01` a `16`, HUs de compras, documento técnico del módulo de integración y minutas de reunión.  
**Alcance:** flujos CRM, STKItem, WO (Manufactura de Odoo), SOR, POR, REC, STK, PCK, BIL, WIP y pruebas end-to-end.  
**Nivel de detalle:** funcional + QA, con precondiciones, pasos, resultado esperado, datos XML y criterios de aceptación.

---

## 1. Convenciones

| Convención | Significado |
|---|---|
| `CU-<CONTEXTO>-<nn>` | Identificador del caso de uso |
| P1 | Camino feliz o requisito crítico |
| P2 | Flujo alternativo o variante de negocio |
| P3 | Error, borde, cancelación o contingencia |
| INSERT / UPDATE / DELETE / CANCEL | Operación indicada por Metrics |
| Fixture | Archivo XML de `ejemplo completo/` usado como dato de prueba |
| R01–R23 | Reglas de transformación de `generar_excel_metrics.py` |
| HU-01–HU-16 | Historias de usuario del circuito de compras |
| Supuesto | Inferencia del equipo, pendiente de validación |
| Pendiente | Requiere definición de Metrics, negocio o proyecto |
| Estado QA | No ejecutado / OK / Fallo / Bloqueado |

### 1.1 Reglas transversales aplicables a todos los casos

- Una transacción de Metrics se identifica por `TransactionID` y no se procesa dos veces.
- Cada transacción se procesa según su contexto y su operación.
- Al finalizar, Odoo informa el resultado con `SetTransactionResult` (`HasError` 0 o 1 y mensaje).
- Un error en una transacción no debe frenar las siguientes.
- Los documentos recibidos de Metrics son de solo lectura en Odoo, salvo la factura de proveedor.
- Los maestros faltantes generan error claro y no crean registros parciales.
- La bitácora de integración se confirma independientemente del resultado del negocio.

### 1.2 Template de caso de uso

| Campo | Descripción |
|---|---|
| Contexto / operación | Contexto Metrics y operación esperada |
| Prioridad | P1, P2 o P3 |
| Fixture | XML de prueba |
| Precondiciones | Configuración y maestros necesarios |
| Datos clave | Campos del XML que se validan |
| Flujo principal | Pasos esperados |
| Alternativos / errores | Variantes y fallos controlados |
| Postcondiciones | Estado final en Odoo y en la bitácora |
| Reglas | R, HU o sección del manual |
| Criterios | Dado / Cuando / Entonces |
| Evidencia | Bitácora, XML de respuesta, captura o reporte |

---

## 2. Resumen por flujo

| Prefijo | Flujo | Fixtures | Casos |
|---|---|---|---|
| CU-INF | Transversal e integración | — | 10 |
| CU-CRM | Clientes y proveedores | 01, 02 | 13 |
| CU-ITM | Ítems de stock | 03, 04, clasificación | 13 |
| CU-WO | Órdenes de producción con Manufactura | 05, OP compartida | 21 |
| CU-SOR | Pedidos de venta | 06 | 9 |
| CU-POR | Órdenes de compra | 07 | 9 |
| CU-REC | Remitos de compra | 08 | 6 |
| CU-STK | Movimientos de stock | 09–13, transferencia | 31 |
| CU-PCK | Separación de materiales | 15 | 5 |
| CU-BIL | Remisión y facturación | 14, 16 | 13 |
| CU-WIP | Work in Progress | Manual 11.16–11.17 | 6 |
| CU-E2E | Flujos completos | 01–16 | 4 |
| **Total** | | | **140** |

---

## 3. Casos transversales de integración (`CU-INF`)

### CU-INF-01 · Configurar credenciales y entorno

| Campo | Valor |
|---|---|
| Contexto / operación | Configuración, sin transacción de negocio |
| Prioridad | P1 |
| Fixture | No aplica |
| Precondiciones | Usuario administrador de Odoo |
| Datos clave | URL del WSDL, usuario, contraseña, entorno (Sandbox/Homologación o Producción), cursor delta |
| Flujo principal | 1. Abrir ajustes de integración. 2. Cargar URL, usuario y contraseña. 3. Seleccionar entorno. 4. Guardar. 5. Verificar persistencia en `ir.config_parameter` y contraseña encriptada. |
| Alternativos / errores | URL vacía o inválida; entorno no seleccionado; contraseña vacía. |
| Postcondiciones | Credenciales persistidas; contraseña no visible en claro ni en logs. |
| Reglas | Documento técnico §2; HU-01 |
| Criterios | Dado un administrador, cuando guarda credenciales válidas, entonces quedan persistidas y la contraseña no se expone. |
| Evidencia | Captura de ajustes y registro de parámetros sin contraseña. |

### CU-INF-02 · Testear conexión exitosa

| Campo | Valor |
|---|---|
| Contexto / operación | Handshake SOAP |
| Prioridad | P1 |
| Fixture | No aplica |
| Precondiciones | Credenciales válidas y endpoint disponible |
| Datos clave | URL, usuario, contraseña, entorno |
| Flujo principal | 1. Presionar “Testear conexión”. 2. Odoo ejecuta handshake. 3. Mostrar banner verde de éxito. |
| Alternativos / errores | Respuesta lenta; certificado TLS inválido. |
| Postcondiciones | Notificación de éxito sin bloquear la pantalla. |
| Reglas | Documento técnico §2; HU-01 |
| Criterios | Dado un endpoint disponible, cuando se prueba la conexión, entonces se muestra éxito en menos del tiempo de timeout configurado. |
| Evidencia | Captura del banner y log de la llamada. |

### CU-INF-03 · Testear conexión con error

| Campo | Valor |
|---|---|
| Contexto / operación | Handshake SOAP |
| Prioridad | P2 |
| Fixture | No aplica |
| Precondiciones | Credenciales inválidas o endpoint caído |
| Datos clave | Código HTTP, mensaje SOAP, timeout |
| Flujo principal | 1. Presionar “Testear conexión”. 2. Odoo recibe error o timeout. 3. Mostrar diálogo de advertencia con código y mensaje. |
| Alternativos / errores | Timeout, DNS, 401, 500, WSDL inválido. |
| Postcondiciones | No se guardan datos parciales; el error queda visible. |
| Reglas | Documento técnico §2; HU-01 |
| Criterios | Dado un endpoint caído, cuando se prueba la conexión, entonces se muestra el error sin bloquear la interfaz. |
| Evidencia | Captura del diálogo y código devuelto. |

### CU-INF-04 · Lectura por lotes y actualización del cursor

| Campo | Valor |
|---|---|
| Contexto / operación | Importación por lotes |
| Prioridad | P1 |
| Fixture | Cualquiera de 01–16 |
| Precondiciones | Cursor de última sincronización configurado |
| Datos clave | Fecha de último éxito, límite 100, fecha del último registro procesado |
| Flujo principal | 1. Leer cursor. 2. Solicitar transacciones pendientes con límite 100. 3. Encolar cada registro nuevo. 4. Al completar el lote, actualizar el cursor. |
| Alternativos / errores | Lote incompleto; error a mitad; registro sin TransactionID; cursor no avanza. |
| Postcondiciones | Cursor actualizado solo si el lote se procesó completo. |
| Reglas | Documento técnico §3; HU-02 |
| Criterios | Dado un lote de 100, cuando termina correctamente, entonces el cursor toma la fecha del último registro y no se reprocesa el lote. |
| Evidencia | Log de lotes, tabla de bitácora y valor del cursor antes/después. |

### CU-INF-05 · Idempotencia por TransactionID

| Campo | Valor |
|---|---|
| Contexto / operación | Cualquier contexto |
| Prioridad | P1 |
| Fixture | `11- Consumo de Material.txt` repetido |
| Precondiciones | Transacción ya registrada en la bitácora |
| Datos clave | `TransactionID`, `transactioncodeextref` |
| Flujo principal | 1. Recibir transacción. 2. Buscar `TransactionID` en la bitácora. 3. Si existe, ignorar. 4. Informar resultado sin reprocesar. |
| Alternativos / errores | ID vacío; ID duplicado con distinto payload; reintento tras error. |
| Postcondiciones | No se duplican registros de negocio ni movimientos de stock. |
| Reglas | Documento técnico §1 y §3; HU-02 |
| Criterios | Dada una transacción ya procesada, cuando vuelve a llegar, entonces se descarta y no se crea un segundo registro. |
| Evidencia | Conteo de registros antes/después y bitácora. |

### CU-INF-06 · Bitácora de integración y reproceso

| Campo | Valor |
|---|---|
| Contexto / operación | Auditoría |
| Prioridad | P1 |
| Fixture | Transacción forzada con error |
| Precondiciones | Módulo de integración instalado |
| Datos clave | `transaction_id`, `context_type`, `xml_operation`, `xml_data`, `has_error`, `return_code`, `xml_return`, `dt_processing` |
| Flujo principal | 1. Registrar cada transacción entrante o saliente. 2. Guardar XML original, contexto, operación, estado y fecha UTC. 3. Permitir filtrar por estado y reprocesar. |
| Alternativos / errores | Error de negocio; error de red; XML malformado. |
| Postcondiciones | La bitácora conserva el detalle aun si el negocio falla. |
| Reglas | Documento técnico §1 y §4; HU-03 |
| Criterios | Dada una transacción fallida, cuando el usuario filtra por error, entonces la ve con su mensaje y puede reprocesarla. |
| Evidencia | Captura de la bitácora y del reproceso. |

### CU-INF-07 · Aislamiento de logs y prueba del ácido

| Campo | Valor |
|---|---|
| Contexto / operación | Transaccionalidad |
| Prioridad | P1 |
| Fixture | Cualquiera, con fallo forzado |
| Precondiciones | Cola de trabajos o savepoint configurado |
| Datos clave | `has_error`, rollback de negocio, commit de bitácora |
| Flujo principal | 1. Registrar la transacción y confirmar. 2. Delegar el negocio a un job o savepoint. 3. Si el negocio falla, hacer rollback solo del negocio. 4. Marcar la bitácora con error y detalle. |
| Alternativos / errores | Caída del servidor intermedio; excepción no controlada; job reintentado. |
| Postcondiciones | No quedan datos basura; la bitácora conserva el error. |
| Reglas | Documento técnico §4 |
| Criterios | Dado un fallo crítico a mitad de la importación, cuando se revisa Odoo, entonces no hay registros comerciales parciales y la bitácora muestra `has_error = True`. |
| Evidencia | Consulta a tablas de negocio y bitácora. |

### CU-INF-08 · Equivalencias de maestros

| Campo | Valor |
|---|---|
| Contexto / operación | Validación previa |
| Prioridad | P1 |
| Fixture | 01, 04, 07, 09 |
| Precondiciones | Tablas de equivalencia configuradas |
| Datos clave | `suppliercode`, `stockcode`, `unitcode`, `idcurrency`, `idcompany`, `stockplacecode` |
| Flujo principal | 1. Resolver cada código contra Odoo. 2. Si falta una equivalencia, detener la transacción. 3. Informar el código faltante. |
| Alternativos / errores | Moneda desconocida; UOM inexistente; ubicación inválida; empresa inactiva. |
| Postcondiciones | No se crea nada a medias. |
| Reglas | HU-04; R01 |
| Criterios | Dado un `stockcode` sin equivalencia, cuando se procesa la transacción, entonces queda en error con mensaje claro y no se crea el documento. |
| Evidencia | Mensaje de error y ausencia del registro. |

### CU-INF-09 · Informar resultado a Metrics

| Campo | Valor |
|---|---|
| Contexto / operación | `SetTransactionResult` |
| Prioridad | P1 |
| Fixture | Cualquiera |
| Precondiciones | Transacción procesada |
| Datos clave | `TransactionID`, `HasError` 0/1, mensaje |
| Flujo principal | 1. Procesar la transacción. 2. Informar resultado con una operación por llamada. 3. Registrar la respuesta. |
| Alternativos / errores | Metrics no responde; respuesta duplicada; error al informar. |
| Postcondiciones | Metrics conoce el resultado; Odoo conserva evidencia. |
| Reglas | Manual 11.1 y 11.3; HU-02 |
| Criterios | Dado un procesamiento exitoso, cuando Odoo informa el resultado, entonces Metrics recibe `HasError = 0`; si falla, recibe `HasError = 1` con mensaje. |
| Evidencia | XML de respuesta y bitácora. |

### CU-INF-10 · Orden de llegada y reintentos

| Campo | Valor |
|---|---|
| Contexto / operación | Concurrencia y reintentos |
| Prioridad | P1 |
| Fixture | 08 y 09 en orden invertido |
| Precondiciones | Cola de trabajos activa |
| Datos clave | Dependencia REC/OC, fecha de transacción, contador de reintentos |
| Flujo principal | 1. Detectar dependencia faltante. 2. Encolar reintento con espera. 3. Reintentar hasta el máximo configurado. 4. Si persiste, marcar error. |
| Alternativos / errores | Llegada de STK antes que REC; UPDATE antes que INSERT; dependencia circular. |
| Postcondiciones | No hay bucles infinitos; la transacción queda en error accionable si no se resuelve. |
| Reglas | HU-02; documento técnico §3 |
| Criterios | Dado un STK que llega antes que su REC, cuando se reintenta, entonces espera la creación del remito y luego se procesa. |
| Evidencia | Log de reintentos y estado final. |

---

## 4. Casos de CRM (`CU-CRM`)

### CU-CRM-01 · Alta de cliente activo

| Campo | Valor |
|---|---|
| Contexto / operación | CRM / INSERT |
| Prioridad | P1 |
| Fixture | `01- Clientes.txt` |
| Precondiciones | Tipo de identificación, país y moneda disponibles |
| Datos clave | `code=327`, `name`, `fullname`, `iscustomer=1`, `isactv=1`, `persontype=1`, `countrycode=639` |
| Flujo principal | 1. Crear `res.partner`. 2. Asignar `customer_rank > 0`. 3. Guardar `code` como referencia externa. 4. Crear dirección y contacto. |
| Alternativos / errores | Cliente ya existente; documento fiscal duplicado; país desconocido. |
| Postcondiciones | Cliente creado una sola vez, con dirección y contacto. |
| Reglas | R02, R03, R04, R05, R06, R19, R22 |
| Criterios | Dado un cliente activo, cuando se procesa el XML, entonces se crea un `res.partner` con `customer_rank > 0`, dirección y contacto, sin duplicados. |
| Evidencia | Ficha del partner y bitácora. |

### CU-CRM-02 · Alta de proveedor

| Campo | Valor |
|---|---|
| Contexto / operación | CRM / INSERT |
| Prioridad | P1 |
| Fixture | `02- Proveedores.txt` |
| Precondiciones | Moneda y país disponibles |
| Datos clave | `code=329`, `issupplier=1`, `iscustomer=0`, `countrydocumentnumber`, `conditionpaymentstandard` |
| Flujo principal | 1. Crear `res.partner`. 2. Asignar `supplier_rank > 0`. 3. Crear dirección. 4. Asociar condición de pago si existe. |
| Alternativos / errores | Proveedor existente; condición de pago inexistente; documento inválido. |
| Postcondiciones | Proveedor creado y disponible para OC y facturas. |
| Reglas | R02, R03, R05, R06 |
| Criterios | Dado un proveedor activo, cuando se procesa el XML, entonces se crea con `supplier_rank > 0` y sus datos fiscales. |
| Evidencia | Ficha del partner y bitácora. |

### CU-CRM-03 · Actor mixto cliente y proveedor

| Campo | Valor |
|---|---|
| Contexto / operación | CRM / INSERT o UPDATE |
| Prioridad | P2 |
| Fixture | Variante de 01 con `iscustomer=1` e `issupplier=1` |
| Precondiciones | Partner existente o nuevo |
| Datos clave | `iscustomer`, `issupplier`, `customer_rank`, `supplier_rank` |
| Flujo principal | 1. Crear o actualizar el partner. 2. Asignar ambos ranks. 3. Mantener una sola ficha. |
| Alternativos / errores | Dos fichas para el mismo actor; ranks inconsistentes. |
| Postcondiciones | Una sola ficha con ambos roles. |
| Reglas | R06 |
| Criterios | Dado un actor mixto, cuando se procesa, entonces queda una única ficha con `customer_rank > 0` y `supplier_rank > 0`. |
| Evidencia | Ficha única y ranks. |

### CU-CRM-04 · Persona física, jurídica, gobierno y exportación

| Campo | Valor |
|---|---|
| Contexto / operación | CRM / INSERT |
| Prioridad | P2 |
| Fixture | Variantes de 01 con `persontype` 0, 1, 2 y 3 |
| Precondiciones | Sin datos previos del actor |
| Datos clave | `persontype`, `persontypecompl`, `isperson` |
| Flujo principal | 1. Mapear `0 → person`. 2. Mapear `1, 2, 3 → company`. 3. Ajustar tipo de identificación. |
| Alternativos / errores | `persontype` desconocido; `isperson` contradictorio. |
| Postcondiciones | `company_type` correcto. |
| Reglas | R02, R06 |
| Criterios | Dado `persontype=0`, cuando se procesa, entonces el partner es `person`; dado `persontype=1`, entonces es `company`. |
| Evidencia | Campo `company_type` en la ficha. |

### CU-CRM-05 · Documento fiscal por país

| Campo | Valor |
|---|---|
| Contexto / operación | CRM / INSERT o UPDATE |
| Prioridad | P1 |
| Fixture | 01 y 02 |
| Precondiciones | Módulo de localización del país instalado |
| Datos clave | `countrydocumentnumber`, `countrycode=639`, `countryfiscalcode=13`, `persontype` |
| Flujo principal | 1. Identificar país por código BACEN. 2. Validar documento. 3. Asignar tipo de identificación y responsabilidad fiscal. |
| Alternativos / errores | CUIT inválido; documento vacío; país sin localización; documento duplicado. |
| Postcondiciones | `vat` y tipo de identificación asignados. |
| Reglas | R03, R04, R05, R21 |
| Criterios | Dado un CUIT argentino válido, cuando se procesa, entonces se asigna como `vat` y tipo CUIT; dado un CUIT inválido, entonces la transacción falla. |
| Evidencia | Ficha fiscal y mensaje de error. |

### CU-CRM-06 · Direcciones múltiples

| Campo | Valor |
|---|---|
| Contexto / operación | CRM / INSERT o UPDATE |
| Prioridad | P1 |
| Fixture | 01 y 02, nodo `sdilcrmaddress` |
| Precondiciones | Partner creado |
| Datos clave | `isbilling`, `ischarging`, `ismailing`, `isdelivery`, `addressprefix`, `addressname`, `addressnumber`, `zipcode` |
| Flujo principal | 1. Leer cada dirección. 2. Mapear `isbilling → invoice`. 3. Mapear `isdelivery → delivery`. 4. Mapear `ischarging → other`. 5. Concatenar calle. |
| Alternativos / errores | Dirección sin tipo; múltiples direcciones del mismo tipo; dirección duplicada. |
| Postcondiciones | Direcciones creadas como contactos hijos. |
| Reglas | R19, R22 |
| Criterios | Dada una dirección con `isbilling=1` e `isdelivery=1`, cuando se procesa, entonces se crean los tipos correspondientes sin perder datos. |
| Evidencia | Contactos hijos y tipos. |

### CU-CRM-07 · Contactos del actor

| Campo | Valor |
|---|---|
| Contexto / operación | CRM / INSERT o UPDATE |
| Prioridad | P2 |
| Fixture | 01, nodo `sdilcrmactorcontact` |
| Precondiciones | Partner creado |
| Datos clave | `code=328`, `name`, `fullname`, `phone`, `email`, `isactv` |
| Flujo principal | 1. Crear contacto hijo. 2. Asociarlo al partner. 3. Guardar referencia externa. |
| Alternativos / errores | Contacto sin código; contacto inactivo; duplicado. |
| Postcondiciones | Contacto hijo creado una sola vez. |
| Reglas | R06, R19 |
| Criterios | Dado un contacto con código, cuando se procesa, entonces se crea como hijo del partner y no se duplica al reintentar. |
| Evidencia | Contacto hijo y bitácora. |

### CU-CRM-08 · Condición de pago, crédito y vendedor

| Campo | Valor |
|---|---|
| Contexto / operación | CRM / INSERT o UPDATE |
| Prioridad | P2 |
| Fixture | 01 y 02 |
| Precondiciones | Términos de pago y vendedores disponibles |
| Datos clave | `conditionpaymentstandard`, `limitvaluecredit`, `creditexpirationdt`, `salesmancode` |
| Flujo principal | 1. Buscar término de pago por nombre. 2. Si no existe, crearlo. 3. Asignar límite y vencimiento de crédito. 4. Asociar vendedor. |
| Alternativos / errores | Término inexistente; vendedor inexistente; crédito en cero. |
| Postcondiciones | Datos comerciales asignados. |
| Reglas | HU-06 |
| Criterios | Dada una condición “45 dias” inexistente, cuando se procesa, entonces se crea el término y se asocia al partner. |
| Evidencia | Partner y término de pago. |

### CU-CRM-09 · Prospecto o cliente inactivo

| Campo | Valor |
|---|---|
| Contexto / operación | CRM / INSERT |
| Prioridad | P1 |
| Fixture | Variante de 01 con `isprospect=1` o `isactv=0` |
| Precondiciones | Configuración “solo activos” |
| Datos clave | `isprospect`, `isactv` |
| Flujo principal | 1. Detectar prospecto o inactivo. 2. No crear el partner. 3. Registrar la transacción como omitida. |
| Alternativos / errores | Prospecto que luego se activa; inactivo con documentos previos. |
| Postcondiciones | Odoo no recibe prospectos ni inactivos. |
| Reglas | Minuta funcional §1 |
| Criterios | Dado un prospecto, cuando se procesa, entonces no se crea el partner y la bitácora lo registra como omitido. |
| Evidencia | Bitácora y ausencia del partner. |

### CU-CRM-10 · Actualización sin duplicar

| Campo | Valor |
|---|---|
| Contexto / operación | CRM / UPDATE |
| Prioridad | P1 |
| Fixture | 01 procesado dos veces con cambios |
| Precondiciones | Partner existente con `code` |
| Datos clave | `code`, `name`, `phone`, `email`, `isactv` |
| Flujo principal | 1. Buscar partner por `code`. 2. Actualizar campos enviados. 3. Preservar campos propios de Odoo no informados. |
| Alternativos / errores | `code` inexistente; cambio de documento fiscal; partner archivado. |
| Postcondiciones | Un solo partner actualizado. |
| Reglas | R06 |
| Criterios | Dado un partner existente, cuando llega un UPDATE, entonces se actualiza la misma ficha y no se crea otra. |
| Evidencia | Comparación antes/después y conteo de partners. |

### CU-CRM-11 · Responsabilidad AFIP e IIBB

| Campo | Valor |
|---|---|
| Contexto / operación | CRM / INSERT o UPDATE |
| Prioridad | P2 |
| Fixture | 01 y 02 |
| Precondiciones | Módulo `l10n_ar` y `l10n_ar_ux` si aplica |
| Datos clave | `broptingsimplenational`, `countryfiscalcode`, `state` |
| Flujo principal | 1. Mapear responsabilidad AFIP. 2. Asignar jurisdicción de IIBB por provincia. 3. Guardar datos fiscales. |
| Alternativos / errores | Código fiscal desconocido; provincia sin jurisdicción; responsabilidad contradictoria. |
| Postcondiciones | Partner con responsabilidad AFIP e IIBB coherentes. |
| Reglas | R05, R21, R23 |
| Criterios | Dado `broptingsimplenational=3`, cuando se procesa, entonces se asigna Responsable Inscripto. |
| Evidencia | Ficha fiscal y jurisdicciones. |

### CU-CRM-12 · Error por país o moneda desconocidos

| Campo | Valor |
|---|---|
| Contexto / operación | CRM / INSERT |
| Prioridad | P3 |
| Fixture | Variante de 01 con `countrycode=999` |
| Precondiciones | Código no configurado |
| Datos clave | `countrycode`, `idcurrency`, `unitcode` |
| Flujo principal | 1. Intentar resolver el código. 2. No encontrarlo. 3. Registrar error y no crear el partner. |
| Alternativos / errores | Código vacío; país inactivo; moneda sin tabla. |
| Postcondiciones | Sin registro parcial; error accionable. |
| Reglas | HU-04; R04 |
| Criterios | Dado un país desconocido, cuando se procesa, entonces la transacción falla con mensaje y no se crea nada. |
| Evidencia | Bitácora y ausencia de partner. |

### CU-CRM-13 · Baja o desactivación de actor

| Campo | Valor |
|---|---|
| Contexto / operación | CRM / UPDATE o DELETE |
| Prioridad | P2 |
| Fixture | Variante de 01 con `isactv=0` |
| Precondiciones | Partner existente |
| Datos clave | `code`, `isactv` |
| Flujo principal | 1. Detectar baja. 2. Archivar el partner. 3. No borrar historial. |
| Alternativos / errores | Actor con documentos abiertos; actor con movimientos de stock. |
| Postcondiciones | Partner archivado, historial conservado. |
| Reglas | Minuta funcional §1 |
| Criterios | Dado un cliente inactivo, cuando se procesa, entonces se archiva y no se elimina su historial. |
| Evidencia | Estado `active` y documentos vinculados. |

---

## 5. Casos de ítems de stock (`CU-ITM`)

### CU-ITM-01 · Alta de producto terminado

| Campo | Valor |
|---|---|
| Contexto / operación | STKITEM / INSERT |
| Prioridad | P1 |
| Fixture | `03- Producto Terminado.txt` |
| Precondiciones | Categorías y UOM disponibles |
| Datos clave | `iditem=1`, `materialtype=6`, `itemtype=1`, `stockcode=99.0001`, `unitcode=UN`, `unitcodedemand=UN`, `unitcodecost=UN`, `mastermaterialgroupcode=99`, `uselot=1`, `controltraceability=1` |
| Flujo principal | 1. Crear `product.product`. 2. Asignar `default_code=stockcode`. 3. Mapear `itemtype=1 → type=product`. 4. Asignar UOM y categoría. 5. Configurar trazabilidad. |
| Alternativos / errores | Código duplicado; UOM inexistente; categoría inexistente. |
| Postcondiciones | PT creado y disponible para WO, SOR y STK. |
| Reglas | R01, R07, R08, R09, R10 |
| Criterios | Dado un PT con `stockcode=99.0001`, cuando se procesa, entonces existe un producto almacenable con ese código y su trazabilidad. |
| Evidencia | Ficha del producto y bitácora. |

### CU-ITM-02 · Alta de materia prima

| Campo | Valor |
|---|---|
| Contexto / operación | STKITEM / INSERT |
| Prioridad | P1 |
| Fixture | `04- Material.txt` |
| Precondiciones | Categorías de sustratos disponibles |
| Datos clave | `iditem=5`, `materialtype=4`, `itemtype=0`, `stockcode=02.01.0003`, `unitcode=FL`, `unitcodedemand=FL`, `unitcodecost=KG`, `materialgroupcode=02.01`, `mastermaterialgroupcode=02`, `weightkg=1`, `searchkey=KLABIN` |
| Flujo principal | 1. Crear `product.product`. 2. Mapear `itemtype=0 → type=product`. 3. Asignar UOM de stock, demanda y costo. 4. Crear jerarquía de categorías. |
| Alternativos / errores | UOM de costo distinta a KG; categoría inexistente; código duplicado. |
| Postcondiciones | MP creada con UOM de compra/stock/consumo diferenciadas. |
| Reglas | R01, R07, R08, R10 |
| Criterios | Dado `unitcode=FL` y `unitcodecost=KG`, cuando se procesa, entonces el producto conserva ambas unidades y el factor de conversión. |
| Evidencia | Ficha del producto y conversiones. |

### CU-ITM-03 · Alta de intermediario, servicio y consumible

| Campo | Valor |
|---|---|
| Contexto / operación | STKITEM / INSERT |
| Prioridad | P2 |
| Fixture | Variantes de 03 y 04 con `itemtype=2, 3 y 4` |
| Precondiciones | Categorías disponibles |
| Datos clave | `itemtype` |
| Flujo principal | 1. Mapear `2 → product`. 2. Mapear `3 → service`. 3. Mapear `4 → consu`. 4. Ajustar configuración de inventario. |
| Alternativos / errores | Servicio con lote; consumible con trazabilidad. |
| Postcondiciones | Tipo de producto correcto y sin inventario cuando no corresponde. |
| Reglas | R07 |
| Criterios | Dado `itemtype=3`, cuando se procesa, entonces el producto es de tipo servicio y no controla stock. |
| Evidencia | Campo `type` y configuración de inventario. |

### CU-ITM-04 · Clasificación de producto

| Campo | Valor |
|---|---|
| Contexto / operación | STKITEM / INSERT o UPDATE |
| Prioridad | P2 |
| Fixture | `XML STKITEM con Clasificacion de Producto.txt` |
| Precondiciones | Tabla de clasificación de producto cargada |
| Datos clave | `stockcode=99.0014`, `productclassification=Láminas`, `needseparation=1`, `differentlotsseparation=1` |
| Flujo principal | 1. Leer `productclassification`. 2. Buscar la clasificación en Odoo. 3. Asociarla al producto o a su categoría. 4. Guardar flags de separación. |
| Alternativos / errores | Clasificación inexistente; valor vacío; clasificación duplicada. |
| Postcondiciones | Producto clasificado y con flags de separación. |
| Reglas | CSV `Clasificacion de Producto.csv`; minuta funcional §4 |
| Criterios | Dado `productclassification=Láminas`, cuando se procesa, entonces el producto queda asociado a esa clasificación sin crear una nueva si ya existe. |
| Evidencia | Ficha del producto y tabla de clasificación. |

### CU-ITM-05 · Jerarquía de categorías

| Campo | Valor |
|---|---|
| Contexto / operación | STKITEM / INSERT |
| Prioridad | P1 |
| Fixture | 04 |
| Precondiciones | Categoría raíz “Metrics” |
| Datos clave | `mastermaterialgroupcode=02`, `mastermaterialgroupdescription=Sustratos`, `materialgroupcode=02.01`, `materialgroupdescription=Papel Cartón` |
| Flujo principal | 1. Crear nivel master. 2. Crear nivel group como hijo. 3. Asignar el producto al nivel group. |
| Alternativos / errores | Master existente; group con distinto padre; códigos repetidos con distinta descripción. |
| Postcondiciones | Jerarquía master → group → producto. |
| Reglas | R08, R10 |
| Criterios | Dado un producto con master y group, cuando se procesa, entonces se crea la jerarquía sin duplicar categorías. |
| Evidencia | Árbol de categorías. |

### CU-ITM-06 · UOM y conversiones

| Campo | Valor |
|---|---|
| Contexto / operación | STKITEM / INSERT o UPDATE |
| Prioridad | P1 |
| Fixture | 03 y 04 |
| Precondiciones | UOM base disponibles |
| Datos clave | `unitcode`, `unitcodedemand`, `unitcodecost`, `sdistkunitconversion.unitcodeorigin`, `unitcodedestiny`, `factor` |
| Flujo principal | 1. Buscar cada UOM por nombre o símbolo. 2. Crear la UOM si no existe. 3. Guardar factores de conversión. 4. Validar coherencia entre compra, stock, consumo e ingeniería. |
| Alternativos / errores | UOM inexistente; factor cero o negativo; conversión duplicada. |
| Postcondiciones | UOM y factores disponibles para STK y WO. |
| Reglas | R01; minuta funcional §5 |
| Criterios | Dado un producto con `unitcodecost=KG`, cuando se procesa, entonces el costo y el stock se expresan en KG y la cantidad original en FL queda informativa. |
| Evidencia | UOM del producto y tabla de conversiones. |

### CU-ITM-07 · Trazabilidad por lote o serie

| Campo | Valor |
|---|---|
| Contexto / operación | STKITEM / INSERT o UPDATE |
| Prioridad | P1 |
| Fixture | 03 y 04 |
| Precondiciones | Producto sin tracking definido |
| Datos clave | `uselot`, `controltraceability` |
| Flujo principal | 1. Evaluar `uselot`. 2. Evaluar `controltraceability`. 3. Asignar `lot`, `serial` o `none` según R09. |
| Alternativos / errores | Ambos flags en 1; PT con serie cuando el negocio espera lote; cambio de tracking con stock existente. |
| Postcondiciones | `tracking` configurado. |
| Reglas | R09 |
| Criterios | Dado `uselot=1` y `controltraceability=0`, cuando se procesa, entonces `tracking=lot`. |
| Evidencia | Campo `tracking` del producto. |

### CU-ITM-08 · NCM, EAN, FSC y pesos

| Campo | Valor |
|---|---|
| Contexto / operación | STKITEM / INSERT o UPDATE |
| Prioridad | P2 |
| Fixture | 03, 04 y clasificación |
| Precondiciones | Módulo de localización para NCM |
| Datos clave | `ncm`, `ean`, `isfsc`, `weightkg`, `unitweight`, `grammage`, `height`, `width`, `packagingqty`, `packagingunit` |
| Flujo principal | 1. Asignar NCM. 2. Asignar EAN como código de barras. 3. Guardar peso y dimensiones. 4. Guardar unidad de empaque. |
| Alternativos / errores | NCM inválido; EAN duplicado; peso cero. |
| Postcondiciones | Datos fiscales y logísticos completos. |
| Reglas | AGENTS.md; mapeo STKItem |
| Criterios | Dado un producto con EAN, cuando se procesa, entonces el código de barras queda asignado y no se duplica en otro producto. |
| Evidencia | Ficha del producto. |

### CU-ITM-09 · Vínculo de bobina madre e hija (OriginItem)

| Campo | Valor |
|---|---|
| Contexto / operación | STKITEM / INSERT o UPDATE |
| Prioridad | P1 |
| Fixture | Pendiente: muestra con `originitem` distinto de 0 |
| Precondiciones | Ítem madre existente |
| Datos clave | `stockcode`, `originitem`, `usesctrlvolume`, `unitcodecost` |
| Flujo principal | 1. Leer `originitem`. 2. Buscar el ítem madre. 3. Vincular la hija con la madre. 4. Heredar o prorratear costo según regla de negocio. |
| Alternativos / errores | Madre inexistente; `originitem=0`; ciclos de dependencia; costo sin prorrateo. |
| Postcondiciones | Relación madre/hija trazable y costo heredado. |
| Reglas | Minuta funcional §6; AGENTS.md |
| Criterios | Dado un ítem hija con `originitem` válido, cuando se procesa, entonces queda vinculado a la madre y el costo se prorratea según la regla definida. |
| Evidencia | Vínculo entre productos y costo resultante. |

### CU-ITM-10 · Control por volúmenes

| Campo | Valor |
|---|---|
| Contexto / operación | STKITEM / INSERT o UPDATE |
| Prioridad | P2 |
| Fixture | Variante de 04 con `usesctrlvolume=1` y `sdistkitemvolumeinfo` |
| Precondiciones | Configuración de volúmenes |
| Datos clave | `usesctrlvolume`, `standarddiameter`, `volumemaxweight`, `volumeminweight`, `labeldescription` |
| Flujo principal | 1. Detectar `usesctrlvolume=1`. 2. Configurar control individual por volumen. 3. Guardar límites de peso y diámetro. |
| Alternativos / errores | Ítem volumétrico sin etiqueta; movimiento sin colector; límites en cero. |
| Postcondiciones | Producto marcado como volumétrico. |
| Reglas | Minuta funcional §4; AGENTS.md |
| Criterios | Dado `usesctrlvolume=1`, cuando se procesa, entonces el producto queda marcado como volumétrico y solo se mueve por el circuito permitido. |
| Evidencia | Configuración del producto. |

### CU-ITM-11 · Modificación de ítem existente

| Campo | Valor |
|---|---|
| Contexto / operación | STKITEM / UPDATE |
| Prioridad | P1 |
| Fixture | 03 y 04 procesados con cambios |
| Precondiciones | Producto existente por `stockcode` |
| Datos clave | `stockcode`, `materialname`, `unitcode`, `materialgroupcode`, `status` |
| Flujo principal | 1. Buscar producto por `default_code`. 2. Actualizar campos enviados. 3. Preservar campos propios de Odoo. 4. No duplicar. |
| Alternativos / errores | Cambio de código; producto archivado; cambio de UOM con stock. |
| Postcondiciones | Producto actualizado una sola vez. |
| Reglas | R07, R08 |
| Criterios | Dado un producto existente, cuando llega un UPDATE, entonces se actualiza la misma ficha y no se crea otra. |
| Evidencia | Comparación antes/después. |

### CU-ITM-12 · Error por UOM o categoría faltante

| Campo | Valor |
|---|---|
| Contexto / operación | STKITEM / INSERT |
| Prioridad | P3 |
| Fixture | Variante de 04 con `unitcode=ZZ` |
| Precondiciones | Código no configurado |
| Datos clave | `unitcode`, `materialgroupcode`, `mastermaterialgroupcode` |
| Flujo principal | 1. Intentar resolver la UOM o categoría. 2. No encontrarla. 3. Registrar error. 4. No crear el producto. |
| Alternativos / errores | Categoría sin descripción; UOM inactiva; factor de conversión inválido. |
| Postcondiciones | Sin producto parcial; error accionable. |
| Reglas | HU-04; R01 |
| Criterios | Dada una UOM inexistente, cuando se procesa, entonces la transacción falla y no se crea el producto. |
| Evidencia | Bitácora y ausencia de producto. |

### CU-ITM-13 · Discrepancia de MaterialType entre STKItem y WO

| Campo | Valor |
|---|---|
| Contexto / operación | Validación de reglas |
| Prioridad | P1 |
| Fixture | 03, 04, 05 y OP compartida |
| Precondiciones | Mapeos R08 y materialtype de WO cargados |
| Datos clave | `materialtype` de STKItem: 1 Tinta, 2 Plancha, 3 Otros, 4 Papel Hoja, 5 Papel Bobina, 6 Personalizado; `materialtype` de WO: 0 Papel, 1 Tinta, 2 Plancha, 3 Otros |
| Flujo principal | 1. Identificar el contexto del XML. 2. Aplicar la tabla de materialtype correspondiente. 3. No reutilizar la tabla de WO en STKItem ni viceversa. |
| Alternativos / errores | Aplicar R08 a WO; interpretar `3` como “Otros” en STKItem y como “Otros” en WO con distinto origen; `materialtype=6` en WO. |
| Postcondiciones | Categorías correctas según contexto. |
| Reglas | R08; AGENTS.md |
| Criterios | Dado un STKItem con `materialtype=4`, cuando se procesa, entonces se crea “Papel Hoja” y no “Otros”; dado un WO con `materialtype=3`, entonces se interpreta como “Otros”. |
| Evidencia | Categoría asignada y tabla de mapeo usada. |

---

## 6. Casos de órdenes de producción con Manufactura de Odoo (`CU-WO`)

> **Modelo:** el flujo WO se implementa con el módulo Manufactura (`mrp`). La cabecera es `mrp.production`; las operaciones son `mrp.workorder`; la estructura es `mrp.bom` y `mrp.bom.line`. El consumo real se descuenta por STK TType 0 y WIP se usa solo para conciliar.

### CU-WO-01 · Alta de orden de manufactura

| Campo | Valor |
|---|---|
| Contexto / operación | WO / INSERT |
| Prioridad | P1 |
| Fixture | `05- OP WO.txt` |
| Precondiciones | PT con BOM, UOM y centro de trabajo |
| Datos clave | `wonumber=OFC00001`, `wodescription`, `status=3`, `insertdt`, `sdilwofinisheditem.stockcode=99.0001`, `quantity=100000`, `unitcode=UN`, `deliverydt` |
| Flujo principal | 1. Crear `mrp.production`. 2. Asignar `product_id` y `product_qty`. 3. Asignar UOM y empresa. 4. Guardar `origin=wonumber`. 5. Asignar `date_deadline`. |
| Alternativos / errores | PT inexistente; BOM inexistente; cantidad cero; `wonumber` duplicado. |
| Postcondiciones | MO creada en el estado que corresponda y vinculada al `wonumber`. |
| Reglas | R13, R14; AGENTS.md |
| Criterios | Dado un WO con PT y cantidad, cuando se procesa, entonces se crea una MO con `origin=wonumber`, producto y cantidad correctos. |
| Evidencia | Ficha de la MO y bitácora. |

### CU-WO-02 · Cabecera, estados y fechas

| Campo | Valor |
|---|---|
| Contexto / operación | WO / INSERT o UPDATE |
| Prioridad | P1 |
| Fixture | 05 y variantes de `status` 0–6 |
| Precondiciones | MO existente |
| Datos clave | `idcompany`, `wonumber`, `wodescription`, `quotenumber`, `status`, `insertdt`, `projectcode`, `projecttitle` |
| Flujo principal | 1. Mapear `status` a `mrp.production.state` según R13. 2. Guardar cotización, proyecto y fechas. 3. Validar que el estado no retroceda sin regla. |
| Alternativos / errores | `status=4` con MO en producción; `status=6`; estado no contemplado; transición inválida. |
| Postcondiciones | MO con estado y datos de cabecera coherentes. |
| Reglas | R13 |
| Criterios | Dado `status=3`, cuando se procesa, entonces la MO queda en estado cerrado o terminado según la tabla acordada; dado un estado no mapeado, entonces falla con mensaje. |
| Evidencia | Estado de la MO y bitácora. |

### CU-WO-03 · Materias primas a la BOM

| Campo | Valor |
|---|---|
| Contexto / operación | WO / INSERT o UPDATE |
| Prioridad | P1 |
| Fixture | `05- OP WO.txt` y OP compartida |
| Precondiciones | MP existentes por `stockcode` |
| Datos clave | `sdiworawmaterial.materialtype`, `stockcode`, `materialname`, `unitcode`, `quantity`, `unitcode2`, `quantity2`, `idativ` |
| Flujo principal | 1. Leer cada MP. 2. Resolver `stockcode`. 3. Crear o actualizar `mrp.bom.line`. 4. Asignar cantidad y UOM. 5. Guardar `idativ` como referencia. |
| Alternativos / errores | `stockcode` vacío y solo `materialname`; MP inexistente; cantidad cero; MP duplicada; `materialtype` inconsistente. |
| Postcondiciones | BOM de la MO con las MP declaradas. |
| Reglas | R08, R14; decisión “ambos alimentan la BOM” |
| Criterios | Dada una MP con `stockcode` válido, cuando se procesa, entonces existe una línea de BOM con producto, cantidad y UOM; si el `stockcode` viene vacío, entonces se resuelve por nombre o falla con mensaje. |
| Evidencia | BOM de la MO y bitácora. |

### CU-WO-04 · Componentes a la BOM y validación de semántica

| Campo | Valor |
|---|---|
| Contexto / operación | WO / INSERT o UPDATE |
| Prioridad | P1 |
| Fixture | 05 y OP compartida |
| Precondiciones | BOM de la MO |
| Datos clave | `sdiwocomponent.name`, `stockcode`, `quantity`, `sdilwoinputcomponent` |
| Flujo principal | 1. Leer cada componente. 2. Resolver `stockcode`. 3. Agregar a `mrp.bom.line` si es insumo. 4. Ignorar o marcar si repite el PT. |
| Alternativos / errores | El componente repite el `stockcode` del PT (como en las muestras); `quantity=0`; componente sin stockcode; BOM circular. |
| Postcondiciones | BOM sin líneas circulares ni duplicadas. |
| Reglas | Decisión “ambos alimentan la BOM”; AGENTS.md |
| Criterios | Dado un componente con `stockcode` distinto al PT, cuando se procesa, entonces se agrega a la BOM; dado un componente igual al PT, entonces se detecta y no se crea una BOM circular. |
| Evidencia | BOM resultante y advertencia registrada. |

### CU-WO-05 · Operaciones y work orders

| Campo | Valor |
|---|---|
| Contexto / operación | WO / INSERT o UPDATE |
| Prioridad | P1 |
| Fixture | 05 y OP compartida |
| Precondiciones | Centros de trabajo disponibles |
| Datos clave | `processgroupcode`, `processgroupseq`, `idativ`, `allocgrpcode`, `activitycode`, `sequence`, `quantity`, `unitcode`, `resourcecode`, `resourcename` |
| Flujo principal | 1. Crear o actualizar `mrp.routing.workcenter`. 2. Generar `mrp.workorder` en la MO. 3. Asignar secuencia, cantidad y centro de trabajo. 4. Guardar `idativ` como referencia externa. |
| Alternativos / errores | Centro de trabajo inexistente; secuencia duplicada; `unitcode` no mapeada; operación sin `resourcecode`. |
| Postcondiciones | Work orders creadas y vinculadas a la MO. |
| Reglas | R14 |
| Criterios | Dada una operación con `idativ`, cuando se procesa, entonces se crea una work order con secuencia y centro de trabajo, y `idativ` queda trazable. |
| Evidencia | Work orders de la MO y vínculo `idativ`. |

### CU-WO-06 · Centros de trabajo, tiempos y mermas

| Campo | Valor |
|---|---|
| Contexto / operación | WO / INSERT o UPDATE |
| Prioridad | P2 |
| Fixture | OP compartida |
| Precondiciones | Centros de trabajo configurados |
| Datos clave | `resourcecode`, `resourcename`, `setuptime`, `totaltime`, `productiontime`, `setupwaste`, `productionwaste` |
| Flujo principal | 1. Resolver o crear el centro de trabajo por código. 2. Asignar tiempos de setup y producción. 3. Guardar mermas. |
| Alternativos / errores | Código de recurso inexistente; tiempos negativos; merma mayor a la cantidad. |
| Postcondiciones | Costos y tiempos de la MO disponibles. |
| Reglas | Mapeo WO |
| Criterios | Dado un `resourcecode` inexistente, cuando se procesa, entonces se crea el centro de trabajo o se informa error según la política definida. |
| Evidencia | Centros de trabajo y work orders. |

### CU-WO-07 · OP simple con un producto terminado

| Campo | Valor |
|---|---|
| Contexto / operación | WO / INSERT |
| Prioridad | P1 |
| Fixture | `05- OP WO.txt` |
| Precondiciones | Un PT, operaciones y BOM |
| Datos clave | `wonumber=OFC00001`, `sdilwofinisheditem.lcount=1`, `sdilwooperation.lcount=6` |
| Flujo principal | 1. Crear la MO. 2. Cargar BOM. 3. Generar work orders. 4. Confirmar la MO según `status`. |
| Alternativos / errores | Sin MP (`lcount=0`); sin operaciones; PT sin BOM. |
| Postcondiciones | MO simple lista para producir. |
| Reglas | R13, R14 |
| Criterios | Dada una OP con un PT, cuando se procesa, entonces se crea una sola MO con su BOM y sus work orders. |
| Evidencia | MO, BOM y work orders. |

### CU-WO-08 · OP compartida con múltiples productos terminados

| Campo | Valor |
|---|---|
| Contexto / operación | WO / INSERT |
| Prioridad | P1 |
| Fixture | `XML CON OP COMPARTIDA PROD. DIFERENTES.txt` |
| Precondiciones | Dos PT existentes; MP compartidas |
| Datos clave | `wonumber=OFC00008`, `sdilwofinisheditem.lcount=2` (`99.0002` y `99.0029`), `sdilworawmaterial.lcount=12`, `sdilwooperation.lcount=10`, `sdilwooutsourcing.lcount=2` |
| Flujo principal | 1. Crear una MO por cada PT. 2. Usar el mismo `wonumber` como origen. 3. Distribuir MP y costos por porcentaje. 4. Generar work orders en cada MO. 5. Vincular las MO entre sí por `wonumber`. |
| Alternativos / errores | Un PT sin BOM; cantidades desiguales; MP compartida sin criterio de reparto; work orders duplicadas. |
| Postcondiciones | Dos MO vinculadas, con MP y costos distribuidos. |
| Reglas | Decisión “una MO por PT” y “porcentual por cantidad planificada” |
| Criterios | Dada una OP con dos PT, cuando se procesa, entonces se crean dos MO con el mismo `wonumber` y la suma de MP asignadas equivale al total de la OP. |
| Evidencia | MO creadas, BOM de cada una y reporte de distribución. |

### CU-WO-09 · Cálculo del porcentaje por cantidad planificada

| Campo | Valor |
|---|---|
| Contexto / operación | WO / cálculo |
| Prioridad | P1 |
| Fixture | OP compartida |
| Precondiciones | Cantidades de cada PT |
| Datos clave | `quantity` de `sdiwofinisheditem` |
| Flujo principal | 1. Sumar las cantidades de todos los PT. 2. Calcular `% PT_i = quantity_i / suma`. 3. Aplicar el porcentaje a MP y costos compartidos. 4. Guardar el porcentaje usado. |
| Alternativos / errores | Suma cero; cantidad negativa; PT sin cantidad; porcentajes que no suman 100%. |
| Postcondiciones | Distribución porcentual documentada y auditable. |
| Reglas | Decisión de negocio aprobada |
| Criterios | Dados dos PT de 1.000.000 cada uno, cuando se calcula, entonces cada uno recibe 50%; dados 750.000 y 250.000, entonces reciben 75% y 25%. |
| Evidencia | Reporte de porcentajes y cantidades. |

### CU-WO-10 · Redondeo y residuo del porcentaje

| Campo | Valor |
|---|---|
| Contexto / operación | WO / cálculo |
| Prioridad | P2 |
| Fixture | OP compartida con cantidades no divisibles |
| Precondiciones | Distribución porcentual calculada |
| Datos clave | Porcentaje, decimales configurados, cantidad total de MP |
| Flujo principal | 1. Calcular porcentajes con decimales configurados. 2. Ajustar el último PT para absorber el residuo. 3. Verificar que la suma de asignaciones iguale el total. |
| Alternativos / errores | Residuo negativo; diferencia mayor a tolerancia; porcentaje 0%. |
| Postcondiciones | Asignaciones que suman exactamente el total. |
| Reglas | Decisión de negocio aprobada |
| Criterios | Dada una distribución con residuo, cuando se ajusta, entonces la suma de las MO iguala el total de la OP dentro de la tolerancia. |
| Evidencia | Reporte de asignación y diferencias. |

### CU-WO-11 · Tercerización como costo de la MO

| Campo | Valor |
|---|---|
| Contexto / operación | WO / INSERT |
| Prioridad | P2 |
| Fixture | OP compartida, nodo `sdiwooutsourcing` |
| Precondiciones | MO creada |
| Datos clave | `code=TERC TERM`, `title`, `quantity`, `unitcode`, `totalvalue`, `costaccountcode=2304`, `costaccountdescription`, `currency` |
| Flujo principal | 1. Leer la tercerización. 2. No crear subcontratación ni OC. 3. Registrar el costo en la MO o en el análisis de costos. 4. Distribuir por porcentaje si la OP es compartida. |
| Alternativos / errores | Moneda distinta; cuenta contable inexistente; valor cero; tercerización sin cantidad. |
| Postcondiciones | Costo de tercerización reflejado sin documento de compra. |
| Reglas | Decisión “solo costo” |
| Criterios | Dada una tercerización de 29.666,67, cuando se procesa, entonces el costo aparece en la MO y no se crea una OC ni una subcontratación. |
| Evidencia | Costo de la MO y ausencia de OC. |

### CU-WO-12 · Reserva y disponibilidad de componentes

| Campo | Valor |
|---|---|
| Contexto / operación | WO / confirmación |
| Prioridad | P2 |
| Fixture | 05 y OP compartida |
| Precondiciones | Stock de componentes |
| Datos clave | Componentes de la BOM, ubicación, cantidad |
| Flujo principal | 1. Confirmar la MO. 2. Reservar componentes disponibles. 3. Informar faltantes. 4. Permitir producir con faltante según política. |
| Alternativos / errores | Stock insuficiente; lote no disponible; ubicación sin stock; componente bloqueado. |
| Postcondiciones | Reservas creadas y faltantes visibles. |
| Reglas | Mapeo WO |
| Criterios | Dado un componente sin stock, cuando se confirma la MO, entonces el faltante queda visible y no se descuenta stock inexistente. |
| Evidencia | Reservas y reporte de faltantes. |

### CU-WO-13 · Consumo real por STK TType 0

| Campo | Valor |
|---|---|
| Contexto / operación | STK / INSERT, TType 0, operationtype 1 |
| Prioridad | P1 |
| Fixture | `11- Consumo de Material.txt` |
| Precondiciones | MO existente con `wonumber=OFC00001` y componente `02.01.0003` |
| Datos clave | `stockcode=02.01.0003`, `quantity=100`, `unitcode=FL`, `quantityunitcost=6.038`, `unitcostcode=KG`, `lot=00000017`, `wonumber=OFC00001` |
| Flujo principal | 1. Identificar la MO por `wonumber`. 2. Identificar el componente. 3. Descontar del lote indicado. 4. Registrar el consumo en la MO. 5. No duplicar si ya fue aplicado. |
| Alternativos / errores | MO inexistente; componente fuera de la BOM; lote inexistente; saldo insuficiente; consumo mayor al planificado. |
| Postcondiciones | Componente descontado y consumo reflejado en la MO. |
| Reglas | R11, R12 |
| Criterios | Dado un consumo de 100 FL, cuando se procesa, entonces se descuentan 6.038 KG del lote y la MO registra el consumo una sola vez. |
| Evidencia | Movimiento de stock y consumo de la MO. |

### CU-WO-14 · Conciliación con WIP

| Campo | Valor |
|---|---|
| Contexto / operación | WIP / exportación |
| Prioridad | P2 |
| Fixture | WIP y WIP_TR del manual 11.16–11.17 |
| Precondiciones | MO y consumos STK cargados |
| Datos clave | `ProcessID` ↔ `idativ`, `IdPalletLabel`, `TransactionType=17/18`, `QtyBefore`, `QtyAfter` |
| Flujo principal | 1. Leer WIP. 2. Vincular por `ProcessID` con `idativ` de la operación. 3. Comparar consumo WIP contra consumo STK. 4. Reportar diferencias. |
| Alternativos / errores | WIP sin `ProcessID`; etiqueta sin transacción; diferencia mayor a tolerancia; WIP no disponible. |
| Postcondiciones | Reporte de conciliación sin generar movimientos de stock. |
| Reglas | AGENTS.md; manual 11.16–11.17 |
| Criterios | Dado un WIP con `ProcessID` coincidente, cuando se concilia, entonces el consumo real se compara con el STK y las diferencias quedan reportadas. |
| Evidencia | Reporte de conciliación. |

### CU-WO-15 · Entrega de producción y cierre de MO

| Campo | Valor |
|---|---|
| Contexto / operación | STK / INSERT, TType 1 |
| Prioridad | P1 |
| Fixture | `13- Entrega de produccion.txt` |
| Precondiciones | MO existente y PT con lote |
| Datos clave | `stockcode=99.0001`, `quantity=50000`, `unitcode=UN`, `wonumber=OFC00001`, `lot=00000018`, `quantityunitcost=50000`, `unitcostcode=UN` |
| Flujo principal | 1. Identificar la MO. 2. Registrar la producción del PT. 3. Asignar lote. 4. Cerrar o actualizar la MO. 5. Evitar doble descuento con la finalización de la MO. |
| Alternativos / errores | MO inexistente; cantidad mayor a la planificada; lote duplicado; entrega ya registrada. |
| Postcondiciones | PT en stock y MO actualizada. |
| Reglas | R11, R12 |
| Criterios | Dada una entrega de 50.000 UN, cuando se procesa, entonces el PT ingresa con su lote y la MO refleja la cantidad producida una sola vez. |
| Evidencia | Movimiento de PT y estado de la MO. |

### CU-WO-16 · Vínculo entre pedido de venta y MO

| Campo | Valor |
|---|---|
| Contexto / operación | SOR / WO |
| Prioridad | P1 |
| Fixture | `06- Pedido de Venta.txt` y 05 |
| Precondiciones | Pedido y MO existentes |
| Datos clave | `saleordernumber=5Q-1`, `wonumber=OFC00001`, `quotenumber=5` |
| Flujo principal | 1. Leer la línea del pedido. 2. Buscar la MO por `wonumber`. 3. Vincular pedido, línea y MO. 4. Propagar cambios de cantidad o fecha según regla. |
| Alternativos / errores | MO inexistente; pedido sin `wonumber`; múltiples MO para un pedido; cambio de cantidad posterior. |
| Postcondiciones | Trazabilidad pedido → MO. |
| Reglas | R14; minuta funcional §2 |
| Criterios | Dada una línea con `wonumber`, cuando se procesa, entonces queda vinculada a la MO y al pedido. |
| Evidencia | Vínculo entre documentos. |

### CU-WO-17 · Modificación, cancelación y reproceso de MO

| Campo | Valor |
|---|---|
| Contexto / operación | WO / UPDATE o CANCEL |
| Prioridad | P2 |
| Fixture | 05 con cambios y `status=4` |
| Precondiciones | MO existente |
| Datos clave | `wonumber`, `status`, `quantity`, `deliverydt` |
| Flujo principal | 1. Buscar la MO por `wonumber`. 2. Actualizar cantidades, fechas u operaciones. 3. Cancelar si `status=4`. 4. Registrar el motivo. |
| Alternativos / errores | MO ya cerrada; MO con consumo; cancelación con PT entregado; reproceso duplicado. |
| Postcondiciones | MO actualizada o cancelada sin duplicar movimientos. |
| Reglas | R13 |
| Criterios | Dado `status=4`, cuando se procesa, entonces la MO se cancela o se marca según la regla, sin borrar el historial. |
| Evidencia | Estado de la MO y bitácora. |

### CU-WO-18 · Costeo promedio y valorización

| Campo | Valor |
|---|---|
| Contexto / operación | WO / costos |
| Prioridad | P2 |
| Fixture | 05 y OP compartida |
| Precondiciones | Costos de componentes y método promedio |
| Datos clave | Costo de MP, costo de operaciones, tercerización, costo del PT |
| Flujo principal | 1. Calcular el costo de la MO con costo promedio. 2. Incluir operaciones y tercerización. 3. Distribuir por porcentaje en OP compartida. 4. Comparar con el valor de Metrics. |
| Alternativos / errores | Componente sin costo; moneda distinta; diferencia con Metrics; costo negativo. |
| Postcondiciones | Costo de la MO y del PT calculados. |
| Reglas | Minuta funcional §3; decisión de costo promedio |
| Criterios | Dada una MO con componentes y tercerización, cuando se valora, entonces el costo incluye ambos conceptos y queda disponible para comparar con Metrics. |
| Evidencia | Reporte de costos de la MO. |

### CU-WO-19 · Errores de estructura de la OP

| Campo | Valor |
|---|---|
| Contexto / operación | WO / INSERT |
| Prioridad | P3 |
| Fixture | Variantes de 05 y OP compartida |
| Precondiciones | Datos incompletos o inconsistentes |
| Datos clave | PT sin BOM, componente inexistente, operación sin centro, `stockcode` vacío, cantidades inconsistentes |
| Flujo principal | 1. Validar PT, BOM, componentes, operaciones y cantidades. 2. Detener ante el primer error crítico. 3. Informar el campo y el valor. 4. No crear la MO. |
| Alternativos / errores | Error parcial; MO creada sin BOM; operación sin work order; ciclo de BOM. |
| Postcondiciones | Sin MO parcial; error accionable. |
| Reglas | R13, R14 |
| Criterios | Dado un PT sin BOM, cuando se procesa, entonces la MO no se crea y la bitácora informa el faltante. |
| Evidencia | Bitácora y ausencia de MO. |

### CU-WO-20 · Consumibles no medibles por centro de costo

| Campo | Valor |
|---|---|
| Contexto / operación | WO / costos |
| Prioridad | P2 |
| Fixture | Variante de 05 con tintas y pegamentos |
| Precondiciones | Centro de costo configurado |
| Datos clave | `materialtype=1` (tintas), consumibles no medibles |
| Flujo principal | 1. Detectar consumible no medible. 2. No incluirlo como componente de la MO. 3. Cargar el consumo contra el centro de costo. 4. Mantenerlo fuera del costo directo de la OP. |
| Alternativos / errores | Consumible medible; centro de costo inexistente; doble imputación. |
| Postcondiciones | Consumible imputado al centro de costo y no a la MO. |
| Reglas | Minuta funcional §7 |
| Criterios | Dada una tinta no medible, cuando se procesa, entonces no se crea línea de BOM y el costo va al centro de costo. |
| Evidencia | Asiento o reporte de centro de costo y BOM sin la tinta. |

### CU-WO-21 · BOM multinivel y producto intermedio

| Campo | Valor |
|---|---|
| Contexto / operación | WO / INSERT |
| Prioridad | P2 |
| Fixture | Pendiente: muestra con BOM multinivel |
| Precondiciones | Producto intermedio con BOM propia |
| Datos clave | PT, producto intermedio, MP, `idativ` |
| Flujo principal | 1. Detectar producto intermedio. 2. Crear o actualizar su BOM. 3. Vincular la BOM del PT con la del intermedio. 4. Validar explosión de materiales. |
| Alternativos / errores | Intermedio sin BOM; ciclo; cantidades inconsistentes; costo duplicado. |
| Postcondiciones | BOM multinivel consistente. |
| Reglas | Decisión “ambos alimentan la BOM” |
| Criterios | Dado un PT con producto intermedio, cuando se procesa, entonces la explosión de materiales incluye ambos niveles sin ciclos. |
| Evidencia | Árbol de BOM y reporte de explosión. |

---

## 7. Casos de pedidos de venta (`CU-SOR`)

### CU-SOR-01 · Alta de pedido de venta desde cotización aprobada

| Campo | Valor |
|---|---|
| Contexto / operación | SOR / INSERT |
| Prioridad | P1 |
| Fixture | `06- Pedido de Venta.txt` |
| Precondiciones | Cliente y producto existentes |
| Datos clave | `saleordernumber=5Q-1`, `status=2`, `customerorderid`, `quotationdt`, `duedt`, `idcurrency=1`, `exchangerate=1` |
| Flujo principal | 1. Crear `sale.order`. 2. Asignar cliente, moneda y fechas. 3. Crear líneas. 4. Confirmar según `status`. |
| Alternativos / errores | Cliente inexistente; producto inexistente; pedido duplicado; cotización no aprobada. |
| Postcondiciones | Pedido creado con sus líneas y estado. |
| Reglas | R15 |
| Criterios | Dado un pedido con `status=2`, cuando se procesa, entonces se crea el pedido confirmado con cliente, moneda y líneas correctas. |
| Evidencia | Pedido y bitácora. |

### CU-SOR-02 · Líneas con orden de producción y cotización

| Campo | Valor |
|---|---|
| Contexto / operación | SOR / INSERT |
| Prioridad | P1 |
| Fixture | 06 |
| Precondiciones | MO y cotización existentes |
| Datos clave | `stockcode=99.0001`, `quantity=100000`, `unitvalue=0.0254`, `totalvalue=2540`, `unitcode=UN`, `wonumber=OFC00001`, `quotenumber=5`, `itemmarkuprate=9.88` |
| Flujo principal | 1. Crear `sale.order.line`. 2. Asignar producto, cantidad, precio y UOM. 3. Guardar `wonumber` y `quotenumber` como referencias. 4. Validar total de línea. |
| Alternativos / errores | Producto sin precio; cantidad cero; `wonumber` inexistente; total de línea distinto a cantidad por precio. |
| Postcondiciones | Línea vinculada a la OP y a la cotización. |
| Reglas | R15; minuta funcional §2 |
| Criterios | Dada una línea de 100.000 UN a 0,0254, cuando se procesa, entonces el total es 2.540 y queda vinculada a `OFC00001`. |
| Evidencia | Línea del pedido y vínculo con la MO. |

### CU-SOR-03 · Condición de pago y vencimientos

| Campo | Valor |
|---|---|
| Contexto / operación | SOR / INSERT o UPDATE |
| Prioridad | P2 |
| Fixture | 06 |
| Precondiciones | Términos de pago disponibles |
| Datos clave | `conditioncode=Al contado`, `duedate=2026-07-24`, `value=2540` |
| Flujo principal | 1. Buscar o crear el término de pago. 2. Asignarlo al pedido. 3. Guardar vencimientos informados. 4. Comparar con el cálculo de Odoo. |
| Alternativos / errores | Término inexistente; vencimiento distinto; múltiples vencimientos. |
| Postcondiciones | Término y vencimientos asignados. |
| Reglas | HU-06 |
| Criterios | Dado un pedido “Al contado” con vencimiento, cuando se procesa, entonces el término y el vencimiento quedan registrados y se muestra cualquier diferencia. |
| Evidencia | Pedido y vencimientos. |

### CU-SOR-04 · Moneda y tipo de cambio

| Campo | Valor |
|---|---|
| Contexto / operación | SOR / INSERT o UPDATE |
| Prioridad | P2 |
| Fixture | 06 |
| Precondiciones | Monedas y tasas configuradas |
| Datos clave | `idcurrency=1`, `exchangerate=1`, `unitvalue`, `totalvalue` |
| Flujo principal | 1. Resolver la moneda. 2. Asignar la tasa. 3. Guardar importes en moneda del pedido y en moneda de la empresa. |
| Alternativos / errores | Moneda desconocida; tasa cero; tasa desactualizada; fecha de tasa distinta. |
| Postcondiciones | Importes coherentes en ambas monedas. |
| Reglas | HU-07; decisión multimoneda |
| Criterios | Dado un pedido en moneda extranjera, cuando se procesa, entonces se conservan los importes originales y su equivalente en moneda de la empresa. |
| Evidencia | Pedido y tabla de tasas. |

### CU-SOR-05 · Entregas parciales y direcciones

| Campo | Valor |
|---|---|
| Contexto / operación | SOR / INSERT o UPDATE |
| Prioridad | P2 |
| Fixture | 06, nodo `sdisoritemdelivery` |
| Precondiciones | Cliente con direcciones |
| Datos clave | `deliverydt`, `deliveryqty=100000`, `billing=1`, `delivery=1`, `status=0`, `address`, `carriercode` |
| Flujo principal | 1. Leer entregas de la línea. 2. Guardar fecha, cantidad y estado. 3. Asociar dirección de entrega. 4. Asociar transportista si existe. |
| Alternativos / errores | Cantidad entregada mayor a la pedida; múltiples entregas; dirección inexistente; transportista inexistente. |
| Postcondiciones | Entregas planificadas y direcciones vinculadas. |
| Reglas | R19; minuta funcional §8 |
| Criterios | Dada una entrega parcial de 100.000, cuando se procesa, entonces queda registrada con su fecha y dirección sin modificar la cantidad pedida. |
| Evidencia | Líneas de entrega y direcciones. |

### CU-SOR-06 · Estados del pedido de venta

| Campo | Valor |
|---|---|
| Contexto / operación | SOR / INSERT o UPDATE |
| Prioridad | P2 |
| Fixture | 06 y variantes de `status` 0–5 |
| Precondiciones | Pedido existente |
| Datos clave | `status` |
| Flujo principal | 1. Mapear `0/1 → draft`. 2. Mapear `2 → sale`. 3. Mapear `3 → sent`. 4. Mapear `4 → done`. 5. Mapear `5 → cancel`. |
| Alternativos / errores | Estado desconocido; transición inválida; pedido cancelado con entregas. |
| Postcondiciones | Estado del pedido coherente. |
| Reglas | R15 |
| Criterios | Dado `status=5`, cuando se procesa, entonces el pedido queda cancelado sin borrar el historial. |
| Evidencia | Estado del pedido y bitácora. |

### CU-SOR-07 · Modificación y cancelación

| Campo | Valor |
|---|---|
| Contexto / operación | SOR / UPDATE o CANCEL |
| Prioridad | P2 |
| Fixture | 06 con cambios |
| Precondiciones | Pedido existente |
| Datos clave | `saleordernumber`, `quantity`, `unitvalue`, `status` |
| Flujo principal | 1. Buscar pedido por número. 2. Actualizar líneas y fechas. 3. Cancelar si corresponde. 4. No duplicar líneas. |
| Alternativos / errores | Pedido facturado; pedido con entrega; línea eliminada; cambio de cliente. |
| Postcondiciones | Pedido actualizado o cancelado. |
| Reglas | R15 |
| Criterios | Dado un pedido existente, cuando llega un UPDATE, entonces se actualizan sus líneas y no se crea un pedido nuevo. |
| Evidencia | Comparación antes/después. |

### CU-SOR-08 · Error por cliente o producto inexistente

| Campo | Valor |
|---|---|
| Contexto / operación | SOR / INSERT |
| Prioridad | P3 |
| Fixture | Variante de 06 con `code=999` o `stockcode=ZZ` |
| Precondiciones | Maestro faltante |
| Datos clave | `sdisorcustomerinfo.code`, `stockcode` |
| Flujo principal | 1. Resolver cliente y producto. 2. Detectar faltante. 3. Fallar la transacción. 4. No crear pedido ni línea. |
| Alternativos / errores | Cliente inactivo; producto archivado; moneda no disponible. |
| Postcondiciones | Sin pedido parcial; error accionable. |
| Reglas | HU-04 |
| Criterios | Dado un cliente inexistente, cuando se procesa, entonces no se crea el pedido y la bitácora informa el código faltante. |
| Evidencia | Bitácora y ausencia de pedido. |

### CU-SOR-09 · Disparo de la orden de producción

| Campo | Valor |
|---|---|
| Contexto / operación | SOR → WO |
| Prioridad | P1 |
| Fixture | 06 y 05 |
| Precondiciones | Pedido confirmado y producto con BOM |
| Datos clave | `saleordernumber=5Q-1`, `wonumber=OFC00001`, `stockcode=99.0001` |
| Flujo principal | 1. Confirmar el pedido. 2. Detectar líneas que requieren producción. 3. Crear o vincular la MO por `wonumber`. 4. No duplicar si la MO ya existe. |
| Alternativos / errores | Producto sin BOM; MO existente; pedido sin `wonumber`; producto de compra. |
| Postcondiciones | Pedido y MO vinculados. |
| Reglas | Minuta funcional §2; R14 |
| Criterios | Dado un pedido confirmado con `wonumber`, cuando se procesa, entonces la MO queda vinculada y no se genera una segunda orden. |
| Evidencia | Pedido, MO y bitácora. |

---

## 8. Casos de órdenes de compra (`CU-POR`)

### CU-POR-01 · Alta de orden de compra nacional

| Campo | Valor |
|---|---|
| Contexto / operación | POR / INSERT |
| Prioridad | P1 |
| Fixture | `07- Orden de Compra.txt` |
| Precondiciones | Proveedor y producto existentes |
| Datos clave | `purchaseordernumber=1`, `suppliercode=329`, `emissiondt`, `idcurrency=1`, `situation=1`, `status=0`, `stockcode=02.01.0003`, `quantity=3623.04`, `unitvalue=2900`, `totalvalue=10506816` |
| Flujo principal | 1. Crear `purchase.order`. 2. Asignar proveedor, moneda y fechas. 3. Crear líneas con producto, cantidad y precio. 4. Guardar número de OC como referencia única. |
| Alternativos / errores | Proveedor inexistente; producto inexistente; OC duplicada; moneda desconocida. |
| Postcondiciones | OC creada y disponible para recepción. |
| Reglas | HU-05; RN-02, RN-03 |
| Criterios | Dada una OC con una línea de 3.623,04 KG a 2.900, cuando se procesa, entonces el total de línea es 10.506.816 y la OC queda vinculada al proveedor. |
| Evidencia | OC y bitácora. |

### CU-POR-02 · Orden de compra en moneda extranjera

| Campo | Valor |
|---|---|
| Contexto / operación | POR / INSERT o UPDATE |
| Prioridad | P1 |
| Fixture | 07 |
| Precondiciones | Moneda y tasa disponibles |
| Datos clave | `idcurrency=2`, `exchangerate=1450`, `exchangeratedt`, `unitvalue_foreigncurrency=2`, `totalvalue_foreigncurrency=7246.08` |
| Flujo principal | 1. Resolver moneda extranjera. 2. Guardar importes en moneda extranjera. 3. Aplicar tasa y guardar equivalente en moneda de la empresa. 4. Guardar fecha de tasa. |
| Alternativos / errores | Moneda sin tabla; tasa ausente; diferencia de redondeo; fecha de tasa inválida. |
| Postcondiciones | Importes bimonedas consistentes. |
| Reglas | HU-07; RN-12, RN-13 |
| Criterios | Dado un valor unitario de 2 USD con tasa 1.450, cuando se procesa, entonces el valor en moneda de la empresa es 2.900 por KG. |
| Evidencia | Línea de OC en ambas monedas. |

### CU-POR-03 · Condición de pago y vencimientos

| Campo | Valor |
|---|---|
| Contexto / operación | POR / INSERT o UPDATE |
| Prioridad | P2 |
| Fixture | 07 |
| Precondiciones | Términos de pago disponibles |
| Datos clave | `conditioncode=45 dias`, `duedate=2026-09-14`, `value=12713247.36` |
| Flujo principal | 1. Buscar el término por nombre. 2. Crearlo si no existe. 3. Guardar vencimientos informados. 4. Comparar con el cálculo de Odoo. |
| Alternativos / errores | Término inexistente; regla de vencimiento no definida; múltiples vencimientos. |
| Postcondiciones | Término y vencimientos asignados. |
| Reglas | HU-06 |
| Criterios | Dada una condición “45 dias”, cuando se procesa, entonces se crea o reutiliza el término y se guarda el vencimiento informado. |
| Evidencia | OC y vencimientos. |

### CU-POR-04 · Actualización de OC y control de duplicados

| Campo | Valor |
|---|---|
| Contexto / operación | POR / UPDATE |
| Prioridad | P1 |
| Fixture | 07 procesado dos veces con cambios |
| Precondiciones | OC existente por `purchaseordernumber` |
| Datos clave | `purchaseordernumber`, `suppliercode`, `quantity`, `unitvalue`, `status` |
| Flujo principal | 1. Buscar la OC por número. 2. Actualizar cabecera y líneas. 3. Mantener una sola OC. 4. No duplicar líneas. |
| Alternativos / errores | OC con factura; línea ya facturada; cambio de proveedor; OC inexistente. |
| Postcondiciones | OC actualizada sin duplicados. |
| Reglas | HU-05; RN-04 |
| Criterios | Dada una OC ya existente, cuando llega un INSERT repetido, entonces se actualiza y no se crea una segunda OC. |
| Evidencia | Conteo de OC y comparación de líneas. |

### CU-POR-05 · Anulación o eliminación de OC

| Campo | Valor |
|---|---|
| Contexto / operación | POR / DELETE o CANCEL |
| Prioridad | P2 |
| Fixture | Variante de 07 con operación DELETE |
| Precondiciones | OC existente |
| Datos clave | `purchaseordernumber`, `status` |
| Flujo principal | 1. Buscar la OC. 2. Verificar que no tenga recepciones ni facturas. 3. Cancelar o eliminar según la regla. 4. Registrar el motivo. |
| Alternativos / errores | OC con recepción; OC facturada; OC ya cancelada. |
| Postcondiciones | OC anulada sin romper documentos vinculados. |
| Reglas | HU-05 |
| Criterios | Dada una OC sin documentos vinculados, cuando se anula, entonces queda cancelada o eliminada según la política definida. |
| Evidencia | Estado de la OC y bitácora. |

### CU-POR-06 · Orden de compra no aprobada

| Campo | Valor |
|---|---|
| Contexto / operación | POR / INSERT |
| Prioridad | P2 |
| Fixture | Variante de 07 con `situation=0` |
| Precondiciones | Regla de negocio definida |
| Datos clave | `situation` (0 no aprobada, 1 aprobada, 2 rechazada, 3 en aprobación) |
| Flujo principal | 1. Leer `situation`. 2. Si no está aprobada, no crear o crear en borrador según la política. 3. Registrar la decisión. |
| Alternativos / errores | OC rechazada; OC en aprobación; OC aprobada posteriormente. |
| Postcondiciones | OC coherente con la decisión de negocio. |
| Reglas | HU-05 |
| Criterios | Dada una OC no aprobada, cuando se procesa, entonces se aplica la política definida y no se crea una OC operativa. |
| Evidencia | Estado de la OC y bitácora. |

### CU-POR-07 · OC de solo lectura en Odoo

| Campo | Valor |
|---|---|
| Contexto / operación | POR / control de acceso |
| Prioridad | P1 |
| Fixture | 07 |
| Precondiciones | Usuario estándar y usuario bot |
| Datos clave | Permisos de `purchase.order` |
| Flujo principal | 1. Crear la OC con el bot. 2. Ingresar con usuario estándar. 3. Verificar que no puede editar ni eliminar. 4. Verificar que el bot sí puede modificar. |
| Alternativos / errores | Usuario administrador; permisos heredados; edición por importación. |
| Postcondiciones | OC de solo lectura para usuarios funcionales. |
| Reglas | Regla de negocio 1; resumen de compras |
| Criterios | Dado un usuario funcional, cuando abre la OC, entonces puede verla pero no editarla ni eliminarla. |
| Evidencia | Prueba de permisos. |

### CU-POR-08 · Error por proveedor, producto o moneda inexistente

| Campo | Valor |
|---|---|
| Contexto / operación | POR / INSERT |
| Prioridad | P3 |
| Fixture | Variante de 07 con `suppliercode=999` |
| Precondiciones | Maestro faltante |
| Datos clave | `suppliercode`, `stockcode`, `idcurrency` |
| Flujo principal | 1. Resolver los maestros. 2. Detectar el faltante. 3. Fallar la transacción. 4. No crear la OC. |
| Alternativos / errores | Proveedor inactivo; producto archivado; moneda no configurada. |
| Postcondiciones | Sin OC parcial; error accionable. |
| Reglas | HU-04; RN-08 |
| Criterios | Dado un proveedor inexistente, cuando se procesa, entonces la OC no se crea y la bitácora informa el código. |
| Evidencia | Bitácora y ausencia de OC. |

### CU-POR-09 · Impuestos y total de cabecera

| Campo | Valor |
|---|---|
| Contexto / operación | POR / validación |
| Prioridad | P2 |
| Fixture | 07 |
| Precondiciones | Impuestos configurados |
| Datos clave | `totalvalue=12713247.36`, total de línea `10506816` |
| Flujo principal | 1. Sumar líneas sin impuestos. 2. Calcular impuestos. 3. Comparar con el total de cabecera. 4. Informar diferencia si supera la tolerancia. |
| Alternativos / errores | Total de cabecera con IVA; total sin impuestos; diferencia por redondeo. |
| Postcondiciones | Totales conciliados y diferencia visible. |
| Reglas | HU-05; regla de base sin impuestos |
| Criterios | Dado un total de cabecera de 12.713.247,36 y una base de 10.506.816, cuando se valida, entonces la diferencia corresponde al 21% y queda documentada. |
| Evidencia | Reporte de conciliación de totales. |

---

## 9. Casos de remitos de compra (`CU-REC`)

### CU-REC-01 · Alta de remito vinculado a OC

| Campo | Valor |
|---|---|
| Contexto / operación | REC / INSERT |
| Prioridad | P1 |
| Fixture | `08- Recepcion de Material por Remito.txt` |
| Precondiciones | OC existente y proveedor configurado |
| Datos clave | `providercode=329`, `receiptserie=1`, `receiptnumber=12132`, `receiptdate`, `paycondition`, `receiptcurrencycode=1` |
| Flujo principal | 1. Crear recepción en borrador. 2. Asociar proveedor y OC. 3. Guardar serie, número y fecha. 4. Guardar condición de pago y moneda. |
| Alternativos / errores | OC inexistente; remito duplicado; proveedor inexistente; serie vacía. |
| Postcondiciones | Recepción en borrador vinculada a la OC. |
| Reglas | RR-01, RR-02; HU-08 |
| Criterios | Dado un remito con proveedor, serie y número, cuando se procesa, entonces se crea una recepción en borrador vinculada a la OC. |
| Evidencia | Recepción y vínculo con la OC. |

### CU-REC-02 · Actualización de remito

| Campo | Valor |
|---|---|
| Contexto / operación | REC / UPDATE |
| Prioridad | P2 |
| Fixture | 08 procesado con cambios |
| Precondiciones | Remito existente |
| Datos clave | `providercode`, `receiptserie`, `receiptnumber`, `receiptdate` |
| Flujo principal | 1. Buscar remito por proveedor + serie + número. 2. Actualizar datos. 3. No duplicar. |
| Alternativos / errores | Remito validado; remito con ingreso; cambio de proveedor. |
| Postcondiciones | Remito actualizado. |
| Reglas | RR-01; HU-08 |
| Criterios | Dado un remito existente, cuando llega un UPDATE, entonces se actualiza el mismo documento. |
| Evidencia | Comparación antes/después. |

### CU-REC-03 · Cancelación de remito

| Campo | Valor |
|---|---|
| Contexto / operación | REC / CANCEL |
| Prioridad | P2 |
| Fixture | Variante CANCEL de 08 |
| Precondiciones | Remito existente |
| Datos clave | `receiptserie`, `receiptnumber`, `providercode` |
| Flujo principal | 1. Buscar remito. 2. Verificar ingresos asociados. 3. Cancelar la recepción. 4. Revertir stock si corresponde. |
| Alternativos / errores | Remito con material consumido; remito ya validado; ingreso sin reversión. |
| Postcondiciones | Remito cancelado y stock consistente. |
| Reglas | RR-08; HU-08 |
| Criterios | Dado un remito sin consumo posterior, cuando se cancela, entonces la recepción y el stock se revierten. |
| Evidencia | Estado de la recepción y stock. |

### CU-REC-04 · Control de remito duplicado

| Campo | Valor |
|---|---|
| Contexto / operación | REC / INSERT |
| Prioridad | P1 |
| Fixture | 08 procesado dos veces |
| Precondiciones | Remito existente |
| Datos clave | `providercode`, `receiptserie`, `receiptnumber` |
| Flujo principal | 1. Buscar por la clave compuesta. 2. Si existe, no crear otro. 3. Actualizar o ignorar según operación. |
| Alternativos / errores | Mismo número con distinta serie; mismo número con distinto proveedor; número vacío. |
| Postcondiciones | Un solo remito por clave. |
| Reglas | RR-01; HU-08 |
| Criterios | Dado un remito ya registrado, cuando vuelve a llegar, entonces no se duplica. |
| Evidencia | Conteo de remitos. |

### CU-REC-05 · Orden invertido entre STK y REC

| Campo | Valor |
|---|---|
| Contexto / operación | STK / INSERT con dependencia |
| Prioridad | P1 |
| Fixture | 09 procesado antes que 08 |
| Precondiciones | Cola de reintentos |
| Datos clave | `docnumber=12132` en STK; `receiptnumber=12132` en REC |
| Flujo principal | 1. Detectar que el remito no existe. 2. Encolar reintento. 3. Procesar el REC cuando llegue. 4. Reintentar el STK. |
| Alternativos / errores | Reintento agotado; remito nunca llega; número de remito distinto. |
| Postcondiciones | El ingreso se aplica una vez que existe el remito. |
| Reglas | RR-04; HU-02 |
| Criterios | Dado un STK que llega antes que su REC, cuando se reintenta, entonces espera y luego se aplica sin duplicar. |
| Evidencia | Log de reintentos y estado final. |

### CU-REC-06 · Remito con ítems (muestra pendiente)

| Campo | Valor |
|---|---|
| Contexto / operación | REC / INSERT |
| Prioridad | P3 |
| Fixture | `08` (ítem vacío) |
| Precondiciones | Muestra con `sdiprovideritemreceipt` poblado |
| Datos clave | Ítems, OC atendidas, cantidad, valor, unidad |
| Flujo principal | 1. Validar que el XML traiga ítems. 2. Vincular cada ítem a la línea de OC. 3. Guardar cantidades y valores. |
| Alternativos / errores | XML sin ítems; ítem sin OC; cantidad que excede la OC; unidad distinta. |
| Postcondiciones | Recepción con líneas vinculadas a la OC. |
| Reglas | HU-08 |
| Criterios | Dado un remito con ítems, cuando se procesa, entonces cada línea queda vinculada a su OC; mientras no exista la muestra, el caso queda bloqueado. |
| Evidencia | Recepción con líneas y OC. |

---

## 10. Casos de movimientos de stock (`CU-STK`)

> **Referencias de TransactionType:** 0 atención/devolución de solicitud de MP, 1 entrega de producción, 2 compras, 3 ventas, 4 inventario, 5 transferencia entre ítems, 6 volúmenes, 7 transferencia entre empresas, 8 transferencia, 9 ajuste de saldo, 10 otro.  
> **OperationType:** 0 entrada, 1 salida.  
> **Nota:** la semántica de `stockmovementtype` en las muestras no coincide con R12. Ver CU-STK-31.

### CU-STK-01 · Ingreso de material por compra

| Campo | Valor |
|---|---|
| Contexto / operación | STK / INSERT, TType 2, operationtype 0 |
| Prioridad | P1 |
| Fixture | `09- Ingreso de Material por compra.txt` |
| Precondiciones | OC y remito existentes; producto y ubicación configurados |
| Datos clave | `transactiontype=2`, `operationtype=0`, `stockcode=02.01.0003`, `quantity=60000`, `unitcode=FL`, `quantityunitcost=3623.04`, `unitcostcode=KG`, `totalvalue=10506815.98`, `lot=00000017` |
| Flujo principal | 1. Crear movimiento de entrada. 2. Asignar producto, cantidad en KG y valor. 3. Asignar lote y ubicación. 4. Validar la recepción. |
| Alternativos / errores | Producto inexistente; ubicación inválida; cantidad cero; remito inexistente; lote duplicado. |
| Postcondiciones | Stock incrementado con lote y valor. |
| Reglas | R11, R12; HU-09 |
| Criterios | Dado un ingreso de 60.000 FL equivalentes a 3.623,04 KG, cuando se procesa, entonces el stock sube 3.623,04 KG en el lote indicado. |
| Evidencia | Movimiento de stock y ficha del lote. |

### CU-STK-02 · Lote, lote de proveedor, fechas y ubicación

| Campo | Valor |
|---|---|
| Contexto / operación | STK / INSERT |
| Prioridad | P1 |
| Fixture | 09 |
| Precondiciones | Producto con tracking por lote |
| Datos clave | `lot=00000017`, `providerlot=41654654`, `productiondate=2026-06-15`, `expirationdate=2027-06-15`, `stockplacecode=PADRON`, `stockaddress=UNICO` |
| Flujo principal | 1. Crear o reutilizar el lote. 2. Guardar lote de proveedor. 3. Guardar fechas de producción y vencimiento. 4. Asignar ubicación. |
| Alternativos / errores | Lote inexistente; lote ya usado con otro producto; vencimiento anterior a producción; ubicación inexistente. |
| Postcondiciones | Lote con trazabilidad completa. |
| Reglas | HU-09; RR-02 |
| Criterios | Dado un lote con fechas y ubicación, cuando se procesa, entonces la trazabilidad queda completa y disponible para consumo. |
| Evidencia | Ficha del lote y ubicación. |

### CU-STK-03 · Conversión FL a KG

| Campo | Valor |
|---|---|
| Contexto / operación | STK / INSERT |
| Prioridad | P1 |
| Fixture | 09 y 11 |
| Precondiciones | Factor FL→KG definido para el producto |
| Datos clave | `quantity=60000`, `unitcode=FL`, `quantityunitcost=3623.04`, `unitcostcode=KG`; consumo `quantity=100`, `quantityunitcost=6.038` |
| Flujo principal | 1. Usar `quantityunitcost` como cantidad de stock. 2. Guardar `quantity` y `unitcode` como dato original. 3. Validar factor por producto. |
| Alternativos / errores | Factor ausente; redondeo distinto; unidad de costo distinta a KG; cantidad original cero. |
| Postcondiciones | Stock en KG y cantidad original conservada. |
| Reglas | R01; HU-10 |
| Criterios | Dado un ingreso de 60.000 FL y 3.623,04 KG, cuando se procesa, entonces el stock queda en KG y la cantidad original en FL se conserva. |
| Evidencia | Movimiento y conversión aplicada. |

### CU-STK-04 · Vínculo con remito y orden de compra

| Campo | Valor |
|---|---|
| Contexto / operación | STK / INSERT |
| Prioridad | P1 |
| Fixture | 09 y 08 |
| Precondiciones | Remito y OC existentes |
| Datos clave | `docnumber=12132`, `docnumbercompl=329`, `stockmovementtype=2` |
| Flujo principal | 1. Buscar el remito por `docnumber`. 2. Vincular el movimiento a la recepción. 3. Vincular la recepción a la OC. 4. Guardar la referencia. |
| Alternativos / errores | `docnumber` vacío; remito inexistente; `docnumbercompl` no corresponde al proveedor; múltiples OC. |
| Postcondiciones | Movimiento vinculado a remito y OC. |
| Reglas | HU-09; RR-04 |
| Criterios | Dado un ingreso con `docnumber=12132`, cuando se procesa, entonces queda vinculado al remito 12132 y a su OC. |
| Evidencia | Vínculo entre documentos. |

### CU-STK-05 · Valor de ingreso como base del ajuste

| Campo | Valor |
|---|---|
| Contexto / operación | STK / INSERT |
| Prioridad | P1 |
| Fixture | 09 y 10 |
| Precondiciones | Ingreso validado |
| Datos clave | `totalvalue=10506815.98` (ingreso), `totalvalue=50000` (ajuste) |
| Flujo principal | 1. Guardar el valor del ingreso. 2. Usarlo como base para el ajuste por factura. 3. Registrar la referencia de la recepción. |
| Alternativos / errores | Valor cero; valor distinto al de la OC; múltiples ingresos para la misma recepción. |
| Postcondiciones | Base de ajuste disponible y trazable. |
| Reglas | HU-13 |
| Criterios | Dado un ingreso de 10.506.815,98, cuando se calcula el ajuste, entonces se usa ese valor como base. |
| Evidencia | Valor del movimiento y cálculo del ajuste. |

### CU-STK-06 · Cancelación de ingreso

| Campo | Valor |
|---|---|
| Contexto / operación | STK / CANCEL, TType 2 |
| Prioridad | P2 |
| Fixture | Variante CANCEL de 09 |
| Precondiciones | Ingreso existente |
| Datos clave | `transactioncodeextref`, `lot`, `quantityunitcost` |
| Flujo principal | 1. Buscar el movimiento original. 2. Verificar que no haya consumo posterior. 3. Revertir el stock. 4. Registrar la cancelación. |
| Alternativos / errores | Lote consumido; lote transferido; movimiento ya cancelado; valor ya ajustado. |
| Postcondiciones | Stock revertido y trazabilidad conservada. |
| Reglas | HU-09 |
| Criterios | Dado un ingreso sin consumo posterior, cuando se cancela, entonces el stock vuelve al valor anterior; si hay consumo, entonces falla con mensaje. |
| Evidencia | Movimiento de reversión y bitácora. |

### CU-STK-07 · Error por lote o ubicación inválidos

| Campo | Valor |
|---|---|
| Contexto / operación | STK / INSERT |
| Prioridad | P3 |
| Fixture | Variante de 09 con `lot` inexistente o `stockplacecode=ZZ` |
| Precondiciones | Lote o ubicación no configurados |
| Datos clave | `lot`, `stockplacecode`, `stockaddress` |
| Flujo principal | 1. Resolver lote y ubicación. 2. Detectar faltante. 3. Fallar la transacción. 4. No mover stock. |
| Alternativos / errores | Lote de otro producto; ubicación inactiva; dirección de stock inválida. |
| Postcondiciones | Sin movimiento parcial; error accionable. |
| Reglas | HU-04; HU-09 |
| Criterios | Dada una ubicación inexistente, cuando se procesa, entonces no se crea el movimiento y se informa el código. |
| Evidencia | Bitácora y ausencia de movimiento. |

### CU-STK-08 · Residuo de redondeo FL a KG

| Campo | Valor |
|---|---|
| Contexto / operación | STK / conciliación |
| Prioridad | P3 |
| Fixture | 09 y 11 en tandas de 100 FL |
| Precondiciones | Factor FL→KG definido |
| Datos clave | 60.000 FL → 3.623,04 KG; 600 consumos de 100 FL → 6,038 KG cada uno |
| Flujo principal | 1. Sumar los consumos redondeados. 2. Comparar con el ingreso. 3. Reportar la diferencia. 4. Aplicar la política de residuo definida. |
| Alternativos / errores | Diferencia acumulada; ajuste por residuo; consumo total mayor al ingreso. |
| Postcondiciones | Diferencia documentada y tratada. |
| Reglas | HU-10 |
| Criterios | Dados 600 consumos de 6,038 KG, cuando se concilia, entonces la diferencia contra 3.623,04 KG queda reportada y se aplica la política acordada. |
| Evidencia | Reporte de conciliación. |

### CU-STK-09 · Consumo de material

| Campo | Valor |
|---|---|
| Contexto / operación | STK / INSERT, TType 0, operationtype 1 |
| Prioridad | P1 |
| Fixture | `11- Consumo de Material.txt` |
| Precondiciones | MO existente; lote con saldo |
| Datos clave | `transactiontype=0`, `operationtype=1`, `stockcode=02.01.0003`, `quantity=100`, `quantityunitcost=6.038`, `lot=00000017`, `wonumber=OFC00001` |
| Flujo principal | 1. Identificar la MO por `wonumber`. 2. Identificar el componente. 3. Descontar del lote. 4. Registrar el consumo. |
| Alternativos / errores | Lote sin saldo; componente fuera de BOM; MO inexistente; consumo duplicado. |
| Postcondiciones | Stock descontado y consumo registrado. |
| Reglas | R11, R12; HU-11 |
| Criterios | Dado un consumo de 100 FL, cuando se procesa, entonces se descuentan 6,038 KG y la MO registra el consumo. |
| Evidencia | Movimiento de salida y consumo de MO. |

### CU-STK-10 · Vínculo del consumo con la orden de producción

| Campo | Valor |
|---|---|
| Contexto / operación | STK / INSERT |
| Prioridad | P1 |
| Fixture | 11 |
| Precondiciones | MO existente |
| Datos clave | `wonumber=OFC00001`, `docnumber=1`, `docnumbercompl=OFC00001` |
| Flujo principal | 1. Leer `wonumber`. 2. Buscar la MO. 3. Asociar el movimiento a la MO y a la operación. 4. Guardar referencias. |
| Alternativos / errores | `wonumber` vacío; MO inexistente; MO cerrada; `docnumbercompl` distinto. |
| Postcondiciones | Consumo vinculado a la MO. |
| Reglas | R14; HU-11 |
| Criterios | Dado un consumo con `wonumber=OFC00001`, cuando se procesa, entonces queda vinculado a esa MO y no a otra. |
| Evidencia | Movimiento y MO. |

### CU-STK-11 · Descuento por lote y saldo insuficiente

| Campo | Valor |
|---|---|
| Contexto / operación | STK / INSERT |
| Prioridad | P1 |
| Fixture | 11 con saldo insuficiente |
| Precondiciones | Lote con stock |
| Datos clave | `lot=00000017`, `quantityunitcost`, saldo del lote |
| Flujo principal | 1. Verificar saldo del lote. 2. Descontar si alcanza. 3. Si no alcanza, fallar o consumir parcial según política. |
| Alternativos / errores | Saldo insuficiente; lote inexistente; lote de otro producto; consumo parcial. |
| Postcondiciones | Stock consistente; sin saldo negativo. |
| Reglas | HU-11 |
| Criterios | Dado un consumo mayor al saldo del lote, cuando se procesa, entonces la transacción falla con mensaje claro y no deja saldo negativo. |
| Evidencia | Saldo del lote y bitácora. |

### CU-STK-12 · Cancelación de consumo

| Campo | Valor |
|---|---|
| Contexto / operación | STK / CANCEL, TType 0 |
| Prioridad | P2 |
| Fixture | Variante CANCEL de 11 |
| Precondiciones | Consumo existente |
| Datos clave | `transactioncodeextref`, `lot`, `quantityunitcost` |
| Flujo principal | 1. Buscar el consumo original. 2. Revertir el descuento. 3. Registrar la cancelación. 4. No duplicar. |
| Alternativos / errores | Consumo ya cancelado; lote modificado; MO cerrada. |
| Postcondiciones | Stock repuesto y consumo anulado. |
| Reglas | HU-11 |
| Criterios | Dado un consumo existente, cuando se cancela, entonces el stock vuelve al lote y el consumo deja de impactar en la MO. |
| Evidencia | Movimiento de reversión y MO. |

### CU-STK-13 · Consumo informado por WIP

| Campo | Valor |
|---|---|
| Contexto / operación | WIP / exportación |
| Prioridad | P2 |
| Fixture | WIP_TR 17/18 |
| Precondiciones | MO y etiquetas WIP |
| Datos clave | `TransactionType=17`, `18`, `IdPalletLabel`, `QtyBefore`, `QtyAfter`, `ProcessID` |
| Flujo principal | 1. Leer la transacción WIP. 2. Vincular por `ProcessID` con la operación. 3. Comparar con el consumo STK. 4. Reportar diferencias. |
| Alternativos / errores | WIP sin vínculo; consumo total y parcial; etiqueta no encontrada. |
| Postcondiciones | Consumo real conciliado sin movimiento adicional. |
| Reglas | AGENTS.md; R20 |
| Criterios | Dado un WIP_TR 17, cuando se concilia, entonces el consumo total se compara con el STK y la diferencia queda visible. |
| Evidencia | Reporte de conciliación. |

### CU-STK-14 · Valorización del consumo

| Campo | Valor |
|---|---|
| Contexto / operación | STK / costos |
| Prioridad | P2 |
| Fixture | 11 |
| Precondiciones | Costo promedio configurado |
| Datos clave | `totalvalue=17593.53`, `quantityunitcost=6.038` |
| Flujo principal | 1. Leer el valor informado por Metrics. 2. Comparar con el costo de Odoo. 3. Aplicar la regla de valorización definida. 4. Registrar la diferencia. |
| Alternativos / errores | Valor de Metrics distinto al costo de Odoo; costo cero; moneda distinta. |
| Postcondiciones | Consumo valorizado según la regla acordada. |
| Reglas | Decisión pendiente: valor de Metrics vs costo de Odoo |
| Criterios | Dado un consumo con valor de Metrics, cuando se valoriza, entonces se aplica la regla definida y la diferencia queda documentada. |
| Evidencia | Asiento o reporte de costo. |

### CU-STK-15 · Ajuste de cantidad de stock

| Campo | Valor |
|---|---|
| Contexto / operación | STK / INSERT, TType 9, operationtype 1 |
| Prioridad | P1 |
| Fixture | `12- Ajuste Cantidad de Stock.txt` |
| Precondiciones | Producto, lote y ubicación existentes |
| Datos clave | `transactiontype=9`, `operationtype=1`, `stockcode=02.01.0003`, `quantity=500`, `quantityunitcost=30.192`, `lot=00000017`, `docnumber=test` |
| Flujo principal | 1. Crear movimiento de ajuste. 2. Aplicar cantidad positiva o negativa. 3. Asignar lote y ubicación. 4. Registrar el motivo. |
| Alternativos / errores | Ajuste que deja stock negativo; lote inexistente; cantidad cero; motivo vacío. |
| Postcondiciones | Stock ajustado según la cantidad informada. |
| Reglas | R11; AGENTS.md |
| Criterios | Dado un ajuste de 500 FL, cuando se procesa, entonces el stock del lote se ajusta y la operación queda registrada como ajuste, no como consumo. |
| Evidencia | Movimiento de ajuste y stock. |

### CU-STK-16 · Ajuste de cantidad con lote y vencimiento

| Campo | Valor |
|---|---|
| Contexto / operación | STK / INSERT |
| Prioridad | P2 |
| Fixture | 12 |
| Precondiciones | Lote con trazabilidad |
| Datos clave | `lot=00000017`, `productiondate`, `expirationdate`, `providerlot=41654654` |
| Flujo principal | 1. Validar lote. 2. Validar fechas. 3. Aplicar ajuste solo al lote indicado. 4. No afectar otros lotes. |
| Alternativos / errores | Lote sin vencimiento; fecha inválida; lote de otro producto. |
| Postcondiciones | Ajuste aplicado al lote correcto. |
| Reglas | HU-09 |
| Criterios | Dado un ajuste con lote, cuando se procesa, entonces solo se modifica ese lote y su trazabilidad se conserva. |
| Evidencia | Movimiento y ficha del lote. |

### CU-STK-17 · Idempotencia y cancelación del ajuste de cantidad

| Campo | Valor |
|---|---|
| Contexto / operación | STK / CANCEL |
| Prioridad | P2 |
| Fixture | 12 repetido y variante CANCEL |
| Precondiciones | Ajuste existente |
| Datos clave | `transactioncodeextref=970264967106610` |
| Flujo principal | 1. Detectar duplicado por `transactioncodeextref`. 2. Ignorar o cancelar. 3. Revertir el ajuste si corresponde. 4. No duplicar stock. |
| Alternativos / errores | Ajuste ya cancelado; ajuste con movimiento posterior; referencia repetida. |
| Postcondiciones | Un solo ajuste aplicado o ajuste revertido. |
| Reglas | Documento técnico §1 |
| Criterios | Dado un ajuste ya aplicado, cuando vuelve a llegar, entonces no se aplica dos veces. |
| Evidencia | Conteo de movimientos y stock. |

### CU-STK-18 · Entrega de producción

| Campo | Valor |
|---|---|
| Contexto / operación | STK / INSERT, TType 1, operationtype 0 |
| Prioridad | P1 |
| Fixture | `13- Entrega de produccion.txt` |
| Precondiciones | MO existente; PT con lote |
| Datos clave | `transactiontype=1`, `operationtype=0`, `stockcode=99.0001`, `quantity=50000`, `unitcode=UN`, `wonumber=OFC00001`, `lot=00000018`, `quantityunitcost=50000`, `unitcostcode=UN` |
| Flujo principal | 1. Identificar la MO. 2. Registrar el ingreso del PT. 3. Asignar lote. 4. Actualizar la MO. 5. No duplicar con la finalización de la MO. |
| Alternativos / errores | MO inexistente; PT sin lote; cantidad mayor a la planificada; entrega duplicada. |
| Postcondiciones | PT en stock y MO actualizada. |
| Reglas | R11; AGENTS.md |
| Criterios | Dada una entrega de 50.000 UN, cuando se procesa, entonces el PT ingresa con lote y la MO refleja la producción una sola vez. |
| Evidencia | Movimiento de PT y MO. |

### CU-STK-19 · Unidades UN y PZ en entrega de producción

| Campo | Valor |
|---|---|
| Contexto / operación | STK / validación de UOM |
| Prioridad | P1 |
| Fixture | 13 y muestras históricas con PZ |
| Precondiciones | UOM del PT configurada |
| Datos clave | `unitcode=UN`, `quantity=50000`; muestras previas con `PZ` |
| Flujo principal | 1. Resolver la UOM informada. 2. Convertir a la UOM del producto. 3. Validar que no se altere la cantidad. 4. Reportar diferencias. |
| Alternativos / errores | `UN` y `PZ` sin factor; factor incorrecto; cantidad duplicada por conversión. |
| Postcondiciones | Cantidad entregada consistente. |
| Reglas | R01; AGENTS.md |
| Criterios | Dada una entrega en PZ, cuando se convierte a UN, entonces la cantidad es equivalente y la diferencia queda documentada. |
| Evidencia | Movimiento y factor aplicado. |

### CU-STK-20 · Entrega parcial frente a cantidad planificada

| Campo | Valor |
|---|---|
| Contexto / operación | STK / validación |
| Prioridad | P2 |
| Fixture | 13 y 05 |
| Precondiciones | MO con cantidad planificada |
| Datos clave | Planificado `100000`; entregado `50000` |
| Flujo principal | 1. Comparar entregado con planificado. 2. Permitir entregas parciales. 3. Actualizar el saldo pendiente. 4. Alertar si la diferencia supera la tolerancia. |
| Alternativos / errores | Entrega mayor a la planificada; múltiples entregas; entrega con MO cerrada. |
| Postcondiciones | Saldo pendiente y alerta visibles. |
| Reglas | AGENTS.md |
| Criterios | Dada una entrega de 50.000 sobre 100.000 planificados, cuando se procesa, entonces la MO muestra 50.000 pendientes y no se cierra. |
| Evidencia | MO y reporte de avance. |

### CU-STK-21 · Lote y vencimiento del producto terminado

| Campo | Valor |
|---|---|
| Contexto / operación | STK / INSERT |
| Prioridad | P2 |
| Fixture | 13 |
| Precondiciones | PT con tracking |
| Datos clave | `lot=00000018`, `productiondate=2026-07-23`, `expirationdate=1899-12-30` |
| Flujo principal | 1. Crear o reutilizar lote del PT. 2. Guardar fecha de producción. 3. Interpretar vencimiento vacío o 1899 como sin vencimiento. |
| Alternativos / errores | Lote duplicado; vencimiento inválido; lote de otro PT. |
| Postcondiciones | Lote del PT con trazabilidad. |
| Reglas | HU-09 |
| Criterios | Dado un PT con lote, cuando se procesa, entonces el lote queda asociado y el vencimiento vacío no genera error. |
| Evidencia | Ficha del lote. |

### CU-STK-22 · Cancelación de entrega de producción

| Campo | Valor |
|---|---|
| Contexto / operación | STK / CANCEL, TType 1 |
| Prioridad | P2 |
| Fixture | Variante CANCEL de 13 |
| Precondiciones | Entrega existente |
| Datos clave | `transactioncodeextref`, `lot`, `quantityunitcost` |
| Flujo principal | 1. Buscar la entrega. 2. Verificar que el PT no esté entregado al cliente. 3. Revertir el ingreso. 4. Actualizar la MO. |
| Alternativos / errores | PT ya vendido; lote consumido; entrega ya cancelada. |
| Postcondiciones | Stock del PT revertido y MO actualizada. |
| Reglas | AGENTS.md |
| Criterios | Dada una entrega sin venta posterior, cuando se cancela, entonces el stock del PT se revierte y la MO vuelve a su saldo. |
| Evidencia | Movimiento de reversión y MO. |

### CU-STK-23 · Transferencia de un ítem a varios

| Campo | Valor |
|---|---|
| Contexto / operación | STK / INSERT, TType 5 |
| Prioridad | P2 |
| Fixture | `XML DE TRANSCION DE UNO ITEM PARA VARIOS.txt` |
| Precondiciones | Producto origen con stock y productos destino existentes |
| Datos clave | Origen `99.0014` con dos salidas de 10 y 15; destinos `99.0004` y `99.0005` con entradas de 10 y 15; lotes `00000024`, `00000029`, `00000030` |
| Flujo principal | 1. Procesar las salidas del origen. 2. Procesar las entradas en los destinos. 3. Vincular cada par por referencias. 4. Validar que las cantidades cuadren. |
| Alternativos / errores | Salidas sin entradas; cantidades desiguales; lote de destino inexistente; stock insuficiente. |
| Postcondiciones | Stock transferido y movimientos vinculados. |
| Reglas | R11; AGENTS.md |
| Criterios | Dada una transferencia de 10 y 15 unidades, cuando se procesa, entonces el origen baja 25 y los destinos suben 10 y 15. |
| Evidencia | Movimientos y stock por producto. |

### CU-STK-24 · Vínculos entre movimientos de transferencia

| Campo | Valor |
|---|---|
| Contexto / operación | STK / validación |
| Prioridad | P2 |
| Fixture | Transferencia uno a varios |
| Precondiciones | Movimientos de transferencia cargados |
| Datos clave | `relatedtransactioncodeextref`, `transactionoriginextref`, `transactioncodeextref` |
| Flujo principal | 1. Leer las referencias. 2. Emparejar salida y entrada. 3. Validar que cada entrada tenga su salida. 4. Reportar huérfanos. |
| Alternativos / errores | Referencia inexistente; entrada sin salida; salida sin entrada; referencia duplicada. |
| Postcondiciones | Pares de transferencia conciliados. |
| Reglas | AGENTS.md; R11 |
| Criterios | Dado un par salida-entrada con `relatedtransactioncodeextref`, cuando se concilia, entonces ambas quedan vinculadas y no hay movimientos huérfanos. |
| Evidencia | Reporte de pares y huérfanos. |

### CU-STK-25 · Cálculo del ajuste de valor por factura

| Campo | Valor |
|---|---|
| Contexto / operación | STK / salida Odoo → Metrics |
| Prioridad | P1 |
| Fixture | `10- Ajuste de valor de stock por factura.txt` |
| Precondiciones | Factura de proveedor y ingreso validados |
| Datos clave | Factura sin impuestos, `totalvalue` del ingreso, ajustes ya enviados |
| Flujo principal | 1. Tomar la factura sin impuestos. 2. Restar el valor del ingreso. 3. Restar ajustes ya enviados. 4. Obtener el ajuste. |
| Alternativos / errores | Diferencia menor a tolerancia; múltiples facturas; ajustes parciales; valor negativo. |
| Postcondiciones | Ajuste calculado y listo para enviar. |
| Reglas | HU-13; regla de base sin impuestos |
| Criterios | Dada una factura de 10.556.815,98 y un ingreso de 10.506.815,98, cuando se calcula, entonces el ajuste es 50.000. |
| Evidencia | Cálculo y documentación de respaldo. |

### CU-STK-26 · Envío del ajuste a Metrics

| Campo | Valor |
|---|---|
| Contexto / operación | STK / INSERT desde Odoo, TType 9 |
| Prioridad | P1 |
| Fixture | 10 |
| Precondiciones | Ajuste calculado |
| Datos clave | `transactiontype=9`, `stockmovementtype=1`, `operationtype=0`, `quantity=0`, `lot=UNICO`, `stockaddress=UNICO`, `totalvalue=50000`, `transactioncodeextref` único |
| Flujo principal | 1. Generar `transactioncodeextref` numérico y único. 2. Enviar por `ProcessTransaction`. 3. Registrar la respuesta. 4. Guardar el código para cancelar. |
| Alternativos / errores | Metrics no responde; código duplicado; `docnumber` vacío; error de validación. |
| Postcondiciones | Ajuste informado y respuesta registrada. |
| Reglas | HU-14; manual 11.10 |
| Criterios | Dado un ajuste de 50.000, cuando se envía, entonces Metrics recibe el movimiento con `transactiontype=9` y Odoo guarda el `transactioncodeextref`. |
| Evidencia | XML enviado y respuesta. |

### CU-STK-27 · Tolerancia del ajuste

| Campo | Valor |
|---|---|
| Contexto / operación | STK / validación |
| Prioridad | P2 |
| Fixture | 07 y 10 |
| Precondiciones | Tolerancia configurada |
| Datos clave | Diferencia por redondeo de 0,02 |
| Flujo principal | 1. Calcular la diferencia. 2. Comparar con la tolerancia. 3. Si está dentro, no enviar. 4. Si supera, enviar. |
| Alternativos / errores | Tolerancia cero; diferencia negativa; ajuste acumulado. |
| Postcondiciones | Solo se envían ajustes significativos. |
| Reglas | HU-13 |
| Criterios | Dada una diferencia de 0,02 y una tolerancia mayor, cuando se evalúa, entonces no se envía ajuste. |
| Evidencia | Reporte de diferencias y bandeja de ajustes. |

### CU-STK-28 · Ajuste en moneda extranjera

| Campo | Valor |
|---|---|
| Contexto / operación | STK / cálculo |
| Prioridad | P2 |
| Fixture | 07 y factura en moneda extranjera |
| Precondiciones | Tipo de cambio definido |
| Datos clave | Moneda de factura, tasa, fecha, valor en moneda de la empresa |
| Flujo principal | 1. Convertir la factura a moneda de la empresa. 2. Calcular el ajuste. 3. Guardar la tasa y la fecha usadas. |
| Alternativos / errores | Tasa ausente; fecha de tasa distinta a la factura; diferencia por redondeo. |
| Postcondiciones | Ajuste en moneda de la empresa con trazabilidad de tasa. |
| Reglas | HU-13; decisión multimoneda |
| Criterios | Dada una factura en USD, cuando se calcula el ajuste, entonces se usa la tasa definida y la fecha queda registrada. |
| Evidencia | Cálculo y tasa aplicada. |

### CU-STK-29 · Cancelación del ajuste de valor

| Campo | Valor |
|---|---|
| Contexto / operación | STK / CANCEL desde Odoo |
| Prioridad | P2 |
| Fixture | 10 y variante CANCEL |
| Precondiciones | Ajuste enviado |
| Datos clave | `transactioncodeextref` original, fecha original, operación CANCEL |
| Flujo principal | 1. Detectar anulación o reversión de factura. 2. Enviar CANCEL con el mismo código y la fecha original. 3. Registrar la respuesta. |
| Alternativos / errores | Metrics rechaza; código no encontrado; fecha distinta; cancelación duplicada. |
| Postcondiciones | Ajuste cancelado en Metrics. |
| Reglas | HU-15; manual 11.10 |
| Criterios | Dada una factura anulada, cuando se envía CANCEL, entonces Metrics recibe el mismo `transactioncodeextref` y la fecha original. |
| Evidencia | XML de cancelación y respuesta. |

### CU-STK-30 · Reintento del ajuste sin duplicar

| Campo | Valor |
|---|---|
| Contexto / operación | STK / reintento |
| Prioridad | P1 |
| Fixture | 10 con fallo de red |
| Precondiciones | Ajuste pendiente |
| Datos clave | `transactioncodeextref`, estado del envío |
| Flujo principal | 1. Fallar el envío. 2. Registrar el error. 3. Reintentar con el mismo código. 4. Confirmar que no se duplica. |
| Alternativos / errores | Metrics recibió pero Odoo no supo; reintento con código nuevo; doble ajuste. |
| Postcondiciones | Un solo ajuste aplicado en Metrics. |
| Reglas | HU-14; documento técnico §1 |
| Criterios | Dado un envío fallido, cuando se reintenta, entonces se reutiliza el código y no se crea un segundo ajuste. |
| Evidencia | Bitácora y movimientos en Metrics. |

### CU-STK-31 · Discrepancia de stockmovementtype y operationtype

| Campo | Valor |
|---|---|
| Contexto / operación | STK / validación de reglas |
| Prioridad | P1 |
| Fixture | 09, 10, 11, 12 y 13 |
| Precondiciones | R12 cargada |
| Datos clave | 09: `stockmovementtype=2` con `operationtype=0`; 11: `stockmovementtype=0` con `operationtype=1`; 10: `stockmovementtype=1` |
| Flujo principal | 1. Comparar los valores de las muestras con R12. 2. Documentar la discrepancia. 3. Definir la tabla real con Metrics. 4. Bloquear la implementación hasta confirmarla. |
| Alternativos / errores | Implementar R12 sin validar; invertir entrada y salida; ajuste tratado como entrada. |
| Postcondiciones | Tabla de mapeo confirmada y versionada. |
| Reglas | R12; manual 11.10 |
| Criterios | Dado un conflicto entre R12 y las muestras, cuando se define el mapeo, entonces prevalece la tabla confirmada por Metrics y queda documentada. |
| Evidencia | Tabla de equivalencias firmada. |

---

## 11. Casos de separación de materiales (`CU-PCK`)

### CU-PCK-01 · Solicitud de separación de materiales

| Campo | Valor |
|---|---|
| Contexto / operación | PCK / INSERT |
| Prioridad | P1 |
| Fixture | `15- Separacion de Materiales.txt` |
| Precondiciones | Pedido, producto y stock disponibles |
| Datos clave | `idseparation=1`, `customercode=1`, `invoicereqnumber=10000`, `status=3`, `netweight=14000`, `grossweight=14000`, `contents=2000` |
| Flujo principal | 1. Crear la separación. 2. Asociar cliente y solicitud de facturación. 3. Cargar ítems. 4. Guardar pesos y contenido. |
| Alternativos / errores | Cliente inexistente; solicitud inexistente; separación duplicada; pesos inconsistentes. |
| Postcondiciones | Separación creada y lista para liberación. |
| Reglas | Minuta funcional §8; flujo PCK |
| Criterios | Dada una separación con cliente y solicitud, cuando se procesa, entonces se crea con sus ítems y pesos. |
| Evidencia | Separación y bitácora. |

### CU-PCK-02 · Ítems, lotes y bultos

| Campo | Valor |
|---|---|
| Contexto / operación | PCK / INSERT |
| Prioridad | P1 |
| Fixture | 15 |
| Precondiciones | Producto con lote y stock |
| Datos clave | `stockcode=99.0001`, `quantity=100000`, `lot=00000018`, `packagequantity=2000`, `unitpackage=CX`, `stockplacecode=PADRON`, `stockaddress=UNICO` |
| Flujo principal | 1. Crear ítem de separación. 2. Asignar lote. 3. Crear bultos con cantidad y unidad de empaque. 4. Asignar ubicación. |
| Alternativos / errores | Lote sin stock; bultos que no suman la cantidad; unidad de empaque inexistente; ubicación inválida. |
| Postcondiciones | Ítems y bultos listos para remito. |
| Reglas | Minuta funcional §8 |
| Criterios | Dado un ítem de 100.000 UN en bultos de 2.000, cuando se procesa, entonces se crean 50 bultos y la suma coincide con la cantidad. |
| Evidencia | Ítems, bultos y stock reservado. |

### CU-PCK-03 · Pesos neto y bruto

| Campo | Valor |
|---|---|
| Contexto / operación | PCK / validación |
| Prioridad | P2 |
| Fixture | 15 |
| Precondiciones | Peso unitario del producto |
| Datos clave | `netweight=14000`, `grossweight=14000`, `unitweight=0.14`, `quantity=100000` |
| Flujo principal | 1. Calcular peso neto. 2. Comparar con `netweight`. 3. Comparar bruto con neto. 4. Reportar diferencia. |
| Alternativos / errores | Bruto menor a neto; peso unitario cero; diferencia por redondeo. |
| Postcondiciones | Pesos conciliados. |
| Reglas | Minuta funcional §8 |
| Criterios | Dado un peso unitario de 0,14 y 100.000 unidades, cuando se calcula, entonces el neto es 14.000 y coincide con el XML. |
| Evidencia | Cálculo y reporte de pesos. |

### CU-PCK-04 · Estados y liberación para remito

| Campo | Valor |
|---|---|
| Contexto / operación | PCK / UPDATE |
| Prioridad | P1 |
| Fixture | 15 y flujo de remisión |
| Precondiciones | Separación existente |
| Datos clave | `status=3`, ítem `status=2`, `invoicereqnumber` |
| Flujo principal | 1. Leer estado de la separación. 2. Liberar para emisión de remito. 3. Vincular con la solicitud de remisión. 4. No liberar si falta stock. |
| Alternativos / errores | Estado desconocido; separación incompleta; remito ya emitido. |
| Postcondiciones | Separación liberada y vinculada al remito. |
| Reglas | Flujo PCK del diagrama |
| Criterios | Dada una separación en estado 3, cuando se procesa, entonces queda liberada para emisión de remito. |
| Evidencia | Estado y vínculo con remito. |

### CU-PCK-05 · Error por stock o lote insuficiente

| Campo | Valor |
|---|---|
| Contexto / operación | PCK / INSERT |
| Prioridad | P3 |
| Fixture | Variante de 15 con lote sin stock |
| Precondiciones | Lote inexistente o sin saldo |
| Datos clave | `lot`, `quantity`, `stockplacecode` |
| Flujo principal | 1. Validar stock del lote. 2. Detectar faltante. 3. Fallar la separación. 4. No reservar parcialmente. |
| Alternativos / errores | Stock parcial; lote de otro producto; ubicación sin stock. |
| Postcondiciones | Sin separación parcial; error accionable. |
| Reglas | Minuta funcional §8 |
| Criterios | Dado un lote sin stock, cuando se procesa la separación, entonces falla y no se reserva nada. |
| Evidencia | Bitácora y ausencia de reserva. |

---

## 12. Casos de remisión y facturación (`CU-BIL`)

### CU-BIL-01 · Solicitud de remisión

| Campo | Valor |
|---|---|
| Contexto / operación | BIL / INSERT |
| Prioridad | P1 |
| Fixture | `14- Solicitud de remision.txt` |
| Precondiciones | Pedido y cliente existentes; stock separado |
| Datos clave | `invoicereqnumber=10000`, `invoicenumber=0`, `invoicecompl=1`, `status=1`, `invoicetype=1`, `sdibilitemsoritemref.delivery=1`, `billing=0`, `salesordernumber=5Q-1` |
| Flujo principal | 1. Crear solicitud de remisión. 2. Vincular pedido y líneas. 3. Asociar direcciones. 4. Preparar emisión de remito. |
| Alternativos / errores | Pedido inexistente; línea sin `delivery=1`; dirección de entrega faltante; solicitud duplicada. |
| Postcondiciones | Solicitud de remisión creada. |
| Reglas | Minuta funcional §8; flujo BIL |
| Criterios | Dada una solicitud con `delivery=1` y `billing=0`, cuando se procesa, entonces se prepara el remito sin generar factura. |
| Evidencia | Solicitud y vínculo con pedido. |

### CU-BIL-02 · Solicitud de facturación

| Campo | Valor |
|---|---|
| Contexto / operación | BIL / INSERT |
| Prioridad | P1 |
| Fixture | `16- Solicitud de Facturacion.txt` |
| Precondiciones | Pedido y cliente existentes |
| Datos clave | `invoicereqnumber=10001`, `invoicenumber=0`, `invoicecompl=1`, `status=1`, `invoicetype=1`, `billing=1`, `delivery=0`, `totalvalue=2540` |
| Flujo principal | 1. Crear solicitud de facturación. 2. Vincular pedido y líneas. 3. Asociar condición de pago. 4. Preparar emisión de factura. |
| Alternativos / errores | Pedido inexistente; línea sin `billing=1`; moneda faltante; solicitud duplicada. |
| Postcondiciones | Solicitud de facturación creada. |
| Reglas | Minuta funcional §8; flujo BIL |
| Criterios | Dada una solicitud con `billing=1` y `delivery=0`, cuando se procesa, entonces se prepara la factura sin generar remito. |
| Evidencia | Solicitud y vínculo con pedido. |

### CU-BIL-03 · Vínculo con pedido, línea y orden de producción

| Campo | Valor |
|---|---|
| Contexto / operación | BIL / validación |
| Prioridad | P1 |
| Fixture | 14 y 16 |
| Precondiciones | Pedido, línea y MO existentes |
| Datos clave | `salesordernumber=5Q-1`, `wonumber=OFC00001`, `quotenumber=5`, `itemid=1`, `stockcode=99.0001` |
| Flujo principal | 1. Resolver el pedido por número. 2. Resolver la línea por ítem. 3. Vincular con la MO. 4. Guardar la referencia. |
| Alternativos / errores | Pedido inexistente; línea no encontrada; MO inexistente; múltiples coincidencias. |
| Postcondiciones | Documento vinculado a pedido, línea y MO. |
| Reglas | Minuta funcional §8; R14 |
| Criterios | Dado un ítem con `salesordernumber`, `wonumber` y `quotenumber`, cuando se procesa, entonces queda vinculado a los tres documentos. |
| Evidencia | Vínculos entre documentos. |

### CU-BIL-04 · Direcciones de facturación, cobro y entrega

| Campo | Valor |
|---|---|
| Contexto / operación | BIL / INSERT |
| Prioridad | P2 |
| Fixture | 14 y 16 |
| Precondiciones | Cliente con direcciones |
| Datos clave | `isbilling`, `ischarging`, `isdelivery`, `addressname`, `district`, `zipcode` |
| Flujo principal | 1. Leer cada dirección. 2. Asignar tipo. 3. Crear contactos si no existen. 4. Asociar al documento. |
| Alternativos / errores | Dirección sin tipo; múltiples direcciones del mismo tipo; dirección inexistente. |
| Postcondiciones | Direcciones correctas en el documento. |
| Reglas | R19, R22 |
| Criterios | Dada una dirección con `isbilling=1`, cuando se procesa, entonces la factura usa esa dirección y el remito usa la de entrega. |
| Evidencia | Documento y direcciones asociadas. |

### CU-BIL-05 · Emisión de remito

| Campo | Valor |
|---|---|
| Contexto / operación | BIL / INSERT |
| Prioridad | P1 |
| Fixture | 14 |
| Precondiciones | Solicitud de remisión y separación liberada |
| Datos clave | `invoicereqnumber=10000`, ítems, lotes, `local=PADRON` |
| Flujo principal | 1. Tomar la solicitud de remisión. 2. Generar remito. 3. Descontar stock o reservar según política. 4. Vincular con la separación. |
| Alternativos / errores | Sin separación; stock insuficiente; remito duplicado; dirección faltante. |
| Postcondiciones | Remito emitido y stock afectado. |
| Reglas | Minuta funcional §8 |
| Criterios | Dada una solicitud de remisión liberada, cuando se emite, entonces el remito sale con los ítems y lotes separados. |
| Evidencia | Remito y movimiento de stock. |

### CU-BIL-06 · Rama “¿Es remisión?” del flujo

| Campo | Valor |
|---|---|
| Contexto / operación | BIL / decisión |
| Prioridad | P1 |
| Fixture | 14 y 16 |
| Precondiciones | Documento con `billing` y `delivery` |
| Flujo principal | 1. Evaluar si el documento es remisión. 2. Si es remisión, liberar separación y emitir remito. 3. Si no, emitir factura. |
| Flujo alternativo | Documento mixto con `billing=1` y `delivery=1`: emitir remito y factura según regla. |
| Alternativos / errores | Ambos flags en 1; ambos en 0; documento sin ítems. |
| Postcondiciones | Se emite el documento correcto sin duplicar. |
| Reglas | Flujo BIL del diagrama |
| Criterios | Dado un documento de remisión, cuando se procesa, entonces no se emite factura; dado uno de facturación, entonces no se emite remito. |
| Evidencia | Documentos emitidos y bitácora. |

### CU-BIL-07 · Numeración de factura argentina

| Campo | Valor |
|---|---|
| Contexto / operación | BIL / validación |
| Prioridad | P1 |
| Fixture | 14 y 16 |
| Precondiciones | Diario y punto de venta configurados |
| Datos clave | `invoicecompl=1`, `invoicenumber=0`, formato `0001-00000000` |
| Flujo principal | 1. Tomar punto de venta de `invoicecompl`. 2. Tomar número de `invoicenumber`. 3. Completar con ceros. 4. Asignar `l10n_latam_document_number`. |
| Alternativos / errores | `invoicenumber=0`; punto de venta inexistente; número duplicado; solicitud previa a la emisión. |
| Postcondiciones | Número de comprobante formateado. |
| Reglas | R17 |
| Criterios | Dado `invoicecompl=1` e `invoicenumber=0`, cuando se procesa, entonces se interpreta como solicitud previa y no como factura emitida. |
| Evidencia | Número asignado o estado de solicitud. |

### CU-BIL-08 · Tipo de comprobante y CFOP

| Campo | Valor |
|---|---|
| Contexto / operación | BIL / INSERT |
| Prioridad | P1 |
| Fixture | 14 y 16 |
| Precondiciones | Posición fiscal del cliente configurada |
| Datos clave | `invoicetype=1`, `cfop` (vacío en las muestras) |
| Flujo principal | 1. Mapear `invoicetype=1 → out_invoice`. 2. Determinar CFOP por operación y posición fiscal. 3. Asignar a la línea. |
| Alternativos / errores | CFOP vacío; tipo de comprobante desconocido; operación sin CFOP. |
| Postcondiciones | Comprobante con tipo y CFOP correctos. |
| Reglas | R16, R18 |
| Criterios | Dado `invoicetype=1`, cuando se procesa, entonces la factura es de venta y el CFOP se determina por la posición fiscal. |
| Evidencia | Factura y CFOP asignado. |

### CU-BIL-09 · Impuestos de la factura

| Campo | Valor |
|---|---|
| Contexto / operación | BIL / cálculo |
| Prioridad | P2 |
| Fixture | 16 (impuestos vacíos) |
| Precondiciones | Impuestos configurados |
| Datos clave | `sdilbilitemtaxinfo`, `totalvalue=2540`, `unitvalue=0.0254` |
| Flujo principal | 1. Leer impuestos del XML. 2. Si están vacíos, aplicar impuestos por producto o configuración. 3. Calcular base e impuesto. 4. Comparar con el total. |
| Alternativos / errores | Impuesto inexistente; base sin impuestos distinta; total que no cierra. |
| Postcondiciones | Factura con impuestos correctos. |
| Reglas | R18; decisión de base sin impuestos |
| Criterios | Dado un ítem sin impuestos en el XML, cuando se procesa, entonces se aplican los impuestos configurados y el total cuadra. |
| Evidencia | Factura y reporte de impuestos. |

### CU-BIL-10 · Nota de crédito y devolución

| Campo | Valor |
|---|---|
| Contexto / operación | BIL / INSERT |
| Prioridad | P2 |
| Fixture | Variante de 16 con `invoicetype=3` y `sdibilitemreturned` |
| Precondiciones | Factura original existente |
| Datos clave | `invoicetype=3`, `returnedinvocenumber`, `returnedtotalquantity`, `returnedtotalvalue` |
| Flujo principal | 1. Detectar devolución. 2. Crear nota de crédito. 3. Vincular a la factura original. 4. Revertir stock si corresponde. |
| Alternativos / errores | Factura original inexistente; devolución mayor a lo facturado; nota duplicada. |
| Postcondiciones | Nota de crédito vinculada y stock consistente. |
| Reglas | R16, R18 |
| Criterios | Dada una devolución de venta, cuando se procesa, entonces se crea una nota de crédito (`out_refund`) vinculada a la factura original. |
| Evidencia | Nota de crédito y vínculo. |

### CU-BIL-11 · Condición de pago y vencimientos

| Campo | Valor |
|---|---|
| Contexto / operación | BIL / INSERT |
| Prioridad | P2 |
| Fixture | 14 y 16 |
| Precondiciones | Términos de pago disponibles |
| Datos clave | `conditioncode=Al contado`, `duedate=2026-07-24`, `value=2540` |
| Flujo principal | 1. Buscar o crear el término. 2. Asignarlo al comprobante. 3. Guardar vencimientos. 4. Comparar con Odoo. |
| Alternativos / errores | Término inexistente; vencimiento distinto; múltiples vencimientos. |
| Postcondiciones | Comprobante con condición y vencimientos. |
| Reglas | HU-06 |
| Criterios | Dado “Al contado” con vencimiento, cuando se procesa, entonces el término y el vencimiento quedan registrados. |
| Evidencia | Comprobante y vencimientos. |

### CU-BIL-12 · Moneda de la factura

| Campo | Valor |
|---|---|
| Contexto / operación | BIL / INSERT |
| Prioridad | P2 |
| Fixture | 14 y 16 |
| Precondiciones | Moneda configurada |
| Datos clave | `idcurrency=1`, `unitvalue`, `totalvalue` |
| Flujo principal | 1. Resolver la moneda. 2. Asignar importes en moneda del comprobante. 3. Convertir a moneda de la empresa. |
| Alternativos / errores | Moneda desconocida; tasa ausente; importe cero. |
| Postcondiciones | Factura con importes coherentes. |
| Reglas | Decisión multimoneda |
| Criterios | Dada una factura en moneda extranjera, cuando se procesa, entonces se conservan los importes originales y su equivalente. |
| Evidencia | Factura y tasa aplicada. |

### CU-BIL-13 · Error por cliente, producto o pedido inexistente

| Campo | Valor |
|---|---|
| Contexto / operación | BIL / INSERT |
| Prioridad | P3 |
| Fixture | Variante de 16 con `code=999` o `stockcode=ZZ` |
| Precondiciones | Maestro faltante |
| Datos clave | `sdibilcustomerinfo.code`, `stockcode`, `salesordernumber` |
| Flujo principal | 1. Resolver cliente, producto y pedido. 2. Detectar faltante. 3. Fallar la transacción. 4. No crear el comprobante. |
| Alternativos / errores | Cliente inactivo; producto archivado; pedido cancelado. |
| Postcondiciones | Sin comprobante parcial; error accionable. |
| Reglas | HU-04 |
| Criterios | Dado un cliente inexistente, cuando se procesa, entonces no se crea el comprobante y la bitácora informa el código. |
| Evidencia | Bitácora y ausencia de comprobante. |

---

## 13. Casos de WIP (`CU-WIP`)

> WIP es solo exportación desde Metrics. Odoo no envía WIP a Metrics. En este proyecto WIP se usa para conciliar el consumo real, no para descontar stock.

### CU-WIP-01 · Etiqueta WIP

| Campo | Valor |
|---|---|
| Contexto / operación | WIP / exportación |
| Prioridad | P2 |
| Fixture | Manual 11.16 |
| Precondiciones | Orden de producción y etiqueta en Metrics |
| Datos clave | `IdPalletLabel`, `BarCode`, `Quantity`, `QuantityKG`, `UnitCode`, `StkCode`, `ComponentId`, `Lot`, `ProcessID`, `IsFinalProduct`, `Status` |
| Flujo principal | 1. Leer la etiqueta. 2. Vincular `StkCode` con el producto. 3. Vincular `ProcessID` con `idativ`. 4. Guardar estado y validación. |
| Alternativos / errores | `StkCode` inexistente; `ProcessID` sin operación; etiqueta duplicada; estado desconocido. |
| Postcondiciones | Etiqueta WIP disponible para conciliación. |
| Reglas | R20; manual 11.16 |
| Criterios | Dada una etiqueta con `StkCode` y `ProcessID`, cuando se procesa, entonces queda vinculada al producto y a la operación. |
| Evidencia | Etiqueta y vínculos. |

### CU-WIP-02 · Transacciones WIP por tipo

| Campo | Valor |
|---|---|
| Contexto / operación | WIP_TR / exportación |
| Prioridad | P2 |
| Fixture | Manual 11.17 |
| Precondiciones | Etiqueta WIP existente |
| Datos clave | `TransactionType` 1, 2, 3, 4, 7, 10, 11, 16, 17, 18, 20, 24, 27; `QtyBefore`, `QtyAfter`, `StockPlaceCodeBefore`, `StockPlaceCodeAfter` |
| Flujo principal | 1. Leer la transacción. 2. Interpretar el tipo. 3. Vincular por `IdPalletLabel`. 4. Guardar cantidades antes y después. |
| Alternativos / errores | Tipo desconocido; etiqueta inexistente; cantidades inconsistentes; movimiento sin ubicación. |
| Postcondiciones | Historial de la etiqueta disponible. |
| Reglas | R20; manual 11.17 |
| Criterios | Dada una transacción tipo 17, cuando se procesa, entonces se registra el consumo total y la etiqueta queda vinculada. |
| Evidencia | Historial de la etiqueta. |

### CU-WIP-03 · Vínculo ProcessID con idativ

| Campo | Valor |
|---|---|
| Contexto / operación | WIP → WO |
| Prioridad | P1 |
| Fixture | 05 y WIP |
| Precondiciones | Operación de WO con `idativ` |
| Datos clave | `WIP.ProcessID`, `WO.sdiwooperation.idativ` |
| Flujo principal | 1. Leer `ProcessID`. 2. Buscar la operación con el mismo `idativ`. 3. Vincular etiqueta, operación y MO. 4. Reportar no vinculados. |
| Alternativos / errores | `ProcessID` sin `idativ`; múltiples coincidencias; operación eliminada. |
| Postcondiciones | Trazabilidad WIP → WO. |
| Reglas | R14; AGENTS.md |
| Criterios | Dado un WIP con `ProcessID=1015`, cuando se vincula, entonces se asocia a la operación de WO con `idativ=1015`. |
| Evidencia | Vínculo WIP y work order. |

### CU-WIP-04 · Vínculo IdPalletLabel con WIP_TR

| Campo | Valor |
|---|---|
| Contexto / operación | WIP / validación |
| Prioridad | P1 |
| Fixture | WIP y WIP_TR |
| Precondiciones | Etiquetas y transacciones cargadas |
| Datos clave | `WIP.IdPalletLabel`, `WIP_TR.IdPalletLabel` |
| Flujo principal | 1. Leer `IdPalletLabel`. 2. Buscar la etiqueta. 3. Vincular cada transacción. 4. Reportar huérfanas. |
| Alternativos / errores | Transacción sin etiqueta; etiqueta sin transacciones; etiqueta duplicada. |
| Postcondiciones | Historial completo por etiqueta. |
| Reglas | AGENTS.md |
| Criterios | Dada una transacción con `IdPalletLabel`, cuando se procesa, entonces se adjunta a la etiqueta correcta y no queda huérfana. |
| Evidencia | Reporte de etiquetas y transacciones. |

### CU-WIP-05 · Conciliación del consumo real

| Campo | Valor |
|---|---|
| Contexto / operación | WIP / conciliación |
| Prioridad | P2 |
| Fixture | WIP_TR 17/18 y STK 11 |
| Precondiciones | Consumos STK y transacciones WIP cargados |
| Datos clave | `QtyBefore`, `QtyAfter`, `StockCode`, `ProcessID`, `wonumber` del STK |
| Flujo principal | 1. Agrupar consumo por operación. 2. Comparar WIP con STK. 3. Calcular diferencia. 4. Reportar por producto y por OP. |
| Alternativos / errores | Diferencia mayor a tolerancia; consumo parcial; etiqueta sin cierre. |
| Postcondiciones | Reporte de conciliación disponible. |
| Reglas | Minuta funcional §7; AGENTS.md |
| Criterios | Dado un consumo WIP de 100 y un STK de 100, cuando se concilia, entonces la diferencia es cero; si difiere, entonces queda reportada. |
| Evidencia | Reporte de conciliación. |

### CU-WIP-06 · Confirmación de no importabilidad

| Campo | Valor |
|---|---|
| Contexto / operación | WIP / validación |
| Prioridad | P2 |
| Fixture | WIP |
| Precondiciones | Módulo de integración |
| Datos clave | Contexto WIP |
| Flujo principal | 1. Intentar enviar WIP de Odoo a Metrics. 2. El sistema debe rechazarlo. 3. Registrar el rechazo. |
| Alternativos / errores | Envío accidental; reproceso; configuración incorrecta. |
| Postcondiciones | WIP no se importa a Metrics. |
| Reglas | Manual 11.16–11.17; AGENTS.md |
| Criterios | Dado un intento de exportar WIP desde Odoo, cuando se ejecuta, entonces el sistema lo rechaza y no genera una transacción. |
| Evidencia | Log del rechazo. |

---

## 14. Casos end-to-end (`CU-E2E`)

### CU-E2E-01 · Flujo de producto nuevo

| Campo | Valor |
|---|---|
| Contexto / operación | E2E |
| Prioridad | P1 |
| Fixture | 01, 03, 05, 06, 07, 08, 09, 11, 13, 15 y 14 o 16 |
| Precondiciones | Base limpia y configuración completa |
| Datos clave | Cliente 327, PT 99.0001, WO OFC00001, pedido 5Q-1 |
| Flujo principal | 1. Crear cliente y proveedor. 2. Crear material y PT. 3. Crear pedido y OP. 4. Generar necesidad y OC. 5. Recibir remito e ingreso. 6. Consumir material. 7. Entregar producción. 8. Separar materiales. 9. Emitir remito o factura. |
| Alternativos / errores | Faltante de maestro; stock insuficiente; entrega parcial; factura sin remito. |
| Postcondiciones | Producto nuevo producido, entregado y facturado con trazabilidad completa. |
| Reglas | Diagrama “Producto Nuevo”; todos los flujos |
| Criterios | Dado un producto nuevo, cuando se ejecuta el circuito completo, entonces cada documento queda vinculado y el stock y la facturación cierran. |
| Evidencia | Paquete de documentos y reporte de trazabilidad. |

### CU-E2E-02 · Flujo de producto repetido

| Campo | Valor |
|---|---|
| Contexto / operación | E2E |
| Prioridad | P1 |
| Fixture | 06, 05, 11, 13, 15 y 14 o 16 |
| Precondiciones | Cliente, producto y BOM existentes |
| Datos clave | Pedido 5Q-1, WO OFC00001, PT 99.0001 |
| Flujo principal | 1. Crear pedido. 2. Generar OP. 3. Solicitar y consumir material. 4. Entregar producción. 5. Separar. 6. Emitir remito o factura. |
| Alternativos / errores | Sin OP; producto sin BOM; entrega parcial; factura separada del remito. |
| Postcondiciones | Producto repetido producido y entregado sin recrear maestros. |
| Reglas | Diagrama “Producto Repetido” |
| Criterios | Dado un producto ya existente, cuando se ejecuta el circuito, entonces no se recrean maestros y el pedido se produce y factura. |
| Evidencia | Documentos y trazabilidad. |

### CU-E2E-03 · Flujo completo de compra

| Campo | Valor |
|---|---|
| Contexto / operación | E2E |
| Prioridad | P1 |
| Fixture | 07, 08, 09, 10 y factura de proveedor |
| Precondiciones | Proveedor, producto y moneda |
| Datos clave | OC 1, remito 12132, ingreso 3.623,04 KG, ajuste 50.000 |
| Flujo principal | 1. Crear OC. 2. Recibir remito. 3. Ingresar material. 4. Registrar factura de proveedor. 5. Calcular y enviar ajuste. 6. Verificar stock y valor. |
| Alternativos / errores | Remito antes que OC; OC no aprobada; factura con diferencia; ajuste dentro de tolerancia. |
| Postcondiciones | Compra cerrada con stock y valor ajustado. |
| Reglas | HU-05 a HU-15 |
| Criterios | Dada una compra completa, cuando se ejecuta, entonces el stock, la factura y el ajuste quedan conciliados. |
| Evidencia | OC, recepción, ingreso, factura y ajuste. |

### CU-E2E-04 · Trazabilidad WO → WIP → STK

| Campo | Valor |
|---|---|
| Contexto / operación | E2E |
| Prioridad | P2 |
| Fixture | 05, WIP, 11 y 13 |
| Precondiciones | OP, etiquetas WIP y movimientos |
| Datos clave | `idativ`, `ProcessID`, `IdPalletLabel`, lote, `wonumber` |
| Flujo principal | 1. Crear OP con operaciones. 2. Cargar WIP. 3. Conciliar consumo WIP y STK. 4. Registrar entrega de PT. 5. Reportar trazabilidad completa. |
| Alternativos / errores | WIP sin vínculo; consumo no conciliado; entrega sin lote. |
| Postcondiciones | Reporte que une OP, operación, etiqueta, consumo y PT. |
| Reglas | AGENTS.md; R14, R20 |
| Criterios | Dada una OP con WIP y movimientos, cuando se ejecuta la trazabilidad, entonces se reconstruye qué se consumió y qué se produjo por operación. |
| Evidencia | Reporte de trazabilidad completo. |

---

## 15. Matriz de ejecución

| ID | Flujo | Prioridad | Fixture |
|---|---|---|---|
| CU-INF-01 | Transversal | P1 | — |
| CU-INF-02 | Transversal | P1 | — |
| CU-INF-03 | Transversal | P2 | — |
| CU-INF-04 | Transversal | P1 | 01–16 |
| CU-INF-05 | Transversal | P1 | 11 |
| CU-INF-06 | Transversal | P1 | Error forzado |
| CU-INF-07 | Transversal | P1 | Error forzado |
| CU-INF-08 | Transversal | P1 | 01, 04, 07, 09 |
| CU-INF-09 | Transversal | P1 | 01–16 |
| CU-INF-10 | Transversal | P1 | 08, 09 |
| CU-CRM-01 | CRM | P1 | 01 |
| CU-CRM-02 | CRM | P1 | 02 |
| CU-CRM-03 | CRM | P2 | 01 |
| CU-CRM-04 | CRM | P2 | 01 |
| CU-CRM-05 | CRM | P1 | 01, 02 |
| CU-CRM-06 | CRM | P1 | 01, 02 |
| CU-CRM-07 | CRM | P2 | 01 |
| CU-CRM-08 | CRM | P2 | 01, 02 |
| CU-CRM-09 | CRM | P1 | 01 |
| CU-CRM-10 | CRM | P1 | 01 |
| CU-CRM-11 | CRM | P2 | 01, 02 |
| CU-CRM-12 | CRM | P3 | 01 |
| CU-CRM-13 | CRM | P2 | 01 |
| CU-ITM-01 | STKItem | P1 | 03 |
| CU-ITM-02 | STKItem | P1 | 04 |
| CU-ITM-03 | STKItem | P2 | 03, 04 |
| CU-ITM-04 | STKItem | P2 | Clasificación |
| CU-ITM-05 | STKItem | P1 | 04 |
| CU-ITM-06 | STKItem | P1 | 03, 04 |
| CU-ITM-07 | STKItem | P1 | 03, 04 |
| CU-ITM-08 | STKItem | P2 | 03, 04 |
| CU-ITM-09 | STKItem | P1 | Pendiente |
| CU-ITM-10 | STKItem | P2 | 04 |
| CU-ITM-11 | STKItem | P1 | 03, 04 |
| CU-ITM-12 | STKItem | P3 | 04 |
| CU-ITM-13 | STKItem | P1 | 03, 04, 05 |
| CU-WO-01 | WO | P1 | 05 |
| CU-WO-02 | WO | P1 | 05 |
| CU-WO-03 | WO | P1 | 05, OP compartida |
| CU-WO-04 | WO | P1 | 05, OP compartida |
| CU-WO-05 | WO | P1 | 05, OP compartida |
| CU-WO-06 | WO | P2 | OP compartida |
| CU-WO-07 | WO | P1 | 05 |
| CU-WO-08 | WO | P1 | OP compartida |
| CU-WO-09 | WO | P1 | OP compartida |
| CU-WO-10 | WO | P2 | OP compartida |
| CU-WO-11 | WO | P2 | OP compartida |
| CU-WO-12 | WO | P2 | 05, OP compartida |
| CU-WO-13 | WO | P1 | 11 |
| CU-WO-14 | WO | P2 | WIP |
| CU-WO-15 | WO | P1 | 13 |
| CU-WO-16 | WO | P1 | 06, 05 |
| CU-WO-17 | WO | P2 | 05 |
| CU-WO-18 | WO | P2 | 05, OP compartida |
| CU-WO-19 | WO | P3 | 05, OP compartida |
| CU-WO-20 | WO | P2 | 05 |
| CU-WO-21 | WO | P2 | Pendiente |
| CU-SOR-01 | SOR | P1 | 06 |
| CU-SOR-02 | SOR | P1 | 06 |
| CU-SOR-03 | SOR | P2 | 06 |
| CU-SOR-04 | SOR | P2 | 06 |
| CU-SOR-05 | SOR | P2 | 06 |
| CU-SOR-06 | SOR | P2 | 06 |
| CU-SOR-07 | SOR | P2 | 06 |
| CU-SOR-08 | SOR | P3 | 06 |
| CU-SOR-09 | SOR | P1 | 06, 05 |
| CU-POR-01 | POR | P1 | 07 |
| CU-POR-02 | POR | P1 | 07 |
| CU-POR-03 | POR | P2 | 07 |
| CU-POR-04 | POR | P1 | 07 |
| CU-POR-05 | POR | P2 | 07 |
| CU-POR-06 | POR | P2 | 07 |
| CU-POR-07 | POR | P1 | 07 |
| CU-POR-08 | POR | P3 | 07 |
| CU-POR-09 | POR | P2 | 07 |
| CU-REC-01 | REC | P1 | 08 |
| CU-REC-02 | REC | P2 | 08 |
| CU-REC-03 | REC | P2 | 08 |
| CU-REC-04 | REC | P1 | 08 |
| CU-REC-05 | REC | P1 | 08, 09 |
| CU-REC-06 | REC | P3 | 08 |
| CU-STK-01 | STK | P1 | 09 |
| CU-STK-02 | STK | P1 | 09 |
| CU-STK-03 | STK | P1 | 09, 11 |
| CU-STK-04 | STK | P1 | 09, 08 |
| CU-STK-05 | STK | P1 | 09, 10 |
| CU-STK-06 | STK | P2 | 09 |
| CU-STK-07 | STK | P3 | 09 |
| CU-STK-08 | STK | P3 | 09, 11 |
| CU-STK-09 | STK | P1 | 11 |
| CU-STK-10 | STK | P1 | 11 |
| CU-STK-11 | STK | P1 | 11 |
| CU-STK-12 | STK | P2 | 11 |
| CU-STK-13 | STK | P2 | WIP, 11 |
| CU-STK-14 | STK | P2 | 11 |
| CU-STK-15 | STK | P1 | 12 |
| CU-STK-16 | STK | P2 | 12 |
| CU-STK-17 | STK | P2 | 12 |
| CU-STK-18 | STK | P1 | 13 |
| CU-STK-19 | STK | P1 | 13 |
| CU-STK-20 | STK | P2 | 13, 05 |
| CU-STK-21 | STK | P2 | 13 |
| CU-STK-22 | STK | P2 | 13 |
| CU-STK-23 | STK | P2 | Transferencia |
| CU-STK-24 | STK | P2 | Transferencia |
| CU-STK-25 | STK | P1 | 09, 10 |
| CU-STK-26 | STK | P1 | 10 |
| CU-STK-27 | STK | P2 | 07, 10 |
| CU-STK-28 | STK | P2 | 07, 10 |
| CU-STK-29 | STK | P2 | 10 |
| CU-STK-30 | STK | P1 | 10 |
| CU-STK-31 | STK | P1 | 09–13 |
| CU-PCK-01 | PCK | P1 | 15 |
| CU-PCK-02 | PCK | P1 | 15 |
| CU-PCK-03 | PCK | P2 | 15 |
| CU-PCK-04 | PCK | P1 | 15 |
| CU-PCK-05 | PCK | P3 | 15 |
| CU-BIL-01 | BIL | P1 | 14 |
| CU-BIL-02 | BIL | P1 | 16 |
| CU-BIL-03 | BIL | P1 | 14, 16 |
| CU-BIL-04 | BIL | P2 | 14, 16 |
| CU-BIL-05 | BIL | P1 | 14 |
| CU-BIL-06 | BIL | P1 | 14, 16 |
| CU-BIL-07 | BIL | P1 | 14, 16 |
| CU-BIL-08 | BIL | P1 | 14, 16 |
| CU-BIL-09 | BIL | P2 | 16 |
| CU-BIL-10 | BIL | P2 | 16 |
| CU-BIL-11 | BIL | P2 | 14, 16 |
| CU-BIL-12 | BIL | P2 | 14, 16 |
| CU-BIL-13 | BIL | P3 | 16 |
| CU-WIP-01 | WIP | P2 | Manual 11.16 |
| CU-WIP-02 | WIP | P2 | Manual 11.17 |
| CU-WIP-03 | WIP | P1 | 05, WIP |
| CU-WIP-04 | WIP | P1 | WIP, WIP_TR |
| CU-WIP-05 | WIP | P2 | WIP_TR, 11 |
| CU-WIP-06 | WIP | P2 | WIP |
| CU-E2E-01 | E2E | P1 | 01–16 |
| CU-E2E-02 | E2E | P1 | 05, 06, 11, 13, 14/16 |
| CU-E2E-03 | E2E | P1 | 07–10 |
| CU-E2E-04 | E2E | P2 | 05, 11, 13, WIP |

---

## 16. Pendientes consolidados

| # | Pendiente | Responsable | Impacta |
|---|---|---|---|
| 1 | Endpoint y WSDL del WebService | Metrics | CU-INF-01 a 03 |
| 2 | Tabla de códigos de moneda (`idcurrency`) | Metrics | CU-INF-08, CU-POR-02 |
| 3 | Regla de vencimiento de “45 dias” | Metrics / negocio | CU-POR-03, CU-BIL-11 |
| 4 | Muestra REC con ítems y número de OC | Metrics | CU-REC-06 |
| 5 | Muestra STKItem de `02.01.0003` con unidades y `WeightKg` | Metrics | CU-ITM-06, CU-STK-03 |
| 6 | Definir si se importa REQ y con qué muestra | Metrics | CU-STK-09, CU-STK-13 |
| 7 | Ajustes negativos y contenido de `docnumber` | Metrics | CU-STK-25 a 30 |
| 8 | Política para OC no aprobada | Negocio | CU-POR-06 |
| 9 | Tolerancia, tipo de cambio y fecha del ajuste | Negocio | CU-STK-25 a 28 |
| 10 | Tratamiento del residuo de kilos | Negocio | CU-STK-08 |
| 11 | Valorización del consumo: Metrics vs Odoo | Negocio | CU-STK-14 |
| 12 | Confirmar semántica real de `stockmovementtype` | Metrics | CU-STK-31 |
| 13 | Confirmar semántica de `sdiwocomponent` (¿insumo o PT?) | Metrics | CU-WO-04 |
| 14 | Muestra de bobina madre/hija con `originitem` | Metrics | CU-ITM-09 |
| 15 | Muestra de BOM multinivel | Metrics | CU-WO-21 |
| 16 | Versión de Odoo y módulos usados | Proyecto | Todos |
| 17 | Destino exacto de `productclassification` | Proyecto | CU-ITM-04 |
| 18 | Regla de absorción del residuo porcentual | Negocio | CU-WO-10 |
| 19 | Tratamiento de PT con `controltraceability=1` | Negocio | CU-ITM-07 |
| 20 | Definir si el ajuste se envía al confirmar o al publicar la factura | Negocio | CU-STK-26 |

---

## 17. Trazabilidad documental

| Fuente | Uso en este documento |
|---|---|
| `ejemplo completo/01–16` | Fixtures de todos los casos |
| Manual Metrics revisión 93, secciones 11.1–11.17 | Contextos, operaciones, WIP y WIP_TR |
| `HU Integración Odoo METRICS.md` | HU-01 a HU-16, reglas de compras |
| `cu/cu integracion tecnico modulo.txt` | CU-INF-01 a 10 |
| `resumen_flujo_compras_metrics_odoo.md` | Reglas RR, RN y flujo de compras |
| `resumen_meet_integracion_funcional.txt` | Reglas de negocio de CRM, ventas, costos, UOM y remitos |
| `investigacion.md` | Estructura WO, STK y WIP |
| `generar_excel_metrics.py` | Reglas R01 a R23 |
| `Clasificacion de Producto.csv` | CU-ITM-04 |
| `Flujo Integracion Producto Nuevo.png` y `Producto Repetido 2.png` | CU-E2E-01 y CU-E2E-02 |
| `XML CON OP COMPARTIDA PROD. DIFERENTES.txt` | CU-WO-08 a 11 |
| `XML DE TRANSCION DE UNO ITEM PARA VARIOS.txt` | CU-STK-23 y 24 |
| `XML STKITEM con Clasificacion de Producto.txt` | CU-ITM-04 |

---

## 18. Criterios de salida de la etapa de pruebas

- Todos los casos P1 ejecutados y aprobados.
- Casos P2 ejecutados o con desvío aceptado y documentado.
- Casos P3 ejecutados al menos una vez con evidencia del error controlado.
- Cero duplicados en maestros y documentos al reprocesar una transacción.
- Cero datos parciales ante fallos de negocio.
- Bitácora completa para todas las transacciones.
- Conciliación de stock y valores dentro de la tolerancia acordada.
- Pendientes 1 a 20 resueltos o aceptados formalmente antes de producción.

