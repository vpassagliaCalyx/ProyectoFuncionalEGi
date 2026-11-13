---
name: plan-de-pruebas
description: Genera un plan de pruebas en Excel (casos de prueba y validación de circuitos) para marcar la ejecución, con identidad Calyx / PGK-TGS. Usar cuando se pida armar o completar casos de prueba o un plan de pruebas de un módulo, circuito o integración.
---

# Plan de pruebas (Excel)

Fuente del contenido: `contexto/guia-formatos.md`, sección "Plan de Pruebas (Test Plan) y Validación".
La salida es **Excel (.xlsx)**, no Word, para que el equipo marque el estado de cada prueba.

## Estructura del archivo
1. **Hoja "Resumen"** (portada):
   - Logos Calyx + PGK/TGS (+ cliente si hay logo), título "Casos de Prueba: [Módulo o Circuito]".
   - Datos: cliente, proyecto, versión, fecha, responsable.
   - Avance por hoja y por CU con fórmulas vivas (se actualiza solo al marcar estados).
2. **Una hoja por módulo, modelo o circuito**, con la tabla:
   ID Caso | Ref. | CU | Prioridad | Escenario | Precondiciones | Datos de prueba | Pasos | Resultado Esperado | Evidencia esperada | Observación | **Estado** | Resultado obtenido | Notas / Evidencia | Fecha ejecución | Tester | Defecto / ticket
   - IDs: TC-001, TC-002, ... (únicos en todo el archivo). "Ref." guarda el ID de origen (CU, HU, etc.) cuando exista.
   - Pasos numerados dentro de la celda.
   - Estado con lista desplegable: Pendiente / Aprobado / Fallido / Bloqueado / No aplica, con colores (Pendiente en naranja `#E85E00`).
   - Las columnas desde "Resultado obtenido" quedan vacías para quien ejecuta.

## Reglas específicas
- Los casos salen de las especificaciones y entradas disponibles (`salidas/`, `entradas/`, `contexto/`). No inventar escenarios que no estén respaldados; si propongo casos extra, marcarlos como "propuesto" en Observación.
- **Estado inicial: "Pendiente"**. "Bloqueado" solo si falta una muestra o definición (explicarlo en Observación). "Aprobado" solo si hay evidencia en las entradas y yo lo confirmo.
- Resultados esperados concretos y verificables. Si dependen de una regla fiscal o contable que no está en las entradas, `[VERIFICAR]`. Nombres de campos o métodos no confirmados: `[VERIFICAR EN SISTEMA]`.
- Los ejemplos de la plantilla (cobro combinado, padrón Salta) no se copian.

## Generación
1. Armar `salidas/AAAA-MM-DD_plan-pruebas_<cliente>_<modulo>.spec.json` con el formato documentado al inicio de `scripts/build_xlsx.py`.
2. Ejecutar desde la raíz del proyecto:
   `py -I .claude/skills/plan-de-pruebas/scripts/build_xlsx.py salidas/<nombre>.spec.json salidas/<nombre>.xlsx`
3. Requiere `openpyxl`. Los logos requieren `Pillow`: si falta, el script pone el encabezado en texto y avisa; preguntarme antes de instalar nada.

## Salida
`salidas/AAAA-MM-DD_plan-pruebas_<cliente>_<modulo>.xlsx` (y su `.spec.json` al lado).
