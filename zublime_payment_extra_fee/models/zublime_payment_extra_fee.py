# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class AccountPaymentRegister(models.TransientModel):
    _inherit = 'account.payment.register'

    tariff = fields.Float(string="Tariff 3.5%",)

    def _create_payment_vals_from_wizard(self):
        if self.payment_method_id.name == 'Tarjeta de Crédito':  # self.tariff   payment_method_id
            tariff = self.amount * 0.035
            self.tariff = tariff
            partner_id = self.env['res.partner'].search([('id', '=', self.partner_id.id)], limit=1)
            if partner_id:
                partner_id.write({"tariff": tariff, })
                self.line_ids[0].account_id.write({"tariff": tariff, })

            payment_vals = {
                'date': self.payment_date,
                'amount': self.amount,
                'payment_type': self.payment_type,
                'partner_type': self.partner_type,
                'ref': self.communication,
                'journal_id': self.journal_id.id,
                'currency_id': self.currency_id.id,
                'partner_id': self.partner_id.id,
                'partner_bank_id': self.partner_bank_id.id,
                'payment_method_id': self.payment_method_id.id,
                'tariff': self.amount * 0.035,
                'destination_account_id': self.line_ids[0].account_id.id
            }
        else:
            payment_vals = {
                'date': self.payment_date,
                'amount': self.amount,
                'payment_type': self.payment_type,
                'partner_type': self.partner_type,
                'ref': self.communication,
                'journal_id': self.journal_id.id,
                'currency_id': self.currency_id.id,
                'partner_id': self.partner_id.id,
                'partner_bank_id': self.partner_bank_id.id,
                'payment_method_id': self.payment_method_id.id,
                'destination_account_id': self.line_ids[0].account_id.id
            }

        if not self.currency_id.is_zero(self.payment_difference) and self.payment_difference_handling == 'reconcile':
            payment_vals['write_off_line_vals'] = {
                'name': self.writeoff_label,
                'amount': self.payment_difference,
                'account_id': self.writeoff_account_id.id,
            }
        return payment_vals


class AccountPayment(models.Model):
    _inherit = "account.payment"

    tariff = fields.Float(string="Tariff 3.5%")


class Partner(models.Model):
    _inherit = "res.partner"

    tariff = fields.Float(string="Tariff 3.5%")


class AccountInvoice(models.Model):
    _inherit = "account.move"

    tariff = fields.Float(string="Tariff 3.5%")
