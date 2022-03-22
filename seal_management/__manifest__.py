# -*- coding: utf-8 -*-
{
    'name': "印章",
    'summary': """印章""",
    'sequence': 1,
    'description': """
       印章
    """,
    'version': '0.1',
    'depends': ['base',
                'web'],
    'data': [
        'security/ir.model.access.csv',
        'views/templates.xml',
        'views/seal_list_view.xml',
        'views/menu_view.xml',
    ],
    'qweb': [
        'static/src/xml/seal_list.xml',
        'static/src/xml/iframe.xml'
        # 'static/src/xml/seal_item.xml'
    ],
    'installable': True,
    'application': True
}
