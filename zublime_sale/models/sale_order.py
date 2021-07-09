# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    maximum_price = fields.Float('Maximum retail price', digits='Maximum retail price', default=0.0)
    discount_one = fields.Float(string='Discount1 (%)', digits='Discount', default=0.0)

    @api.onchange('product_id')
    def product_id_change(self):
        res = super(SaleOrderLine, self).product_id_change()
        if self.product_id and self.product_id.maximum_price:
            self.maximum_price = self.product_id.maximum_price

        return res

    @api.onchange('maximum_price', 'price_unit')
    def _onchange_discount_one(self):
        for account in self:
            if account.maximum_price and account.price_unit:
                discount1 = account.maximum_price - account.price_unit
                account.discount_one = discount1/account.maximum_price*100
