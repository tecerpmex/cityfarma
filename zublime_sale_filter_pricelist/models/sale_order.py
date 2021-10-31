from odoo import fields, models, api, _



class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'


    def action_list_precio(self):
        view_id = self.env.ref('product.product_pricelist_item_tree_view_from_product').id
        return {
            'name': 'List Prices Items',
            'view_mode': 'tree',
            'views': [[view_id, 'tree']],
            'res_model': 'product.pricelist.item',
            'type': 'ir.actions.act_window',
            'context': {'default_pricelist_id': self.order_id.pricelist_id.id, 'default_product_tmpl_id': self.product_id.product_tmpl_id.id},
            'domain': [('pricelist_id', '=', self.order_id.pricelist_id.id), ('product_tmpl_id', '=', self.product_id.product_tmpl_id.id)],
            'target': 'new',
        }