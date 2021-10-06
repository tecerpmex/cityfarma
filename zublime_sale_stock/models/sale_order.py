# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import Warning, ValidationError, UserError
import warnings

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_confirm(self):
        i = 0
        for line in self.order_line:
                if line.virtual_available_at_date < line.product_uom_qty:
                    i += 1
        if i > 0:
            if not self.env.user.has_group('sales_team.group_sale_manager'):
                raise UserError(_(
                        "Requires an administrator to confirm it due to products without availability."))
            else:
                if self.env.context.get('pass_action'):
                    super(SaleOrder, self).action_confirm()
                else:
                    return self.env["ir.actions.actions"]._for_xml_id("zublime_sale_stock.action_sale_stock_action_confirm")
        return super(SaleOrder, self).action_confirm()

class SaleStockActionConfirm(models.TransientModel):
    _name = 'sale.stock.action.confirm'
    _description = 'Warning administrator to confirm it due to products without availability'

    def action_confirm(self):
        if self.env.context.get('default_order_id'):
            var = self.env['sale.order'].search([('id', '=', self.env.context['default_order_id'])])
            var.with_context(pass_action=True).action_confirm()
        return {'type': 'ir.actions.client', 'tag': 'reload'}