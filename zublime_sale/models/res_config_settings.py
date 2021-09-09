# -*- coding: utf-8 -*-

from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    group_discount_price_max = fields.Boolean("Discounts price max", default=True,
                                              implied_group='zublime_sale.group_discount_price_max')
    group_discount_subtotal = fields.Boolean("Discounts by subtotal", default=False,
                                             implied_group='zublime_sale.group_discount_subtotal')

    @api.onchange('group_discount_price_max')
    def _onchange_product_price_max_setting(self):
        if self.group_discount_price_max:
            self.group_discount_subtotal = False

    @api.onchange('group_discount_subtotal')
    def _onchange_product_price_subtotal_setting(self):
        if self.group_discount_subtotal:
            self.group_discount_price_max = False