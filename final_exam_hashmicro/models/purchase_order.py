from odoo import models, fields, api, _
from datetime import date


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

    def button_confirm(self):
        res = super(PurchaseOrder, self).button_confirm()
        self.update_vendor_price()
        self.update_purchase_date()
        return res

    def update_vendor_price(self):
        for line in self.order_line:
            products = self.env['product.product'].browse(line.product_id.id)
            for vendor in products.seller_ids:
                if self.partner_id.id == vendor.name.id:
                    vendor.write({
                        'price': line.price_unit
                    })

    def update_purchase_date(self):
        for line in self.order_line:
            products = self.env['product.product'].browse(line.product_id.id)
            purchase_date = date.today()
            for vendor in products.seller_ids:
                if self.partner_id.id == vendor.name.id:
                    vendor.write({
                        'purchase_date': purchase_date
                    })

