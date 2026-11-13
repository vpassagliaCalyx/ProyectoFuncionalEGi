---
name: manual-usuario
description: Genera un manual de usuario, instructivo o guía de capacitación para usuarios finales de un proceso. Usar cuando se pida armar documentación operativa paso a paso.
---

# Manual de usuario / Guía de capacitación

Fuente del formato: `contexto/guia-formatos.md`, sección "Guía de Usuario / Capacitación".

## Estructura
1. **Título**: "Manual de Usuario: [Proceso / Área]".
2. **1. Introducción**: objetivo del proceso y quién lo ejecuta.
3. **2. Prerrequisitos**: permisos y datos previos.
4. **3. Paso a Paso**: pasos numerados con ruta de menú, campos a completar (indicar los obligatorios) y notas importantes en recuadro.
5. **4. Preguntas Frecuentes y Solución de Problemas**: pregunta, solución.

## Reglas específicas
- Rutas de menú, nombres de campos y mensajes de error: solo los que estén en mis entradas o capturas. Si no, `[VERIFICAR EN SISTEMA]`. No describir pantallas de memoria.
- Permisos requeridos: `[COMPLETAR]` si no los tengo.
- FAQ: solo problemas que aparezcan en las entradas o que yo cite. No inventar errores.
- Lenguaje simple, dirigido a usuario final, un paso por acción.
- Si hay capturas de pantalla en `entradas/`, indicar en qué paso van, sin describir lo que no se ve.

## Entrada en formato SRT
Si la entrada es una transcripción `.srt`, aplicar primero la skill `transcripcion-srt`.

## Convenciones de redacción
- Trato cercano y operativo, en la forma de estos ejemplos: "hacé clic", "verificá", "seleccioná".
- Frases cortas. Máximo 2 oraciones por paso.
- Pasos: siempre en un bloque `numbered`.
- Sub-ítems de un paso: campo `sub` del item (nivel 1 indentado).
- Campos de pantalla: **negrita**.
- Rutas de menú: módulo → submenú → opción (separados por →).
- Nunca escribir viñetas Unicode (•) a mano en el texto; usar los bloques `bullets` / `numbered`.
- Pendientes de la reunión y advertencias del consultor: bloque `note` (barra naranja).

## Salida
`salidas/AAAA-MM-DD_manual_<cliente>_<proceso>.docx`

Generar el Word con la skill `documentos-calyx-pgk` (ver `CLAUDE.md`, sección "Generación del Word").
