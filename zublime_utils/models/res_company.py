# -*- coding: utf-8 -*-
from odoo import api, fields, models, _

class ResCompany(models.Model):
    _inherit = 'res.company'

    zublime = fields.Boolean(string='Enable', default=False, readonly=False)
    url_zublime = fields.Char(string='Endpoint', default='https://warehouse.cityfarma.com.mx/api')

    ### BEGIN ADDED BY ZUBLIME C0001
    symfony_branch_office_id = fields.Integer(
        string='Branch-office Symfony ID',
        default=0,
        required=True)
    ### END ADDED BY ZUBLIME