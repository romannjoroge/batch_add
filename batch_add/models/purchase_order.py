# -*- coding: utf-8 -*-
from odoo import models


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    def action_open_batch_import_wizard(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": "Batch Add Purchase Lines",
            "res_model": "purchase.order.batch.import.wizard",
            "view_mode": "form",
            "target": "new",
            "context": {
                "default_order_id": self.id,
            },
        }

