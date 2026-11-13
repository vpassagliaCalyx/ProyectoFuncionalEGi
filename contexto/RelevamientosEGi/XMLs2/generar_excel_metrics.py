import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

wb = openpyxl.Workbook()

header_font = Font(bold=True, size=11, color="FFFFFF")
header_fill = PatternFill(start_color="2F5496", end_color="2F5496", fill_type="solid")
header_fill2 = PatternFill(start_color="548235", end_color="548235", fill_type="solid")
header_align = Alignment(horizontal="center", vertical="center", wrap_text=True)
cell_align = Alignment(vertical="top", wrap_text=True)
thin_border = Border(
    left=Side(style='thin'), right=Side(style='thin'),
    top=Side(style='thin'), bottom=Side(style='thin')
)

COLUMNS = [
    "Elemento ID", "Elemento XML", "Atributo", "Tipo", "Longitud",
    "Obligatorio", "Descripción", "Observaciones",
    "Modelo Odoo", "Campo Odoo", "Módulo Odoo"
]

def write_sheet(ws, title, data):
    ws.title = title
    for col_idx, header in enumerate(COLUMNS, 1):
        cell = ws.cell(row=1, column=col_idx, value=header)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = header_align
        cell.border = thin_border

    for row_idx, row_data in enumerate(data, 2):
        for col_idx, value in enumerate(row_data, 1):
            cell = ws.cell(row=row_idx, column=col_idx, value=value)
            cell.alignment = cell_align
            cell.border = thin_border

    ws.column_dimensions['A'].width = 14
    ws.column_dimensions['B'].width = 28
    ws.column_dimensions['C'].width = 26
    ws.column_dimensions['D'].width = 12
    ws.column_dimensions['E'].width = 12
    ws.column_dimensions['F'].width = 12
    ws.column_dimensions['G'].width = 50
    ws.column_dimensions['H'].width = 40
    ws.column_dimensions['I'].width = 22
    ws.column_dimensions['J'].width = 30
    ws.column_dimensions['K'].width = 20
    ws.auto_filter.ref = ws.dimensions
    ws.freeze_panes = "A2"

def write_complejo_sheet(ws, data):
    ws.title = "Mapeo Complejo"
    headers = ["ID Regla", "Origen (Metrics)", "Atributo Metrics", "Destino (Odoo)", "Campo Odoo", "Tipo Transformación", "Descripción / Regla", "Módulo Odoo"]
    for col_idx, header in enumerate(headers, 1):
        cell = ws.cell(row=1, column=col_idx, value=header)
        cell.font = header_font
        cell.fill = header_fill2
        cell.alignment = header_align
        cell.border = thin_border
    for row_idx, row_data in enumerate(data, 2):
        for col_idx, value in enumerate(row_data, 1):
            cell = ws.cell(row=row_idx, column=col_idx, value=value)
            cell.alignment = cell_align
            cell.border = thin_border
    ws.column_dimensions['A'].width = 12
    ws.column_dimensions['B'].width = 25
    ws.column_dimensions['C'].width = 25
    ws.column_dimensions['D'].width = 25
    ws.column_dimensions['E'].width = 30
    ws.column_dimensions['F'].width = 22
    ws.column_dimensions['G'].width = 65
    ws.column_dimensions['H'].width = 20
    ws.auto_filter.ref = ws.dimensions
    ws.freeze_panes = "A2"

# ========================
# Odoo Mapping Dictionary
# key = (elemento_xml, atributo) or (elemento_xml, '')
# value = (modelo_odoo, campo_odoo, modulo_odoo)
# ========================
ODOO_MAP = {}

def m(elemento, attr, modelo, campo, modulo):
    ODOO_MAP[(elemento, attr)] = (modelo, campo, modulo)

# --- CRM ---
m("<sdiCrmActor>", "Code", "res.partner", "ref", "base")
m("<sdiCrmActor>", "OwnerCode", "res.partner", "commercial_partner_id", "base")
m("<sdiCrmActor>", "PersonTypeCompl", "res.partner", "", "l10n_ar_ux")  # custom: branch type
m("<sdiCrmActor>", "PersonType", "res.partner", "company_type", "base")
m("<sdiCrmActor>", "IdCountry", "res.country", "id", "base")
m("<sdiCrmActor>", "CountryDocumentNumber", "res.partner", "vat", "base")
m("<sdiCrmActor>", "CountryDocumentNumber", "res.partner", "l10n_latam_identification_type_id", "l10n_ar")
m("<sdiCrmActor>", "StateDocumentNumber", "res.partner", "company_registry", "base")
m("<sdiCrmActor>", "CityDocumentNumber", "res.partner", "", "")  # custom field or x_city_document
m("<sdiCrmActor>", "Name", "res.partner", "name", "base")
m("<sdiCrmActor>", "FullName", "res.partner", "display_name", "base")
m("<sdiCrmActor>", "Phone", "res.partner", "phone", "base")
m("<sdiCrmActor>", "Website", "res.partner", "website", "base")
m("<sdiCrmActor>", "Fax", "res.partner", "fax", "base")
m("<sdiCrmActor>", "Note", "res.partner", "comment", "base")
m("<sdiCrmActor>", "ExtRef", "res.partner", "ref", "base")
m("<sdiCrmActor>", "ExtRefOwnerCode", "res.partner", "", "")  # custom
m("<sdiCrmActor>", "IsActv", "res.partner", "active", "base")
m("<sdiCrmActor>", "IsCustomer", "res.partner", "customer_rank", "base")
m("<sdiCrmActor>", "IsSupplier", "res.partner", "supplier_rank", "base")
m("<sdiCrmActor>", "IsPerson", "res.partner", "company_type", "base")
m("<sdiCrmActor>", "IsBroker", "res.partner", "", "")  # custom
m("<sdiCrmActor>", "isCustomerService", "res.partner", "", "")  # discontinued
m("<sdiCrmActor>", "IsRepres", "res.partner", "", "")  # custom: is representative
m("<sdiCrmActor>", "IsTransport", "res.partner", "", "")  # custom: is carrier
m("<sdiCrmActor>", "CountryCode", "res.partner", "country_id", "base")
m("<sdiCrmActor>", "CountryFiscalCode", "res.partner", "l10n_ar_afip_responsibility_type_id", "l10n_ar")
m("<sdiCrmActor>", "UserFieldClassic1", "res.partner", "x_user_field1", "base")
m("<sdiCrmActor>", "UserFieldClassic2", "res.partner", "x_user_field2", "base")
m("<sdiCrmActor>", "UserFieldClassic3", "res.partner", "x_user_field3", "base")
m("<sdiCrmActor>", "UserFieldClassic4", "res.partner", "x_user_field4", "base")
m("<sdiCrmActor>", "UserFieldClassic5", "res.partner", "x_user_field5", "base")
m("<sdiCrmActor>", "ConditionPaymentStandard", "res.partner", "property_payment_term_id", "account")
m("<sdiCrmActor>", "Email", "res.partner", "email", "base")
m("<sdiCrmActor>", "Emailtax", "res.partner", "l10n_ar_afip_tax_email", "l10n_ar")
m("<sdiCrmActor>", "BroptingSimpleNational", "res.partner", "l10n_ar_afip_responsibility_type_id", "l10n_ar")
m("<sdiCrmActor>", "LimitValueCredit", "res.partner", "credit_limit", "base")
m("<sdiCrmActor>", "CreditExpirationDt", "res.partner", "credit_expiration_date", "base")  # custom
m("<sdiCrmActor>", "EmailBilling", "res.partner", "l10n_ar_afip_invoicing_email", "l10n_ar")
m("<sdiCrmActor>", "InvoiceCFOP", "res.partner", "property_account_position_id", "account")
m("<sdiCrmActor>", "ShippingCFOP", "res.partner", "property_account_position_id", "account")
m("<sdiCrmActor>", "InvoiceandShippingCFOP", "res.partner", "property_account_position_id", "account")
# Contacts
m("<sdiCrmActorContact>", "Code", "res.partner", "ref", "base")
m("<sdiCrmActorContact>", "Name", "res.partner", "name", "base")
m("<sdiCrmActorContact>", "FullName", "res.partner", "display_name", "base")
m("<sdiCrmActorContact>", "ExtRef", "res.partner", "ref", "base")
m("<sdiCrmActorContact>", "Phone", "res.partner", "phone", "base")
m("<sdiCrmActorContact>", "PhoneExtension", "res.partner", "", "")  # custom
m("<sdiCrmActorContact>", "MobilePhone", "res.partner", "mobile", "base")
m("<sdiCrmActorContact>", "EMail", "res.partner", "email", "base")
m("<sdiCrmActorContact>", "Division", "res.partner", "function", "base")
m("<sdiCrmActorContact>", "Note", "res.partner", "comment", "base")
m("<sdiCrmActorContact>", "BirthDate", "res.partner", "birthdate", "base")
m("<sdiCrmActorContact>", "TreatmentForm", "res.partner", "title", "base")
m("<sdiCrmActorContact>", "IsActv", "res.partner", "active", "base")
# Addresses
m("<sdiCrmAddress>", "IdAddress", "res.partner", "id", "base")
m("<sdiCrmAddress>", "CityCode", "res.city", "id", "base")
m("<sdiCrmAddress>", "AddressPrefix", "res.partner", "street", "base")
m("<sdiCrmAddress>", "AddressName", "res.partner", "street", "base")
m("<sdiCrmAddress>", "AddressNumber", "res.partner", "street", "base")
m("<sdiCrmAddress>", "AddressComplement", "res.partner", "street2", "base")
m("<sdiCrmAddress>", "District", "res.partner", "", "")  # custom or street3
m("<sdiCrmAddress>", "ZipCode", "res.partner", "zip", "base")
m("<sdiCrmAddress>", "Reference", "res.partner", "street3", "base")
m("<sdiCrmAddress>", "Note", "res.partner", "comment", "base")
m("<sdiCrmAddress>", "ExtRef", "res.partner", "ref", "base")
# Customer specific
m("<sdiCrmCustomer>", "SalesManCode", "res.partner", "user_id", "base")
m("<sdiCrmCustomer>", "Note", "res.partner", "comment", "base")
m("<sdiCrmCustomer>", "IsActv", "res.partner", "active", "base")

# --- STKItem ---
m("<sdiStkItem>", "idItem", "product.product", "id", "base")
m("<sdiStkItem>", "StockCode", "product.product", "default_code", "base")
m("<sdiStkItem>", "Status", "product.product", "active", "base")
m("<sdiStkItem>", "MaterialType", "product.category", "name", "base")
m("<sdiStkItem>", "ItemType", "product.product", "type", "base")
m("<sdiStkItem>", "MaterialName", "product.product", "name", "base")
m("<sdiStkItem>", "UnitCode", "product.product", "uom_id", "base")
m("<sdiStkItem>", "UnitCodeDemand", "product.product", "uom_po_id", "base")
m("<sdiStkItem>", "UnitCodeCost", "product.product", "cost_method", "base")
m("<sdiStkItem>", "Height", "product.product", "product_height", "base")
m("<sdiStkItem>", "Width", "product.product", "product_width", "base")
m("<sdiStkItem>", "Grammage", "product.product", "product_grammage", "base")  # custom
m("<sdiStkItem>", "CustomMaterialTypeCode", "product.category", "name", "base")
m("<sdiStkItem>", "CustomMaterialTypeDescription", "product.category", "description", "base")
m("<sdiStkItem>", "MaterialGroupCode", "product.product", "categ_id", "base")
m("<sdiStkItem>", "MaterialGroupDescription", "product.category", "name", "base")
m("<sdiStkItem>", "MasterMaterialGroupCode", "product.category", "parent_id", "base")
m("<sdiStkItem>", "MasterMaterialGroupDescription", "product.category", "parent_id.name", "base")
m("<sdiStkItem>", "UsesCtrlVolume", "product.product", "", "")  # custom
m("<sdiStkItem>", "NCM", "product.product", "l10n_latam_product_ncm", "l10n_latam")
m("<sdiStkItem>", "NCM", "product.product", "hs_code", "base")
m("<sdiStkItem>", "ISBN", "product.product", "isbn", "base")
m("<sdiStkItem>", "WeightKg", "product.product", "weight", "base")
m("<sdiStkItem>", "UnitWeight", "product.product", "weight", "base")
m("<sdiStkItem>", "EAN", "product.product", "barcode", "base")
m("<sdiStkItem>", "OriginItem", "product.product", "origin", "base")
m("<sdiStkItem>", "IsFSC", "product.product", "is_fsc", "base")  # custom
m("<sdiStkItem>", "Obs", "product.product", "description", "base")
m("<sdiStkItem>", "UseLot", "product.product", "tracking", "base")  # 'lot'
m("<sdiStkItem>", "UseAddress", "product.product", "storage_location", "stock")
m("<sdiStkItem>", "IsInventoried", "product.product", "inventory_valuation", "base")
m("<sdiStkItem>", "ControlTraceability", "product.product", "tracking", "base")  # 'serial'
m("<sdiStkItem>", "TipoItemSped", "product.product", "l10n_latam_product_sped_type", "l10n_ar")
m("<sdiStkItem>", "IsSupplied", "product.product", "purchase_ok", "base")
m("<sdiStkItem>", "FinancialNatureCode", "product.product", "product_nature_id", "account")
m("<sdiStkItem>", "BusinessUnitCode", "product.product", "business_unit_id", "base")  # custom
m("<sdiStkItem>", "PackagingQty", "product.product", "packaging_qty", "base")  # custom
m("<sdiStkItem>", "PackagingUnit", "product.product", "packaging_uom_id", "base")
m("<sdiStkItem>", "BillingDescription", "product.product", "description_sale", "base")
m("<sdiStkItem>", "ProductClassification", "product.product", "product_classification", "base")  # custom
m("<sdiStkItem>", "NeedSeparation", "product.product", "", "")  # custom
m("<sdiStkItem>", "DifferentLotsSeparation", "product.product", "", "")  # custom
m("<sdiStkItem>", "InvoiceItemType", "product.product", "invoice_policy", "base")
m("<sdiStkItem>", "ShippingItemType", "product.product", "shipping_policy", "base")

# --- STK ---
m("<sdistktransaction>", "transactiontype", "stock.picking", "picking_type_id", "stock")
m("<sdistktransaction>", "operationtype", "stock.move", "operation_type", "stock")
m("<sdistktransaction>", "transactiondt", "stock.move", "date", "stock")
m("<sdistktransaction>", "stockcode", "stock.move", "product_id", "stock")
m("<sdistktransaction>", "unitcode", "stock.move", "product_uom", "stock")
m("<sdistktransaction>", "quantity", "stock.move", "product_uom_qty", "stock")
m("<sdistktransaction>", "totalvalue", "stock.move", "price_unit", "stock")
m("<sdistktransaction>", "wonumber", "stock.move", "origin", "stock")
m("<sdistktransaction>", "stockplacecode", "stock.move", "location_id", "stock")
m("<sdistktransaction>", "stockplacecode", "stock.move", "location_dest_id", "stock")
m("<sdistktransaction>", "idcompany", "stock.move", "company_id", "base")
m("<sdistktransaction>", "lot", "stock.move", "lot_ids", "stock")
m("<sdistktransaction>", "expirationdate", "stock.lot", "expiration_date", "stock")
m("<sdistktransaction>", "productiondate", "stock.lot", "production_date", "stock")
m("<sdistktransaction>", "providerlot", "stock.lot", "supplier_lot", "stock")
m("<sdistktransaction>", "unitlot", "stock.lot", "uom_id", "stock")
m("<sdistktransaction>", "docnumber", "stock.picking", "name", "stock")
m("<sdistktransaction>", "docnumbercompl", "stock.picking", "origin", "stock")
m("<sdistktransaction>", "stockaddress", "stock.move.line", "location_dest_id", "stock")
m("<sdistktransaction>", "stockmovementtype", "stock.move", "type", "stock")  # in/out/internal
m("<sdistktransaction>", "costcentercode", "stock.move", "analytic_account_id", "analytic")
m("<sdistktransaction>", "costcentername", "account.analytic.account", "name", "analytic")
m("<sdistktransaction>", "transactioncode", "stock.picking", "origin", "stock")
m("<sdistktransaction>", "quantityunitcost", "stock.move", "quantity", "stock")
m("<sdistktransaction>", "unitcostcode", "stock.move", "price_unit", "stock")
m("<sdistktransaction>", "transactioncodeextref", "stock.picking", "origin", "stock")
m("<sdistktransaction>", "loguser", "stock.move", "write_uid", "base")
m("<sdistktransaction>", "grossweight", "stock.move.line", "weight", "stock")

# --- WO ---
m("<sdiwoworkorderinfo>", "idcompany", "mrp.production", "company_id", "base")
m("<sdiwoworkorderinfo>", "wonumber", "mrp.production", "name", "mrp")
m("<sdiwoworkorderinfo>", "wodescription", "mrp.production", "origin", "mrp")
m("<sdiwoworkorderinfo>", "quotenumber", "mrp.production", "origin", "mrp")
m("<sdiwoworkorderinfo>", "status", "mrp.production", "state", "mrp")
m("<sdiwoworkorderinfo>", "insertdt", "mrp.production", "date_planned_start", "mrp")
m("<sdiwoworkorderinfo>", "projectcode", "mrp.production", "project_id", "project")
m("<sdiwoworkorderinfo>", "projecttitle", "mrp.production", "analytic_account_id", "analytic")
m("<sdiwoworkorderinfo>", "userinfo1", "mrp.production", "x_userinfo1", "base")
m("<sdiwoworkorderinfo>", "userinfo2", "mrp.production", "x_userinfo2", "base")
m("<sdiwoworkorderinfo>", "userinfo3", "mrp.production", "x_userinfo3", "base")
m("<sdiwoworkorderinfo>", "userinfo4", "mrp.production", "x_userinfo4", "base")
m("<sdiwoworkorderinfo>", "userinfo5", "mrp.production", "x_userinfo5", "base")
# Customer
m("<sdiwocustomerinfo>", "code", "mrp.production", "partner_id", "mrp")
m("<sdiwocustomerinfo>", "extref", "res.partner", "ref", "base")
m("<sdiwocustomerinfo>", "name", "res.partner", "name", "base")
# Finished Items
m("<sdiwofinisheditem>", "stockcode", "mrp.production", "product_id", "mrp")
m("<sdiwofinisheditem>", "productname", "mrp.production", "product_name", "mrp")
m("<sdiwofinisheditem>", "unitcode", "mrp.production", "product_uom_id", "mrp")
m("<sdiwofinisheditem>", "quantity", "mrp.production", "product_qty", "mrp")
m("<sdiwofinisheditem>", "deliverydt", "mrp.production", "date_planned_finished", "mrp")
m("<sdiwofinisheditem>", "isfsc", "mrp.production", "is_fsc", "mrp")  # custom
# Raw Materials
m("<sdiworawmaterial>", "materialtype", "stock.move", "scrapped", "stock")  # or custom
m("<sdiworawmaterial>", "stockcode", "stock.move", "product_id", "stock")
m("<sdiworawmaterial>", "materialname", "stock.move", "description_picking", "stock")
m("<sdiworawmaterial>", "unitcode", "stock.move", "product_uom", "stock")
m("<sdiworawmaterial>", "quantity", "stock.move", "product_uom_qty", "stock")
m("<sdiworawmaterial>", "processgroupcode", "mrp.workorder", "workcenter_id", "mrp")
m("<sdiworawmaterial>", "idativ", "mrp.workorder", "operation_id", "mrp")
m("<sdiworawmaterial>", "unitcode2", "stock.move", "", "")  # secondary UOM
m("<sdiworawmaterial>", "quantity2", "stock.move", "", "")  # secondary qty
# Operations
m("<sdiwooperation>", "processgroupcode", "mrp.routing.workcenter", "", "")
m("<sdiwooperation>", "processgroupseq", "mrp.routing.workcenter", "sequence", "mrp")
m("<sdiwooperation>", "idativ", "mrp.workorder", "operation_id", "mrp")
m("<sdiwooperation>", "allocgrpcode", "mrp.workorder", "workcenter_id", "mrp")
m("<sdiwooperation>", "activitycode", "mrp.workorder", "operation_id.name", "mrp")
m("<sdiwooperation>", "sequence", "mrp.routing.workcenter", "sequence", "mrp")
m("<sdiwooperation>", "quantity", "mrp.workorder", "qty_produced", "mrp")
m("<sdiwooperation>", "unitcode", "mrp.workorder", "product_uom_id", "mrp")
m("<sdiwooperation>", "setuptime", "mrp.workorder", "time_setup", "mrp")
m("<sdiwooperation>", "totaltime", "mrp.workorder", "time_cycle", "mrp")
m("<sdiwooperation>", "resourcecode", "mrp.workorder", "workcenter_id.code", "mrp")
m("<sdiwooperation>", "resourcename", "mrp.workorder", "workcenter_id.name", "mrp")
m("<sdiwooperation>", "setupwaste", "mrp.workorder", "", "")  # custom
m("<sdiwooperation>", "productionwaste", "mrp.workorder", "", "")  # custom
m("<sdiwooperation>", "productiontime", "mrp.workorder", "time_cycle", "mrp")
# Components
m("<sdiwocomponent>", "name", "mrp.bom", "name", "mrp")
m("<sdiwocomponent>", "stockcode", "mrp.bom.line", "product_id", "mrp")
m("<sdiwocomponent>", "quantity", "mrp.bom.line", "product_qty", "mrp")

# --- SOR ---
m("<sdiSorInfo>", "OrderNumber", "sale.order", "name", "sale")
m("<sdiSorInfo>", "EmissionDt", "sale.order", "date_order", "sale")
m("<sdiSorInfo>", "DeliveryDt", "sale.order", "commitment_date", "sale")
m("<sdiSorInfo>", "IdCompany", "sale.order", "company_id", "base")
m("<sdiSorInfo>", "CustomerCode", "sale.order", "partner_id", "sale")
m("<sdiSorInfo>", "CustomerPurchaseOrder", "sale.order", "client_order_ref", "sale")
m("<sdiSorInfo>", "ExtRef", "sale.order", "origin", "sale")
m("<sdiSorInfo>", "Status", "sale.order", "state", "sale")
m("<sdiSorInfo>", "UserInfo1", "sale.order", "x_userinfo1", "base")
m("<sdiSorInfo>", "UserInfo2", "sale.order", "x_userinfo2", "base")
m("<sdiSorInfo>", "UserInfo3", "sale.order", "x_userinfo3", "base")
m("<sdiSorInfo>", "UserInfo4", "sale.order", "x_userinfo4", "base")
m("<sdiSorInfo>", "UserInfo5", "sale.order", "x_userinfo5", "base")
# Items
m("<sdiSorItem>", "Seq", "sale.order.line", "sequence", "sale")
m("<sdiSorItem>", "StockCode", "sale.order.line", "product_id", "sale")
m("<sdiSorItem>", "ProductName", "sale.order.line", "name", "sale")
m("<sdiSorItem>", "Quantity", "sale.order.line", "product_uom_qty", "sale")
m("<sdiSorItem>", "UnitCode", "sale.order.line", "product_uom", "sale")
m("<sdiSorItem>", "UnitValue", "sale.order.line", "price_unit", "sale")
m("<sdiSorItem>", "TotalValue", "sale.order.line", "price_subtotal", "sale")
m("<sdiSorItem>", "DeliveryDt", "sale.order.line", "commitment_date", "sale")
m("<sdiSorItem>", "CFOP", "sale.order.line", "cfop_id", "l10n_ar")
# Customer
m("<sdiSorCustomer>", "Code", "res.partner", "id", "base")
m("<sdiSorCustomer>", "Name", "res.partner", "name", "base")
m("<sdiSorCustomer>", "ExtRef", "res.partner", "ref", "base")
m("<sdiSorCustomer>", "CountryDocumentNumber", "res.partner", "vat", "base")

# --- BIL ---
m("<sdiBilInvoiceInfo>", "InvoiceReqNumber", "account.move", "name", "account")
m("<sdiBilInvoiceInfo>", "InvoiceNumber", "account.move", "l10n_latam_document_number", "l10n_ar")
m("<sdiBilInvoiceInfo>", "InvoiceCompl", "account.move", "l10n_latam_document_number", "l10n_ar")
m("<sdiBilInvoiceInfo>", "Status", "account.move", "state", "account")
m("<sdiBilInvoiceInfo>", "EmissionDt", "account.move", "invoice_date", "account")
m("<sdiBilInvoiceInfo>", "IdCompany", "account.move", "company_id", "base")
m("<sdiBilInvoiceInfo>", "Extref", "account.move", "ref", "account")
m("<sdiBilInvoiceInfo>", "UserInfo1", "account.move", "x_userinfo1", "base")
m("<sdiBilInvoiceInfo>", "UserInfo2", "account.move", "x_userinfo2", "base")
m("<sdiBilInvoiceInfo>", "UserInfo3", "account.move", "x_userinfo3", "base")
m("<sdiBilInvoiceInfo>", "UserInfo4", "account.move", "x_userinfo4", "base")
m("<sdiBilInvoiceInfo>", "UserInfo5", "account.move", "x_userinfo5", "base")
m("<sdiBilInvoiceInfo>", "InvoiceType", "account.move", "move_type", "account")
m("<sdiBilInvoiceInfo>", "InvoiceMessage", "account.move", "narration", "account")
m("<sdiBilInvoiceInfo>", "IsBrokerResponsiblePayment", "account.move", "", "")  # custom
m("<sdiBilInvoiceInfo>", "accesskey", "account.move", "l10n_latam_document_access_key", "l10n_ar")
# Payment Conditions
m("<sdiBilPayConInfo>", "ConditionCode", "account.move", "invoice_payment_term_id", "account")
m("<sdiBilPayConInfo>", "ExtRef", "account.move", "ref", "account")
# Due dates
m("<sdiBilPayCondDueDate>", "DueDate", "account.move.line", "date_maturity", "account")
m("<sdiBilPayCondDueDate>", "Value", "account.move.line", "amount_residual", "account")
# Address
m("<sdiBilAddress>", "AddressPrefix", "res.partner", "street", "base")
m("<sdiBilAddress>", "AddressName", "res.partner", "street", "base")
m("<sdiBilAddress>", "AddressNumber", "res.partner", "street", "base")
m("<sdiBilAddress>", "AddressComplement", "res.partner", "street2", "base")
m("<sdiBilAddress>", "District", "res.partner", "street3", "base")
m("<sdiBilAddress>", "ZipCode", "res.partner", "zip", "base")
m("<sdiBilAddress>", "CityName", "res.partner", "city", "base")
m("<sdiBilAddress>", "StateName", "res.partner", "state_id", "base")
m("<sdiBilAddress>", "CountryName", "res.partner", "country_id", "base")
m("<sdiBilAddress>", "IsBilling", "res.partner", "type", "base")  # 'invoice'
m("<sdiBilAddress>", "IsCharging", "res.partner", "type", "base")  # 'other'
m("<sdiBilAddress>", "IsDelivery", "res.partner", "type", "base")  # 'delivery'
# Customer
m("<sdiBilCustomerInfo>", "Code", "account.move", "partner_id", "account")
m("<sdiBilCustomerInfo>", "Name", "res.partner", "name", "base")
m("<sdiBilCustomerInfo>", "ExtRef", "res.partner", "ref", "base")
m("<sdiBilCustomerInfo>", "ContactName", "account.move", "partner_id.name", "account")
# Items
m("<sdiBilItemInfo>", "ItemID", "account.move.line", "id", "account")
m("<sdiBilItemInfo>", "Seq", "account.move.line", "sequence", "account")
m("<sdiBilItemInfo>", "StockCode", "account.move.line", "product_id", "account")
m("<sdiBilItemInfo>", "CustomerStockCode", "account.move.line", "", "")  # customer product code
m("<sdiBilItemInfo>", "ProductName", "account.move.line", "name", "account")
m("<sdiBilItemInfo>", "UnitValue", "account.move.line", "price_unit", "account")
m("<sdiBilItemInfo>", "Quantity", "account.move.line", "quantity", "account")
m("<sdiBilItemInfo>", "TotalValue", "account.move.line", "price_subtotal", "account")
m("<sdiBilItemInfo>", "UnitCode", "account.move.line", "product_uom_id", "account")
m("<sdiBilItemInfo>", "CFOP", "account.move.line", "l10n_latam_document_cfop_id", "l10n_ar")
m("<sdiBilItemInfo>", "CustomerPurchaseOrder", "account.move.line", "purchase_order_name", "account")
m("<sdiBilItemInfo>", "CustomerItemPurchaseOrder", "account.move.line", "", "")
# Returned
m("<sdiBilItemReturned>", "ReturnedInvoiceNumber", "account.move", "reversed_entry_id", "account")
m("<sdiBilItemReturned>", "ReturnedInvoiceCompl", "account.move", "reversed_entry_id", "account")
m("<sdiBilItemReturned>", "Seq", "account.move.line", "sequence", "account")
m("<sdiBilItemReturned>", "ReturnedTotalQuantity", "account.move.line", "quantity", "account")
m("<sdiBilItemReturned>", "UnitCode", "account.move.line", "product_uom_id", "account")
m("<sdiBilItemReturned>", "ReturnedTotalValue", "account.move.line", "price_subtotal", "account")
# Return lots
m("<sdiBilItemReturnedDetail>", "ReturnedQuantity", "stock.move.line", "qty_done", "stock")
m("<sdiBilItemReturnedDetail>", "Lot", "stock.move.line", "lot_id", "stock")
m("<sdiBilItemReturnedDetail>", "StockPlaceCode", "stock.move.line", "location_id", "stock")
m("<sdiBilItemReturnedDetail>", "StockAddress", "stock.move.line", "location_dest_id", "stock")
# Tax
m("<sdiBilItemTaxInfo>", "Name", "account.tax", "name", "account")
m("<sdiBilItemTaxInfo>", "Value", "account.move.line", "tax_base_amount", "account")

# --- WIP ---
m("<sdiWIPLabel>", "IdPalletLabel", "mrp.workorder", "id", "mrp")
m("<sdiWIPLabel>", "BarCode", "mrp.workorder", "barcode", "mrp")
m("<sdiWIPLabel>", "Quantity", "mrp.workorder", "qty_produced", "mrp")
m("<sdiWIPLabel>", "QuantityKG", "mrp.workorder", "", "")  # custom
m("<sdiWIPLabel>", "UnitCode", "mrp.workorder", "product_uom_id", "mrp")
m("<sdiWIPLabel>", "IsValid", "mrp.workorder", "is_validated", "mrp")  # custom
m("<sdiWIPLabel>", "DtValidation", "mrp.workorder", "date_start", "mrp")
m("<sdiWIPLabel>", "UserValidation", "mrp.workorder", "user_id", "mrp")
m("<sdiWIPLabel>", "Status", "mrp.workorder", "state", "mrp")
m("<sdiWIPLabel>", "InsDt", "mrp.workorder", "create_date", "base")
m("<sdiWIPLabel>", "InsUser", "mrp.workorder", "create_uid", "base")
m("<sdiWIPLabel>", "IsFinalProduct", "mrp.workorder", "is_final_product", "mrp")
m("<sdiWIPLabel>", "StkCode", "mrp.workorder", "product_id", "mrp")
m("<sdiWIPLabel>", "StkDescription", "mrp.workorder", "name", "mrp")
m("<sdiWIPLabel>", "Shift", "mrp.workorder", "", "")  # custom
m("<sdiWIPLabel>", "Note", "mrp.workorder", "note", "mrp")
m("<sdiWIPLabel>", "PalletWeight", "stock.move.line", "weight", "stock")
m("<sdiWIPLabel>", "IsBobbin", "mrp.workorder", "", "")  # custom
m("<sdiWIPLabel>", "ComponentId", "stock.move.line", "component_id", "mrp")  # custom
m("<sdiWIPLabel>", "Lot", "stock.move.line", "lot_id", "stock")
m("<sdiWIPLabel>", "ProcessID", "mrp.workorder", "operation_id", "mrp")
m("<sdiWIPLabel>", "ProcessDescription", "mrp.routing.workcenter", "name", "mrp")
# WIP Transaction
m("<sdiWIPTransaction>", "TransactionType", "stock.move", "type", "stock")
m("<sdiWIPTransaction>", "IdPalletLabel", "stock.move", "workorder_id", "mrp")
m("<sdiWIPTransaction>", "TransactionDt", "stock.move", "date", "stock")
m("<sdiWIPTransaction>", "Status", "stock.move", "state", "stock")
m("<sdiWIPTransaction>", "QtyBefore", "stock.move.line", "qty_before", "stock")
m("<sdiWIPTransaction>", "QtyAfter", "stock.move.line", "qty_done", "stock")
m("<sdiWIPTransaction>", "QtyBeforeKG", "stock.move.line", "", "")  # custom
m("<sdiWIPTransaction>", "QtyAfterKG", "stock.move.line", "", "")  # custom
m("<sdiWIPTransaction>", "StockPlaceCodeBefore", "stock.move.line", "location_id", "stock")
m("<sdiWIPTransaction>", "StockPlaceCodeAfter", "stock.move.line", "location_dest_id", "stock")
m("<sdiWIPTransaction>", "StockAddressBefore", "stock.move.line", "location_id", "stock")
m("<sdiWIPTransaction>", "StockAddressAfter", "stock.move.line", "location_dest_id", "stock")
m("<sdiWIPTransaction>", "LogUser", "stock.move", "write_uid", "base")
m("<sdiWIPTransaction>", "Note", "stock.move", "note", "stock")
m("<sdiWIPTransaction>", "Lot", "stock.move.line", "lot_id", "stock")
m("<sdiWIPTransaction>", "MachineInputCode", "mrp.workorder", "", "")  # custom

def get_odoo_mapping(elemento, atributo):
    key = (elemento, atributo)
    if key in ODOO_MAP:
        return ODOO_MAP[key]
    return ("", "", "")

# ========================
# CRM - Relaciones
# ========================
crm_data = [
    ["CE01", "<metrics>", "", "", "", "Sí", "Inicia y finaliza el archivo XML", "", "", "", ""],
    ["CE02", "<sdiCrmActor>", "", "", "", "Sí", "Contiene datos referentes a la relación", "", "res.partner", "", "base"],
    ["CE02", "", "Code", "Int", "", "Sí", "Código de la relación", "", "res.partner", "ref", "base"],
    ["CE02", "", "OwnerCode", "Int", "", "No", "Código del propietario", "", "res.partner", "commercial_partner_id", "base"],
    ["CE02", "", "PersonTypeCompl", "Int", "", "Sí", "Estructura Corporativa: 0=Matriz, 1=Sucursal, 2=Area", "", "res.partner", "", "l10n_ar_ux"],
    ["CE02", "", "PersonType", "Int", "", "Sí", "Tipo relación: 0=Física, 1=Jurídica, 2=Gobierno, 3=Exportación", "", "res.partner", "company_type", "base"],
    ["CE02", "", "IdCountry", "SmallInt", "", "No", "ID del registro del país en el M3", "", "res.country", "id", "base"],
    ["CE02", "", "CountryDocumentNumber", "String", "35", "Sí", "RUC/RUT/CUIT", "", "res.partner", "vat", "base"],
    ["CE02", "", "StateDocumentNumber", "String", "35", "No", "Inscripción Estadual", "", "res.partner", "company_registry", "base"],
    ["CE02", "", "CityDocumentNumber", "String", "35", "No", "Inscripción Municipal", "", "res.partner", "", ""],
    ["CE02", "", "Name", "String", "70", "Sí", "Nombre de fantasía", "", "res.partner", "name", "base"],
    ["CE02", "", "FullName", "String", "140", "Sí", "Razón Social", "", "res.partner", "display_name", "base"],
    ["CE02", "", "Phone", "String", "60", "No", "Teléfono comercial", "", "res.partner", "phone", "base"],
    ["CE02", "", "Website", "String", "50", "No", "Dirección del website", "", "res.partner", "website", "base"],
    ["CE02", "", "Fax", "String", "60", "No", "Número de fax", "", "res.partner", "fax", "base"],
    ["CE02", "", "Note", "Text", "", "No", "Observación acerca de la relación", "", "res.partner", "comment", "base"],
    ["CE02", "", "ExtRef", "String", "50", "Sí", "Código en sistema tercero", "Debe ser diferente del ExtRef del contacto y dirección", "res.partner", "ref", "base"],
    ["CE02", "", "ExtRefOwnerCode", "String", "50", "No", "Código de referencia del propietario", "", "", "", ""],
    ["CE02", "", "IsActv", "Boolean", "", "Sí", "Relación activa? 0=No, 1=Sí", "", "res.partner", "active", "base"],
    ["CE02", "", "IsCustomer", "Boolean", "", "Sí", "Es cliente? 0=No, 1=Sí", "", "res.partner", "customer_rank", "base"],
    ["CE02", "", "IsSupplier", "Boolean", "", "Sí", "Es proveedor? 0=No, 1=Sí", "", "res.partner", "supplier_rank", "base"],
    ["CE02", "", "IsPerson", "Boolean", "", "Sí", "Es persona física? 0=No, 1=Sí", "", "res.partner", "company_type", "base"],
    ["CE02", "", "IsBroker", "Boolean", "", "No", "Es agencia? 0=No, 1=Sí", "", "", "", ""],
    ["CE02", "", "isCustomerService", "Int", "", "No", "Descontinuado, no utilizar", "", "", "", ""],
    ["CE02", "", "IsRepres", "Boolean", "", "No", "Es vendedor? 0=No, 1=Sí", "", "", "", ""],
    ["CE02", "", "IsTransport", "Boolean", "", "No", "Es transportista? 0=No, 1=Sí", "", "", "", ""],
    ["CE02", "", "CountryCode", "String", "10", "Sí", "Código de países BACEN", "", "res.partner", "country_id", "base"],
    ["CE02", "", "CountryFiscalCode", "String", "10", "Sí", "Código fiscal del país", "", "res.partner", "l10n_ar_afip_responsibility_type_id", "l10n_ar"],
    ["CE02", "", "UserFieldClassic1", "String", "50", "No", "Campo de usuario 1", "", "res.partner", "x_user_field1", "base"],
    ["CE02", "", "UserFieldClassic2", "String", "50", "No", "Campo de usuario 2", "", "res.partner", "x_user_field2", "base"],
    ["CE02", "", "UserFieldClassic3", "String", "50", "No", "Campo de usuario 3", "", "res.partner", "x_user_field3", "base"],
    ["CE02", "", "UserFieldClassic4", "String", "50", "No", "Campo de usuario 4", "", "res.partner", "x_user_field4", "base"],
    ["CE02", "", "UserFieldClassic5", "String", "50", "No", "Campo de usuario 5", "", "res.partner", "x_user_field5", "base"],
    ["CE02", "", "ConditionPaymentStandard", "String", "30", "No", "Condición de pago estándar", "", "res.partner", "property_payment_term_id", "account"],
    ["CE02", "", "Email", "String", "200", "No", "Email", "", "res.partner", "email", "base"],
    ["CE02", "", "Emailtax", "String", "200", "No", "Email fiscal", "", "res.partner", "l10n_ar_afip_tax_email", "l10n_ar"],
    ["CE02", "", "BroptingSimpleNational", "Int", "", "No", "Optante simple nacional: 0=Ningún, 1=Simple, 2=Exceso, 3=Normal", "", "res.partner", "l10n_ar_afip_responsibility_type_id", "l10n_ar"],
    ["CE02", "", "LimitValueCredit", "Float", "", "No", "Límite de crédito", "", "res.partner", "credit_limit", "base"],
    ["CE02", "", "CreditExpirationDt", "TDateTime", "", "No", "Fecha expiración límite crédito", "", "res.partner", "credit_expiration_date", "base"],
    ["CE02", "", "EmailBilling", "String", "255", "No", "Email de cobro", "", "res.partner", "l10n_ar_afip_invoicing_email", "l10n_ar"],
    ["CE02", "", "InvoiceCFOP", "String", "10", "No", "Operación Factura", "", "res.partner", "property_account_position_id", "account"],
    ["CE02", "", "ShippingCFOP", "String", "10", "No", "Operación Remisión", "", "res.partner", "property_account_position_id", "account"],
    ["CE02", "", "InvoiceandShippingCFOP", "String", "10", "No", "Operación Factura/Remisión", "", "res.partner", "property_account_position_id", "account"],
    # Contactos
    ["CE03", "<sdiLCrmActorContact>", "", "", "", "Sí", "Contactos de la relación", "", "res.partner", "", "base"],
    ["CE03", "", "LCount", "Int", "", "Sí", "Número de contactos. Ej: LCount='8'", "", "", "", ""],
    ["CE04", "<sdiCrmActorContact>", "", "", "", "Sí", "Contacto de la relación", "", "res.partner", "", "base"],
    ["CE04", "", "Code", "String", "50", "Sí", "Código del contacto en M3", "", "res.partner", "ref", "base"],
    ["CE04", "", "Name", "String", "70", "Sí", "Primer nombre del contacto", "", "res.partner", "name", "base"],
    ["CE04", "", "FullName", "String", "140", "No", "Nombre completo del contacto", "", "res.partner", "display_name", "base"],
    ["CE04", "", "ExtRef", "String", "50", "No", "Código en sistema tercero", "", "res.partner", "ref", "base"],
    ["CE04", "", "Phone", "String", "60", "No", "Teléfono", "", "res.partner", "phone", "base"],
    ["CE04", "", "PhoneExtension", "String", "10", "No", "DDD del teléfono", "", "", "", ""],
    ["CE04", "", "MobilePhone", "String", "60", "No", "Teléfono móvil", "", "res.partner", "mobile", "base"],
    ["CE04", "", "EMail", "String", "200", "No", "Email", "", "res.partner", "email", "base"],
    ["CE04", "", "Division", "String", "50", "No", "Sector del contacto", "", "res.partner", "function", "base"],
    ["CE04", "", "Note", "Text", "", "No", "Comentarios", "", "res.partner", "comment", "base"],
    ["CE04", "", "BirthDate", "TDateTime", "", "No", "Fecha de nacimiento", "", "res.partner", "birthdate", "base"],
    ["CE04", "", "TreatmentForm", "String", "20", "No", "Tipo de tratamiento", "", "res.partner", "title", "base"],
    ["CE04", "", "IsActv", "Boolean", "", "No", "Contacto activo? 0=No, 1=Sí", "", "res.partner", "active", "base"],
    # Direcciones
    ["CE05", "<sdiLCrmAddress>", "", "", "", "Sí", "Direcciones", "", "res.partner", "", "base"],
    ["CE05", "", "LCount", "Int", "", "Sí", "Número de direcciones", "", "", "", ""],
    ["CE06", "<sdiCrmAddress>", "", "", "", "Sí", "Dirección", "", "res.partner", "", "base"],
    ["CE06", "", "IdAddress", "Int", "", "Sí", "Código de la dirección en M3", "", "res.partner", "id", "base"],
    ["CE06", "", "CityCode", "Int", "", "Sí", "Código de la ciudad en M3", "", "res.city", "id", "base"],
    ["CE06", "", "AddressPrefix", "String", "10", "Sí", "Calle, Avenida, etc.", "", "res.partner", "street", "base"],
    ["CE06", "", "AddressName", "String", "100", "Sí", "Descripción de la dirección", "", "res.partner", "street", "base"],
    ["CE06", "", "AddressNumber", "String", "10", "Sí", "Número", "", "res.partner", "street", "base"],
    ["CE06", "", "AddressComplement", "String", "60", "No", "Complemento", "", "res.partner", "street2", "base"],
    ["CE06", "", "District", "String", "60", "Sí", "Barrio", "", "res.partner", "", ""],
    ["CE06", "", "ZipCode", "String", "20", "Sí", "Código postal", "", "res.partner", "zip", "base"],
    ["CE06", "", "Reference", "String", "50", "No", "Referencia adicional", "", "res.partner", "street3", "base"],
    ["CE06", "", "Note", "String", "100", "No", "Observación", "", "res.partner", "comment", "base"],
    ["CE06", "", "ExtRef", "String", "50", "No", "Referencia externa", "", "res.partner", "ref", "base"],
    # Cliente specific
    ["CE07", "<sdiCrmCustomer>", "", "", "", "No", "Informaciones específicas del cliente", "", "res.partner", "", "l10n_ar"],
    ["CE07", "", "SalesManCode", "String", "20", "No", "Código del vendedor", "", "res.partner", "user_id", "base"],
    ["CE07", "", "Note", "Text", "", "No", "Observación del cliente", "", "res.partner", "comment", "base"],
    ["CE07", "", "IsActv", "Boolean", "", "No", "Cliente activo?", "", "res.partner", "active", "base"],
    ["CE08", "<crmcustomer_u>", "", "", "", "No", "Campos de usuario del cliente", "", "", "", ""],
    ["CE09", "<sdiCrmSupplier>", "", "", "", "No", "Informaciones específicas del proveedor", "", "res.partner", "", "l10n_ar"],
    ["CE10", "<crmSupplier_u>", "", "", "", "No", "Campos de usuario del proveedor", "", "", "", ""],
]

# ========================
# STKItem - Ítems de Stock
# ========================
stkitem_data = [
    ["STE01", "<metrics>", "", "", "", "Sí", "Inicia y finaliza el archivo XML", "", "", "", ""],
    ["STE02", "<sdiStkItem>", "", "", "", "Sí", "Ítem de stock", "", "product.product", "", "base"],
    ["STE02", "", "idItem", "Int", "", "No", "Llave primaria (solo exportación)", "", "product.product", "id", "base"],
    ["STE02", "", "StockCode", "String", "20", "Sí", "Código del ítem de stock", "", "product.product", "default_code", "base"],
    ["STE02", "", "Status", "Boolean", "", "Sí", "Ítem activo? 0=No, 1=Sí", "", "product.product", "active", "base"],
    ["STE02", "", "MaterialType", "Int", "", "Sí", "Tipo: 1=tinta, 2=plancha, 3=otros, 4=papel hoja, 5=bobina, 6=personalizado", "", "product.category", "name", "base"],
    ["STE02", "", "ItemType", "Int", "", "Sí", "0=MP, 1=PT, 2=intermediario, 3=servicio, 4=consumible", "", "product.product", "type", "base"],
    ["STE02", "", "MaterialName", "String", "60", "Sí", "Nombre del material", "", "product.product", "name", "base"],
    ["STE02", "", "UnitCode", "String", "8", "Sí", "Unidad. Ej: KG, UN, FL, PZ", "", "product.product", "uom_id", "base"],
    ["STE02", "", "UnitCodeDemand", "String", "8", "Sí", "Unidad de consumo. Ej: HJ", "", "product.product", "uom_po_id", "base"],
    ["STE02", "", "UnitCodeCost", "String", "8", "Sí", "Unidad de costo. Ej: KG", "", "product.product", "cost_method", "base"],
    ["STE02", "", "Height", "Double", "", "No", "Altura", "", "product.product", "product_height", "base"],
    ["STE02", "", "Width", "Double", "", "No", "Anchura", "", "product.product", "product_width", "base"],
    ["STE02", "", "Grammage", "Int", "", "No", "Gramaje", "", "product.product", "product_grammage", "base"],
    ["STE02", "", "CustomMaterialTypeCode", "String", "4", "No", "Código tipo material personalizado", "", "product.category", "name", "base"],
    ["STE02", "", "CustomMaterialTypeDescription", "String", "60", "No", "Descripción tipo material personalizado", "", "product.category", "description", "base"],
    ["STE02", "", "MaterialGroupCode", "String", "20", "No", "Código grupo de materiales", "", "product.product", "categ_id", "base"],
    ["STE02", "", "MaterialGroupDescription", "String", "50", "Sí", "Descripción grupo de materiales", "", "product.category", "name", "base"],
    ["STE02", "", "MasterMaterialGroupCode", "String", "20", "Sí", "Código grupo máster de materiales", "", "product.category", "parent_id", "base"],
    ["STE02", "", "MasterMaterialGroupDescription", "String", "40", "Sí", "Descripción grupo máster", "", "product.category", "parent_id.name", "base"],
    ["STE02", "", "UsesCtrlVolume", "Boolean", "", "No", "Usa control volúmenes?", "", "", "", ""],
    ["STE02", "", "NCM", "Varchar", "20", "No", "Clasificación fiscal del ítem", "", "product.product", "l10n_latam_product_ncm", "l10n_latam"],
    ["STE02", "", "ISBN", "Varchar", "40", "No", "Número ISBN", "", "product.product", "isbn", "base"],
    ["STE02", "", "WeightKg", "Double", "", "No", "Peso (kg)", "", "product.product", "weight", "base"],
    ["STE02", "", "UnitWeight", "Double", "", "No", "Descontinuado", "", "product.product", "weight", "base"],
    ["STE02", "", "EAN", "Varchar", "20", "No", "Código EAN", "", "product.product", "barcode", "base"],
    ["STE02", "", "OriginItem", "Int", "", "No", "Origen del ítem", "", "product.product", "origin", "base"],
    ["STE02", "", "IsFSC", "Boolean", "", "No", "Es FSC? 0=No, 1=Sí", "", "product.product", "is_fsc", "base"],
    ["STE02", "", "Obs", "Varchar", "255", "No", "Observaciones", "", "product.product", "description", "base"],
    ["STE02", "", "UseLot", "Boolean", "", "No", "Requiere lote? 0=No, 1=Sí", "", "product.product", "tracking", "stock"],
    ["STE02", "", "UseAddress", "Boolean", "", "No", "Requiere localización? 0=No, 1=Sí", "", "product.product", "storage_location", "stock"],
    ["STE02", "", "IsInventoried", "Boolean", "", "No", "Es inventariado? 0=No, 1=Sí", "", "product.product", "inventory_valuation", "base"],
    ["STE02", "", "ControlTraceability", "Boolean", "", "No", "Controlado por trazabilidad? 0=No, 1=Sí", "", "product.product", "tracking", "stock"],
    ["STE02", "", "TipoItemSped", "Boolean", "", "No", "Tipo SPED", "", "product.product", "l10n_latam_product_sped_type", "l10n_ar"],
    ["STE02", "", "IsSupplied", "Boolean", "", "No", "Material suministrado?", "", "product.product", "purchase_ok", "base"],
    ["STE02", "", "FinancialNatureCode", "String", "20", "No", "Código Naturaleza Financiera", "", "product.product", "product_nature_id", "account"],
    ["STE02", "", "BusinessUnitCode", "String", "10", "No", "Código Unidad de Negocios", "", "", "", ""],
    ["STE02", "", "PackagingQty", "Double", "", "No", "Cantidad por embalaje", "", "product.product", "packaging_qty", "base"],
    ["STE02", "", "PackagingUnit", "String", "4", "No", "Unidad de embalaje", "", "product.product", "packaging_uom_id", "base"],
    ["STE02", "", "BillingDescription", "String", "400", "No", "Descripción para factura", "", "product.product", "description_sale", "base"],
    ["STE02", "", "ProductClassification", "String", "32", "No", "Clasificación del producto", "", "", "", ""],
    ["STE02", "", "NeedSeparation", "Boolean", "", "No", "Requiere separación de material?", "", "", "", ""],
    ["STE02", "", "DifferentLotsSeparation", "Boolean", "", "No", "Separación por lotes diferentes?", "", "", "", ""],
    ["STE02", "", "InvoiceItemType", "Int", "", "No", "Tipo ítem facturación", "", "product.product", "invoice_policy", "base"],
    ["STE02", "", "ShippingItemType", "Int", "", "No", "Tipo ítem remisión", "", "product.product", "shipping_policy", "base"],
]

# ========================
# STK - Movimientos de Stock
# ========================
stk_data = [
    ["ST01", "<metrics>", "", "", "", "Sí", "Inicia y finaliza el archivo XML", "", "", "", ""],
    ["ST02", "<sdistktransactiongroup>", "", "", "", "Sí", "Agrupa transacciones de stock", "", "stock.picking", "", "stock"],
    ["ST03", "<sdilstktransaction>", "", "", "", "Sí", "Lista de transacciones", "", "stock.picking", "", "stock"],
    ["ST03", "", "LCount", "Int", "", "Sí", "Cantidad de transacciones. Ej: LCount='1'", "", "", "", ""],
    ["ST04", "<sdistktransaction>", "", "", "", "Sí", "Transacción de stock", "", "stock.move", "", "stock"],
    ["ST04", "", "transactiontype", "Int", "", "Sí", "Tipo: 0=Atención/Devolución, 1=Entrega prod, 2=Compras, 3=Ventas, 4=Inventario, 5=Transferencia, 6=Volúmenes, 7=Transf.empresas, 8=Transferencia, 9=Ajuste, 10=Otro", "", "stock.picking", "picking_type_id", "stock"],
    ["ST04", "", "operationtype", "Int", "", "Sí", "Tipo de operación", "", "stock.move", "operation_type", "stock"],
    ["ST04", "", "transactiondt", "TDateTime", "", "Sí", "Fecha de la transacción", "", "stock.move", "date", "stock"],
    ["ST04", "", "stockcode", "String", "20", "Sí", "Código del ítem de stock", "", "stock.move", "product_id", "stock"],
    ["ST04", "", "unitcode", "String", "8", "Sí", "Unidad. Ej: KG, UN, FL, PZ", "", "stock.move", "product_uom", "stock"],
    ["ST04", "", "quantity", "Double", "", "Sí", "Cantidad", "", "stock.move", "product_uom_qty", "stock"],
    ["ST04", "", "totalvalue", "Double", "", "Sí", "Valor total", "", "stock.move", "price_unit", "stock"],
    ["ST04", "", "wonumber", "String", "20", "No", "Número de OP", "", "stock.move", "origin", "stock"],
    ["ST04", "", "stockplacecode", "String", "20", "Sí", "Local de stock", "", "stock.move", "location_id", "stock"],
    ["ST04", "", "idcompany", "Int", "", "Sí", "Código de empresa", "", "stock.move", "company_id", "base"],
    ["ST04", "", "lot", "String", "20", "No", "Lote", "", "stock.move", "lot_ids", "stock"],
    ["ST04", "", "expirationdate", "TDateTime", "", "No", "Fecha vencimiento", "", "stock.lot", "expiration_date", "stock"],
    ["ST04", "", "productiondate", "TDateTime", "", "No", "Fecha producción", "", "stock.lot", "production_date", "stock"],
    ["ST04", "", "providerlot", "String", "20", "No", "Lote proveedor", "", "stock.lot", "supplier_lot", "stock"],
    ["ST04", "", "unitlot", "String", "20", "No", "Unidad del lote", "", "stock.lot", "uom_id", "stock"],
    ["ST04", "", "docnumber", "String", "20", "Sí", "N° documento", "", "stock.picking", "name", "stock"],
    ["ST04", "", "docnumbercompl", "String", "20", "No", "Complemento documento", "", "stock.picking", "origin", "stock"],
    ["ST04", "", "stockaddress", "String", "20", "No", "Localización de stock", "", "stock.move.line", "location_dest_id", "stock"],
    ["ST04", "", "stockmovementtype", "Int", "", "No", "0=Entrada, 1=Salida, 2=Ajuste", "", "stock.move", "type", "stock"],
    ["ST04", "", "costcentercode", "String", "20", "No", "Código centro de costo", "", "stock.move", "analytic_account_id", "analytic"],
    ["ST04", "", "costcentername", "String", "50", "No", "Nombre centro de costo", "", "account.analytic.account", "name", "analytic"],
    ["ST04", "", "transactioncode", "String", "30", "Sí", "Código transacción", "", "stock.picking", "origin", "stock"],
    ["ST04", "", "quantityunitcost", "Double", "", "No", "Cantidad costo unitario", "", "stock.move", "quantity", "stock"],
    ["ST04", "", "unitcostcode", "String", "8", "No", "Unidad costo unitario", "", "stock.move", "price_unit", "stock"],
    ["ST04", "", "transactioncodeextref", "String", "30", "No", "Código externo transacción", "", "stock.picking", "origin", "stock"],
    ["ST04", "", "userfield1", "String", "50", "No", "Campo de usuario 1", "", "", "", ""],
    ["ST04", "", "userfield2", "String", "50", "No", "Campo de usuario 2", "", "", "", ""],
    ["ST04", "", "userfield3", "String", "50", "No", "Campo de usuario 3", "", "", "", ""],
    ["ST04", "", "userfield4", "String", "50", "No", "Campo de usuario 4", "", "", "", ""],
    ["ST04", "", "userfield5", "String", "50", "No", "Campo de usuario 5", "", "", "", ""],
    ["ST04", "", "loguser", "String", "32", "No", "Usuario transacción", "", "stock.move", "write_uid", "base"],
    ["ST04", "", "grossweight", "Double", "", "No", "Peso bruto total", "", "stock.move.line", "weight", "stock"],
    ["ST04", "", "relatedtransactioncodeextref", "String", "30", "No", "Transacción relacionada", "", "", "", ""],
    ["ST04", "", "transactionoriginextref", "String", "30", "No", "Transacción origen", "", "", "", ""],
]

# ========================
# WO - Órdenes de Producción
# ========================
wo_data = [
    ["WO01", "<metrics>", "", "", "", "Sí", "Inicia y finaliza el archivo XML", "", "", "", ""],
    ["WO02", "<sdiwoworkorder>", "", "", "", "Sí", "Orden de producción", "", "mrp.production", "", "mrp"],
    ["WO02", "", "loguser", "String", "32", "No", "Usuario que registró", "", "mrp.production", "write_uid", "base"],
    ["WO03", "<sdiwoworkorderinfo>", "", "", "", "Sí", "Cabecera de la OP", "", "mrp.production", "", "mrp"],
    ["WO03", "", "idcompany", "Int", "", "Sí", "Código de empresa", "", "mrp.production", "company_id", "base"],
    ["WO03", "", "wonumber", "String", "20", "Sí", "Número de OP", "", "mrp.production", "name", "mrp"],
    ["WO03", "", "wodescription", "String", "100", "No", "Descripción de la OP", "", "mrp.production", "origin", "mrp"],
    ["WO03", "", "quotenumber", "String", "20", "Sí", "Número del presupuesto", "", "mrp.production", "origin", "mrp"],
    ["WO03", "", "status", "Int", "", "Sí", "0=Pendiente, 1=Procesando, 2=Terminada, 3=Cerrada, 4=Parada, 5=Bloqueada, 6=Evaluación", "", "mrp.production", "state", "mrp"],
    ["WO03", "", "insertdt", "TDateTime", "", "Sí", "Fecha de inserción", "", "mrp.production", "date_planned_start", "mrp"],
    ["WO03", "", "projectcode", "String", "20", "No", "Código del proyecto", "", "mrp.production", "project_id", "project"],
    ["WO03", "", "projecttitle", "String", "100", "No", "Título del proyecto", "", "mrp.production", "analytic_account_id", "analytic"],
    ["WO03", "", "userinfo1", "String", "50", "No", "Campo usuario 1", "", "mrp.production", "x_userinfo1", "base"],
    ["WO03", "", "userinfo2", "String", "50", "No", "Campo usuario 2", "", "mrp.production", "x_userinfo2", "base"],
    ["WO03", "", "userinfo3", "String", "50", "No", "Campo usuario 3", "", "mrp.production", "x_userinfo3", "base"],
    ["WO03", "", "userinfo4", "String", "50", "No", "Campo usuario 4", "", "mrp.production", "x_userinfo4", "base"],
    ["WO03", "", "userinfo5", "String", "50", "No", "Campo usuario 5", "", "mrp.production", "x_userinfo5", "base"],
    ["WO04", "<sdiwocustomerinfo>", "", "", "", "Sí", "Información del cliente", "", "res.partner", "", "base"],
    ["WO04", "", "code", "String", "20", "Sí", "Código del cliente", "", "res.partner", "partner_id", "mrp"],
    ["WO04", "", "extref", "String", "50", "No", "Referencia externa", "", "res.partner", "ref", "base"],
    ["WO04", "", "name", "String", "70", "Sí", "Nombre del cliente", "", "res.partner", "name", "base"],
    ["WO05", "<sdilwofinisheditem>", "", "", "", "Sí", "Lista de productos terminados", "", "mrp.production", "", "mrp"],
    ["WO05", "", "LCount", "Int", "", "Sí", "Cantidad de PT", "", "", "", ""],
    ["WO06", "<sdiwofinisheditem>", "", "", "", "Sí", "Producto terminado", "", "mrp.production", "", "mrp"],
    ["WO06", "", "stockcode", "String", "20", "Sí", "Código del PT", "", "mrp.production", "product_id", "mrp"],
    ["WO06", "", "productname", "String", "100", "Sí", "Nombre del producto", "", "mrp.production", "product_name", "mrp"],
    ["WO06", "", "unitcode", "String", "8", "Sí", "Unidad. Ej: UN, PZ", "", "mrp.production", "product_uom_id", "mrp"],
    ["WO06", "", "quantity", "Double", "", "Sí", "Cantidad planeada", "", "mrp.production", "product_qty", "mrp"],
    ["WO06", "", "deliverydt", "TDateTime", "", "Sí", "Fecha de entrega", "", "mrp.production", "date_planned_finished", "mrp"],
    ["WO06", "", "isfsc", "Boolean", "", "No", "Es FSC? 0=No, 1=Sí", "", "mrp.production", "is_fsc", "mrp"],
    ["WO07", "<sdilworawmaterial>", "", "", "", "Sí", "Lista de materias primas", "", "stock.move", "", "stock"],
    ["WO07", "", "LCount", "Int", "", "Sí", "Cantidad de MP", "", "", "", ""],
    ["WO08", "<sdiworawmaterial>", "", "", "", "Sí", "Materia prima", "", "stock.move", "", "stock"],
    ["WO08", "", "materialtype", "Int", "", "Sí", "0=Papel, 1=Tintas, 2=Planchas", "", "stock.move", "scrapped", "stock"],
    ["WO08", "", "stockcode", "String", "20", "Sí", "Código del material", "", "stock.move", "product_id", "stock"],
    ["WO08", "", "materialname", "String", "100", "Sí", "Nombre del material", "", "stock.move", "description_picking", "stock"],
    ["WO08", "", "unitcode", "String", "8", "Sí", "Unidad principal", "", "stock.move", "product_uom", "stock"],
    ["WO08", "", "quantity", "Double", "", "Sí", "Cantidad", "", "stock.move", "product_uom_qty", "stock"],
    ["WO08", "", "processgroupcode", "String", "20", "No", "Código grupo proceso", "", "mrp.workorder", "workcenter_id", "mrp"],
    ["WO08", "", "idativ", "String", "30", "Sí", "ID actividad (vínculo WIP)", "", "mrp.workorder", "operation_id", "mrp"],
    ["WO08", "", "unitcode2", "String", "8", "No", "Unidad secundaria", "", "", "", ""],
    ["WO08", "", "quantity2", "Double", "", "No", "Cantidad secundaria", "", "", "", ""],
    ["WO09", "<sdilwooperation>", "", "", "", "Sí", "Lista de operaciones", "", "mrp.workorder", "", "mrp"],
    ["WO09", "", "LCount", "Int", "", "Sí", "Cantidad de operaciones", "", "", "", ""],
    ["WO10", "<sdiwooperation>", "", "", "", "Sí", "Operación", "", "mrp.workorder", "", "mrp"],
    ["WO10", "", "processgroupcode", "String", "20", "No", "Código grupo proceso", "", "mrp.routing.workcenter", "workcenter_id", "mrp"],
    ["WO10", "", "processgroupseq", "Int", "", "No", "Secuencia grupo proceso", "", "mrp.routing.workcenter", "sequence", "mrp"],
    ["WO10", "", "idativ", "String", "30", "Sí", "ID actividad (vínculo WIP)", "", "mrp.workorder", "operation_id", "mrp"],
    ["WO10", "", "allocgrpcode", "String", "20", "No", "Código grupo asignación", "", "mrp.workorder", "workcenter_id", "mrp"],
    ["WO10", "", "activitycode", "String", "20", "No", "Código actividad", "", "mrp.workorder", "operation_id.name", "mrp"],
    ["WO10", "", "sequence", "Int", "", "Sí", "Secuencia operación", "", "mrp.routing.workcenter", "sequence", "mrp"],
    ["WO10", "", "quantity", "Double", "", "Sí", "Cantidad", "", "mrp.workorder", "qty_produced", "mrp"],
    ["WO10", "", "unitcode", "String", "8", "Sí", "Unidad de medida", "", "mrp.workorder", "product_uom_id", "mrp"],
    ["WO10", "", "setuptime", "Double", "", "No", "Tiempo preparación (horas)", "", "mrp.workorder", "time_setup", "mrp"],
    ["WO10", "", "totaltime", "Double", "", "No", "Tiempo total (horas)", "", "mrp.workorder", "time_cycle", "mrp"],
    ["WO10", "", "resourcecode", "String", "20", "No", "Código recurso/máquina", "", "mrp.workorder", "workcenter_id.code", "mrp"],
    ["WO10", "", "resourcename", "String", "100", "No", "Nombre recurso/máquina", "", "mrp.workorder", "workcenter_id.name", "mrp"],
    ["WO10", "", "setupwaste", "Double", "", "No", "Desperdicio preparación", "", "", "", ""],
    ["WO10", "", "productionwaste", "Double", "", "No", "Desperdicio producción", "", "", "", ""],
    ["WO10", "", "productiontime", "Double", "", "No", "Tiempo producción (horas)", "", "mrp.workorder", "time_cycle", "mrp"],
    ["WO11", "<sdilwooutsourcing>", "", "", "", "No", "Lista de terceirización", "", "", "", ""],
    ["WO12", "<sdilwocomponent>", "", "", "", "No", "Lista de componentes", "", "mrp.bom", "", "mrp"],
    ["WO12", "", "LCount", "Int", "", "Sí", "Cantidad de componentes", "", "", "", ""],
    ["WO13", "<sdiwocomponent>", "", "", "", "No", "Componente", "", "mrp.bom.line", "", "mrp"],
    ["WO13", "", "name", "String", "50", "Sí", "Nombre del componente", "", "mrp.bom", "name", "mrp"],
    ["WO13", "", "stockcode", "String", "20", "Sí", "Código del componente", "", "mrp.bom.line", "product_id", "mrp"],
    ["WO13", "", "quantity", "Double", "", "Sí", "Cantidad", "", "mrp.bom.line", "product_qty", "mrp"],
]

# ========================
# SOR - Pedidos de Venta
# ========================
sor_data = [
    ["SO01", "<metrics>", "", "", "", "Sí", "Inicia y finaliza el archivo XML", "", "", "", ""],
    ["SO02", "<sdiSorHeader>", "", "", "", "Sí", "Cabecera del pedido de venta", "", "sale.order", "", "sale"],
    ["SO03", "<sdiSorInfo>", "", "", "", "Sí", "Información del pedido", "", "sale.order", "", "sale"],
    ["SO03", "", "OrderNumber", "Int", "", "Sí", "Número del pedido de venta", "", "sale.order", "name", "sale"],
    ["SO03", "", "EmissionDt", "TDateTime", "", "Sí", "Fecha de emisión", "", "sale.order", "date_order", "sale"],
    ["SO03", "", "DeliveryDt", "TDateTime", "", "Sí", "Fecha de entrega", "", "sale.order", "commitment_date", "sale"],
    ["SO03", "", "IdCompany", "Int", "", "Sí", "Código de empresa", "", "sale.order", "company_id", "base"],
    ["SO03", "", "CustomerCode", "String", "20", "Sí", "Código del cliente", "", "sale.order", "partner_id", "sale"],
    ["SO03", "", "CustomerPurchaseOrder", "String", "20", "No", "OC del cliente", "", "sale.order", "client_order_ref", "sale"],
    ["SO03", "", "ExtRef", "String", "50", "No", "Referencia externa", "", "sale.order", "origin", "sale"],
    ["SO03", "", "Status", "Int", "", "Sí", "Estado del pedido", "", "sale.order", "state", "sale"],
    ["SO03", "", "UserInfo1", "String", "50", "No", "Campo usuario 1", "", "sale.order", "x_userinfo1", "base"],
    ["SO03", "", "UserInfo2", "String", "50", "No", "Campo usuario 2", "", "sale.order", "x_userinfo2", "base"],
    ["SO03", "", "UserInfo3", "String", "50", "No", "Campo usuario 3", "", "sale.order", "x_userinfo3", "base"],
    ["SO03", "", "UserInfo4", "String", "50", "No", "Campo usuario 4", "", "sale.order", "x_userinfo4", "base"],
    ["SO03", "", "UserInfo5", "String", "50", "No", "Campo usuario 5", "", "sale.order", "x_userinfo5", "base"],
    ["SO04", "<sdiLSorItem>", "", "", "", "Sí", "Lista de ítems", "", "sale.order.line", "", "sale"],
    ["SO04", "", "LCount", "Int", "", "Sí", "Cantidad de ítems", "", "", "", ""],
    ["SO05", "<sdiSorItem>", "", "", "", "Sí", "Ítem del pedido", "", "sale.order.line", "", "sale"],
    ["SO05", "", "Seq", "Int", "", "Sí", "Secuencia del ítem", "", "sale.order.line", "sequence", "sale"],
    ["SO05", "", "StockCode", "String", "20", "Sí", "Código del ítem", "", "sale.order.line", "product_id", "sale"],
    ["SO05", "", "ProductName", "String", "100", "Sí", "Nombre del producto", "", "sale.order.line", "name", "sale"],
    ["SO05", "", "Quantity", "Double", "", "Sí", "Cantidad", "", "sale.order.line", "product_uom_qty", "sale"],
    ["SO05", "", "UnitCode", "String", "8", "Sí", "Unidad de medida", "", "sale.order.line", "product_uom", "sale"],
    ["SO05", "", "UnitValue", "Double", "", "Sí", "Valor unitario", "", "sale.order.line", "price_unit", "sale"],
    ["SO05", "", "TotalValue", "Double", "", "Sí", "Valor total", "", "sale.order.line", "price_subtotal", "sale"],
    ["SO05", "", "DeliveryDt", "TDateTime", "", "No", "Fecha entrega ítem", "", "sale.order.line", "commitment_date", "sale"],
    ["SO05", "", "CFOP", "String", "5", "No", "Operación fiscal", "", "sale.order.line", "cfop_id", "l10n_ar"],
    ["SO06", "<sdiLSorItemDelivery>", "", "", "", "No", "Entregas del ítem", "", "stock.move", "", "stock"],
    ["SO06", "", "LCount", "Int", "", "Sí", "Cantidad de entregas", "", "", "", ""],
    ["SO07", "<sdiSorItemDelivery>", "", "", "", "No", "Entrega del ítem", "", "stock.move", "", "stock"],
    ["SO07", "", "Seq", "Int", "", "Sí", "Secuencia entrega", "", "stock.move", "sequence", "stock"],
    ["SO07", "", "Quantity", "Double", "", "Sí", "Cantidad entregada", "", "stock.move", "product_uom_qty", "stock"],
    ["SO07", "", "DeliveryDt", "TDateTime", "", "Sí", "Fecha entrega", "", "stock.move", "date", "stock"],
    ["SO08", "<sdiSorCustomer>", "", "", "", "No", "Datos adicionales del cliente", "", "res.partner", "", "base"],
    ["SO08", "", "Code", "String", "20", "Sí", "Código del cliente", "", "res.partner", "id", "base"],
    ["SO08", "", "Name", "String", "70", "Sí", "Nombre del cliente", "", "res.partner", "name", "base"],
    ["SO08", "", "ExtRef", "String", "50", "No", "Referencia externa", "", "res.partner", "ref", "base"],
    ["SO08", "", "CountryDocumentNumber", "String", "35", "No", "RUC/RUT/CUIT", "", "res.partner", "vat", "base"],
]

# ========================
# BIL - Facturas/Remisiones
# ========================
bil_data = [
    ["BE01", "<metrics>", "", "", "", "Sí", "Inicia y finaliza el archivo XML", "", "", "", ""],
    ["BE02", "<sdiBilInvoice>", "", "", "", "Sí", "Factura fiscal", "", "account.move", "", "account"],
    ["BE03", "<sdiBilInvoiceInfo>", "", "", "", "Sí", "Info factura", "", "account.move", "", "account"],
    ["BE03", "", "InvoiceReqNumber", "String", "10", "Sí", "N° solicitud factura", "", "account.move", "name", "account"],
    ["BE03", "", "InvoiceNumber", "String", "10", "Sí", "N° factura fiscal", "", "account.move", "l10n_latam_document_number", "l10n_ar"],
    ["BE03", "", "InvoiceCompl", "String", "3", "Sí", "Serie factura", "", "account.move", "l10n_latam_document_number", "l10n_ar"],
    ["BE03", "", "Status", "Int", "", "Sí", "1=No procesado, 2=Procesado, 3=Cancelado", "", "account.move", "state", "account"],
    ["BE03", "", "EmissionDt", "TDateTime", "", "Sí", "Fecha emisión", "", "account.move", "invoice_date", "account"],
    ["BE03", "", "IdCompany", "Int", "", "Sí", "Código empresa", "", "account.move", "company_id", "base"],
    ["BE03", "", "Extref", "String", "50", "Sí", "Referencia externa", "", "account.move", "ref", "account"],
    ["BE03", "", "UserInfo1", "String", "50", "No", "Campo usuario 1", "", "account.move", "x_userinfo1", "base"],
    ["BE03", "", "UserInfo2", "String", "50", "No", "Campo usuario 2", "", "account.move", "x_userinfo2", "base"],
    ["BE03", "", "UserInfo3", "String", "50", "No", "Campo usuario 3", "", "account.move", "x_userinfo3", "base"],
    ["BE03", "", "UserInfo4", "String", "50", "No", "Campo usuario 4", "", "account.move", "x_userinfo4", "base"],
    ["BE03", "", "UserInfo5", "String", "50", "No", "Campo usuario 5", "", "account.move", "x_userinfo5", "base"],
    ["BE03", "", "InvoiceType", "Int", "", "Sí", "0=Compra, 1=Venta, 2=Dev.Compra, 3=Dev.Venta", "", "account.move", "move_type", "account"],
    ["BE03", "", "InvoiceMessage", "Text", "", "Sí", "Mensaje factura", "", "account.move", "narration", "account"],
    ["BE03", "", "IsBrokerResponsiblePayment", "Boolean", "", "Sí", "Agencia responsable pago?", "", "", "", ""],
    ["BE03", "", "accesskey", "String", "100", "No", "Llave acceso FFe", "", "account.move", "l10n_latam_document_access_key", "l10n_ar"],
    ["BE04", "<sdiBilPayConInfo>", "", "", "", "Sí", "Condiciones de pago", "", "account.move", "", "account"],
    ["BE04", "", "ConditionCode", "String", "30", "Sí", "Código condición pago", "", "account.move", "invoice_payment_term_id", "account"],
    ["BE04", "", "ExtRef", "String", "30", "Sí", "Ref. sistema externo", "", "account.move", "ref", "account"],
    ["BE05", "<sdiLBilPayCondDueDate>", "", "", "", "Sí", "Vencimientos", "", "account.move.line", "", "account"],
    ["BE05", "", "LCount", "Int", "", "Sí", "Cantidad vencimientos", "", "", "", ""],
    ["BE06", "<sdiBilPayCondDueDate>", "", "", "", "Sí", "Vencimiento", "", "account.move.line", "", "account"],
    ["BE06", "", "DueDate", "TDateTime", "", "Sí", "Fecha vencimiento", "", "account.move.line", "date_maturity", "account"],
    ["BE06", "", "Value", "Double", "", "Sí", "Valor vencimiento", "", "account.move.line", "amount_residual", "account"],
    ["BE07", "<sdilAddress>", "", "", "", "Sí", "Direcciones facturación", "", "res.partner", "", "base"],
    ["BE07", "", "LCount", "Int", "", "Sí", "Cantidad direcciones", "", "", "", ""],
    ["BE08", "<sdiBilAddress>", "", "", "", "Sí", "Dirección facturación", "", "res.partner", "", "base"],
    ["BE08", "", "AddressPrefix", "String", "10", "Sí", "Calle/Avenida", "", "res.partner", "street", "base"],
    ["BE08", "", "AddressName", "String", "100", "Sí", "Descripción dirección", "", "res.partner", "street", "base"],
    ["BE08", "", "AddressNumber", "String", "10", "Sí", "Número", "", "res.partner", "street", "base"],
    ["BE08", "", "AddressComplement", "String", "60", "No", "Complemento", "", "res.partner", "street2", "base"],
    ["BE08", "", "District", "String", "60", "Sí", "Barrio", "", "res.partner", "street3", "base"],
    ["BE08", "", "ZipCode", "String", "20", "Sí", "Código postal", "", "res.partner", "zip", "base"],
    ["BE08", "", "CityName", "String", "70", "Sí", "Ciudad", "", "res.partner", "city", "base"],
    ["BE08", "", "StateName", "String", "70", "Sí", "Estado", "", "res.partner", "state_id", "base"],
    ["BE08", "", "CountryName", "String", "70", "Sí", "País", "", "res.partner", "country_id", "base"],
    ["BE08", "", "IsBilling", "Boolean", "", "Sí", "Direc. facturación?", "", "res.partner", "type", "base"],
    ["BE08", "", "IsCharging", "Boolean", "", "Sí", "Direc. cobro?", "", "res.partner", "type", "base"],
    ["BE08", "", "IsDelivery", "Boolean", "", "Sí", "Direc. entrega?", "", "res.partner", "type", "base"],
    ["BE08", "", "ExtRef", "String", "50", "No", "Ref. externa", "", "res.partner", "ref", "base"],
    ["BE09", "<sdiBilCustomerInfo>", "", "", "", "Sí", "Info cliente", "", "res.partner", "", "base"],
    ["BE09", "", "Code", "String", "32", "Sí", "Código cliente", "", "account.move", "partner_id", "account"],
    ["BE09", "", "Name", "String", "70", "Sí", "Nombre fantasía", "", "res.partner", "name", "base"],
    ["BE09", "", "ExtRef", "String", "50", "Sí", "Ref. externa cliente", "", "res.partner", "ref", "base"],
    ["BE09", "", "ContactName", "String", "75", "Sí", "Nombre contacto", "", "account.move", "partner_id.name", "account"],
    ["BE10", "<sdiLBilItemInfo>", "", "", "", "Sí", "Lista ítems factura", "", "account.move.line", "", "account"],
    ["BE10", "", "LCount", "Int", "", "Sí", "Cantidad ítems", "", "", "", ""],
    ["BE11", "<sdiBilItemInfo>", "", "", "", "Sí", "Ítem factura", "", "account.move.line", "", "account"],
    ["BE11", "", "ItemID", "String", "20", "Sí", "Código interno Metrics", "", "account.move.line", "id", "account"],
    ["BE11", "", "Seq", "Int", "", "Sí", "Secuencial", "", "account.move.line", "sequence", "account"],
    ["BE11", "", "StockCode", "String", "20", "Sí", "Código ítem Metrics", "", "account.move.line", "product_id", "account"],
    ["BE11", "", "CustomerStockCode", "String", "30", "Sí", "Código ítem proveedor", "", "", "", ""],
    ["BE11", "", "ProductName", "String", "400", "Sí", "Descripción producto", "", "account.move.line", "name", "account"],
    ["BE11", "", "UnitValue", "Double", "", "Sí", "Valor unitario", "", "account.move.line", "price_unit", "account"],
    ["BE11", "", "Quantity", "Double", "", "Sí", "Cantidad total", "", "account.move.line", "quantity", "account"],
    ["BE11", "", "TotalValue", "Double", "", "Sí", "Valor total", "", "account.move.line", "price_subtotal", "account"],
    ["BE11", "", "UnitCode", "String", "10", "Sí", "Unidad", "", "account.move.line", "product_uom_id", "account"],
    ["BE11", "", "CFOP", "String", "5", "Sí", "Operación ítem", "", "account.move.line", "l10n_latam_document_cfop_id", "l10n_ar"],
    ["BE11", "", "CustomerPurchaseOrder", "Varchar", "15", "No", "N° OC cliente", "", "account.move.line", "purchase_order_name", "account"],
    ["BE11", "", "CustomerItemPurchaseOrder", "Varchar", "6", "No", "N° ítem OC", "", "", "", ""],
    ["BE12", "<sdiBilItemReturned>", "", "", "", "No", "Factura devuelta", "", "account.move", "", "account"],
    ["BE12", "", "ReturnedInvoiceNumber", "Int", "", "Sí", "N° factura origen", "", "account.move", "reversed_entry_id", "account"],
    ["BE12", "", "ReturnedInvoiceCompl", "String", "3", "Sí", "Serie factura origen", "", "account.move", "reversed_entry_id", "account"],
    ["BE12", "", "Seq", "Int", "", "Sí", "Orden ítem origen", "", "account.move.line", "sequence", "account"],
    ["BE12", "", "ReturnedTotalQuantity", "Double", "", "Sí", "Cantidad devuelta", "", "account.move.line", "quantity", "account"],
    ["BE12", "", "UnitCode", "String", "5", "Sí", "Unidad", "", "account.move.line", "product_uom_id", "account"],
    ["BE12", "", "ReturnedTotalValue", "Double", "", "Sí", "Valor devuelto", "", "account.move.line", "price_subtotal", "account"],
    ["BE13", "<sdiBilLItemReturnedDetail>", "", "", "", "No", "Detalle lotes devueltos", "", "stock.move.line", "", "stock"],
    ["BE13", "", "LCount", "Int", "", "Sí", "Cantidad lotes", "", "", "", ""],
    ["BE14", "<sdiBilItemReturnedDetail>", "", "", "", "No", "Lote devuelto", "", "stock.move.line", "", "stock"],
    ["BE14", "", "ReturnedQuantity", "Double", "", "Sí", "Cantidad devuelta", "", "stock.move.line", "qty_done", "stock"],
    ["BE14", "", "UnitCode", "String", "5", "", "Unidad", "", "stock.move.line", "product_uom_id", "stock"],
    ["BE14", "", "Lot", "String", "20", "", "Lote stock", "", "stock.move.line", "lot_id", "stock"],
    ["BE14", "", "StockPlaceCode", "String", "20", "", "Local stock", "", "stock.move.line", "location_id", "stock"],
    ["BE14", "", "StockAddress", "String", "20", "", "Localización stock", "", "stock.move.line", "location_dest_id", "stock"],
    ["BE15", "<sdiLBilItemTaxInfo>", "", "", "", "No", "Impuestos ítem", "", "account.tax", "", "account"],
    ["BE15", "", "LCount", "Int", "", "Sí", "Cantidad impuestos", "", "", "", ""],
    ["BE16", "<sdiBilItemTaxInfo>", "", "", "", "No", "Impuesto ítem", "", "account.tax", "", "account"],
    ["BE16", "", "Name", "String", "16", "Sí", "Nombre tasa", "", "account.tax", "name", "account"],
    ["BE16", "", "Value", "Double", "", "Sí", "Valor impuesto", "", "account.move.line", "tax_base_amount", "account"],
    ["BE17", "<sdiLBilItemCommissionInfo>", "", "", "", "No", "Comisiones ítem", "", "", "", ""],
    ["BE18", "<sdiBilItemCommissionInfo>", "", "", "", "No", "Comisión ítem", "", "", "", ""],
]

# ========================
# WIP - Work-in-Progress
# ========================
wip_data = [
    ["WP01", "<sdiWIPLabel>", "", "", "", "Sí", "Etiqueta WIP", "Solo exportación", "mrp.workorder", "", "mrp"],
    ["WP01", "", "IdPalletLabel", "Int", "", "Sí", "Código etiqueta pallet", "", "mrp.workorder", "id", "mrp"],
    ["WP01", "", "BarCode", "String", "100", "Sí", "Código barras WIP", "", "mrp.workorder", "barcode", "mrp"],
    ["WP01", "", "Quantity", "Double", "", "Sí", "Cantidad WIP", "", "mrp.workorder", "qty_produced", "mrp"],
    ["WP01", "", "QuantityKG", "Double", "", "No", "Cantidad Kg", "", "", "", ""],
    ["WP01", "", "UnitCode", "String", "10", "Sí", "Unidad medida", "", "mrp.workorder", "product_uom_id", "mrp"],
    ["WP01", "", "IsValid", "Boolean", "", "No", "Validada?", "", "mrp.workorder", "is_validated", "mrp"],
    ["WP01", "", "DtValidation", "TDateTime", "", "No", "Fecha validación", "", "mrp.workorder", "date_start", "mrp"],
    ["WP01", "", "UserValidation", "String", "32", "No", "Usuario validó", "", "mrp.workorder", "user_id", "mrp"],
    ["WP01", "", "Status", "Int", "", "Sí", "1=Esperando, 2=En Uso, 3=Procesado, 4=Parcial, 5=No usado, 6=Cancelado, 7=Dividido, 8=En máquina, 9=Bloqueado, 10=Revisión", "", "mrp.workorder", "state", "mrp"],
    ["WP01", "", "InsDt", "TDateTime", "", "Sí", "Fecha ingreso", "", "mrp.workorder", "create_date", "base"],
    ["WP01", "", "InsUser", "String", "32", "", "Usuario ingresó", "", "mrp.workorder", "create_uid", "base"],
    ["WP01", "", "IsFinalProduct", "Boolean", "", "No", "Es producto final?", "", "mrp.workorder", "is_final_product", "mrp"],
    ["WP01", "", "StkCode", "String", "20", "Sí", "Código ítem stock", "", "mrp.workorder", "product_id", "mrp"],
    ["WP01", "", "StkDescription", "String", "100", "No", "Descripción ítem", "", "mrp.workorder", "name", "mrp"],
    ["WP01", "", "Shift", "Int", "", "No", "Turno", "", "", "", ""],
    ["WP01", "", "Note", "String", "50", "No", "Observación", "", "mrp.workorder", "note", "mrp"],
    ["WP01", "", "PalletWeight", "Double", "", "No", "Peso pallet", "", "stock.move.line", "weight", "stock"],
    ["WP01", "", "IsBobbin", "Boolean", "", "No", "Es bobina?", "", "", "", ""],
    ["WP01", "", "ComponentId", "String", "32", "", "ID componente", "", "stock.move.line", "component_id", "mrp"],
    ["WP01", "", "Lot", "String", "20", "No", "Lote ítem", "", "stock.move.line", "lot_id", "stock"],
    ["WP01", "", "ProcessID", "Int", "", "Sí", "Código proceso (vínculo WO.idativ)", "", "mrp.workorder", "operation_id", "mrp"],
    ["WP01", "", "ProcessDescription", "String", "200", "No", "Descripción proceso", "", "mrp.routing.workcenter", "name", "mrp"],
    ["WP02", "<sdiWIPTransaction>", "", "", "", "Sí", "Transacción etiqueta WIP", "", "stock.move", "", "stock"],
    ["WP02", "", "TransactionType", "Int", "", "Sí", "1=Nuevo, 2=Validación, 3=Movimiento, 4=Pesaje, 7=Finalización, 10=Entrada stock, 16=Dividida, 17=Consumido total, 18=Consumido parcial, 20=Entrega Prod, 24=Reapertura, 27=Cancelado", "", "stock.move", "type", "stock"],
    ["WP02", "", "IdPalletLabel", "Int", "", "Sí", "Código etiqueta pallet", "", "stock.move", "workorder_id", "mrp"],
    ["WP02", "", "TransactionDt", "TDateTime", "", "Sí", "Fecha transacción", "", "stock.move", "date", "stock"],
    ["WP02", "", "Status", "Int", "", "Sí", "Situación etiqueta", "", "stock.move", "state", "stock"],
    ["WP02", "", "QtyBefore", "Double", "", "Sí", "Cantidad antes", "", "stock.move.line", "qty_before", "stock"],
    ["WP02", "", "QtyAfter", "Double", "", "Sí", "Cantidad después", "", "stock.move.line", "qty_done", "stock"],
    ["WP02", "", "UnitCode", "String", "10", "Sí", "Unidad medida", "", "stock.move.line", "product_uom_id", "stock"],
    ["WP02", "", "QtyBeforeKG", "Double", "", "No", "Cantidad antes Kg", "", "", "", ""],
    ["WP02", "", "QtyAfterKG", "Double", "", "No", "Cantidad después Kg", "", "", "", ""],
    ["WP02", "", "StockPlaceCodeBefore", "String", "32", "No", "Local stock antes", "", "stock.move.line", "location_id", "stock"],
    ["WP02", "", "StockPlaceCodeAfter", "String", "32", "No", "Local stock después", "", "stock.move.line", "location_dest_id", "stock"],
    ["WP02", "", "StockAddressBefore", "String", "30", "No", "Localización antes", "", "stock.move.line", "location_id", "stock"],
    ["WP02", "", "StockAddressAfter", "String", "30", "No", "Localización después", "", "stock.move.line", "location_dest_id", "stock"],
    ["WP02", "", "LogUser", "String", "32", "No", "Usuario transacción", "", "stock.move", "write_uid", "base"],
    ["WP02", "", "Note", "String", "100", "No", "Observaciones", "", "stock.move", "note", "stock"],
    ["WP02", "", "Lot", "String", "20", "No", "Lote ítem", "", "stock.move.line", "lot_id", "stock"],
    ["WP02", "", "MachineInputCode", "String", "30", "No", "Código entrada máquina", "", "", "", ""],
]

# ========================
# Mapeo Complejo - Reglas de Transformación
# ========================
complejo_data = [
    ["R01", "CRM / STKItem", "UnitCode", "product.product", "uom_id", "Búsqueda por nombre",
     "Buscar UOM en Odoo por nombre exacto o símbolo (ej: 'KG'→'kg', 'UN'→'Units', 'FL'→'Units', 'PZ'→'Dozens'). Si no existe, crear registro en uom.uom.",
     "base"],
    ["R02", "CRM", "PersonType (0/1/2/3)", "res.partner", "company_type", "Mapeo directo",
     "0=Física→'person', 1=Jurídica→'company', 2=Gobierno→'company', 3=Exportación→'company'",
     "base"],
    ["R03", "CRM", "CountryDocumentNumber", "res.partner", "vat / l10n_latam_identification_type_id", "Validación + busqueda tipo ID",
     "Según país: AR→validar CUIT (11 dígitos) y asignar l10n_latam_identification_type_id=1 (CUIT parcial) o type_id de CUIT según código 80. PE→RUC, CL→RUT, etc.",
     "l10n_ar"],
    ["R04", "CRM", "CountryCode (BACEN)", "res.partner", "country_id", "Mapeo código BACEN",
     "Mapa: 54=Argentina (base.ar), 76=Brasil, 858=Uruguay, etc. Buscar res.country por código BACEN en caso de existir campo, o por código ISO.",
     "base"],
    ["R05", "CRM", "CountryFiscalCode", "res.partner", "l10n_ar_afip_responsibility_type_id", "Mapeo código fiscal",
     "Mapa según código fiscal del país. En Argentina: 1=IVA Responsable Inscripto, 2=IVA Sujeto Exento, 3=IVA Monotributo, 4=IVA No Responsable, 5=IVA Consumidor Final, etc.",
     "l10n_ar"],
    ["R06", "CRM", "IsCustomer / IsSupplier / IsPerson", "res.partner", "customer_rank / supplier_rank / company_type", "Cálculo booleano",
     "IsCustomer=1→customer_rank=1 (o >0). IsSupplier=1→supplier_rank=1. IsPerson=1→company_type='person', sino 'company'. Los 3 pueden coexistir.",
     "base"],
    ["R07", "STKItem", "ItemType (0-4)", "product.product", "type (product/consu/service)", "Mapeo directo",
     "0=MP→'product' (almacenar), 1=PT→'product', 2=Intermediario→'product', 3=Servicio→'service', 4=Consumible→'consu'",
     "base"],
    ["R08", "STKItem", "MaterialType (0-6)", "product.category", "categ_id", "Mapeo + creación categorías",
     "Crear categorías hijas de una categoría raíz 'Metrics' según MaterialType: 1='Tinta', 2='Plancha', 3='Otros', 4='Papel Hoja', 5='Papel Bobina', 6='Personalizado'.",
     "base"],
    ["R09", "STKItem", "UseLot / ControlTraceability", "product.product", "tracking", "Mapeo condicional",
     "UseLot=1 → tracking='lot'. ControlTraceability=1 → tracking='serial'. Si ambos=1 → tracking='serial' (más restrictivo). Si ambos=0 → tracking='none'.",
     "stock"],
    ["R10", "STKItem", "MaterialGroupCode+Desc / MasterMaterialGroupCode+Desc", "product.category", "categ_id / parent_id", "Crear jerarquía de categorías",
     "Crear categorías: MasterMaterialGroup (nivel 1) → MaterialGroup (nivel 2) → Producto (asignado a nivel 2). Buscar por código, crear si no existe.",
     "base"],
    ["R11", "STK", "transactiontype (0-10)", "stock.picking", "picking_type_id", "Mapeo a tipo de operación",
     "0=Recepciones, 1=Entrega Fabricación→picking_type producción, 2=Compras→Recepciones, 3=Ventas→Delivery, 4=Inventario→Recuento, 5/6/7/8=Transferencias internas, 9=Ajuste→Ajuste inventario, 10=Otro→picking manual.",
     "stock"],
    ["R12", "STK", "stockmovementtype (0/1/2)", "stock.move", "type (in/out/internal)", "Mapeo directo",
     "0=Entrada→'in', 1=Salida→'out', 2=Ajuste→'internal' (usar location_id = inventory adjustment)",
     "stock"],
    ["R13", "WO", "status (0-6)", "mrp.production", "state", "Mapeo directo",
     "0=Pendiente→'confirmed', 1=Procesando→'progress', 2=Terminada→'done', 3=Cerrada→'done', 4=Parada→'cancelled', 5=Bloqueada→'confirmed', 6=Evaluación→'confirmed'",
     "mrp"],
    ["R14", "WO / WIP", "idativ", "mrp.workorder", "operation_id", "Mapeo de vínculo",
     "WO.sdiwooperation.idativ ↔ WIP.ProcessID. Usar como reference externa para vincular operaciones de ruta (mrp.routing.workcenter) con workorders.",
     "mrp"],
    ["R15", "SOR", "Status", "sale.order", "state", "Mapeo directo",
     "Mapear estados: 0/1=Borrador→'draft', 2=Confirmado→'sale', 3=Enviado→'sent', 4=Entregado→'done', 5=Cancelado→'cancel'",
     "sale"],
    ["R16", "BIL", "InvoiceType (0/1/2/3)", "account.move", "move_type", "Mapeo directo",
     "0=Compra→'in_invoice', 1=Venta→'out_invoice', 2=Dev.Compra→'in_refund', 3=Dev.Venta→'out_refund'",
     "account"],
    ["R17", "BIL", "InvoiceNumber + InvoiceCompl", "account.move", "l10n_latam_document_number", "Concatenación con formato",
     "Formato argentino: '0001-00001234' donde 0001=PV (punto de venta, de InvoiceCompl) y 00001234=InvoiceNumber. Se completa con ceros a la izquierda.",
     "l10n_ar"],
    ["R18", "BIL", "InvoiceType + CFOP", "account.move.line", "l10n_latam_document_cfop_id", "Mapeo según operación",
     "CFOP depende del tipo de operación y si es dentro del mismo estado. Argentina: usar posición fiscal del partner para determinar CFOP automáticamente.",
     "l10n_ar"],
    ["R19", "BIL / CRM", "Address: IsBilling/IsCharging/IsDelivery", "res.partner", "type", "Lógica de tipo dirección",
     "IsBilling=1→'invoice'. IsDelivery=1→'delivery'. IsCharging=1→'other'. Si hay múltiples tipos, crear contactos separados con cada tipo.",
     "base"],
    ["R20", "WIP", "TransactionType (1,17,18,10)", "stock.move", "type / reference", "Mapeo a tipo de movimiento",
     "1=Nuevo→workorder creation, 10=Entrada stock→'in', 17=Consumido total→'out', 18=Consumido parcial→'out' (con qty parcial). Vincular a stock.move a través de workorder_id.",
     "stock"],
    ["R21", "CRM", "BroptingSimpleNational (0-3)", "res.partner", "l10n_ar_afip_responsibility_type_id", "Mapeo a responsabilidad AFIP",
     "0=Ningún→según VAT, 1=Simple Nacional→Monotributo (código 4/6), 2=Simple Exceso→Monotributo excedido, 3=Régimen Normal→Responsable Inscripto (código 1/2)",
     "l10n_ar"],
    ["R22", "CRM", "AddressPrefix + AddressName + AddressNumber", "res.partner", "street", "Concatenación",
     "Concatenar: 'AddressPrefix + AddressName + \", \" + AddressNumber'. Ej: 'Av. Corrientes 1234'",
     "base"],
    ["R23", "CRM (ADHOC)", "gross_income_jurisdiction_ids", "res.partner", "gross_income_jurisdiction_ids", "Por defecto provincia del partner",
     "Si no se informan jurisdictions de IIBB, usar la provincia (state_id) del partner como jurisdiction principal. Adhoc módulo l10n_ar_ux.",
     "l10n_ar_ux"],
]

# Create sheets
ws_crm = wb.active
write_sheet(ws_crm, "CRM - Relaciones", crm_data)

ws_stkitem = wb.create_sheet()
write_sheet(ws_stkitem, "STKItem - Itens Stock", stkitem_data)

ws_stk = wb.create_sheet()
write_sheet(ws_stk, "STK - Movimientos Stock", stk_data)

ws_wo = wb.create_sheet()
write_sheet(ws_wo, "WO - Ordenes Produccion", wo_data)

ws_sor = wb.create_sheet()
write_sheet(ws_sor, "SOR - Pedidos Venta", sor_data)

ws_bil = wb.create_sheet()
write_sheet(ws_bil, "BIL - Facturas", bil_data)

ws_wip = wb.create_sheet()
write_sheet(ws_wip, "WIP - Work in Progress", wip_data)

ws_complejo = wb.create_sheet()
write_complejo_sheet(ws_complejo, complejo_data)

output_file = "C:/Users/passagliavanesa/Documents/XMLs2/Metrics_Integracion_XML_Tablas.xlsx"
wb.save(output_file)
print(f"Excel generado: {output_file}")
print("Hojas creadas:")
print("  1. CRM - Relaciones (Clientes/Proveedores) + mapeo Odoo")
print("  2. STKItem - Itens Stock + mapeo Odoo")
print("  3. STK - Movimientos Stock + mapeo Odoo")
print("  4. WO - Ordenes Produccion + mapeo Odoo")
print("  5. SOR - Pedidos Venta + mapeo Odoo")
print("  6. BIL - Facturas + mapeo Odoo")
print("  7. WIP - Work in Progress + mapeo Odoo")
print("  8. Mapeo Complejo - Reglas de transformación")
