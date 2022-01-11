# -*- coding: utf-8 -*-

from odoo import models, fields, api


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

        print('Se activa search_read')
        return {
            'type': 'ir.actions.client',
            'tag': 'do_read',
        }


    def write(self, vals):
        print(vals)
        if 'team_id' in vals:
            team = self.env['crm.team'].search([('id','=',vals['team_id'])])
            partner = self.env['res.partner'].search([('id','=', self.id)])
            print(partner.team_id)
            print(vals['team_id'])
            if partner.team_id.id != vals['team_id']:
                records = self.env['res.partner'].search([('team_id', '=', vals['team_id'])])
                if len(records) == 0:
                    vals['stored_sequence'] = str(team[0].name)[-1] +  str(1).zfill(3)
                else:
                    last_record_index = len(records) - 1
                    sequence = records[last_record_index].sort_sequence
                    vals['sort_sequence'] = sequence + 1
                    vals['stored_sequence'] = str(team[0].name)[-1] +  str(len(records) + 1).zfill(3)
        res = super(ResPartner, self).write(vals)
        return res


    @api.onchange('team_id')
    def _onchange_team_stored_sequence(self):
        print(self.team_id.id)
        records = self.env['res.partner'].search([('team_id', '=', self.team_id.id)])
        print(self.id)
        print(self._origin.id)
        if self._origin in records:
            print('Se Logro')
            print(self._origin.stored_sequence)
            print(self._origin.sort_sequence)
            self.stored_sequence = self._origin.stored_sequence
            self.sort_sequence = self._origin.sort_sequence
        else:
            if len(records) == 0:
                self.stored_sequence = str(self.team_id.name)[-1] +  str(1).zfill(3)
            else:
                last_record_index = len(records) - 1
                sequence = records[last_record_index].sort_sequence
                self.sort_sequence = sequence + 1
                self.stored_sequence = str(self.team_id.name)[-1] +  str(len(records) + 1).zfill(3)
            print(len(records))


    def action_reload(self):
        print('Se activa reload')
        return {
            'type': 'ir.actions.client',
            'tag': 'do_reload',
        }

    def create_all_laps(self):
        print(self)
        print(self.id)
        product_sale_ok = self.env['product.product'].search([('sale_ok', '=', True)])
        laps = self.env['delivery_sequence.lap'].search([])
        partner_laps = []
        for lap_type in laps:
            print(lap_type.name)
            holiday = False
            for day in DAY_SELECTION:
                print(day)
                print(day[0])
                print(day[1])
                is_in = False
                for partner_lap in self.partner_lap_ids:
                    if(partner_lap.day == day[0] and partner_lap.holiday == holiday and partner_lap.lap_id == lap_type ):
                        print('Ya esta presente dentro de partner_laps')
                        is_in = True
                    else:
                        print('No esta presente en partner_laps')
                print('----------------Existe la linea?----------------------')
                if (not is_in):
                    partner_lap_create = {
                        'partner_id': self.id,
                        'lap_id': lap_type.id,
                        'day': day[0],
                        'holiday': holiday,
                    }
                    partner_lap_env = self.env['delivery_sequence.partner_lap']
                    val =  partner_lap_env.create(partner_lap_create)
                    partner_lap_create_id = val.id
                    for product in product_sale_ok:
                        partner_lap_product_create = {
                            'partner_lap_id': partner_lap_create_id,
                            'product_id': product.id,
                            'quantity': 0
                        }
                        partner_lap_product_env = self.env['delivery_sequence.partner_lap_product']
                        val2 = partner_lap_product_env.create(partner_lap_product_create)

                print('------------------------------------------------------')
            holiday = True
            for day in DAY_SELECTION:
                print(day)
                print(day[0])
                print(day[1])
                is_in = False
                for partner_lap in self.partner_lap_ids:
                    if(partner_lap.day == day[0] and partner_lap.holiday == holiday and partner_lap.lap_id == lap_type ):
                        print('Ya esta presente dentro de partner_laps')
                        is_in = True
                    else:
                        print('No esta presente en partner_laps')
                print('----------------Existe la linea?----------------------')
                if (not is_in):
                    partner_lap_create = {
                        'partner_id': self.id,
                        'lap_id': lap_type.id,
                        'day': day[0],
                        'holiday': holiday,
                    }
                    partner_lap_env = self.env['delivery_sequence.partner_lap']
                    val =  partner_lap_env.create(partner_lap_create)
                    partner_lap_create_id = val.id
                    for product in product_sale_ok:
                        partner_lap_product_create = {
                            'partner_lap_id': partner_lap_create_id,
                            'product_id': product.id,
                            'quantity': 0
                        }
                        partner_lap_product_env = self.env['delivery_sequence.partner_lap_product']
                        val2 = partner_lap_product_env.create(partner_lap_product_create)
                print('------------------------------------------------------')
