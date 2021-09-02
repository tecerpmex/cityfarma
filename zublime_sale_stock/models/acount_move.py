# -*- coding: utf-8 -*-
from odoo import SUPERUSER_ID, _, api, fields, models

class AccountMove(models.Model):
    _inherit = "account.move"

    @api.depends()
    def _compute_amount(self):
        super()._compute_amount()
        for move in self:
            if move.payment_state in ('paid', 'in_payment'):
                for smov in move.invoice_line_ids.sale_line_ids.move_ids:
                    smov._action_assign()