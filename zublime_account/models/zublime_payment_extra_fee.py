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
        readonly=False,
    )
    amount_fee = fields.Float(
        string="Total Amount",
        readonly=False,
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
    is_payment_fee = fields.Boolean(store=True)

    # Associated methods sprint 2 requirement 3
    @api.onchange('amount', 'l10n_mx_edi_payment_method_id')
    def _onchange_amount(self):
        self.tariff = self.amount * (self.l10n_mx_edi_payment_method_id.tariff / 100)
        self.amount_fee = self.amount + self.tariff
        # Associated methods sprint 2 requirement 4
        self.cash_received = self.amount

    def _create_payment_vals_from_wizard(self):
        payment_vals = super(AccountPaymentRegister, self)._create_payment_vals_from_wizard()
        payment_vals['tariff'] = self.tariff
        payment_vals['amount_fee'] =self.amount + self.tariff
        return payment_vals

    # Associated methods sprint 2 requirement 4
    @api.depends('source_amount', 'source_amount_currency', 'source_currency_id', 'company_id', 'currency_id',
                 'payment_date')
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

    # @api.onchange('l10n_mx_edi_payment_method_id')
    # def _onchange_payment_method_m(self):
    #     records = self.env.context.get('l10n_mx_edi_payment_method_id')
    #     if records:
    #         if records != 0:
    #             self.is_payment_fee = True
    #         self.l10n_mx_edi_payment_method_id = records
    #         self.tariff = self.amount * (self.l10n_mx_edi_payment_method_id.tariff / 100)
    #         self.amount_fee = self.amount + self.tariff


class AccountPayment(models.Model):
    _inherit = "account.payment"

    tariff = fields.Float(
        string="Tariff",
        store=True,
        compute='_compute_amount'
    )
    amount_fee = fields.Float(
        string="Total Amount",
        store=True,
        compute='_compute_amount'
    )
    fee = fields.Float(
        related='l10n_mx_edi_payment_method_id.tariff',
    )

    @api.onchange('amount', 'l10n_mx_edi_payment_method_id')
    def _onchange_amount(self):
        self.tariff = self.amount * (self.l10n_mx_edi_payment_method_id.tariff / 100)
        self.amount_fee = self.amount + self.tariff

    @api.depends('amount', 'l10n_mx_edi_payment_method_id')
    def _compute_amount(self):
        self.tariff = self.amount * (self.l10n_mx_edi_payment_method_id.tariff / 100)
        self.amount_fee = self.amount + self.tariff


class AccountMove(models.Model):
    _inherit = 'account.move'

    extra_fee_comission = fields.Float(string='Payment commission (%)')
    total_pay = fields.Monetary(string='TOTAL TO PAY')
    card_payment_commission = fields.Monetary(string='Card payment commission')

    def _get_reconciled_info_JSON_values(self):
        self.ensure_one()
        reconciled_vals = []
        pos_order=self.env['pos.order'].search([('account_move', '=', self.id)], limit=1)
        if pos_order:
            for partial, amount, counterpart_line in self._get_reconciled_invoices_partials():
                if counterpart_line.move_id.ref:
                    reconciliation_ref = '%s (%s)' % (counterpart_line.move_id.name, counterpart_line.move_id.ref)
                else:
                    reconciliation_ref = counterpart_line.move_id.name

                reconciled_vals.append({
                    'name': counterpart_line.name,
                    'journal_name': counterpart_line.journal_id.name,
                    'amount': self.total_pay,
                    'currency': self.currency_id.symbol,
                    'digits': [69, self.currency_id.decimal_places],
                    'position': self.currency_id.position,
                    'date': counterpart_line.date,
                    'fee': self.extra_fee_comission,
                    'tariff': self.card_payment_commission,
                    'amount_fee':self.total_pay,
                    'payment_id': counterpart_line.id,
                    'partial_id': partial.id,
                    'account_payment_id': counterpart_line.payment_id.id,
                    'payment_method_name': counterpart_line.payment_id.payment_method_id.name if counterpart_line.journal_id.type == 'bank' else None,
                    'move_id': counterpart_line.move_id.id,
                    'ref': reconciliation_ref,
                })
        else:
            for partial, amount, counterpart_line in self._get_reconciled_invoices_partials():
                if counterpart_line.move_id.ref:
                    reconciliation_ref = '%s (%s)' % (counterpart_line.move_id.name, counterpart_line.move_id.ref)
                else:
                    reconciliation_ref = counterpart_line.move_id.name

                reconciled_vals.append({
                    'name': counterpart_line.name,
                    'journal_name': counterpart_line.journal_id.name,
                    'amount': amount,
                    'currency': self.currency_id.symbol,
                    'digits': [69, self.currency_id.decimal_places],
                    'position': self.currency_id.position,
                    'date': counterpart_line.date,
                    'fee': counterpart_line.payment_id.fee,
                    'tariff': counterpart_line.payment_id.tariff,
                    'amount_fee': counterpart_line.payment_id.amount_fee,
                    'payment_id': counterpart_line.id,
                    'partial_id': partial.id,
                    'account_payment_id': counterpart_line.payment_id.id,
                    'payment_method_name': counterpart_line.payment_id.payment_method_id.name if counterpart_line.journal_id.type == 'bank' else None,
                    'move_id': counterpart_line.move_id.id,
                    'ref': reconciliation_ref,
                })
        print(self.id)
        print(self.card_payment_commission)
        print(self.payment_state)
        return reconciled_vals

    # def action_register_payment(self):
    #     ''' Open the account.payment.register wizard to pay the selected journal entries.
    #     :return: An action opening the account.payment.register wizard.
    #     '''
    #     post_order = self.env['pos.order'].search([('account_move', '=', self.id)], limit=1)
    #     if post_order:
    #         return {
    #             'name': _('Register Payment'),
    #             'res_model': 'account.payment.register',
    #             'view_mode': 'form',
    #             'context': {
    #                 'active_model': 'account.move',
    #                 'active_ids': self.ids,
    #                 'l10n_mx_edi_payment_method_id': post_order.payment_ids[0].payment_method_id.fee.id,
    #             },
    #             'target': 'new',
    #             'type': 'ir.actions.act_window'
    #         }
    #     else:
    #         return {
    #             'name': _('Register Payment'),
    #             'res_model': 'account.payment.register',
    #             'view_mode': 'form',
    #             'context': {
    #                 'active_model': 'account.move',
    #                 'active_ids': self.ids,
    #                 'l10n_mx_edi_payment_method_id': 0,
    #             },
    #             'target': 'new',
    #             'type': 'ir.actions.act_window'
    #         }
