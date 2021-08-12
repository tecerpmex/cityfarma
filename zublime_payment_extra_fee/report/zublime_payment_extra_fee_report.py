# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
# -*- coding:utf-8 -*-
import time
from odoo import api, _, exceptions, fields, models
from itertools import groupby
import itertools


class PDFReportSub(models.AbstractModel):
    _name = 'report.zublime_payment_extra_fee.zublime_payment_extra_fee_pdf'
    _description = u'Report'

    def _get_report_values(self, docids, data=None):
        company = self.env.user.company_id.name
        report_obj = self.env['ir.actions.report']
        report = report_obj._get_report_from_name('zublime_payment_extra_fee.zublime_payment_extra_fee_pdf')
        model = report.model
        payment = self.env[model].search([('id', '=', docids)])
        data = []
        if payment:
            for p in payment:
                data.append((p.name, p.date, p.partner_id.name, p.amount, p.tariff, p.amount + p.tariff, p.move_id.name))
        return {
            'company': company,
            'val': data,
        }
