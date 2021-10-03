# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ProductProduct(models.Model):
    _inherit = 'product.product'
    _description = 'Busqueda por Codigo de Barra'

    @api.model
    def _name_search(self, name='', args=None, operator='ilike', limit=100, name_get_uid=None):
        args = [] if args is None else args.copy()

        if not (name == '' and operator == 'ilike'):
            args += ['|', '|',
                     ('name', operator, name),
                     ('default_code', operator, name),
                     ('barcode', operator, name),
                     ]
        return super(ProductProduct, self)._name_search(name='', args=args, operator='ilike', limit=limit,
                                                        name_get_uid=name_get_uid)