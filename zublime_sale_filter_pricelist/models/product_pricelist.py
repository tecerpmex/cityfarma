# -*- coding: utf-8 -*-

from odoo import api, fields, models, tools, _


class Pricelist(models.Model):
    _inherit = "product.pricelist"

    def get_pricelist_item(self):
        action = self.env['ir.actions.act_window']._for_xml_id('product.product_pricelist_item_action')
        ctx = dict(self.env.context)
        ctx.pop('active_id', None)
        ctx['active_model'] = 'product.pricelist.item'
        ctx['domain'] = [('pricelist_id', '=', self.id)]
        action['context'] = ctx,
        action.update(
            context=dict(default_pricelist_id=self.id),
            domain=[('pricelist_id', '=', self.id)]
        )
        return  action