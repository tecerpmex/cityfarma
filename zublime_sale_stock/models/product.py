# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    inoffer = fields.Boolean(
        string='In offer',
        company_dependent=True,
        )

class ProductProduct(models.Model):
    _inherit = 'product.product'

    inoffer = fields.Boolean(
        string='In offer',
        company_dependent=True,
        )    