from odoo import models, fields, api, _


class AccountMove(models.Model):
    _inherit = 'account.move'

    purchase_id = fields.Many2one('purchase.order', string='Purchase Order', store=True)

    def action_post(self):
        super(AccountMove, self).action_post()
        # Create delivery order if the invoice is posted
        if self.state == 'posted':
            self.create_delivery_order()

    def create_delivery_order(self):
        StockPicking = self.env['stock.picking']
        for move in self:
            # Create a delivery order
            if move.move_type == 'out_invoice':
                print('method stock picking ini diklik')
                picking_type_out = self.env.ref('stock.picking_type_out')

                picking_vals = {
                    'partner_id': move.partner_id.id,
                    'location_id': picking_type_out.default_location_src_id.id,
                    'location_dest_id': move.partner_id.property_stock_customer.id,
                    'picking_type_id': picking_type_out.id,
                    'move_type': 'direct',  # 'direct' or 'one' based on your stock configuration
                    'move_lines': [],
                }
                for line in move.invoice_line_ids:
                    if line.product_id.type == 'product':
                        move_line_vals = {
                            'name': line.name,
                            'product_id': line.product_id.id,
                            'product_uom_qty': line.quantity,
                            'product_uom': line.product_uom_id.id,
                            'location_id': self.env.ref('stock.stock_location_stock').id,
                            'location_dest_id': move.partner_id.property_stock_customer.id,
                        }
                        picking_vals['move_lines'].append((0, 0, move_line_vals))

                StockPicking.create(picking_vals)
