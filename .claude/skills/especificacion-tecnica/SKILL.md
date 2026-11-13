---
name: especificacion-tecnica
description: Genera una especificación técnica de integración o script (APIs, web services, conectores entre sistemas, padrones). Usar cuando se pida documentar una integración, un script o un flujo de datos entre sistemas.
---

# Especificación técnica de integración

Fuente del formato: `contexto/guia-formatos.md`, sección "Especificación Técnica de Integración / Script".

## Estructura
1. **Título**: "Especificación Técnica: Integración [Sistema A] <-> [Sistema B]".
2. **Tabla de datos**: Módulo/Componente, Tecnología/Lenguaje, Autor Técnico.
3. **1. Arquitectura del Flujo**: diagrama de texto `[Origen] ---> (Procesador) ---> [Destino]`.
4. **2. Endpoints y Estructura de Datos**: por cada endpoint, método y ruta, descripción, headers y payload JSON.
5. **3. Manejo de Errores y Retries**: reintentos, códigos HTTP considerados, ubicación y formato de logs.

## Reglas específicas
- Endpoints, rutas, nombres de campos, headers y formatos de fecha: solo los que yo aporte o los que estén en código o documentación que me hayan dado. Si no, `[COMPLETAR]`.
- El JSON de ejemplo de la plantilla (CUIT, alícuota, vigencias) es ilustrativo: no usarlo en documentos reales.
- Nunca incluir tokens, claves ni credenciales. Usar `<TOKEN>` o `<CLAVE>` como placeholder.
- Si cito una API externa (por ejemplo AFIP/ARCA), solo referenciar documentación real que yo haya dado; si no hay fuente, "no tengo fuente".
- Reintentos, tiempos y rutas de log: si no están definidos, proponerlos marcados como "estoy suponiendo", no como hechos.
- Bloques de código con fondo gris `#F4F4F4`.

## Salida
`salidas/AAAA-MM-DD_espec-tecnica_<cliente>_<integracion>.docx`

Generar el Word con la skill `documentos-calyx-pgk` (ver `CLAUDE.md`, sección "Generación del Word").
