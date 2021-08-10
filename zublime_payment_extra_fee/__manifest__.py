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
    "depends": ["account", "account_accountant"],
    "data": [
        "views/zublime_payment_extra_fee_view.xml",
        "report/statements_report.xml",
        "report/template_header.xml",
        "report/zublime_payment_extra_fee_report.xml",
        # "views/menu_view.xml",
    ],
    "installable": True,
    "application": False,
}
