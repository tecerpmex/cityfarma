# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    inoffer = fields.Boolean(
        string='In offer',
        compute='_compute_inoffer', 
        inverse='_set_inoffer', 
        search='_search_inoffer'
        )
    
    @api.depends('product_variant_ids.inoffer')
    def _compute_inoffer(self):
        self.inoffer = False
        for template in self:
            if len(template.product_variant_ids) == 1:
                template.inoffer = template.product_variant_ids.inoffer

    def _search_inoffer(self, operator, value):
        templates = self.with_context(active_test=False).search([('product_variant_ids.inoffer', operator, value)])
        return [('id', 'in', templates.ids)]

    def _set_inoffer(self):
        if len(self.product_variant_ids) == 1:
            self.product_variant_ids.inoffer = self.inoffer

class ProductProduct(models.Model):
    _inherit = 'product.product'

    inoffer = fields.Boolean(
        string='In offer',
        company_dependent=True,
        )    