# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
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


class SaleOrderGenerater(models.TransientModel):
    _name = 'delivery_sequence.sale_order_generator.wizard'
    _description = 'Filtro para generar pedidos'


    team_id = fields.Many2one("crm.team", string="Ruta", required=True)
    lap_id = fields.Many2one("delivery_sequence.lap", string="Vuelta", required=True)
    day = fields.Selection(DAY_SELECTION, string="Día", default=lambda self: fields.Datetime.now().strftime('%w'), required=True)
    holiday = fields.Boolean(string="Feriado?", default=0, required=True)
    employee_id = fields.Many2one("hr.employee", string="Vendedor[Nombre]", domain=[('department_id','=',5)], required=True)
    route_id = fields.Many2one("stock.location.route", string="Vendedor[Ruta]", domain=[('sale_selectable','=',True)], required=True)

    #TODO: controlar que un mensaje error si no existen elementos cuando es requerido
    #TODO: Error con algunos productos:  WARNING odoo odoo.http: No se encontró una regla de abastecimiento "[E-COM10] Cubo de pedal" en "Physical Locations/Tránsito entre almacenes".
    #TODO: Ordenar listas de rutas "team_id"

    def action_generator(self):
        # cada vez que uno instancia un objeto sale_order = self.env['sale.order'] y values = sale_order.create(order) el número de orden queda tomado y no se vuelve a utilizar de nuevo. TODO: buscar forma de liberar correlativo.
        for items in self:
            print("int(items.team_id)")
            print(int(items.team_id))
            print("int(items.lap_id)")
            print(int(items.lap_id))
            print("items.day")
            print(items.day)
            print("items.holiday")
            print(items.holiday)
            print("int(items.employee_id)")
            print(int(items.employee_id))
            print("int(items.employee_id.user_id)")
            print(int(items.employee_id.user_id))
            print("int(items.route_id)")
            print(int(items.route_id))
            print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
            sale_data_presort = self.env['delivery_sequence.partner_lap'].search([('team_id','=',int(items.team_id)),('lap_id','=',int(items.lap_id)),('day','=',items.day),('holiday','=',items.holiday),])
            sale_data = sale_data_presort.sorted(lambda s: s.stored_sequence)
            print('Se Ordena por stored Sequence')
            #('team_id','=',int(items.team_id))
            #, order="partner_id.sort_sequence asc")

            """
    partner_id = fields.Many2one("res.partner", string="Cliente", required=True)
    team_id = fields.Char(string="TEAM", related="partner_id.team_id.name")
    sort_sequence = fields.Integer(string="Secuencia", related="partner_id.sort_sequence")
    lap_id = fields.Many2one("delivery_sequence.lap", string="Vuelta", required=True)
    day = fields.Selection(DAY_SELECTION, string="Día", default=lambda self: fields.Datetime.now().strftime('%w'), required=True)
    holiday = fields.Boolean(string="Feriado?", default=0, required=True)
    partner_lap_product_ids = fields.One2many('delivery_sequence.partner_lap_product', 'partner_lap_id', string="Productos en Vueltas")
            """

            len(sale_data)
            print("ffffffffffffgfgfgfgfggfgfgfgg")
            order_created = False
            number_order = 0
            for orders in sale_data:
                print(orders.partner_id.team_id.id)
                print("-----------")
                sum_lines_quantity = 0
                for lines in orders.partner_lap_product_ids:
                    sum_lines_quantity += lines.quantity
                if (orders.partner_lap_product_ids and sum_lines_quantity > 0):
                    order_created = True
                    number_order += 1
                    print(orders.partner_id)
                    print("xxxxxxxxxxxxxxxxxxxx")
                    order = {
                        'date_order': datetime.now(),
                        'state': 'sale',
                        'partner_id': int(orders.partner_id),
                        #'warehouse_id': 1,
                        #'user_id': self.env.user.id,
                        'invoice_status': 'to invoice',
                        'team_id': orders.partner_id.team_id.id,
                        'partner_invoice_id': int(orders.partner_id),
                        'partner_shipping_id': int(orders.partner_id),
                    }
                    print(order)
                    print("11ssssssaaaaaaaaaaaassssssssssssaasasas")
                    # No siempre un empleado tiene un usuario asociado
                    if items.employee_id.user_id:
                        order['user_id'] = int(items.employee_id.user_id)
                    if items.employee_id.user_id.property_warehouse_id:
                        order['warehouse_id'] = int(items.employee_id.user_id.  property_warehouse_id)
                    print(order)
                    print("22ssssssaaaaaaaaaaaassssssssssssaasasas")

                    sale_order = self.env['sale.order']
                    values = sale_order.create(order)
                    sale_order_id = values.id

                    for lines in orders.partner_lap_product_ids:
                        if (lines.quantity > 0):
                            line = {
                                    'order_id': sale_order_id,
                                    'product_id': lines.product_id.id,
                                    'product_uom_qty': lines.quantity,
                                    'route_id': items.route_id.id,
                                    'state': 'sale',
                            }
                            sale_order_line = self.env['sale.order.line']
                            new_line = sale_order_line.create(line)
                            sale_order_line_id = values.id
                            print("aaaaaaaa ------- Imprimio values id para hacer el redirect ------- aaaaaaaaaaaaaaaaaaaaa")
                            print(sale_order_line_id)
                        else:
                            print('Producto sin cantidad')
                else:
                    print("aaaaaaaa ------- vueltas sin productos o sin cantidad ------- aaaaaaaaaaaaaaaaaaaaa")

        if order_created:
            message =  str(number_order) + ' Pedidos'
            return  {
                'name': 'Mensaje',
                'view_mode':'form',
                'view_type':'form',
                'res_model':'delivery_sequence.message.wizard',
                'views': [(self.env.ref('delivery_sequence.message_generator_wizard').id, 'form')],
                'context': {'default_message': message },
                'type':'ir.actions.act_window',
                'target': 'new',
                    }
        else:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': _('Warning'),
                    'message':  'No se creo ningun pedido, revisar que existan y que los productos presenten cantidades',
                    'type': 'danger',  #types: success,warning,danger,info
                    'sticky': False,
                }
            }


    def redirect_to_list(self):
        return  {
                'name': 'Pedidos de ventas',
                'view_mode':'tree,kanban,form,calendar,pivot,graph,activity',
                'view_type':'form',
                'res_model':'sale.order',
                'views': [(self.env.ref('sale.view_order_tree').id, 'tree'),
                            (self.env.ref('sale.view_sale_order_kanban').id, 'kanban'),
                            (self.env.ref('sale.view_order_form').id, 'form'),
                            (self.env.ref('sale.view_sale_order_calendar').id, 'calendar'),
                            (self.env.ref('sale.view_sale_order_pivot').id, 'pivot'),
                            (self.env.ref('sale.view_sale_order_graph').id, 'graph'),
                            (self.env.ref('sale.sale_order_view_activity').id, 'activity')],
                'type':'ir.actions.act_window',
                'target': 'main',
                'nodestroy': True
        }




    # TODO:llamar a la función en partner_lap para no repetir el código de la creación de pedidos. self.env['delivery_sequence.partner_lap'].action_generate(asasdsa)