# -*- coding: utf-8 -*-
from odoo import fields, models
from odoo.exceptions import UserError


class StockPickingBatchImportWizard(models.TransientModel):
    _name = "stock.picking.batch.import.wizard"
    _description = "Stock Picking Batch Import Wizard"
    _inherit = "batch_add.batch_import_wizard_mixin"

    picking_id = fields.Many2one("stock.picking", required=True, readonly=True)
    line_ids = fields.One2many(
        "stock.picking.batch.import.line",
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

        move_vals = [
            (0, 0, self._prepare_picking_move_vals(line.product_id, line.quantity))
            for line in lines_to_add
        ]
        self.picking_id.write({"move_ids_without_package": move_vals})
        return {"type": "ir.actions.act_window_close"}

    def _prepare_picking_move_vals(self, product, quantity):
        vals = {
            "picking_id": self.picking_id.id,
            "name": product.display_name,
            "product_id": product.id,
            "product_uom_qty": quantity,
            "product_uom": product.uom_id.id,
            "location_id": self.picking_id.location_id.id,
            "location_dest_id": self.picking_id.location_dest_id.id,
            "company_id": self.picking_id.company_id.id,
            "picking_type_id": self.picking_id.picking_type_id.id,
        }
        return self._prepare_stock_move_vals(vals)

    def _prepare_stock_move_vals(self, vals):
        Move = self.env["stock.move"]
        new_move = Move.new(vals)
        if hasattr(new_move, "_onchange_product_id"):
            new_move._onchange_product_id()
        if hasattr(new_move, "_onchange_product_uom_qty"):
            new_move._onchange_product_uom_qty()
        if hasattr(new_move, "_onchange_quantity"):
            new_move._onchange_quantity()
        return new_move._convert_to_write(new_move._cache)

    def _get_product_domain(self):
        Product = self.env["product.product"]
        if "detailed_type" in Product._fields:
            return [("detailed_type", "in", ("product", "consu"))]
        return [("type", "in", ("product", "consu"))]


class StockPickingBatchImportLine(models.TransientModel):
    _name = "stock.picking.batch.import.line"
    _description = "Stock Picking Batch Import Line"

    wizard_id = fields.Many2one(
        "stock.picking.batch.import.wizard",
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
        domain=[("type", "in", ("product", "consu"))],
    )
    candidate_product_ids = fields.Many2many("product.product", string="Candidates")
