# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import api, models, fields


class SaleOrder(models.Model):
    _inherit = "sale.order"

    total_product_weight = fields.Float(
        string="Total Weight (kg)", compute="_compute_total_weight")
    total_product_volume = fields.Float(
        string="Total Volume (m³)", compute="_compute_total_volume")

    @api.depends('order_line.total_product_weight')
    def _compute_total_weight(self):
        for order in self:
            total_product_weight = 0.0
            for line in order.order_line:
                total_product_weight += line.total_product_weight
            order.update({
                'total_product_weight': total_product_weight,
            })

    @api.depends('order_line.total_product_volume')
    def _compute_total_volume(self):
        for order in self:
            total_product_volume = 0.0
            for line in order.order_line:
                total_product_volume += line.total_product_volume
            order.update({
                'total_product_volume': total_product_volume,
            })


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    product_weight = fields.Float(string="Weight (kg)")
    product_volume = fields.Float(string="Volume (m³)")

    total_product_weight = fields.Float(string="Total Weight (kg)")
    total_product_volume = fields.Float(string="Total Volume (m³)")


    @api.onchange('product_id')
    def product_change(self):
        print('onchange product_change')
        if self.product_id:
            self.product_weight = self.product_id.weight
            self.product_volume = self.product_id.volume
        else:
            self.product_weight = 0.0
            self.product_volume = 0.0


    @api.model
    def create(self,vals):
        print(vals)
        print(self)
        if self.product_id:
            vals['product_weight'] = self.product_id.weight
            vals['product_volume'] = self.product_id.volume
        else:
            vals['product_weight'] = 0.0
            vals['product_volume'] = 0.0
        vals['total_product_weight'] = vals['product_weight'] * self.product_uom_qty
        vals['total_product_volume'] = vals['product_volume'] * self.product_uom_qty
        res = super(SaleOrderLine,self).create(vals)
        return res

    def write(self,vals):
        print(vals)
        print(self)
        if self.product_id:
            vals['product_weight'] = self.product_id.weight
            vals['product_volume'] = self.product_id.volume
        else:
            vals['product_weight'] = 0.0
            vals['product_volume'] = 0.0
        if not 'total_product_weight' in vals:
            vals['total_product_weight'] = vals['product_weight'] * self.product_uom_qty
            vals['total_product_volume'] = vals['product_volume'] * self.product_uom_qty
        res = super(SaleOrderLine,self).write(vals)
        return res

    @api.onchange('product_uom_qty', 'product_weight')
    def weight_change(self):
        print('onchange weight_change')
        if self.product_weight:
            for line in self:
                line.total_product_weight = 0.0
                line.total_product_weight = line.product_weight * line.product_uom_qty
        else:
            self.total_product_weight = 0.0

    @api.onchange('product_uom_qty', 'product_volume')
    def volume_change(self):
        print('onchange volume_change')
        if self.product_volume:
            for line in self:
                line.total_product_volume = 0.0
                line.total_product_volume = line.product_volume * line.product_uom_qty
        else:
            self.total_product_volume = 0.0
