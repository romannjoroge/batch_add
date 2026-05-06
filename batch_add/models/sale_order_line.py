# -*- coding: utf-8 -*-
from odoo import models
from odoo.exceptions import UserError


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    def action_open_batch_import_wizard(self):
        order = self.order_id[:1]
        if not order:
            order_id = self.env.context.get("active_id")
            if order_id:
                order = self.env["sale.order"].browse(order_id).exists()
        if not order:
            raise UserError("Please save the Sales Order first.")
        return order.action_open_batch_import_wizard()
