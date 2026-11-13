# Proyecto: Documentación Calyx

Proyecto para generar y completar documentación de consultoría de Calyx (junto a PGK Consultores / TGS y el cliente de cada proyecto): minutas, especificaciones funcionales y técnicas, planes de prueba y manuales de usuario.

## Estructura de carpetas

- `contexto/`: material de referencia fijo. No se modifica salvo que yo lo pida.
  - `contexto/guia-formatos.md`: formatos, plantillas, paleta y tipografía. **Es la fuente de verdad del formato.**
  - `contexto/logos/`: logos de Calyx (`calyx.png`), PGK/TGS (`pgk-tgs.png`) y de clientes.
- `memoria/`: lo que se aprende del trabajo (`clientes.md`, `decisiones.md`). Se actualiza solo con mi confirmación.
- `entradas/`: notas, transcripciones o pedidos crudos que yo dejo para procesar.
- `salidas/`: documentos generados.
- `.claude/skills/`: una skill por tipo de documento, más `transcripcion-srt` (lectura de transcripciones) y `documentos-calyx-pgk` (generador del Word).
- `.claude/agents/`: agente documentador.

## Cómo trabajar

0. **Proyecto EG (integración Metrics ↔ Odoo):** leer primero `memoria/EG_contexto-proyecto.md`. Tiene el resumen de todas las fuentes; abrir los originales solo si falta un detalle.
1. Antes de generar cualquier documento, leer `contexto/guia-formatos.md` y el archivo de `memoria/` del cliente correspondiente, si existe.
2. Si la entrada es una transcripción, aplicar primero la skill `transcripcion-srt`.
3. Identificar el tipo de documento y usar la skill que corresponda. Si no existe, avisarme.
4. Completar la plantilla solo con datos que estén en `entradas/`, en `memoria/` o que yo haya dicho en la conversación.
5. Generar el Word (ver "Generación del Word"), o el Excel en el caso del plan de pruebas, y guardarlo en `salidas/` con el nombre `AAAA-MM-DD_tipo_cliente_tema`.
6. Al terminar, decirme qué campos quedaron sin completar y qué supuestos hice.

## Skills disponibles y faltantes

- Existentes en `.claude/skills/`: `transcripcion-srt`, `minuta`, `especificacion-funcional`, `especificacion-tecnica`, `plan-de-pruebas`, `manual-usuario`, `documentos-calyx-pgk`.
- Si pido un tipo de documento que no tiene skill, avisarme y proponer crearla a partir de `contexto/guia-formatos.md`. Mostrarme el `SKILL.md` antes de guardarlo y crearla solo si confirmo.

## Generación del Word

- Las skills de cada documento definen el **contenido**; la skill `documentos-calyx-pgk` arma el **archivo .docx** (logos, colores, tablas) a partir de un `spec.json`.
- Guardar el `spec.json` en `salidas/` junto al documento y ejecutar el script que indica esa skill.
- Requiere Node y el paquete `docx`. Si falta, avisarme antes de instalar nada.
- Las listas admiten un nivel de sub-ítems; las notas y pendientes van en bloques `note` (barra naranja).

## Reglas de contenido (no negociables)

- **No inventar.** Si falta un dato (fecha, responsable, cargo, alícuota, nombre de módulo), dejar `[COMPLETAR: descripción]` en el documento. No rellenar con ejemplos de la plantilla.
- **Supuestos explícitos.** Si hay que suponer algo, escribir "estoy suponiendo" y dejarlo marcado en el documento.
- **No poner palabras en boca de personas reales.** En minutas, solo registrar acuerdos y dichos que figuren en `entradas/`. Si hay dudas sobre quién dijo o decidió algo, preguntarme.
- **Números y normativa.** Alícuotas, fechas de vigencia, importes y normas fiscales (AFIP/ARCA, rentas provinciales, etc.) solo se copian de las fuentes que yo aporte. Si hay que estimar algo, indicarlo como estimación y pedirme que lo verifique.
- **No inventar funciones de herramientas.** Nombres de módulos, campos, menús o pasos de un sistema (Odoo u otro) solo si están en mis entradas o en documentación que se pueda citar. Si no, marcar `[VERIFICAR EN SISTEMA]`.
- **Fuentes.** No inventar enlaces, libros ni normas. Si no hay fuente real, decir "no tengo fuente".
- **Datos de ejemplo de las plantillas** (nombres propios, jurisdicciones, alícuotas) son solo ilustrativos. Nunca pasarlos a un documento real.
- Si mi pedido no es claro, preguntarme antes de generar. Una pregunta por vez.

## Formato de los documentos

Detalle completo en `contexto/guia-formatos.md`. Resumen:

- Salida en Word (.docx), salvo que pida otra cosa. **Excepción: el plan de pruebas sale en Excel (.xlsx)** para marcar la ejecución; lo genera la propia skill `plan-de-pruebas` (no usa `documentos-calyx-pgk`).
- Logos en el encabezado: Calyx + PGK/TGS + cliente cuando corresponda (ya los aplica el generador).
- Tipografía: Arial, Segoe UI o Calibri. Título 18-20 pt negrita, secciones 14-16 pt negrita, cuerpo y tablas 10-11 pt.
- Colores: azul `#004070` (títulos y encabezados de tabla), naranja `#E85E00` (acentos y estados), gris `#F4F4F4` (filas alternas y bloques de código).
- Idioma: español rioplatense neutro, tono profesional.

## Memoria

- Al cerrar un trabajo, proponerme qué agregar a `memoria/` (cliente, decisiones tomadas, términos del proyecto). Guardar solo si confirmo.
- **Al final de cada sesión del proyecto EG**, actualizar `memoria/EG_contexto-proyecto.md` con lo nuevo: decisiones, CU, pendientes resueltos o nuevos, hallazgos técnicos y archivos generados en `salidas/`. Cambiar la fecha de "Actualizado", mantenerlo corto (sin copiar fuentes) y decirme en una línea qué se cambió.
- No guardar datos sensibles (credenciales, tokens, claves) en ningún archivo del proyecto.
