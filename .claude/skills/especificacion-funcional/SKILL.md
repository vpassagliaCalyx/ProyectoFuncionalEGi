---
name: especificacion-funcional
description: Genera una especificación funcional (requerimiento / historia de usuario) de Calyx para desarrollos a medida o parametrizaciones. Usar cuando se pida documentar, completar o revisar un requerimiento funcional.
---

# Especificación funcional

Fuente del formato: `contexto/guia-formatos.md`, sección "Documento de Requisito Funcional".

## Estructura
1. **Encabezado**: logos del proveedor (Calyx, y PGK/TGS si corresponde) y del cliente.
2. **Título**: "Especificación Funcional: [Nombre del Requerimiento]".
3. **Tabla de datos**: ID Requerimiento (REQ-XXX), Fecha de Creación, Autor, Revisor/Aprobador, Estado (Borrador / En Revisión / Aprobado).
4. **1. Contexto y Objetivo**: problema o necesidad actual y objetivo de la solución.
5. **2. Alcance**: dentro y fuera del alcance.
6. **3. Criterios de Aceptación**: una o más historias de usuario (Como / Quiero / Para) con criterios de validación en formato "Dado / cuando / entonces".
7. **4. Flujo del Proceso**: paso a paso numerado.
8. **5. Reglas de Negocio**: RN-01, RN-02..., incluyendo excepciones.

## Reglas específicas
- Estado inicial: "Borrador". No marcar "Aprobado" sin que yo lo diga.
- ID de requerimiento: si no me lo pasaron o no se puede deducir de `memoria/`, `[COMPLETAR]`. No inventar numeración.
- Reglas de negocio fiscales, financieras o impositivas: solo las que estén en las entradas o que yo aporte. Si hay que suponer una, "estoy suponiendo" y marcarla para verificar.
- Alcance excluido: solo lo que se haya dicho o claramente se infiera; lo demás, preguntarme.
- No inventar nombres de módulos, campos, menús o servicios del sistema destino. Usar `[VERIFICAR EN SISTEMA]`.
- Cada historia de usuario debe poder probarse con sus criterios de validación.

## Salida
`salidas/AAAA-MM-DD_espec-funcional_<cliente>_<requerimiento>.docx`

Generar el Word con la skill `documentos-calyx-pgk` (ver `CLAUDE.md`, sección "Generación del Word").
