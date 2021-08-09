# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
import requests


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    is_paid = fields.Boolean('Paid', compute='_get_sale_paid', store=True)
    paid = fields.Boolean('Prueba')

    def connection_postman(self, id):
        company = self.env['res.company'].sudo().search([('zublime', '=', True),
                                                        ('id', '=', self.env.user.company_id.id)], limit=1)
        service = '/dispatch-order/notify-order-action'
        url = company.url_zublime + service
        data = {
            'id': id,
            'state': 'done'
        }
        #r = requests.get(url)
        #r.status_code
        #headers = {"Content-type": "application/json"}
        headers = {"Content-type": "application/x-www-form-urlencoded"}
        req = requests.request(method='POST', url=url, data=data, headers=headers)
        req.json()

    def action_confirm(self):
        result = super(SaleOrder, self).action_confirm()
        self.connection_postman(self.id)
        return result

    @api.depends('order_line.product_uom_qty', 'order_line.qty_invoiced', 'invoice_ids.state')
    def _get_sale_paid(self):
        state_invoice = True
        for sale in self:
            if not sale.invoice_ids:
                state_invoice = False
            for invoice in sale.invoice_ids:
                if invoice.state != 'posted':
                    state_invoice = False
                    break
            product_uom_qty = sum([x.product_uom_qty for x in sale.order_line])
            qty_invoiced = sum([x.qty_invoiced for x in sale.order_line])
            if product_uom_qty == qty_invoiced and state_invoice:
                sale.is_paid = True

    def write(self, vals):
        res = super(SaleOrder, self).write(vals)
        if 'paid' in vals and self.paid:
            self.connection_paid(self.id)
        return res

    def connection_paid(self, id):
        company = self.env['res.company'].sudo().search([('zublime', '=', True),
                                                        ('id', '=', self.env.user.company_id.id)], limit=1)
        service = '/dispatch-order/notify-order-paid'
        url = company.url_zublime + service
        data = {
            'ids': id,
        }
        headers = {"Content-type": "application/x-www-form-urlencoded"}
        req = requests.request(method='POST', url=url, data=data, headers=headers)
        req.json()


class ResCompany(models.Model):
    _inherit = 'res.company'

    zublime = fields.Boolean(string='Zublime', readonly=False)
    url_zublime = fields.Char('Url service')

