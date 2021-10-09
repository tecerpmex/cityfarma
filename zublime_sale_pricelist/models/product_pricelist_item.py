from odoo import fields, models, api


class ProductPriceListItem(models.Model):
    _inherit = 'product.pricelist.item'

    cost = fields.Float(
        string='Precio Costo',
        store=True, 
        compute='_compute_price'
        )
    utilidad = fields.Float(
        string='Utilidad', 
        store=True, 
        compute='_compute_price'
        )
    margin = fields.Float(
        string='Margin',
        store=True, 
        compute='_compute_price'
        )
    list_price = fields.Float(
        'Sales Price', 
        default=0,
        digits='Product Price',
        compute='_compute_price',     
        store=True,  
        help="Price at which the product is sold to customers."
        )
    taxes_ids = fields.Many2many(
        related='product_tmpl_id.taxes_id'
        )
    
    @api.onchange('product_tmpl_id')
    def onchange_product(self):
        for pro in self:
            pro.cost = 0
            pro.list_price = 0
            pro.margin = 0
            pro.utilidad = 0
            if pro.product_tmpl_id:
                pro.cost = pro.product_tmpl_id.standard_price
                pro.list_price = pro.product_tmpl_id.list_price
                pro.margin = pro.fixed_price - pro.cost
                if pro.cost > 0:
                    pro.utilidad = pro.fixed_price / pro.cost * 100
            if pro.product_id:
                pro.cost = pro.product_id.standard_price
                pro.list_price = pro.product_id.product_tmpl_id.list_price
                pro.margin = pro.fixed_price - pro.cost
                if pro.cost > 0:
                    pro.utilidad = pro.fixed_price / pro.cost * 100

    @api.depends('fixed_price', 'product_tmpl_id', 'product_id')
    def _compute_price(self):
        for pro in self:
            if pro.product_tmpl_id:
                pro.cost = pro.product_tmpl_id.standard_price
                pro.list_price = pro.product_tmpl_id.list_price
                pro.margin = pro.fixed_price - pro.cost
                if pro.cost > 0:
                    pro.utilidad = pro.fixed_price / pro.cost * 100
            if pro.product_id:
                pro.cost = pro.product_id.standard_price
                pro.list_price = pro.product_id.product_tmpl_id.list_price
                pro.margin = pro.fixed_price - pro.cost
                if pro.cost > 0:
                    pro.utilidad = pro.fixed_price / pro.cost * 100
