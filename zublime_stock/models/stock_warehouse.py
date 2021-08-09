# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
import requests


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


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def connection_postman(self):
        company = self.env['res.company'].sudo().search([('zublime', '=', True),
                                                        ('id', '=', self.env.user.company_id.id)], limit=1)
        if self.picking_type_id.sequence_code == 'OUT':
            service = '/dispatch-order/notify-out-action'
        elif self.picking_type_id.sequence_code == 'PACK':
            service = '/dispatch-order/notify-packing-action'
        elif self.picking_type_id.sequence_code == 'PACK':
            service = '/dispatch-order/notify-picking-action'
        url = company.url_zublime + service
        data = {
            'id': self.id,
            'order_id': self.sale_id.id,
            'state': 'done'
        }
        headers = {"Content-type": "application/x-www-form-urlencoded"}
        req = requests.request(method='POST', url=url, data=data, headers=headers)
        req.json()

    def button_validate(self):
        res = super(StockPicking, self).button_validate()
        self.connection_postman()
        return res
