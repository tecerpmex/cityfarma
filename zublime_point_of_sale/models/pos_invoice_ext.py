# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, models, _
from odoo.exceptions import UserError


class PosInvoiceReport(models.AbstractModel):
    _inherit = 'report.point_of_sale.report_invoice'

    @api.model
    def _get_report_values(self, docids, data=None):
        PosOrder = self.env['pos.order']
        ids_to_print = []
        invoiced_posorders_ids = []
        selected_orders = PosOrder.browse(docids)
        for order in selected_orders.filtered(lambda o: o.account_move):
            ids_to_print.append(order.account_move.id)
            invoiced_posorders_ids.append(order.id)
        not_invoiced_orders_ids = list(set(docids) - set(invoiced_posorders_ids))

        if not_invoiced_orders_ids:
            not_invoiced_posorders = PosOrder.browse(not_invoiced_orders_ids)
            not_invoiced_orders_names = [a.name for a in not_invoiced_posorders]
            raise UserError(_('No link to an invoice for %s.') % ', '.join(not_invoiced_orders_names))
        for id_to_print in ids_to_print:
            acount_move = self.env['account.move'].search([('id', '=', id_to_print)], limit=1)
            post_order = self.env['pos.order'].search([('id', '=', invoiced_posorders_ids[0])], limit=1)
            acount_move.extra_fee_comission = post_order.payment_ids[0].payment_method_id.fee.tariff
            acount_move.card_payment_commission = acount_move.amount_total * acount_move.extra_fee_comission / 100
            acount_move.total_pay = acount_move.card_payment_commission + acount_move.amount_total
        return {
            'docs': self.env['account.move'].sudo().browse(ids_to_print),
            'qr_code_urls': self.env['report.account.report_invoice'].sudo()._get_report_values(ids_to_print)[
                'qr_code_urls']
        }
