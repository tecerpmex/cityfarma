# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    maximum_price = fields.Float(
        digits='Maximum retail price', compute='_compute_maximum_price',
        inverse='_set_maximum_price', search='_search_maximum_price')

    @api.depends_context('company')
    @api.depends('product_variant_ids', 'product_variant_ids.maximum_price')
    def _compute_maximum_price(self):
        unique_variants = self.filtered(lambda template: len(template.product_variant_ids) == 1)
        for template in unique_variants:
            template.maximum_price = template.product_variant_ids.maximum_price
        for template in (self - unique_variants):
            template.maximum_price = 0.0

    def _set_maximum_price(self):
        for template in self:
            if len(template.product_variant_ids) == 1:
                template.product_variant_ids.maximum_price = template.maximum_price

    def _search_maximum_price(self, operator, value):
        products = self.env['product.product'].search([('maximum_price', operator, value)], limit=None)
        return [('id', 'in', products.mapped('product_tmpl_id').ids)]


class ProductProduct(models.Model):
    _inherit = 'product.product'

    maximum_price = fields.Float(
        'Maximum retail price', company_dependent=True, digits='Maximum Price')
