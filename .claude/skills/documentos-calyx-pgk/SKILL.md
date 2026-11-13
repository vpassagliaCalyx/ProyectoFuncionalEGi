---
name: documentos-calyx-pgk
description: Generador del archivo Word (.docx) con identidad Calyx y PGK/TGS a partir de un spec.json (logos, colores, tablas, notas). Usar al final, una vez definido el contenido con la skill del documento pedido (minuta, especificaciones, plan de pruebas, manual de usuario).
---

# Documentos corporativos Calyx / PGK-TGS

Genera documentos de proyecto (.docx) con los logos, colores y estructuras estándar del equipo.

## Cuándo usar
Minuta de reunión, especificación funcional / historia de usuario / requisito, especificación técnica de integración o script, plan de pruebas (casos de prueba), manual de usuario o guía de capacitación.

## Flujo
1. Elegir la plantilla en `references/plantillas.md` (leerla antes de redactar; contiene la estructura exacta de cada documento):
   - Minuta → sección 1 · Requisito funcional → sección 2 · Spec técnica → sección 3 · Plan de pruebas → sección 4 · Manual de usuario → sección 5.
2. Completar solo con datos que dio la persona. Lo que falte se deja como placeholder (`[Nombre - Cargo]`, `DD/MM/AAAA`). No inventar fechas, nombres, alícuotas, CUIT ni datos fiscales. Si se supone algo, decirlo en la respuesta.
3. Escribir `salidas/<nombre>.spec.json` y generar el Word desde la raíz del proyecto:
   `node .claude/skills/documentos-calyx-pgk/scripts/build_docx.js salidas/<nombre>.spec.json salidas/<nombre>.docx`
   Requiere Node y el paquete `docx`. Si `require('docx')` falla, avisar antes de ejecutar `npm install docx`.
4. Verificar: si hay LibreOffice (`soffice`) disponible, convertir a PDF y revisar el resultado. Si no, decir que no se pudo verificar visualmente.
5. Informar la ruta del archivo en `salidas/`, los campos que quedaron `[COMPLETAR]` y los supuestos.

## Identidad visual (ya aplicada por el script)
- Encabezado: logo Calyx (izquierda), PGK/TGS (centro), cliente (derecha). Logos en `assets/`.
- Plantilla 2 (requisito funcional): usar `"encabezado": "proveedor_cliente"` para omitir PGK/TGS.
- Fuente Arial. Título 20 pt, secciones 15 pt, cuerpo 10,5 pt; todo en negrita para títulos.
- Azul `#004070` (títulos, encabezados de tabla), naranja `#E85E00` (acentos, estados pendientes), gris `#F4F4F4` (filas alternas, código).
- Si hay logo del cliente (archivo PNG/JPG), pasarlo en `logo_cliente` con `logo_cliente_w` y `logo_cliente_h` en px. Si no, usar `cliente` (texto).
- Los logos tienen baja resolución (≈135 px de ancho). Si la persona tiene versiones más grandes, reemplazar los archivos de `assets/` conservando el nombre.

## Formato de spec.json
```json
{
  "titulo": "Minuta de Reunión",
  "subtitulo": "opcional",
  "cliente": "Nombre cliente",
  "logo_cliente": "/ruta/logo.png", "logo_cliente_w": 130, "logo_cliente_h": 50,
  "encabezado": "proveedor_cliente",
  "pie": "texto del pie de página",
  "ficha": [["Campo", "Detalle"]],
  "secciones": [
    {"titulo": "1. Resumen Ejecutivo", "nivel": 1, "bloques": [ ... ]}
  ]
}
```
`ficha` es la tabla Campo/Detalle del inicio (`\n` separa líneas dentro de una celda).

Bloques (`type`):
- `p` (`text`) · `h3` (`text`) · `note` (`text`, barra naranja: pendientes y advertencias)
- `bullets` / `numbered` / `checks` (`items`: lista de textos; `checks` son casillas ☐ para criterios de validación). En `bullets` y `numbered`, un item puede ser `{"text": "Paso", "sub": ["sub-ítem 1", "sub-ítem 2"]}` para sub-ítems indentados (solo un nivel).
- `table` (`cols`, `rows`, opcional `widths` en proporciones, `center` con índices de columnas, `firstColBold`)
- `code` (`text`, bloque monoespaciado gris: JSON, diagramas de flujo)
- `pagebreak`

Texto inline: `**negrita**` y `` `código` ``. Una columna cuyo encabezado contiene "Estado" pinta en naranja los valores "Pendiente", "Bloqueado" o "Rechazado".

## Reglas de contenido
- Escribir en español rioplatense neutro, tono profesional, frases concisas.
- Minuta: acuerdos como lista numerada; action items en tabla `# | Acción / Tarea | Responsable | Fecha Límite | Estado`.
- Requisito funcional: ID `REQ-XXX`, historias "Como / Quiero / Para", criterios con `checks`, reglas de negocio `RN-01`, `RN-02`.
- Plan de pruebas: IDs `TC-01`, `TC-02`; tabla con ID, escenario, pasos (con `\n`), resultado esperado, estado, notas.
- No atribuir frases o decisiones a personas reales si no fueron dichas por ellas en lo que la persona compartió.
