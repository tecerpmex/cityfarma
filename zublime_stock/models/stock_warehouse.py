# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
import requests
from odoo.tests import Form


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

    def _pre_action_done_hook(self):
        if not self.env.context.get('skip_immediate'):
            pickings_to_immediate = self._check_immediate()
            if pickings_to_immediate:
                wiz = pickings_to_immediate._action_generate_immediate_wizard(show_transfers=self._should_show_transfers())
                wiz = Form(self.env['stock.immediate.transfer'].with_context(wiz['context'])).save().process()

        if not self.env.context.get('skip_backorder'):
            pickings_to_backorder = self._check_backorder()
            if pickings_to_backorder:
                return pickings_to_backorder._action_generate_backorder_wizard(show_transfers=self._should_show_transfers())
        return True
