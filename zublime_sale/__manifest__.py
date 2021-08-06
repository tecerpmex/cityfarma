# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Maximum sale price',
    'version': '1.0',
    'category': 'Sale',
    'summary': 'Maximum sale price',
    'author': 'Easi Coders',
    'depends': ['sale_management', 'account'],
    'data': [
            "views/product.xml",
            "views/sale_order.xml",
            "views/account_move.xml",
            "views/res_company_view.xml"
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}