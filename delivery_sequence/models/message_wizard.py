# -*- coding: utf-8 -*-

from odoo import models, fields, api

class MessageWizard(models.TransientModel):
    _name = 'delivery_sequence.message.wizard'
    _description = 'Mensaje de pedidos'

    message = fields.Text(string="Se han creado ", readonly=True)

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
