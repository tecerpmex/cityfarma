# -*- coding: utf-8 -*-
# © <2021> 
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Payment",
    "version": "1.0",
    "author": "Abelardo",
    "website": "",
    "category": "account",
    "complexity": "normal",
    "description": """ """,
    "depends": ["l10n_mx_edi"],
    "data": [
        "security/ir.model.access.csv",
        "views/zublime_payment_extra_fee_view.xml",
        "report/statements_report.xml",
        "report/template_header.xml",
        "report/zublime_payment_extra_fee_report.xml",
        "report/report_invoice.xml",
    ],
    "installable": True,
    "application": False,
}
