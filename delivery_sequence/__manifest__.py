# -*- coding: utf-8 -*-
{
    'name': "Delivery Sequence",

    'summary': """
Match Partner - Lap - Product
    """,

    'description': """
Match Partner - Lap - Product
    """,

    'author': "Checkmate SpA",
    'website': "https://www.checkmateagencia.cl",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Manufacturing/Manufacturing',
    'version': '14.0.1.0.2',
    'sequence': -100,

    # any module necessary for this one to work correctly
    'depends': [
        'product',
        'sale_management',
        'stock',
        'hr',
        'contacts',
    ],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/lap.xml',
        'views/partner.xml',
        'views/partner_lap.xml',
        'views/sale_order_generator.xml',
        'views/partner_sort_sequence.xml',
        'views/partner_filter.xml',
        'views/choose_team.xml',
        'views/picking.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        #'demo/demo.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
    'license': 'LGPL-3',
}