# -*- coding: utf-8 -*-
{
    'name': "DTID",

    'summary': """
        DTID Service
    """,

    'description': """
        DTID Service for Phadata
    """,

    'author': "tanwei",
    'website': "https://www.phadata.net",

    'category': 'DTID',
    'version': '0.1',

    'depends': [],

    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
     'assets': {
        'web.assets_backend': [
            'phadata_dtid_service/static/src/js/user_menu.js',
        ],
        'web.assets_common': [
        ],
        'web.assets_qweb': [
            'phadata_dtid_service/static/src/xml/**/*',
        ],
    },
    'license': 'LGPL-3',
}
