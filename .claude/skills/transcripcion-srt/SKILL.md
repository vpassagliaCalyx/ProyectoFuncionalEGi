---
name: transcripcion-srt
description: Reglas para leer transcripciones de reuniones (.srt, .vtt, .txt o texto pegado) con ruido de audio y extraer la lógica operativa que se mostró y se habló. Usar siempre que la entrada para una minuta, instructivo o especificación sea una transcripción.
---

# Cómo leer transcripciones de reuniones

Las transcripciones tienen ruido de audio: texto repetido, frases cortadas y errores de reconocimiento. Esta skill define cómo leerlas y qué extraer. **No genera el documento final**: cuando termine, seguir con la skill del documento pedido (`minuta`, `manual-usuario`, etc.).

## Formato SRT
Cada segmento tiene un número, una marca de tiempo (`00:01:02,000 --> 00:01:05,000`) y el texto. Las marcas sirven para ubicar un punto dudoso en la grabación, no para el documento final.

## Proceso

1. **Leer completos todos los archivos de transcripción indicados** antes de escribir nada. Si no me dijeron cuáles son, preguntar.
2. **Ignorar el ruido**:
   - segmentos con texto repetido (ej. "sí, sí, sí, sí…" o "no, no, no…" durante 30 segundos);
   - palabras ininteligibles;
   - frases sin sentido gramatical.
3. **Extraer la lógica operativa**:
   - qué pasos se mostraron, en qué orden;
   - qué campos se mencionaron;
   - qué advertencias dio el consultor;
   - qué preguntas hizo el cliente: indican puntos de confusión y merecen una nota en el instructivo.
4. **No inventar pasos** que no se mencionaron. Si algo quedó pendiente en la reunión, indicarlo explícitamente en el documento con un bloque `note` (barra naranja).
5. **Respetar el vocabulario de adhoc**: posición fiscal, padrón, ARBA, CABA, CAE, remito, anticipo de clientes, créditos por venta, diario, asiento, etc. Si aparece un término parecido pero distinto, no corregirlo por cuenta propia: marcarlo `[VERIFICAR]`.

## Cautelas
- Una transcripción normalmente no dice quién habla. No atribuir una frase a una persona concreta salvo que quede claro; si importa, preguntarme.
- Números, CUIT, alícuotas, fechas y nombres propios pueden estar mal reconocidos. Marcarlos `[VERIFICAR]`.
- Lo que no se entiende queda como `[ININTELIGIBLE]`. No adivinar.
- No completar lo que "seguramente" se hace en el sistema. Si no se dijo ni se mostró, no entra.
- No copiar frases textuales entre comillas salvo que sean literales en la transcripción.

## Resultado de la lectura
Antes de redactar el documento, armar para mí un resumen breve con:
1. **Pasos y orden** en que se mostró el circuito.
2. **Campos y rutas de menú** mencionados.
3. **Advertencias** del consultor.
4. **Preguntas del cliente** (puntos de confusión).
5. **Pendientes** que quedaron abiertos.
6. **Dudas de lectura**: términos, cifras o segmentos marcados `[VERIFICAR]` o `[ININTELIGIBLE]`, con su marca de tiempo.
7. **Ruido descartado**, en una línea.

Si hay dudas que cambian el contenido del documento, preguntármelas antes de generarlo.
