# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class PosPaymentMethod(models.Model):
    # Private attributes
    _inherit = 'pos.payment.method'

    fee = fields.Many2one('l10n_mx_edi.payment.method')
    # Fields declaration
    extra_fee = fields.Float(related='fee.tariff',
                             string='Payment commission (%)')
