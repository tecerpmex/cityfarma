# -*- coding: utf-8 -*-
from odoo import SUPERUSER_ID, _, api, fields, models

class StockMove(models.Model):
    _inherit = "stock.move"


    @api.depends()
    def _action_assign(self):
        for move in self:
            if move.picking_type_id.code == 'outgoing':
                for sale_line in move.sale_line_id:
                    for invoice in sale_line.invoice_lines.move_id:
                        if invoice.payment_state in ('paid', 'in_payment'):
                            super(StockMove, move)._action_assign()
                        else:
                            pass
            else:
                super(StockMove, move)._action_assign()
