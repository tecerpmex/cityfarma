# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class AccountMove(models.Model):
    _inherit = 'account.move.line'

    maximum_price = fields.Float(string='Maximum retail price', digits='Maximum retail price')
    discount_one = fields.Float(string='Discount1 (%)', digits='Discount', default=0.0)

    @api.onchange('product_id')
    def _onchange_product_id(self):
        res = super(AccountMove, self)._onchange_product_id()
        for line in self:
            line.maximum_price = line._get_computed_price_maximum()

    def _get_computed_price_maximum(self):
        self.ensure_one()

        if not self.product_id:
            return self.maximum_price
        elif self.move_id.is_sale_document(include_receipts=True):
            maximum_price = self.product_id.maximum_price
        else:
            return self.maximum_price

        return maximum_price

    @api.onchange('maximum_price', 'price_unit')
    def _onchange_discount_one(self):
        for account in self:
            if account.maximum_price and account.price_unit:
                discount1 = account.maximum_price - account.price_unit
                account.discount_one = discount1/account.maximum_price*100


