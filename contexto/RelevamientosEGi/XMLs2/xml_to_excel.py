import xml.etree.ElementTree as ET
import openpyxl
from openpyxl.utils import get_column_letter
import os
import glob

def extract_attributes(element, parent_path=""):
    rows = []
    tag = element.tag.split('}')[-1] if '}' in element.tag else element.tag
    current_path = f"{parent_path}/{tag}" if parent_path else tag

    for attr_name, attr_value in element.attrib.items():
        label = f"{current_path} @{attr_name}"
        rows.append((label, attr_value))

    for child in element:
        rows.extend(extract_attributes(child, current_path))
        if child.text and child.text.strip():
            label = f"{current_path}/{child.tag.split('}')[-1] if '}' in child.tag else child.tag}/text"
            rows.append((label, child.text.strip()))

    return rows

wb = openpyxl.Workbook()
wb.remove(wb.active)

xml_files = glob.glob("*.xml")

for xml_file in sorted(xml_files):
    sheet_name = os.path.splitext(xml_file)[:24][0]
    ws = wb.create_sheet(title=sheet_name)

    ws['A1'] = "Etiqueta"
    ws['B1'] = "Dato"
    ws['A1'].font = openpyxl.styles.Font(bold=True)
    ws['B1'].font = openpyxl.styles.Font(bold=True)

    tree = ET.parse(xml_file)
    root = tree.getroot()

    data = extract_attributes(root)

    for i, (label, value) in enumerate(data, start=2):
        ws[f'A{i}'] = label
        ws[f'B{i}'] = value

    ws.column_dimensions['A'].width = 55
    ws.column_dimensions['B'].width = 40

output_file = "datos_exportados.xlsx"
wb.save(output_file)
print(f"Archivo creado: {output_file}")
print(f"Archivos procesados: {len(xml_files)}")
