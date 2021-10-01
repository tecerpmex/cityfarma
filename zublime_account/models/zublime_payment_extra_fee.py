# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError


class PaymentMethod(models.Model):
    _inherit = 'l10n_mx_edi.payment.method'

    tariff = fields.Float(string="Tariff")
    effective_type = fields.Boolean(
        string='Effective type',
    )
    


class AccountPaymentRegister(models.TransientModel):
    _inherit = 'account.payment.register'

    # Associated fields sprint 2 requirement 3
    tariff = fields.Float(
        string="Tariff %", 
        readonly=True,
        )
    amount_fee = fields.Float(
        string="Total Amount",
        readonly=True,
        )
    fee = fields.Float(
        related='l10n_mx_edi_payment_method_id.tariff',
    )
    # Associated fields sprint 2 requirement 4
    amount_due = fields.Monetary(
        currency_field='currency_id', 
        string="Amount Due", 
        store=True, 
        readonly=False,
        compute='_compute_amount')
    cash_received = fields.Monetary(
        currency_field='currency_id',
        string="Cash received", 
        )
    change_return = fields.Monetary(
        currency_field='currency_id',
        string="Change to return", 
        readonly=True,
        )
    effective_type = fields.Boolean(
        related='l10n_mx_edi_payment_method_id.effective_type',
    )
     
    #Associated methods sprint 2 requirement 3 
    @api.onchange('amount', 'l10n_mx_edi_payment_method_id')
    def _onchange_amount(self):
        self.tariff = self.amount * (self.l10n_mx_edi_payment_method_id.tariff / 100)
        self.amount_fee = self.amount + self.tariff
        #Associated methods sprint 2 requirement 4
        self.cash_received = self.amount

    def _create_payment_vals_from_wizard(self):
        payment_vals = super(AccountPaymentRegister, self)._create_payment_vals_from_wizard()
        payment_vals['tariff'] = self.tariff
        payment_vals['amount_fee'] = self.amount_fee
        return payment_vals

    #Associated methods sprint 2 requirement 4
    @api.depends('source_amount', 'source_amount_currency', 'source_currency_id', 'company_id', 'currency_id', 'payment_date')
    def _compute_amount(self):
        super(AccountPaymentRegister, self)._compute_amount()
        self.amount_due = self.amount

    @api.onchange('cash_received')
    def _onchange_cash_received(self):
        self.change_return = self.cash_received - self.amount

    @api.constrains('cash_received', 'amount')
    def _check_cash_received(self):
        for record in self:
            if record.cash_received < record.amount:
                raise ValidationError("The cash delivered by the customer is less than the amount")

    @api.constrains('amount_due', 'amount')
    def _check_amount(self):
        for record in self:
            if record.amount_due < record.amount:
                raise ValidationError("The amount to be paid by the customer is greater than the amount owed")

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