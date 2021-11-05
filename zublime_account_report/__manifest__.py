# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Report invoice extra',
    'version': '1.0',
    'category': 'Account',
    'summary': 'Report invoice extra',
    'author': 'Easi Coders',
    'depends': ['zublime_sale'],
    'data': [
            "report/report_definition.xml",
            "report/report_detailed_invoice.xml",
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}