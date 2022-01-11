# -*- coding: utf-8 -*-
{
    'name': 'Production Team - MRP',
    'version': '14.0.1.0.2',
    'author': "Checkmate SpA",
    'summary': """
Set Production Team in Manufacturing
    """,
    'sequence': -100,
    'description': """
Set Production Team in Manufacturing.
    """,
    'category': 'Manufacturing/Manufacturing',
    'website': 'https://www.checkmateagencia.cl',
    'depends':  ['mrp','hr'],
    'data':  [
        'views/mrp_production.xml'
    ],
    'installable': True,
    'auto_install': True,
    'application': False,
    'license': 'LGPL-3'
}