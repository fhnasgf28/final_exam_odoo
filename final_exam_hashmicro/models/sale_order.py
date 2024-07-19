from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    is_booking = fields.Boolean(string='Is Booking', default=False)
    date_created = fields.Datetime(string='Creation Date', default=fields.Datetime.now)
    rfq_created = fields.Boolean(string="RFQ Created", default=False)

    @api.model
    def create(self, vals):
        if vals.get('is_booking'):
            sequence_code = 'booking.order'
        else:
            sequence_code = 'sale.order'
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code(sequence_code) or _('New')
        res = super(SaleOrder, self).create(vals)
        return res

    def action_create_rfq(self):
        for record in self:
            if record.rfq_created:
                raise ValidationError(f'Product {record.name} already been added to RFQ.')
            rfq = self.env['purchase.order'].create({
                'partner_id': record.partner_id.id,
                'date_order': fields.Datetime.now(),
                'name': record.name,
                'is_booking': True,
                'order_line': [(0, 0, {
                    'product_id': line.product_id.id,
                    'name': line.name,
                    'product_qty': line.product_uom_qty,
                    'price_unit': line.price_unit,
                    'date_planned': fields.Datetime.now(),
                }) for line in record.order_line]
            })
            record.rfq_created = True
            return {
                'name': 'RFQ Created',
                'type': 'ir.actions.act_window',
                'res_model': 'purchase.order',
                'res_id': rfq.id,
                'view_mode': 'form',
            }


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    qty_booking = fields.Float(string='Quantity Booking', default=1.0, store=True)
    product_template_id = fields.Many2one('product.template', string='Product Template', compute='_compute_product_template_id')

    @api.onchange('product_uom_qty')
    def _onchange_qty_booking(self):
        for line in self:
            line.qty_booking = line.product_uom_qty

    @api.depends('product_id')
    def _compute_product_template_id(self):
        for record in self:
            record.product_template_id = record.product_id.product_tmpl_id

    # @api.onchange('order_id.is_booking', 'price_unit', 'product_id')
    # def _onchange_is_booking(self):
    #     for line in self:
    #         if line.product_id:
    #             price = line.product_id.lst_price
    #             if line.order_id.is_booking:
    #                 line.price_unit = price * 1.1
    #             else:
    #                 line.price_unit = price
