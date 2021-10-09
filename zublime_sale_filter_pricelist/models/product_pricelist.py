# -*- coding: utf-8 -*-

from odoo import api, fields, models, tools, _


class Pricelist(models.Model):
    _inherit = "product.pricelist"

    def get_pricelist_item(self):
        view_id = self.env.ref('product.product_pricelist_item_tree_view_from_product').id
        return {
            'name': 'List Prices Items',
            'view_mode': 'tree',
            'views': [[view_id, 'tree']],
            'res_model': 'product.pricelist.item',
            'type': 'ir.actions.act_window',
            'context': {'default_pricelist_id': self.id},
            'domain': [('pricelist_id', '=', self.id)],
            'target': 'current',
        }