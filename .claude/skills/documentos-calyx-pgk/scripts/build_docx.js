#!/usr/bin/env node
// Uso: node build_docx.js spec.json salida.docx
// Genera un .docx con encabezado de logos, tipografía y colores corporativos.
// Ver SKILL.md para el formato del spec JSON.
const fs = require("fs");
const path = require("path");
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell, ImageRun,
  Header, Footer, AlignmentType, LevelFormat, BorderStyle, WidthType,
  ShadingType, PageNumber, VerticalAlign,
} = require("docx");

const AZUL = "004070", NARANJA = "E85E00", GRIS = "F4F4F4", BORDE = "BFBFBF";
const FONT = "Arial";
const ASSETS = path.join(__dirname, "..", "assets");
const CONTENT_W = 9638; // A4, márgenes 2 cm (DXA)

const [specPath, outPath] = process.argv.slice(2);
if (!specPath || !outPath) {
  console.error("Uso: node build_docx.js spec.json salida.docx");
  process.exit(1);
}
const spec = JSON.parse(fs.readFileSync(specPath, "utf8"));
const numberingConfigs = [];
let listCounter = 0;

// ---- texto inline: **negrita**, `código` ----
function runs(text, base = {}) {
  const out = [];
  const re = /(\*\*[^*]+\*\*|`[^`]+`)/g;
  String(text).split(re).filter((s) => s !== "").forEach((part) => {
    if (part.startsWith("**")) out.push(new TextRun({ text: part.slice(2, -2), bold: true, font: FONT, ...base }));
    else if (part.startsWith("`")) out.push(new TextRun({ text: part.slice(1, -1), font: "Consolas", ...base }));
    else out.push(new TextRun({ text: part, font: FONT, ...base }));
  });
  return out;
}
const P = (text, opts = {}, base = {}) =>
  new Paragraph({ spacing: { after: 100 }, ...opts, children: runs(text, { size: 21, ...base }) });

// ---- encabezado con logos ----
function logo(file, w, h) {
  return new ImageRun({
    type: "png",
    data: fs.readFileSync(path.join(ASSETS, file)),
    transformation: { width: w, height: h },
    altText: { title: file, description: file, name: file },
  });
}
const noB = { style: BorderStyle.NONE, size: 0, color: "FFFFFF" };
const noBorders = { top: noB, bottom: noB, left: noB, right: noB };
function headerCell(children, align, width) {
  return new TableCell({
    width: { size: width, type: WidthType.DXA }, borders: noBorders,
    verticalAlign: VerticalAlign.CENTER,
    children: [new Paragraph({ alignment: align, children })],
  });
}
function buildHeader() {
  const w3 = [3200, 3238, 3200];
  let clienteChildren = [];
  if (spec.logo_cliente && fs.existsSync(spec.logo_cliente)) {
    clienteChildren = [new ImageRun({
      type: spec.logo_cliente.toLowerCase().endsWith(".png") ? "png" : "jpg",
      data: fs.readFileSync(spec.logo_cliente),
      transformation: { width: spec.logo_cliente_w || 130, height: spec.logo_cliente_h || 50 },
      altText: { title: "Logo cliente", description: "Logo cliente", name: "cliente" },
    })];
  } else if (spec.cliente) {
    clienteChildren = [new TextRun({ text: spec.cliente, font: FONT, bold: true, size: 22, color: AZUL })];
  }
  const useProveedorSolo = spec.encabezado === "proveedor_cliente"; // plantilla 2: sin PGK
  const centro = useProveedorSolo ? [] : [logo("logo_pgk_tgs.png", 102, 56)];
  return new Header({
    children: [
      new Table({
        width: { size: CONTENT_W, type: WidthType.DXA }, columnWidths: w3,
        borders: { top: noB, bottom: noB, left: noB, right: noB, insideHorizontal: noB, insideVertical: noB },
        rows: [new TableRow({ children: [
          headerCell([logo("logo_calyx.png", 117, 44)], AlignmentType.LEFT, w3[0]),
          headerCell(centro, AlignmentType.CENTER, w3[1]),
          headerCell(clienteChildren, AlignmentType.RIGHT, w3[2]),
        ] })],
      }),
      new Paragraph({ spacing: { after: 0 }, border: { bottom: { style: BorderStyle.SINGLE, size: 8, color: AZUL, space: 4 } }, children: [] }),
    ],
  });
}
const footer = new Footer({ children: [new Paragraph({
  alignment: AlignmentType.CENTER,
  children: [
    new TextRun({ text: (spec.pie || spec.titulo || "") + "   |   Página ", font: FONT, size: 16, color: "7F7F7F" }),
    new TextRun({ children: [PageNumber.CURRENT], font: FONT, size: 16, color: "7F7F7F" }),
    new TextRun({ text: " de ", font: FONT, size: 16, color: "7F7F7F" }),
    new TextRun({ children: [PageNumber.TOTAL_PAGES], font: FONT, size: 16, color: "7F7F7F" }),
  ],
})] });

// ---- tablas ----
const cellB = { style: BorderStyle.SINGLE, size: 4, color: BORDE };
const cellBorders = { top: cellB, bottom: cellB, left: cellB, right: cellB };
function cellParas(text, base, align) {
  return String(text).split("\n").map((l) => new Paragraph({ alignment: align || AlignmentType.LEFT, spacing: { after: 40 }, children: runs(l, { size: 20, ...base }) }));
}
function estadoColor(v) {
  const s = String(v).toLowerCase();
  if (/pendiente|bloqueado|rechazado/.test(s)) return NARANJA;
  return null;
}
function table(b) {
  const cols = b.cols, n = cols.length;
  const ratios = b.widths || cols.map(() => 1);
  const sum = ratios.reduce((a, c) => a + c, 0);
  let widths = ratios.map((r) => Math.floor((CONTENT_W * r) / sum));
  widths[n - 1] += CONTENT_W - widths.reduce((a, c) => a + c, 0);
  const center = new Set(b.center || []);
  const head = new TableRow({ tableHeader: true, children: cols.map((c, i) => new TableCell({
    width: { size: widths[i], type: WidthType.DXA }, borders: cellBorders,
    shading: { fill: AZUL, type: ShadingType.CLEAR, color: "auto" },
    margins: { top: 60, bottom: 60, left: 100, right: 100 },
    children: [new Paragraph({ alignment: center.has(i) ? AlignmentType.CENTER : AlignmentType.LEFT,
      children: [new TextRun({ text: c, bold: true, color: "FFFFFF", font: FONT, size: 20 })] })],
  })) });
  const body = b.rows.map((r, ri) => new TableRow({ cantSplit: true, children: r.map((v, i) => {
    const isEstado = /estado/i.test(cols[i]);
    const col = isEstado ? estadoColor(v) : null;
    const first = b.firstColBold && i === 0;
    return new TableCell({
      width: { size: widths[i], type: WidthType.DXA }, borders: cellBorders,
      shading: ri % 2 === 1 ? { fill: GRIS, type: ShadingType.CLEAR, color: "auto" } : undefined,
      margins: { top: 50, bottom: 50, left: 100, right: 100 },
      children: cellParas(v, { bold: first || !!col, color: col || undefined }, center.has(i) ? AlignmentType.CENTER : AlignmentType.LEFT),
    });
  }) }));
  return new Table({ width: { size: CONTENT_W, type: WidthType.DXA }, columnWidths: widths, rows: [head, ...body] });
}
// tabla campo/detalle (ficha)
const ficha = (rows) => table({ cols: ["Campo", "Detalle"], widths: [1, 3], rows, firstColBold: true });

// ---- bloques ----
function listRef(kind) {
  const ref = `${kind}-${++listCounter}`;
  numberingConfigs.push({ reference: ref, levels: [
    { level: 0, format: kind === "num" ? LevelFormat.DECIMAL : LevelFormat.BULLET,
      text: kind === "num" ? "%1." : "\u2022", alignment: AlignmentType.LEFT,
      style: { paragraph: { indent: { left: 720, hanging: 360 } }, run: { font: FONT } } },
    // nivel 1: sub-ítems (se piden con {"text": "...", "sub": ["...", "..."]})
    { level: 1, format: LevelFormat.BULLET, text: "\u2013", alignment: AlignmentType.LEFT,
      style: { paragraph: { indent: { left: 1260, hanging: 360 } }, run: { font: FONT } } },
  ] });
  return ref;
}
// items: texto, o {text, sub:[textos]} para sub-ítems indentados
function listParas(items, ref) {
  const mk = (t, level) => new Paragraph({ numbering: { reference: ref, level }, spacing: { after: 60 }, children: runs(t, { size: 21 }) });
  return items.flatMap((it) => typeof it === "string" ? [mk(it, 0)] : [mk(it.text, 0), ...(it.sub || []).map((x) => mk(x, 1))]);
}
function block(b) {
  switch (b.type) {
    case "p": return [P(b.text)];
    case "h3": return [new Paragraph({ spacing: { before: 200, after: 80 }, keepNext: true,
      children: [new TextRun({ text: b.text, bold: true, font: FONT, size: 24, color: AZUL })] })];
    case "bullets": return listParas(b.items, listRef("bul"));
    case "numbered": return listParas(b.items, listRef("num"));
    case "checks": return b.items.map((t) => new Paragraph({ indent: { left: 360, hanging: 360 }, spacing: { after: 60 }, children: [new TextRun({ text: "☐  ", font: "Segoe UI Symbol", size: 21 }), ...runs(t, { size: 21 })] }));
    case "table": return [table(b), new Paragraph({ spacing: { after: 120 }, children: [] })];
    case "ficha": return [ficha(b.rows), new Paragraph({ spacing: { after: 120 }, children: [] })];
    case "code": return b.text.split("\n").map((l) => new Paragraph({ spacing: { after: 0 }, shading: { type: ShadingType.CLEAR, fill: GRIS, color: "auto" }, indent: { left: 120, right: 120 }, children: [new TextRun({ text: l === "" ? " " : l, font: "Consolas", size: 18 })] }));
    case "note": return [new Paragraph({ spacing: { before: 80, after: 120 }, indent: { left: 200 }, border: { left: { style: BorderStyle.SINGLE, size: 18, color: NARANJA, space: 8 } }, children: runs(b.text, { size: 20, italics: true }) })];
    case "pagebreak": return [new Paragraph({ pageBreakBefore: true, children: [] })];
    default: throw new Error("Tipo de bloque desconocido: " + b.type);
  }
}
const H = (text, lvl) => new Paragraph({
  heading: lvl === 1 ? "Heading1" : "Heading2", keepNext: true,
  children: [new TextRun({ text, font: FONT })],
});

// ---- documento ----
const children = [];
children.push(new Paragraph({ style: "Title", children: [new TextRun({ text: spec.titulo, font: FONT })] }));
if (spec.subtitulo) children.push(P(spec.subtitulo, {}, { color: "595959" }));
if (spec.ficha) children.push(ficha(spec.ficha), new Paragraph({ spacing: { after: 160 }, children: [] }));
(spec.secciones || []).forEach((s) => {
  children.push(H(s.titulo, s.nivel || 1));
  (s.bloques || []).forEach((b) => children.push(...block(b)));
});

const doc = new Document({
  creator: spec.autor || "Calyx", title: spec.titulo,
  styles: {
    default: { document: { run: { font: FONT, size: 21 } } },
    paragraphStyles: [
      { id: "Title", name: "Title", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { font: FONT, size: 40, bold: true, color: AZUL },
        paragraph: { spacing: { before: 120, after: 160 } } },
      { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { font: FONT, size: 30, bold: true, color: AZUL },
        paragraph: { spacing: { before: 320, after: 120 }, keepNext: true, outlineLevel: 0 } },
      { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { font: FONT, size: 26, bold: true, color: AZUL },
        paragraph: { spacing: { before: 240, after: 100 }, keepNext: true, outlineLevel: 1 } },
    ],
  },
  numbering: { config: numberingConfigs },
  sections: [{
    properties: { page: { size: { width: 11906, height: 16838 }, margin: { top: 1700, bottom: 1134, left: 1134, right: 1134, header: 500, footer: 500 } } },
    headers: { default: buildHeader() }, footers: { default: footer }, children,
  }],
});
Packer.toBuffer(doc).then((buf) => { fs.writeFileSync(outPath, buf); console.log("OK ->", outPath); });
