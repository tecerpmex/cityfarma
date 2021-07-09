# -*- coding: utf-8 -*-
{ 
    'name': 'MuK Autovacuum',
    'summary': 'Configure automatic garbage collection',
    'version': '14.0.3.0.1',
    'category': 'Extra Tools',
    'license': 'LGPL-3',
    'depends': [
        'muk_utils',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/rules.xml',
        'data/rules.xml',
    ],
    'qweb': [
        'static/src/xml/*.xml',
    ],
    'images': [
        'static/description/banner.png'
    ],
    'external_dependencies': {
        'python': [],
        'bin': [],
    },
    'application': False,
    'installable': True,
    'auto_install': False,
}