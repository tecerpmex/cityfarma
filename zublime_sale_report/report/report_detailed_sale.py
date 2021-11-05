# -*- coding: utf-8 -*-

from odoo import api, models


class ReportDetailedInvoice(models.AbstractModel):
    _name = 'report.zublime_sale_report.report_detailed_sale_template'

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env['sale.order'].browse(docids)
        return {
            'doc_ids': docids,
            'doc_model': 'sale.order',
            'docs': docs,
            'data': data,
        }
