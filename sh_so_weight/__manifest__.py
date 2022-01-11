# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
{
    "name": "Sale Order Product Weight Information",
    "author": "Softhealer Technologies",
    "website": "https://www.softhealer.com",
    "support": "support@softhealer.com",
    "version": "14.0.2",
    "category": "Sales",
    "summary": "Sale Order Weight, Sales Order Total Order Weight, Sale Order Calculate Weight, Quotation Weight Count App,sale weight,kg kg(s) lb lb(s) support, Sales Product Weight,sale prduct line weight, sale total weight, sale product weight Odoo",
    "description": """This module helps you to know the total weight of the sale order products. You can see the product total weight in the list view. You can print product weight in the report as well. Sale Order Product Weight Information Odoo, Weight In Sale Order Module, Total Order Weight In Sales Order, Calculate Total Sale Order Weight, Quotation Weight Count, Display Product Weight In Sale Order, Sales Product Weight Odoo, Sale Order Weight Module, Sales Order Total Order Weight, Sale Order Calculate Weight, Quotation Weight Count App, Product Weight In Sale Order, Sales Product Weight Odoo """,

    "depends": ['stock', 'sale_management'],
    "data": [
        'views/sale_order.xml',
        'report/sales_quotation_report.xml',
    ],
    'demo': [],
    "images": ['static/description/background.png', ],
    "auto_install": False,
    "application": True,
    "installable": True,
    "price": 10,
    "currency": "EUR"
}
