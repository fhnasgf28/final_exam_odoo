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

    # (optional) fitur refresh price
    def action_refresh_price(self):
        for line in self.order_line:
            supplierinfo = line.product_id.seller_ids.filtered(
                lambda r: r.product_code == line.product_id.default_code and
                          r.partner_id.name == line.order_id.partner_id.name
            )
            if supplierinfo:
                line.price_unit = supplierinfo[0].price

