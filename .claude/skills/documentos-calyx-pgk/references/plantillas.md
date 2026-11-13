# Guía y Plantillas de Documentación de Proyectos

Este documento reúne los formatos estándar y directivas de diseño/identidad visual para la gestión, relevamiento, diseño funcional y documentación técnica de proyectos de software y consultoría.

---

## 0. Estándares de Formato e Identidad Visual

Para mantener una presentación profesional alineada con los documentos corporativos (como las minutas oficiales en Word/PDF), se deben aplicar las siguientes directrices:

### 0.1. Encabezado e Imagen Institucional
* **Logotipos Institucionales:** Todo documento formal (Minuta, Especificación, Entregable) debe incluir en el margen superior/encabezado los logos correspondientes a las partes involucradas.
  * *Ejemplo:* Logo de la Consultora/Proveedor (`Calyx`) + Logo de Firma Miembro / Auditoría (`PGK Consultores / TGS`) 
* **Tipografía y Estilo:** Utilizar fuentes institucionales claras (Arial, Segoe UI o Calibri), manteniendo tamaños jerárquicos:
  * **Título Principal:** 18 - 20 pt (Negrita)
  * **Subtítulos / Secciones:** 14 - 16 pt (Negrita)
  * **Cuerpo de texto / Tablas:** 10 - 11 pt

### 0.2. Paleta de Colores de Referencia
* **Azul Corporativo Primary:** `#004070` (Encabezados de tablas, títulos principales)
* **Naranja / Secundario:** `#E85E00` (Acentos, estados pendientes, alertas)
* **Gris Claro:** `#F4F4F4` (Filas alternadas en tablas, fondos de código)

---

## 1. Minuta de Reunión (Formato Corporativo)

Utilizar este formato para registrar acuerdos, decisiones y compromisos asumidos en reuniones con clientes o equipos internos.

```
+-------------------------------------------------------------------------+
| [ LOGO CALYX ]              [ LOGO PGK / TGS ]         [ LOGO CLIENTE ] |
+-------------------------------------------------------------------------+

# Minuta de Reunión

| Campo | Detalle |
| :--- | :--- |
| **Reunión / Proyecto** | [Nombre de la reunión / Proyecto] |
| **Fecha** | DD/MM/AAAA |
| **Objetivo** | [Propósito principal de la reunión] |
| **Participantes** | **Por Cliente:** [Nombre - Cargo]<br>**Por Calyx / PGK:** [Nombre - Cargo] |
| **Documentos Asociados** | [Links o nombres de archivos adjuntos/presentados] |
| **Próxima Instancia** | [Fecha u objetivo de la próxima reunión] |

---

### 1. Resumen Ejecutivo

#### Metodología e Implementación
* Breve descripción de la metodología acordada (Relevamiento -> Configuración -> Desarrollos -> Migración -> Pruebas -> Capacitación).

#### Tópicos Principales Tratados:
1. **[Tema 1 - ej. Gestión de Pagos Combinados]:** Detalle de módulos a evaluar o utilizar (`payment_mode`, `payment_bundle`).
2. **[Tema 2 - ej. Configuración de Posiciones Fiscales y Alícuotas]:** Tratamiento de normativas locales (ej. DGR Salta, alícuotas 1,8%, 3,6%, etc.).
3. **[Tema 3 - ej. Integración Técnica con Padrones]:** Explicación del flujo de automatización mediante script intermedio (Python / JSON).
4. **[Tema 4 - ej. Integración AFIP / ARCA]:** Consulta de datos fiscales por CUIT y herramientas de depuración/desarrollo.

---

### 2. Acuerdos Alcanzados
*Lista concisa de las decisiones tomadas y consensuadas durante la sesión.*

1. Comenzar por el relevamiento de los flujos antes de avanzar con la configuración definitiva.
2. Identificar durante el relevamiento qué requerimientos necesitan desarrollo y cuáles se resuelven mediante configuración estándar.
3. Realizar pruebas de circuitos con un usuario clave antes de capacitar a los usuarios finales.
4. Profundizar el análisis de necesidades impositivas específicas (padrones, rentas locales).

---

### 3. Pasos a Seguir (Action Items)

| # | Acción / Tarea | Responsable | Fecha Límite | Estado |
| :-: | :--- | :--- | :-: | :-: |
| 1 | Relevar y documentar los flujos actuales de cada área. | [Cliente / Andrea] | DD/MM/AAAA | Pendiente |
| 2 | Definir diseño funcional de flujos y sugerencias de aplicaciones. | [Calyx / Vanesa] | DD/MM/AAAA | En Progreso |
| 3 | Enviar Informe y propuesta de localización / diseño padrón. | [Consultoría] | DD/MM/AAAA | Pendiente |

```

---

## 2. Documento de Requisito Funcional (Especificación / User Story)

Utilizar este formato para especificar desarrollos a medida, personalizaciones de sistemas o nuevas funcionalidades.

```
+-------------------------------------------------------------------------+
| [ LOGO PROVEEDOR ]                                       [ LOGO CLIENTE ] |
+-------------------------------------------------------------------------+

# Especificación Funcional: [Nombre del Requerimiento / Módulo]

| Campo | Detalle |
| :--- | :--- |
| **ID Requerimiento** | REQ-XXX |
| **Fecha de Creación** | DD/MM/AAAA |
| **Autor** | [Nombre del Consultor / Analista] |
| **Revisor / Aprobador** | [Nombre del Líder Técnico o Cliente] |
| **Estado** | [Borrador / En Revisión / Aprobado] |

---

### 1. Contexto y Objetivo
* **Problema / Necesidad:** Explicación del escenario actual y la necesidad del negocio.
* **Objetivo de la Solución:** Explicación de lo que se busca lograr con la implementación.

---

### 2. Alcance (In Scope / Out of Scope)
* **Dentro del Alcance:**
  * Funcionalidad A.
  * Funcionalidad B.
* **Fuera del Alcance:**
  * Integraciones no contempladas.

---

### 3. Criterios de Aceptación (Historias de Usuario)

#### Historia de Usuario 1
* **Como** [tipo de usuario/rol],
* **Quiero** [realizar una acción específica],
* **Para** [obtener un beneficio determinado].

**Criterios de Validación:**
- [ ] Dado que [escenario inicial], cuando [evento], entonces [resultado esperado].
- [ ] Validación de campos obligatorios.

---

### 4. Flujo del Proceso (Diagrama / Paso a Paso)
1. El usuario ingresa a la pantalla X.
2. El sistema valida los datos de entrada según las reglas R1 y R2.
3. El sistema invoca al servicio web Y.
4. El sistema actualiza el registro Z y muestra confirmación al usuario.

---

### 5. Reglas de Negocio
* **RN-01:** Descripción de la regla fiscal, financiera o lógica de negocio.
* **RN-02:** Descripción de excepciones y cómo deben manejarse.

```

---

## 3. Especificación Técnica de Integración / Script

Formato ideal para detallar scripts intermedios, llamadas a APIs o conectores entre sistemas (ej. Odoo, ARCA/AFIP, Padrones).

```
# Especificación Técnica: Integración [Sistema A] <-> [Sistema B]

| Campo | Detalle |
| :--- | :--- |
| **Módulo / Componente** | [Nombre de la integración / Script] |
| **Tecnología / Lenguaje** | Python / REST API / Webservice |
| **Autor Técnico** | [Nombre del Desarrollador / Arquitecto] |

---

### 1. Arquitectura del Flujo

```
[Padrón / Fuente Ext.] ---> (Script Intermedio Python) ---> [Web Service / ERP]
```

---

### 2. Endpoints y Estructura de Datos

#### Endpoint: `POST /api/v1/padron/salta`
* **Descripción:** Envía datos procesados hacia el sistema destino.
* **Headers:** `Content-Type: application/json`, `Authorization: Bearer <TOKEN>`

**Estructura Payload JSON:**
```json
{
  "cuit": "20300000007",
  "alicuota_retencion": 3.6,
  "vigencia_desde": "2026-09-01",
  "vigencia_hasta": "2026-09-30"
}
```

---

### 3. Manejo de Errores y Retries

* **Reintentos:** 3 reintentos con retraso exponencial en caso de timeout (HTTP 504/502).
* **Logs:** Registro de fallas en `/var/log/app/integration.log`.

```

---

## 4. Plan de Pruebas (Test Plan) y Validación

Formato sugerido para la validación de circuitos funcionales con el usuario clave previa capacitación final.

```
# Casos de Prueba: [Nombre del Módulo o Circuito]

| ID Caso | Escenario | Pasos | Resultado Esperado | Estado | Notas / Evidencia |
| :-: | :--- | :--- | :--- | :-: | :--- |
| **TC-01** | Cobro combinado | 1. Cargar factura.<br>2. Registrar pago en tarjeta.<br>3. Registrar cheque. | Saldo en cero y asientos contables correctos. | Aprobado | OK en testing |
| **TC-02** | Aplicación Padrón Salta | 1. Seleccionar cliente.<br>2. Generar comprobante. | Se aplica alícuota correspondiente según JSON. | Pendiente | Requiere ejecutar script previo |

```

---

## 5. Guía de Usuario / Capacitación

Estructura para la entrega final de documentación operacional para usuarios finales.

```
# Manual de Usuario: [Nombre del Proceso / Área]

## 1. Introducción
Breve resumen sobre el objetivo del proceso y quiénes deben ejecutarlo.

## 2. Prerrequisitos
- Permisos requeridos en el sistema.
- Datos previos que deben estar dados de alta.

## 3. Paso a Paso

### Paso 1: Ingreso al Sistema
Navegar al menú **[Nombre de Menú] > [Submenú]**.

### Paso 2: Carga de Datos
Completar los siguientes campos:
* **Campo A:** Descripción.
* **Campo B:** Descripción (Obligatorio).

> **Nota importante:** Si el cliente pertenece a una jurisdicción especial, verificar la posición fiscal antes de confirmar.

### 4. Preguntas Frecuentes y Solución de Problemas (FAQ)
* **¿Qué hacer si el sistema lanza error X?**
  * *Solución:* Verificar que el CUIT esté registrado en el padrón actualizado.

```