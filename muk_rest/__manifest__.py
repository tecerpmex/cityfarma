# -*- coding: utf-8 -*-
{
    'name': 'MuK REST API for Odoo',
    'summary': 'A customizable Restful API for Odoo',
    'version': '14.0.3.7.1',
    'category': 'Extra Tools',
    "license": "LGPL-3",
    'depends': [
        'muk_autovacuum',
    ],
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'views/menu.xml',
        'views/oauth.xml',
        'views/oauth1.xml',
        'views/oauth2.xml',
        'views/access.xml',
        'views/callback.xml',
        'views/request.xml',
        'views/endpoint.xml',
        'views/request_token.xml',
        'views/access_token.xml',
        'views/bearer_token.xml',
        'views/authorization_code.xml',
        'views/res_users.xml',
        'views/documentation.xml',
        'template/assets.xml',
        'template/authorize.xml',
        'data/autovacuum.xml',
    ],
    'demo': [
        'demo/oauth.xml',
        'demo/endpoints.xml',
    ],
    'qweb': [
        'static/src/xml/*.xml',
    ],
    'images': [
        'static/description/banner.png'
    ],
    'external_dependencies': {
        'python': [
            'oauthlib',
        ],
        'bin': [],
    },
    'application': False,
    'installable': True,
    'auto_install': False,
}
