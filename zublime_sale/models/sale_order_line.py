# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    maximum_price = fields.Float('Maximum retail price', digits='Maximum retail price', default=0.0)
    discount_one = fields.Float(string='Reduction (%)', digits='Discount', default=0.0)
    discount_subtotal = fields.Float(string='Reduction (%)', digits='Discount', default=0.0)

    @api.onchange('product_id')
    def product_id_change(self):
        res = super(SaleOrderLine, self).product_id_change()
        if self.product_id and self.product_id.maximum_price:
            self.maximum_price = self.product_id.maximum_price

        return res

    @api.onchange('maximum_price', 'price_unit')
    def _onchange_discount_one(self):
        for line in self:
            if line.maximum_price and line.price_unit:
                discount1 = line.maximum_price - line.price_unit
                line.discount_one = discount1/line.maximum_price*100

    @api.onchange('maximum_price', 'price_unit', 'product_uom_qty', 'discount')
    def _onchange_discount_subtotal(self):
        for line in self:
            if line.price_subtotal and line.maximum_price:
                discount1 = line.maximum_price * line.product_uom_qty
                line.discount_subtotal = (discount1 - line.price_subtotal)/discount1 * 100

    def _prepare_invoice_line(self, **optional_values):
        res = super(SaleOrderLine, self)._prepare_invoice_line(**optional_values)
        discount = 0.0
        if self.discount_one:
            discount = self.discount_one
        else:
            discount = self.discount_subtotal
        res.update({'maximum_price': self.maximum_price, 'discount_one': discount})
        return res

