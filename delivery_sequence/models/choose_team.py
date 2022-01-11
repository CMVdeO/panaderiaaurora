# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ChooseTeam(models.TransientModel):
    _name = 'delivery_sequence.choose_team.wizard'
    _description = 'Elegir la ruta para ver clientes'

    team_id = fields.Many2one("crm.team", string="Rutas", required=True)

    def action_create_list(self):
        print("Button is click")
        if (len(self) == 1):
            for team in self:
                print(team)
                print(team.team_id)
                print(team.team_id.name)
                print(team.team_id.id)
                return  {
                    'name':'Clientes filtrado por ruta',
                    'view_mode':'tree',
                    'view_type':'form',
                    'res_model':'res.partner',
                    'domain': [('team_id','=', team.team_id.id)],
                    'views': [(self.env.ref('delivery_sequence.partner_filter_tree_view').id, 'tree')],
                    'type':'ir.actions.act_window',
                    'target': 'main'
               }
        else:
            print('Se recibió más de una ruta')
