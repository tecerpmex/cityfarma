# -*- coding: utf-8 -*-
from odoo import SUPERUSER_ID, _, api, fields, models

class StockMove(models.Model):
    _inherit = "stock.move"


    @api.depends()
    def _action_assign(self):
        for invoice in self.sale_line_id.invoice_lines.move_id:
            if invoice.payment_state in ('paid', 'in_payment'):
                super()._action_assign()
            else:
                pass