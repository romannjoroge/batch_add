# -*- coding: utf-8 -*-
from odoo import models
from odoo.exceptions import UserError


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    def action_open_batch_import_wizard(self):
        order = self.order_id[:1]
        if not order:
            order_id = self.env.context.get("active_id")
            if order_id:
                order = self.env["purchase.order"].browse(order_id).exists()
        if not order:
            raise UserError("Please save the Purchase Order first.")
        return order.action_open_batch_import_wizard()
