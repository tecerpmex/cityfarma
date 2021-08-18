# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class PaymentMethod(models.Model):
    _inherit = 'l10n_mx_edi.payment.method'

    tariff = fields.Float(string="Tariff")


class AccountPaymentRegister(models.TransientModel):
    _inherit = 'account.payment.register'

    tariff = fields.Float(string="Tariff %", )
    amount_fee = fields.Float(string="Total Amount", )
    fee = fields.Float(
        related='l10n_mx_edi_payment_method_id.tariff',
    )
     
    @api.onchange('amount', 'l10n_mx_edi_payment_method_id')
    def _onchange_amount(self):
        self.tariff = self.amount * (self.l10n_mx_edi_payment_method_id.tariff / 100)
        self.amount_fee = self.amount + self.tariff

    def _create_payment_vals_from_wizard(self):
        payment_vals = super(AccountPaymentRegister, self)._create_payment_vals_from_wizard()
        payment_vals['tariff'] = self.tariff
        payment_vals['amount_fee'] = self.amount_fee
        return payment_vals


class AccountPayment(models.Model):
    _inherit = "account.payment"

    tariff = fields.Float(string="Tariff")
    amount_fee = fields.Float(string="Total Amount", )
    fee = fields.Float(
        related='l10n_mx_edi_payment_method_id.tariff',
    )

    @api.onchange('amount', 'l10n_mx_edi_payment_method_id')
    def _onchange_amount(self):
        self.tariff = self.amount * (self.l10n_mx_edi_payment_method_id.tariff / 100)
        self.amount_fee = self.amount + self.tariff