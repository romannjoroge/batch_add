# -*- coding: utf-8 -*-
from odoo import models


class MrpProduction(models.Model):
    _inherit = "mrp.production"

    def action_open_batch_import_wizard(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": "Batch Add Components",
            "res_model": "mrp.production.batch.import.wizard",
            "view_mode": "form",
            "target": "new",
            "context": {
                "default_production_id": self.id,
            },
        }

