# -*- coding: utf-8 -*-
from odoo import api, fields, models


class MrpProduction(models.Model):
    _inherit = "mrp.production"

    mrp_production_team_ids = fields.Many2many("hr.employee", 'production_employee_rel',  'employee_id', 'production_id', string="Encargados de producción", required=False)