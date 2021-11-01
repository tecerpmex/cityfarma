# -*- coding: utf-8 -*-

from odoo import api, models


class ReportDetailedInvoice(models.AbstractModel):
    _name = 'report.zublime_account_report.report_detailed_invoice_template'

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env['account.move'].browse(docids)
        return {
            'doc_ids': docids,
            'doc_model': 'account.move',
            'docs': docs,
            'data': data,
        }
