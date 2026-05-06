# -*- coding: utf-8 -*-
from odoo import models
from odoo.exceptions import UserError


class StockMove(models.Model):
    _inherit = "stock.move"

    def action_open_batch_import_wizard(self):
        """
        Allow placing the Batch Add button inside x2many list controls (which call
        methods on the line model).
        """
        move = self[:1]

        picking = getattr(move, "picking_id", False)
        if picking:
            if not picking:
                raise UserError("Please save the operation first.")
            return picking.action_open_batch_import_wizard()

        production = getattr(move, "raw_material_production_id", False) or getattr(
            move, "production_id", False
        )
        if production:
            return production.action_open_batch_import_wizard()

        active_model = self.env.context.get("active_model")
        active_id = self.env.context.get("active_id")
        if active_model == "stock.picking" and active_id:
            picking = self.env["stock.picking"].browse(active_id).exists()
            if picking:
                return picking.action_open_batch_import_wizard()

        if active_model == "mrp.production" and active_id:
            production = self.env["mrp.production"].browse(active_id).exists()
            if production:
                return production.action_open_batch_import_wizard()

        default_picking_id = self.env.context.get("default_picking_id")
        if default_picking_id:
            picking = self.env["stock.picking"].browse(default_picking_id).exists()
            if picking:
                return picking.action_open_batch_import_wizard()

        default_production_id = self.env.context.get("default_production_id")
        if default_production_id:
            production = self.env["mrp.production"].browse(default_production_id).exists()
            if production:
                return production.action_open_batch_import_wizard()

        raise UserError("Could not determine the parent document for this line.")
