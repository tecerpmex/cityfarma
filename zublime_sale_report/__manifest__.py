# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Report quotation order detailed',
    'version': '1.0',
    'category': 'Sales',
    'summary': 'Report quotation order detailed',
    'author': 'Easi Coders',
    'depends': ['zublime_sale'],
    'data': [
            "report/report_definition.xml",
            "report/report_detailed_sale.xml",
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}