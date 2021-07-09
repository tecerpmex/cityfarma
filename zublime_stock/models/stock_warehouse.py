# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class StockWarehouse(models.Model):
    _inherit = 'stock.warehouse'

    def get_inventory(self):
        location_model = self.env['stock.location']
        res = []
        for warehouse in self:
            location_res = []
            locations = location_model.search([
                ('location_id', 'child_of', warehouse.view_location_id.id),
                ('location_id.active', '=', True)
            ])
            for location in locations:
                quant_res = []
                for quant in location.quant_ids:
                    quant_res.append({
                        'product_tmpl_id': quant.product_tmpl_id.id,
                        'product_id': quant.product_id.id,
                        'barcode': quant.product_id.barcode,
                        'quantity': quant.quantity,
                    })
                location_res.append({
                    'id': location.id,
                    'name': location.name,
                    'barcode': location.barcode,
                    'stock': quant_res,
                })
            res.append({
                'id': warehouse.id,
                'name': warehouse.name,
                'locations': location_res,
            })
        return res
