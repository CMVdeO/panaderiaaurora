# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'
    _description = 'Agrega campo sort_sequence en res.partner para indicar el orden de generación de OT'
    _order = "team_id asc,sort_sequence"

    sort_sequence = fields.Integer(string="Secuencia", default=1)
    path_sequence = fields.Char(string='Orden de Ruta', compute='_path_sequence')
    stored_sequence = fields.Char(string="Orden",  readonly="1")
    partner_lap_ids = fields.One2many('delivery_sequence.partner_lap', 'partner_id', string="Vueltas")



    @api.depends('sort_sequence','team_id')
    def _path_sequence(self):
        numberOrder = 1
        changeNumber = True
        print(self[0].team_id.id)
        for rec in self:
            new_path_sequence = ''
            print('-------------------------------------------')
            print(rec.team_id.name)
            print('-------------------------------------------')
            print(rec.sort_sequence)
            print('-------------------------------------------')
            if (rec.team_id and rec.sort_sequence >= 0):
                number = str(rec.sort_sequence)
                print('-------------------------------------------')
                print(rec.sort_sequence)
                print('-------------------------------------------')
                print(numberOrder)
                print('-------------------------------------------')
                new_path_sequence = str(rec.team_id.name)[-1] + str(numberOrder).zfill(3)
            print('-------------------------------------------')
            print(new_path_sequence)
            print('-------------------------------------------')
            rec['path_sequence'] = new_path_sequence
            numberOrder += 1
            # posible solución model="ir.sequence" sólo en la vista... la idea es que este campo se componga de la ùltima letra del team_id (RUTA A) más el correlativo de sort_sequence, el tema es que sort_sequence no se detiene al pasar a otra ruta, es un correlativo
            #https://www.youtube.com/watch?v=Cz5eM5FDmTE
        records = self.env['res.partner'].search([('team_id', '=', self[0].team_id.id)])
        for rec in records:
            print('-------------------------------------------')
            print('Sequencia a copiar')
            print(rec.path_sequence)
            print('-------------------------------------------')
            rec.write({'stored_sequence': rec.path_sequence})



    def action_reload(self):
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }