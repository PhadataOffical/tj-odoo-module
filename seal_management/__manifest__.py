# -*- coding: utf-8 -*-
{
    'name': "印章",
    'summary': """印章""",
    'sequence': 1,
    'description': """
       印章
    """,
    'version': '0.1',
    'depends': ['base','web'],
    'data': [
        'security/ir.model.access.csv',
        'views/seal_list_view.xml',
        'views/menu_view.xml',
    ],
    'assets': {
        'web._assets_primary_variables': [],
        'web.assets_backend': [
            '/seal_management/static/src/css/tjmain.css',
            '/seal_management/static/src/js/seal-draw.js',
            '/seal_management/static/src/js/seal.manage.js'
        ],
        'web.assets_frontend': [],
        'web.assets_tests': [],
        'web.qunit_suite_tests': [],
        'web.assets_qweb': [
            'seal_management/static/src/xml/**/*',
        ],
    },
    'installable': True,
    'application': True
}
