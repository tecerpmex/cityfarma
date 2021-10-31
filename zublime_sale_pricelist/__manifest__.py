# -*- coding: utf-8 -*-
{
    'name': "zublime_sale_pricelist",

    'summary': """
        Agregar campo Costo del producto y Utilidad""",

    'description': """
        Agregar campo Costo del producto y Utilidad
    """,

    'author': "Cityfarma",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['product', 'account'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/product_pricelist_inherit.xml',
    ],
    # only loaded in demonstration mode
    'application': True,
    'installable': True,
}
