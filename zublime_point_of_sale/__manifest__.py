# -*- coding: utf-8 -*-
{
    'name': "Point of Sale Extra Fee",
    'summary': "",
    'description': """
    """,

    'author': "",
    'website': "https://easicoders.com/",
    'category': 'Sales/Point of Sale',
    'version': '0.1',

    'depends': ['point_of_sale'],
    'data': [
        'views/inherited_pos_payment_method_views.xml',
        'views/pos_templates.xml',
        'static/src/xml/report_invoice.xml',
    ],
    'qweb': [
        'static/src/xml/OrderReceipt.xml',
        'static/src/xml/PaymentScreenPaymentLines.xml'
    ],
    'demo': [],
}
