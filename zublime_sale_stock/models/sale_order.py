# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import Warning, ValidationError, UserError
import warnings

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.model
    def default_get(self, fields_list):
        vals = []
        res = super(SaleOrder, self).default_get(fields_list)
        product = self.env['product.product'].search([('inoffer', '=', True)], order='create_date DESC')
        for record in product:
            values = {
                'name': record.name,
                'product_id': record.id,
                'quantity': 1,
                'uom_id': record.uom_id.id,
            }
            vals.append((0, 0, values))
        res.update({'sale_order_inoffer_ids': vals})
        return res

    sale_order_inoffer_ids = fields.One2many(
        'sale.order.inoffer', 'order_id', 'In Offer Products Lines',
        copy=True, 
        )
   
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

class SaleOrderInoffer(models.Model):
    _name = "sale.order.inoffer"
    _description = "Products in offer"
    _order = 'sequence, id'

    is_present = fields.Boolean(string="Present on Quotation",
                           help="This field will be checked if the option line's product is "
                                "already present in the quotation.",
                           compute="_compute_is_present", search="_search_is_present")
    order_id = fields.Many2one('sale.order', 'Sales Order Reference', ondelete='set null', index=True)
    line_id = fields.Many2one('sale.order.line', ondelete="set null", copy=False)
    name = fields.Text('Description', required=True)
    product_id = fields.Many2one('product.product', 'Product', required=True, domain=[('sale_ok', '=', True)])
    uom_id = fields.Many2one('uom.uom', 'Unit of Measure ', required=True, domain="[('category_id', '=', product_uom_category_id)]")
    product_uom_category_id = fields.Many2one(related='product_id.uom_id.category_id', readonly=True)
    quantity = fields.Float('Quantity', required=True, digits='Product Unit of Measure', default=1)
    sequence = fields.Integer('Sequence', help="Gives the sequence order when displaying a list of optional products.")

    @api.depends('line_id', 'order_id.order_line', 'product_id')
    def _compute_is_present(self):
        # NOTE: this field cannot be stored as the line_id is usually removed
        # through cascade deletion, which means the compute would be false
        for option in self:
            option.is_present = bool(option.order_id.order_line.filtered(lambda l: l.product_id == option.product_id))

    def _search_is_present(self, operator, value):
        if (operator, value) in [('=', True), ('!=', False)]:
            return [('line_id', '=', False)]
        return [('line_id', '!=', False)]

    def button_add_to_order(self):
        self.add_option_to_order()

    def add_option_to_order(self):
        self.ensure_one()

        sale_order = self.order_id

        if sale_order.state not in ['draft', 'sent']:
            raise UserError(_('You cannot add options to a confirmed order.'))

        values = self._get_values_to_add_to_order()
        order_line = self.env['sale.order.line'].create(values)
        order_line._compute_tax_id()

        self.write({'line_id': order_line.id})
        if sale_order:
            sale_order.add_option_to_order_with_taxcloud()


    def _get_values_to_add_to_order(self):
        self.ensure_one()
        return {
            'order_id': self.order_id.id,
            'name': self.name,
            'product_id': self.product_id.id,
            'product_uom_qty': self.quantity,
            'product_uom': self.uom_id.id,
            'company_id': self.order_id.company_id.id,
        }

class SaleStockActionConfirm(models.TransientModel):
    _name = 'sale.stock.action.confirm'
    _description = 'Warning administrator to confirm it due to products without availability'

    def action_confirm(self):
        if self.env.context.get('default_order_id'):
            var = self.env['sale.order'].search([('id', '=', self.env.context['default_order_id'])])
            var.with_context(pass_action=True).action_confirm()
        return {'type': 'ir.actions.client', 'tag': 'reload'}