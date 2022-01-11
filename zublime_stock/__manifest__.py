# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'zublime_stock',
    'version': '14.0',
    # Categories can be used to filter models in models listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Stock',
    'summary': '',
    'description': """""",
    'license': 'LGPL-3',
    'author': 'Zublime',
    "website": "https://zublime.mx",
    # any module necessary for this one to work correctly
    'depends': ['stock' ,'zublime_utils'],
    # always loaded
    'data': [],
    'installable': True,
    # only loaded in demonstration mode
    'auto_install': False,
    'application': False,
}