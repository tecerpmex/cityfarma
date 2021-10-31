# Copyright (C) 2018 Bonainfo <guoyihot@outlook.com>
# All Rights Reserved
#
##############################################################################
{
    'author': 'Dmmsys 124358678@qq.com ',
    'website': 'www.bonainfo.com,www.dmmsys.com',
    'name': 'Multi Add Item',
    'category': 'Extra Tools',
    'sequence': 1,
    'summary': """Add multi item by select items once. 
                   multi add item
                   batch add item
                   multi add order line

    """,
    'version': '1.0',
    'description': """A powerful tools to help you quickly insert items in order line.
    
    """,
    'license': 'OPL-1',
    'support': '124358678@qq.com, bower_guo@msn.com',
    'price': '68',
    'currency': 'EUR',
    'images': ['static/description/main_banner.gif'],

    # any module necessary for this one to work correctly
    'depends': ['web'],

    # always loaded
    'data': [
        #'security/ir.model.access.csv',
        'views/web_views.xml',
        'views/sale_purchase_view.xml',
    ],
    # only loaded in demonstration mode
    #'demo': [
    #    'demo/demo.xml',
    #],
    'qweb': ['static/src/xml/*.xml']
}
