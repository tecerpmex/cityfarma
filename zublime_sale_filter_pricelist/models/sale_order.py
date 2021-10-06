from odoo import fields, models, api, _


class SaleOrder(models.Model):
    _inherit = 'sale.order'
    _description = 'Description'

    def action_products(self):
        action = self.env['ir.actions.act_window']._for_xml_id('zublime_sale_product_multi_add.wizar_multi_product_act_window')
        ctx = dict(self.env.context)
        ctx.pop('active_id', None)
        ctx['active_ids'] = self.ids
        ctx['active_model'] = 'wizard.multi.product'
        action['context'] = ctx
        return action

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'


    def action_list_precio(self):
        action = self.env['ir.actions.act_window']._for_xml_id('product.product_pricelist_item_action')
        ctx = dict(self.env.context)
        ctx.pop('active_id', None)
        ctx['active_model'] = 'product.pricelist.item'
        ctx['domain'] = [('pricelist_id', '=', self.order_id.pricelist_id.id)]
        action['context'] = ctx,
        action.update(
            context=dict(default_pricelist_id=self.id),
            domain=[('pricelist_id', '=', self.order_id.pricelist_id.id)]
        )
        print('CTX', ctx)
        # print('ACTION', action)
        return action