# HU – Cancelación de Pedido de Venta desde Metrics hacia Odoo

## HU 1 – Cancelación del Pedido de Venta

### Historia de Usuario

**Como** sistema de integración Metrics-Odoo
**Quiero** que cuando un pedido sea cancelado en Metrics, se gestione la cancelación de los documentos relacionados en Odoo
**Para** mantener sincronizados ambos sistemas y evitar que una operación cancelada continúe activa en Odoo.

### Alcance

Cuando Metrics informe la cancelación de una operación, Odoo deberá identificar el Pedido de Venta/SOR y los documentos relacionados:

* Pedido de Venta / SOR.
* Remito / Orden de Entrega.
* Factura.

La cancelación deberá ejecutarse respetando el estado de cada documento.

### Reglas de negocio

| Documento                 | Condición para cancelar     |
| ------------------------- | --------------------------- |
| Pedido de Venta / SOR     | No facturado y no entregado |
| Remito / Orden de Entrega | No emitido/validado         |
| Factura                   | En estado Borrador          |

Una factura emitida/confirmada no deberá eliminarse ni cancelarse mediante este flujo.

Un remito emitido/validado no deberá cancelarse mediante este flujo.

Un Pedido de Venta facturado o entregado no deberá cancelarse mediante este flujo.

### Flujo

```text
Metrics
   │
   │ Solicitud de cancelación
   ▼
Identificar Pedido de Venta / SOR
   │
   ▼
Identificar documentos relacionados
   │
   ├── Factura
   │
   └── Remito / Orden de Entrega
   │
   ▼
Validar estados
   │
   ├── Factura en Borrador
   │       ↓
   │   Cancelar / eliminar
   │
   ├── Remito no emitido
   │       ↓
   │   Cancelar
   │
   └── Pedido no facturado y no entregado
           ↓
       Cancelar Pedido
           ↓
       Informar resultado a Metrics
```

### Criterios de aceptación

#### CA01 – Recepción de cancelación

**Dado** un pedido generado desde Metrics
**Cuando** Metrics informa que la operación fue cancelada
**Entonces** Odoo debe identificar el Pedido de Venta/SOR correspondiente.

#### CA02 – Identificación de documentos

**Dado** un Pedido de Venta identificado
**Cuando** se procesa la cancelación
**Entonces** Odoo debe identificar los remitos y facturas relacionados, si existen.

#### CA03 – Factura en borrador

**Dado** que existe una factura relacionada
**Y** la factura se encuentra en estado Borrador
**Cuando** se procesa la cancelación
**Entonces** la factura debe cancelarse/eliminarse según el mecanismo definido para Odoo.

#### CA04 – Remito no emitido

**Dado** que existe un remito relacionado
**Y** el remito todavía no fue emitido/validado
**Cuando** se procesa la cancelación
**Entonces** el remito debe cancelarse.

#### CA05 – Cancelación del Pedido de Venta

**Dado** que el pedido no está facturado
**Y** no está entregado
**Cuando** se procesa la cancelación
**Entonces** el Pedido de Venta/SOR debe quedar cancelado.

#### CA06 – Confirmación a Metrics

**Dado** que todos los documentos que correspondía cancelar fueron procesados correctamente
**Cuando** finaliza la operación
**Entonces** la integración debe informar a Metrics que la cancelación fue exitosa.

---

# HU 2 – Validaciones y excepciones de cancelación

### Historia de Usuario

**Como** sistema de integración Metrics-Odoo
**Quiero** validar el estado de los documentos antes de ejecutar una cancelación
**Para** evitar modificaciones sobre documentos que ya tuvieron impacto comercial, operativo, contable o fiscal.

### Reglas de bloqueo

La cancelación automática deberá bloquearse cuando se detecte alguna de las siguientes situaciones:

| Situación                     | Resultado                   |
| ----------------------------- | --------------------------- |
| Pedido de Venta facturado     | No cancelar                 |
| Pedido de Venta entregado     | No cancelar                 |
| Remito emitido/validado       | No cancelar                 |
| Factura emitida/confirmada    | No eliminar/cancelar        |
| Pedido parcialmente facturado | No cancelar automáticamente |
| Pedido parcialmente entregado | No cancelar automáticamente |

### Criterios de aceptación

#### CA01 – Pedido facturado

**Dado** un Pedido de Venta relacionado con Metrics
**Y** existe una factura emitida/confirmada
**Cuando** Metrics solicita la cancelación
**Entonces** Odoo no debe cancelar el Pedido de Venta.

Debe informar a Metrics que la operación no puede cancelarse porque el pedido ya fue facturado.

#### CA02 – Pedido entregado

**Dado** un Pedido de Venta relacionado con Metrics
**Y** existe una entrega/remito validado
**Cuando** Metrics solicita la cancelación
**Entonces** Odoo no debe cancelar el Pedido de Venta.

Debe informar a Metrics que la operación no puede cancelarse porque el pedido ya fue entregado.

#### CA03 – Remito emitido

**Dado** un remito relacionado con el Pedido de Venta
**Y** el remito ya fue emitido/validado
**Cuando** Metrics solicita la cancelación
**Entonces** el remito no debe cancelarse automáticamente.

Debe informarse la situación a Metrics.

#### CA04 – Factura emitida

**Dado** una factura relacionada con el Pedido de Venta
**Y** la factura ya fue emitida/confirmada
**Cuando** Metrics solicita la cancelación
**Entonces** la factura no debe eliminarse ni cancelarse automáticamente.

Debe informarse a Metrics que existe una factura emitida.

> El tratamiento posterior de una factura emitida, por ejemplo mediante una nota de crédito, queda fuera de estas HU y debería definirse como un flujo independiente.

#### CA05 – Cancelación parcial

**Dado** que alguno de los documentos relacionados ya avanzó a un estado que impide su cancelación
**Cuando** Metrics solicita cancelar la operación
**Entonces** la integración no debe realizar una cancelación parcial silenciosa.

Debe informar el documento que bloqueó la operación y su estado.

#### CA06 – Idempotencia

**Dado** que una solicitud de cancelación ya fue procesada
**Cuando** Metrics vuelve a enviar la misma solicitud
**Entonces** Odoo debe verificar el estado actual y no ejecutar nuevamente acciones que puedan generar inconsistencias.

#### CA07 – Trazabilidad

La integración deberá registrar:

* Identificador de la operación en Metrics.
* Pedido de Venta/SOR en Odoo.
* Factura relacionada.
* Remito relacionado.
* Estado de cada documento.
* Acción ejecutada.
* Resultado.
* Motivo del bloqueo, cuando corresponda.
* Fecha y hora de procesamiento.

---

# Resultado de la integración

La integración deberá devolver a Metrics un resultado claro.

## CANCELADO

Todos los documentos que correspondía cancelar fueron procesados correctamente.

## NO CANCELADO – PEDIDO FACTURADO

El Pedido de Venta tiene una factura emitida/confirmada.

## NO CANCELADO – PEDIDO ENTREGADO

El Pedido de Venta tiene una entrega/remito validado.

## NO CANCELADO – REMITO EMITIDO

El remito ya fue emitido/validado.

## NO CANCELADO – FACTURA EMITIDA

Existe una factura emitida/confirmada.

## ERROR DE INTEGRACIÓN

La operación no pudo procesarse por un error técnico o de comunicación.

---

# Flujo resumido

```text
                 METRICS
                    │
                    │ Cancelación
                    ▼
             Pedido de Venta
                    │
                    ▼
            Validar documentos
                    │
       ┌────────────┼─────────────┐
       │            │             │
       ▼            ▼             ▼
    Factura       Remito        Pedido
       │            │             │
       ▼            ▼             ▼
 ¿Borrador?     ¿Emitido?    ¿Facturado?
       │            │             │
    Sí │ No       No │ Sí       No │ Sí
       │            │             │
       ▼            ▼             ▼
  Cancelar       Cancelar      ¿Entregado?
                                    │
                                 No │ Sí
                                    │
                                    ▼
                              Cancelar pedido
                                    │
                                    ▼
                              Resultado
                                    │
                                    ▼
                                  Metrics
```

# Fuera de alcance

Estas HU no contemplan:

* Anulación de facturas ya emitidas mediante nota de crédito.
* Reversión de entregas/remitos ya validados.
* Reversión de movimientos de stock ya realizados.
* Cancelación de órdenes de fabricación/WO.
* Reversión de operaciones contables ya confirmadas.

Estos casos deberán definirse en historias de usuario independientes si el negocio requiere su automatización.
