# -*- coding: utf-8 -*-

from odoo import models, fields, api


class PartnerLapProduct(models.Model):
    _name = 'delivery_sequence.partner_lap_product'
    _description = 'Productos que componen una vuelta del cliente'


    partner_lap_id = fields.Many2one("delivery_sequence.partner_lap", ondelete='cascade', string="Vuelta del cliente", required=True)
    product_id = fields.Many2one("product.product", string="Product", required=True, domain="[('sale_ok', '=', False)]")
    quantity = fields.Float(required=True)
    #TODO: decimales en float... quantity = fields.Float(required=True, digits=(16, 4), default=0.0)
