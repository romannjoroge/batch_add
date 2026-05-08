# -*- coding: utf-8 -*-
from odoo import fields, models
from odoo.exceptions import UserError


class PurchaseOrderBatchImportWizard(models.TransientModel):
    _name = "purchase.order.batch.import.wizard"
    _description = "Purchase Order Batch Import Wizard"
    _inherit = "batch_add.batch_import_wizard_mixin"

    order_id = fields.Many2one("purchase.order", required=True, readonly=True)
    line_ids = fields.One2many(
        "purchase.order.batch.import.line",
        "wizard_id",
        string="Lines",
    )

    def action_apply_lines(self):
        self.ensure_one()
        if not self.line_ids:
            raise UserError("There are no lines to apply. Parse a CSV first.")

        lines_to_add = self.line_ids.filtered(lambda line: line.product_id and line.quantity > 0)
        if not lines_to_add:
            raise UserError("Please select at least one product to add.")

        order_lines = [
            (0, 0, self._prepare_po_line_vals(line.product_id, line.quantity))
            for line in lines_to_add
        ]
        self.order_id.write({"order_line": order_lines})
        return {"type": "ir.actions.act_window_close"}

    def _prepare_po_line_vals(self, product, quantity):
        PurchaseLine = self.env["purchase.order.line"]
        vals = {
            "order_id": self.order_id.id,
            "product_id": product.id,
            "product_qty": quantity,
        }

        if "product_uom" in PurchaseLine._fields:
            vals["product_uom"] = (product.uom_po_id or product.uom_id).id
        if "date_planned" in PurchaseLine._fields:
            vals["date_planned"] = fields.Datetime.now()

        new_line = PurchaseLine.new(vals)
        if hasattr(new_line, "_onchange_product_id"):
            new_line._onchange_product_id()
        if hasattr(new_line, "_onchange_quantity"):
            new_line._onchange_quantity()
        if hasattr(new_line, "_onchange_product_qty"):
            new_line._onchange_product_qty()
        return new_line._convert_to_write(new_line._cache)

    def _get_product_domain(self):
        return [("purchase_ok", "=", True)]


class PurchaseOrderBatchImportLine(models.TransientModel):
    _name = "purchase.order.batch.import.line"
    _description = "Purchase Order Batch Import Line"

    wizard_id = fields.Many2one(
        "purchase.order.batch.import.wizard",
        required=True,
        ondelete="cascade",
    )
    row_no = fields.Integer(string="Row")
    raw_data = fields.Text(string="Raw Data")
    description = fields.Char(string="Description")
    quantity = fields.Float(string="Quantity", default=1.0)
    match_status = fields.Selection(
        [
            ("matched", "Matched"),
            ("multiple", "Multiple Matches"),
            ("no_match", "No Match"),
        ],
        string="Status",
    )
    product_id = fields.Many2one(
        "product.product",
        string="Product",
        domain=[("purchase_ok", "=", True)],
    )
    candidate_product_ids = fields.Many2many(
        "product.product",
        string="Candidates",
    )
