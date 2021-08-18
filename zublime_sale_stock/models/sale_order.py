# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_confirm(self):
        if not self.env.user.has_group('sales_team.group_sale_manager'):
            for line in self.order_line:
                if line.product_id.qty_available > 0:
                    continue
                else:
                    raise UserError(_(
                        "Requires an administrator to confirm it due to products without availability."))
        return super(SaleOrder, self).action_confirm()