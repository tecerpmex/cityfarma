# -*- coding: utf-8 -*-
{
    'name': "zublime_sale_filter_pricelist",

    'summary': """
        Agregar filtrado para ver las lista de regla de precio del producto en las lineas de ordenes """,

    'description': """
        Agregar filtrado para ver las lista de regla de precio del producto en las lineas de ordenes
    """,

    'author': "Cityfarma",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'sale',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['sale', 'product'],

    # always loaded
    'data': [
        'views/sale_order_inherit.xml',
    ],
    # only loaded in demonstration mode

}
