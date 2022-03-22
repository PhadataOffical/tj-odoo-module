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

    'depends': ['base'],

    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    'qweb': [
        'static/src/xml/dtid_menu_template.xml',
        'static/src/xml/dtid_page.xml'
    ],
}
