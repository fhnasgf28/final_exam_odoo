from odoo import models, fields, api


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    is_booking = fields.Boolean(string='Is Booking', default=False)
    booking_order_id = fields.Many2one('sale.order', string='Booking Order')

    def write(self, vals):
        for record in self:
            if record.is_booking:
                vals['name'] = self.env['ir.sequence'].next_by_code('request.quotation') or _('New')
        return super(PurchaseOrder, self).write(vals)


