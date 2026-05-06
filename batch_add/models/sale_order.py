# -*- coding: utf-8 -*-
from odoo import models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def action_open_batch_import_wizard(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": "Batch Add Order Lines",
            "res_model": "sale.order.batch.import.wizard",
            "view_mode": "form",
            "target": "new",
            "context": {
                "default_order_id": self.id,
            },
        }

