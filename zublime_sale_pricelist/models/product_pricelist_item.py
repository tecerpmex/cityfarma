from odoo import fields, models, api


class ProductPriceListItem(models.Model):
    _inherit = 'product.pricelist.item'

    cost = fields.Float(string='Precio Costo')
    utilidad = fields.Float(string='Utilidad', compute='compute_cost_price')#
    @api.onchange('product_tmpl_id')
    def onchange_product(self):
        for pro in self:
            if pro.product_tmpl_id:
                pro.cost = pro.product_tmpl_id.standard_price


    def compute_cost_price(self):
        for n in self:
            if n.cost > 0:
                n.utilidad = n.fixed_price / n.cost * 100
