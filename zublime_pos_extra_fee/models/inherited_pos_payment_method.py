# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class PosPaymentMethod(models.Model):
    # Private attributes
    _inherit = 'pos.payment.method'

    # Fields declaration
    extra_fee = fields.Float(
        string='Extra Fee')
