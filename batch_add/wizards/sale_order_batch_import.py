# -*- coding: utf-8 -*-
from odoo import fields, models
from odoo.exceptions import UserError


class SaleOrderBatchImportWizard(models.TransientModel):
    _name = "sale.order.batch.import.wizard"
    _description = "Sale Order Batch Import Wizard"
    _inherit = "batch_add.batch_import_wizard_mixin"

    order_id = fields.Many2one("sale.order", required=True, readonly=True)
    line_ids = fields.One2many(
        "sale.order.batch.import.line",
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
            (0, 0, self._prepare_sale_line_vals(line.product_id, line.quantity))
            for line in lines_to_add
        ]
        self.order_id.write({"order_line": order_lines})
        return {"type": "ir.actions.act_window_close"}

    def _prepare_sale_line_vals(self, product, quantity):
        SaleLine = self.env["sale.order.line"]
        vals = {
            "order_id": self.order_id.id,
            "product_id": product.id,
            "product_uom_qty": quantity,
        }

        if "product_uom" in SaleLine._fields:
            vals["product_uom"] = product.uom_id.id

        new_line = SaleLine.new(vals)
        if hasattr(new_line, "_onchange_product_id"):
            new_line._onchange_product_id()
        new_line.product_uom_qty = quantity
        return new_line._convert_to_write(new_line._cache)

    def _get_product_domain(self):
        return [("sale_ok", "=", True)]


class SaleOrderBatchImportLine(models.TransientModel):
    _name = "sale.order.batch.import.line"
    _description = "Sale Order Batch Import Line"

    wizard_id = fields.Many2one(
        "sale.order.batch.import.wizard",
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
        domain=[("sale_ok", "=", True)],
    )
    candidate_product_ids = fields.Many2many(
        "product.product",
        string="Candidates",
    )
