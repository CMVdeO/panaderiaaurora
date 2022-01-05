# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Lap(models.Model):
    _name = 'delivery_sequence.lap'
    _description = 'Listado o nombre de la vuelta(lap)'

    name = fields.Char(string="Nombre de la vuelta", required=True)