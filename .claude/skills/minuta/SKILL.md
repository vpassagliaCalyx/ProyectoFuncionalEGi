---
name: minuta
description: Genera una minuta de reunión formal de Calyx (con PGK/TGS y cliente) a partir de notas o transcripciones en entradas/. Usar cuando se pida armar, completar o revisar una minuta de reunión.
---

# Minuta de reunión

Fuente del formato: `contexto/guia-formatos.md`, sección "Minuta de Reunión". Si la guía y esta skill difieren, manda la guía y avisame.

## Datos de entrada
Leer en `entradas/` la nota o transcripción de la reunión. Si hay varias, preguntar cuál usar. Si es un `.srt`, aplicar primero la skill `transcripcion-srt`.

## Estructura del documento
1. **Encabezado**: logos Calyx + PGK/TGS + cliente (de `contexto/logos/`).
2. **Título**: "Minuta de Reunión".
3. **Tabla de datos** (Campo | Detalle): Reunión/Proyecto, Fecha, Objetivo, Participantes (separados por Cliente y por Calyx/PGK, con cargo), Documentos Asociados, Próxima Instancia.
4. **1. Resumen Ejecutivo**: metodología acordada (solo si se habló) y tópicos principales tratados, numerados.
5. **2. Acuerdos Alcanzados**: lista numerada de decisiones consensuadas.
6. **3. Pasos a Seguir**: tabla # | Acción / Tarea | Responsable | Fecha Límite | Estado.

## Reglas específicas
- Participantes, cargos y fecha: solo los que consten en la entrada. Si falta, `[COMPLETAR: ...]`.
- Un acuerdo es algo que la entrada muestra como decidido. Si es una idea o propuesta sin cierre, va en tópicos tratados, no en acuerdos. Si no queda claro, preguntarme.
- No poner frases textuales entre comillas ni atribuir dichos a una persona salvo que estén literales en la entrada.
- Estado de las acciones: "Pendiente" por defecto; "En Progreso" o "Completado" solo si la entrada lo dice. Estado en naranja `#E85E00`.
- No copiar los temas de ejemplo de la plantilla (pagos combinados, DGR Salta, alícuotas, AFIP/ARCA) si no se trataron en la reunión.
- Terminar con la lista de campos pendientes y supuestos.

## Salida
`salidas/AAAA-MM-DD_minuta_<cliente>_<tema>.docx`

Generar el Word con la skill `documentos-calyx-pgk` (ver `CLAUDE.md`, sección "Generación del Word").
