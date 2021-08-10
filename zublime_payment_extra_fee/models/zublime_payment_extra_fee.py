# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class PaymentMethod(models.Model):
    _inherit = 'l10n_mx_edi.payment.method'

    tariff = fields.Float(string="Tariff")


class AccountPaymentRegister(models.TransientModel):
    _inherit = 'account.payment.register'

    tariff = fields.Float(string="Tariff %", )

    def _create_payment_vals_from_wizard(self):
        l10n_mx_edi_payment_method_id = self.env['l10n_mx_edi.payment.method'].search(
            [('id', '=', self.l10n_mx_edi_payment_method_id.id)], limit=1)
        if l10n_mx_edi_payment_method_id.tariff > 0:
            tariff = self.amount * (l10n_mx_edi_payment_method_id.tariff / 100)
        else:
            tariff = 0
        self.tariff = tariff
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
            'tariff': tariff,
            'destination_account_id': self.line_ids[0].account_id.id
        }

        if not self.currency_id.is_zero(self.payment_difference) and self.payment_difference_handling == 'reconcile':
            payment_vals['write_off_line_vals'] = {
                'name': self.writeoff_label,
                'amount': self.payment_difference,
                'account_id': self.writeoff_account_id.id,
            }
        data = {
            'options': [payment_vals, tariff],
        }
        # return self.env.ref('zublime_payment_extra_fee.zublime_payment_extra_fee_id').report_action([], data=data)
        return payment_vals


class AccountPayment(models.Model):
    _inherit = "account.payment"

    tariff = fields.Float(string="Tariff")
