# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime

DAY_SELECTION = [
    ('1', 'Monday'),
    ('2', 'Tuesday'),
    ('3', 'Wednesday'),
    ('4', 'Thursday'),
    ('5', 'Friday'),
    ('6', 'Saturday'),
    ('0', 'Sunday'),
]

DAY_SELECTION = [
    ('1', 'Lunes'),
    ('2', 'Martes'),
    ('3', 'Miércoles'),
    ('4', 'Jueves'),
    ('5', 'Viernes'),
    ('6', 'Sábado'),
    ('0', 'Domingo'),
]


class PartnerLap(models.Model):
    _name = 'delivery_sequence.partner_lap'
    _description = 'Asociación entre cliente(res.partner) - vuelta(lap) - día(day)'
    _rec_name = 'partner_id'

    #def _today_day(self):
    #    return datetime.now().strftime('%w')

    partner_id = fields.Many2one("res.partner", string="Cliente", required=True, default=1)
    team_id = fields.Integer(string="TEAM ID", related="partner_id.team_id.id")
    team_name = fields.Char(string="TEAM NAME", related="partner_id.team_id.name")
    stored_sequence = fields.Char(string="Orden", related="partner_id.stored_sequence")
    lap_id = fields.Many2one("delivery_sequence.lap", string="Vuelta", required=True)
    day = fields.Selection(DAY_SELECTION, string="Día", default=lambda self: fields.Datetime.now().strftime('%w'), required=True)
    holiday = fields.Boolean(string="Feriado?", default=0, required=True)
    partner_lap_product_ids = fields.One2many('delivery_sequence.partner_lap_product', 'partner_lap_id', string="Productos en Vueltas")


    """
    @api.model
    def _get_default_partner_id(self):
        return 2

    @api.model
    def default_get(self, fields):
        res = super(PartnerLap, fields).default_get(fields)
        res.update ({
            'partner_id': self.env.user.partnet_id.id or False
        })
    """