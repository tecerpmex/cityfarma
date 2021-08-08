# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class PosOrder(models.Model):
    # Private attributes
    _inherit = 'pos.order'

    @api.model
    def _order_fields(self, ui_order):
        res = super(PosOrder, self)._order_fields(ui_order)
        res.update({'total_extra_fee': ui_order.get('total_extra_fee', 0),})
        return res

    # Fields declaration
    total_extra_fee = fields.Float(
        string='Extra Fee', 
        default=0, 
        readonly=True, 
        required=True)
