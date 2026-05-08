# -*- coding: utf-8 -*-
{
    "name": "Batch Add (CSV)",
    "version": "18.0.1.0.0",
    "category": "Tools",
    "summary": "Batch add product lines from CSV/Excel with fuzzy matching",
    "description": """
Batch Add (CSV)
===============
Adds a **Batch Add (CSV)** button on your product/component lines to import multiple lines at once from **CSV / Excel**.

Supported documents:
- Sales Orders
- Purchase Orders
- Inventory Operations (Receipts, Deliveries, Internal Transfers)
- Manufacturing Orders (raw material components)

How to use
----------
1. Open the document (SO / PO / Picking / MO).
2. Click **Batch Add (CSV)**.
3. Upload a file (`.csv`, `.xls`, `.xlsx`).
4. Click **Parse File** to preview matches.
5. For any row marked **Multiple Matches** or **No Match**, select the correct product.
6. Click **Add Lines**.

Expected columns
----------------
The importer is flexible: it will use *any* non-quantity columns to build a product description used for matching.

Recommended product identifiers:
- `sku` / `code` / `item code` / `product code` (matches `default_code`)
- `barcode` (matches `barcode`)
- `name` / `product` / `description` (used for fuzzy name matching)

Quantity:
Any header containing one of: `qty`, `quantity`, `qtty`, `amount`, `count`.
""",
    "author": "Jeremy Mumia",
    "license": "LGPL-3",
    "depends": [
        "sale",
        "purchase",
        "stock",
        "mrp",
        "web",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/sale_order_views.xml",
        "views/purchase_order_views.xml",
        "views/stock_picking_views.xml",
        "views/mrp_production_views.xml",
        "wizards/sale_order_batch_import_views.xml",
        "wizards/purchase_order_batch_import_views.xml",
        "wizards/stock_picking_batch_import_views.xml",
        "wizards/mrp_production_batch_import_views.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "batch_add/static/src/js/batch_candidate_picker.js",
            "batch_add/static/src/scss/batch_import_dialog.scss",
            "batch_add/static/src/xml/batch_candidate_picker.xml",
        ],
    },
    "installable": True,
    "application": False,
    "auto_install": False,
}

