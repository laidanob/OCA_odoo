# -*- coding: utf-8 -*-
{
    'name': "Oca Odoo Connector",

    'summary': """
        Connector Odoo-Oca for Shipping Payment""",

    'description': """
        Connector Odoo-Oca for Shipping Payment
    """,

    'author': "Moldeo Interactive",
    'website': "https://www.moldeointeractive.com.ar",

    'category': 'Sales',
    'version': '0.1',

    'depends': ['base', 'sale', 'delivery','website_sale_delivery'],

    'data': [
        'views/res_company.xml',
    ]
}
