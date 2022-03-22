{
    'name': '销售签章',
    'version': '1.0',
    'sequence':1,
    'description': """
基于可信数字身份,在销售订单中签章
===================================================
""",
    'depends': ['sale_management','seal_management','phadata_dtid_service'],
    # 'qweb': [
    #     'static/src/xml/sale_sign_pdf_page.xml',
    #     'static/src/xml/sale_sign_form_page.xml',
    #     "static/src/xml/contract_sign_page.xml"
    # ],
    'data': [
        'security/ir.model.access.csv',
        'views/extends_views.xml',
        'views/sale_sign_views.xml',
        'views/menus.xml',
        'views/templates.xml',
    ],
    'external_dependencies': {
        'python': ['minio']
    },
    'assets': {
        'web.assets_backend': [
            'sale_sign/static/src/js/*',
            'sale_sign/static/src/css/*',
        ],
        'web.assets_qweb': [
            'sale_sign/static/src/xml/*',
            'sale_sign/static/src/xml/**/*',
        ],
    },
    'bootstrap': True,
    'application': True,
}

