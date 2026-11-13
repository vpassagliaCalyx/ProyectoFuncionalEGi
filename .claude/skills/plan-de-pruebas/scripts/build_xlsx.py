"""Genera un plan de pruebas en Excel (.xlsx) con identidad Calyx / PGK-TGS a partir de un spec.json.

Uso (desde la raíz del proyecto):
    py -I .claude/skills/plan-de-pruebas/scripts/build_xlsx.py salidas/<nombre>.spec.json salidas/<nombre>.xlsx

Requiere openpyxl. Los logos requieren Pillow; si no está, el encabezado va en texto y se avisa.

spec.json:
{
  "titulo": "Casos de Prueba: <Módulo o Circuito>",
  "cliente": "...", "proyecto": "...", "version": "1.0", "fecha": "DD/MM/AAAA",
  "responsable": "[COMPLETAR]",
  "logo_cliente": "contexto/logos/<archivo>.png"   (opcional),
  "notas": ["texto", ...]                          (opcional, van en la portada),
  "estados": ["Pendiente", "Aprobado", "Fallido", "Bloqueado", "No aplica"]  (opcional),
  "hojas": [
    {"nombre": "<máx 31 caracteres>", "descripcion": "...",
     "casos": [
       {"id": "TC-001", "ref": "CU-WO-01", "cu": "ODOO_CU-2237", "prioridad": "P1",
        "escenario": "...", "precondiciones": "...", "datos": "...",
        "pasos": ["...", "..."], "resultado_esperado": "...", "evidencia_esperada": "...",
        "estado": "Pendiente", "observacion": "..."}
     ]}
  ]
}
"""
import json
import os
import sys

from openpyxl import Workbook
from openpyxl.formatting.rule import CellIsRule
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation

HERE = os.path.dirname(os.path.abspath(__file__))
LOGOS = os.path.normpath(os.path.join(HERE, "..", "..", "documentos-calyx-pgk", "assets"))

AZUL, NARANJA, GRIS = "004070", "E85E00", "F4F4F4"
FONT = "Arial"
ESTADOS_DEF = ["Pendiente", "Aprobado", "Fallido", "Bloqueado", "No aplica"]
ESTADO_COLOR = {  # (relleno, color de letra)
    "Pendiente": (NARANJA, "FFFFFF"),
    "Aprobado": ("C6EFCE", "006100"),
    "Fallido": ("FFC7CE", "9C0006"),
    "Bloqueado": ("7F7F7F", "FFFFFF"),
    "No aplica": ("D9D9D9", "000000"),
}

thin = Side(style="thin", color="BFBFBF")
BORDER = Border(left=thin, right=thin, top=thin, bottom=thin)
WRAP = Alignment(wrap_text=True, vertical="top")
CENTER = Alignment(horizontal="center", vertical="top", wrap_text=True)
F_BODY = Font(name=FONT, size=10)
F_HEAD = Font(name=FONT, size=10, bold=True, color="FFFFFF")
F_TITLE = Font(name=FONT, size=18, bold=True, color=AZUL)
F_SUB = Font(name=FONT, size=14, bold=True, color=AZUL)
F_LABEL = Font(name=FONT, size=10, bold=True, color=AZUL)
FILL_HEAD = PatternFill("solid", fgColor=AZUL)
FILL_ALT = PatternFill("solid", fgColor=GRIS)

# columnas de las hojas de casos: (encabezado, clave, ancho, centrado)
COLS = [
    ("ID Caso", "id", 9, True),
    ("Ref.", "ref", 12, True),
    ("CU", "cu", 15, True),
    ("Prioridad", "prioridad", 9, True),
    ("Escenario", "escenario", 34, False),
    ("Precondiciones", "precondiciones", 30, False),
    ("Datos de prueba", "datos", 32, False),
    ("Pasos", "pasos", 48, False),
    ("Resultado Esperado", "resultado_esperado", 48, False),
    ("Evidencia esperada", "evidencia_esperada", 24, False),
    ("Observación", "observacion", 40, False),
    ("Estado", "estado", 12, True),
    ("Resultado obtenido", "", 32, False),
    ("Notas / Evidencia", "", 32, False),
    ("Fecha ejecución", "", 12, True),
    ("Tester", "", 14, True),
    ("Defecto / ticket", "", 14, True),
]
HEAD_ROW = 4


def try_logo(ws, path, anchor, height_px):
    try:
        from openpyxl.drawing.image import Image as XLImage
        img = XLImage(path)
    except Exception:
        return False
    ratio = img.width / img.height if img.height else 1
    img.height = height_px
    img.width = int(height_px * ratio)
    ws.add_image(img, anchor)
    return True


def cell(ws, r, c, v, font=F_BODY, align=WRAP, fill=None, border=True):
    x = ws.cell(row=r, column=c, value=v)
    x.font, x.alignment = font, align
    if fill:
        x.fill = fill
    if border:
        x.border = BORDER
    return x


def main(spec_path, out_path):
    spec = json.load(open(spec_path, encoding="utf-8"))
    estados = spec.get("estados") or ESTADOS_DEF
    root = os.getcwd()
    wb = Workbook()

    # ------------------------------------------------------------ Portada / Resumen
    ws = wb.active
    ws.title = "Resumen"
    widths = [28, 14] + [12] * len(estados) + [12, 14]
    for i, w in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(i)].width = w
    ws.row_dimensions[1].height = 48
    logos_ok = try_logo(ws, os.path.join(LOGOS, "logo_calyx.png"), "A1", 45)
    logos_ok = try_logo(ws, os.path.join(LOGOS, "logo_pgk_tgs.png"), "C1", 45) and logos_ok
    if spec.get("logo_cliente"):
        try_logo(ws, os.path.join(root, spec["logo_cliente"]), "F1", 45)
    if not logos_ok:
        cell(ws, 1, 1, "Calyx  |  PGK Consultores / TGS" + (f"  |  {spec.get('cliente')}" if spec.get("cliente") else ""),
             font=Font(name=FONT, size=11, bold=True, color=AZUL), border=False)
        print("AVISO: no se pudieron insertar los logos (falta Pillow). El encabezado quedó en texto.")

    cell(ws, 3, 1, spec.get("titulo", "Casos de Prueba: [COMPLETAR]"), font=F_TITLE, align=Alignment(vertical="center"), border=False)
    meta = [("Cliente", spec.get("cliente", "[COMPLETAR]")), ("Proyecto", spec.get("proyecto", "[COMPLETAR]")),
            ("Versión", spec.get("version", "1.0")), ("Fecha", spec.get("fecha", "[COMPLETAR]")),
            ("Responsable", spec.get("responsable", "[COMPLETAR]"))]
    r = 5
    for k, v in meta:
        cell(ws, r, 1, k, font=F_LABEL)
        ws.merge_cells(start_row=r, start_column=2, end_row=r, end_column=len(widths))
        cell(ws, r, 2, v)
        r += 1
    for n in spec.get("notas", []):
        ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=len(widths))
        cell(ws, r, 1, n, font=Font(name=FONT, size=10, italic=True), border=False)
        ws.row_dimensions[r].height = 30
        r += 1

    # resumen por hoja (fórmulas vivas)
    r += 1
    cell(ws, r, 1, "Avance por hoja", font=F_SUB, border=False)
    r += 1
    head = ["Hoja", "Total"] + estados + ["Ejecutados", "% avance"]
    for j, h in enumerate(head, 1):
        cell(ws, r, j, h, font=F_HEAD, fill=FILL_HEAD, align=CENTER)
    first = r + 1
    est_col = get_column_letter([c[1] for c in COLS].index("estado") + 1)
    for h in spec["hojas"]:
        r += 1
        n = len(h["casos"])
        rng = f"'{h['nombre']}'!${est_col}${HEAD_ROW + 1}:${est_col}${HEAD_ROW + max(n, 1)}"
        cell(ws, r, 1, h["nombre"])
        cell(ws, r, 2, f"=COUNTA({rng})", align=CENTER)
        for j, e in enumerate(estados, 3):
            cell(ws, r, j, f'=COUNTIF({rng},"{e}")', align=CENTER)
        c_ej, c_av = 3 + len(estados), 4 + len(estados)
        aprob = get_column_letter(3 + estados.index("Aprobado")) if "Aprobado" in estados else None
        fall = get_column_letter(3 + estados.index("Fallido")) if "Fallido" in estados else None
        parts = [f"{x}{r}" for x in (aprob, fall) if x]
        cell(ws, r, c_ej, "=" + "+".join(parts) if parts else 0, align=CENTER)
        x = cell(ws, r, c_av, f"=IF(B{r}=0,0,{get_column_letter(c_ej)}{r}/B{r})", align=CENTER)
        x.number_format = "0%"
    r += 1
    cell(ws, r, 1, "Total", font=Font(name=FONT, size=10, bold=True))
    for j in range(2, len(head) + 1):
        col = get_column_letter(j)
        if j == len(head):
            x = cell(ws, r, j, f"=IF(B{r}=0,0,{get_column_letter(j - 1)}{r}/B{r})", font=Font(name=FONT, size=10, bold=True), align=CENTER)
            x.number_format = "0%"
        else:
            cell(ws, r, j, f"=SUM({col}{first}:{col}{r - 1})", font=Font(name=FONT, size=10, bold=True), align=CENTER)

    # resumen por CU
    cus = []
    for h in spec["hojas"]:
        for c in h["casos"]:
            for cu in [x.strip() for x in str(c.get("cu", "")).split(",") if x.strip()]:
                if cu not in cus:
                    cus.append(cu)
    if cus:
        r += 2
        cell(ws, r, 1, "Avance por CU", font=F_SUB, border=False)
        r += 1
        head2 = ["CU", "Total"] + estados
        for j, h in enumerate(head2, 1):
            cell(ws, r, j, h, font=F_HEAD, fill=FILL_HEAD, align=CENTER)
        cu_col = get_column_letter([c[1] for c in COLS].index("cu") + 1)
        for cu in cus:
            r += 1
            cell(ws, r, 1, cu)
            tot, by = [], {e: [] for e in estados}
            for h in spec["hojas"]:
                n = len(h["casos"])
                if not n:
                    continue
                a, b = HEAD_ROW + 1, HEAD_ROW + n
                cr = f"'{h['nombre']}'!${cu_col}${a}:${cu_col}${b}"
                er = f"'{h['nombre']}'!${est_col}${a}:${est_col}${b}"
                tot.append(f'COUNTIF({cr},"*{cu}*")')
                for e in estados:
                    by[e].append(f'COUNTIFS({cr},"*{cu}*",{er},"{e}")')
            cell(ws, r, 2, "=" + "+".join(tot), align=CENTER)
            for j, e in enumerate(estados, 3):
                cell(ws, r, j, "=" + "+".join(by[e]), align=CENTER)

    # ------------------------------------------------------------ hojas de casos
    for h in spec["hojas"]:
        wsx = wb.create_sheet(h["nombre"][:31])
        cell(wsx, 1, 1, h["nombre"], font=F_SUB, align=Alignment(vertical="center"), border=False)
        cell(wsx, 2, 1, h.get("descripcion", ""), font=Font(name=FONT, size=10, italic=True), align=Alignment(vertical="top"), border=False)
        for j, (title, _, w, _) in enumerate(COLS, 1):
            cell(wsx, HEAD_ROW, j, title, font=F_HEAD, fill=FILL_HEAD, align=Alignment(wrap_text=True, vertical="center", horizontal="center"))
            wsx.column_dimensions[get_column_letter(j)].width = w
        wsx.row_dimensions[HEAD_ROW].height = 30
        for i, c in enumerate(h["casos"]):
            rr = HEAD_ROW + 1 + i
            fill = FILL_ALT if i % 2 else None
            for j, (_, key, _, center) in enumerate(COLS, 1):
                v = c.get(key, "") if key else ""
                if key == "pasos" and isinstance(v, list):
                    v = "\n".join(f"{k}. {p}" for k, p in enumerate(v, 1))
                if key == "estado" and not v:
                    v = "Pendiente"
                cell(wsx, rr, j, v, align=CENTER if center else WRAP, fill=fill)
        n = len(h["casos"])
        last = HEAD_ROW + max(n, 1)
        ec = [c[1] for c in COLS].index("estado") + 1
        el = get_column_letter(ec)
        dv = DataValidation(type="list", formula1='"' + ",".join(estados) + '"', allow_blank=False,
                            showErrorMessage=True, errorTitle="Estado inválido", error="Elegí un estado de la lista.")
        wsx.add_data_validation(dv)
        dv.add(f"{el}{HEAD_ROW + 1}:{el}{last}")
        fc = [c[0] for c in COLS].index("Fecha ejecución") + 1
        dvd = DataValidation(type="date", operator="greaterThan", formula1="36526", allow_blank=True,
                             showErrorMessage=True, error="Ingresá una fecha (DD/MM/AAAA).")
        wsx.add_data_validation(dvd)
        dvd.add(f"{get_column_letter(fc)}{HEAD_ROW + 1}:{get_column_letter(fc)}{last}")
        for rr in range(HEAD_ROW + 1, last + 1):
            wsx.cell(row=rr, column=fc).number_format = "DD/MM/YYYY"
        for e, (bg, fg) in ESTADO_COLOR.items():
            if e in estados:
                wsx.conditional_formatting.add(
                    f"{el}{HEAD_ROW + 1}:{el}{last}",
                    CellIsRule(operator="equal", formula=[f'"{e}"'], fill=PatternFill("solid", fgColor=bg),
                               font=Font(name=FONT, size=10, bold=True, color=fg)))
        wsx.freeze_panes = wsx.cell(row=HEAD_ROW + 1, column=5)
        wsx.auto_filter.ref = f"A{HEAD_ROW}:{get_column_letter(len(COLS))}{last}"
        wsx.page_setup.orientation = "landscape"
        wsx.page_setup.fitToWidth = 1
        wsx.page_setup.fitToHeight = 0
        wsx.sheet_properties.pageSetUpPr.fitToPage = True
        wsx.print_title_rows = f"{HEAD_ROW}:{HEAD_ROW}"

    wb.save(out_path)
    total = sum(len(h["casos"]) for h in spec["hojas"])
    print(f"OK: {out_path} ({len(spec['hojas'])} hojas, {total} casos)")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit("Uso: build_xlsx.py <spec.json> <salida.xlsx>")
    main(sys.argv[1], sys.argv[2])
