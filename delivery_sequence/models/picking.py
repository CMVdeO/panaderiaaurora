# -*- coding: utf-8 -*-

from odoo import models, fields, api


class StockPicking(models.Model):
    _inherit = 'stock.picking'
    _description = 'Agrega campo team_id a stock.picking'

    team_id = fields.Integer(string='TEAM ID', related='partner_id.team_id.id')
    team_name = fields.Char(string='Ruta', related='partner_id.team_id.name', store= True)
    stored_sequence = fields.Char(string='Orden', related='partner_id.stored_sequence')