from odoo import models, fields, api


class WizardBookingOrderPdf(models.TransientModel):
    _name = 'booking.report.wizardpdf'
    _description = 'Wizard Booking Order PDF'

    from_date = fields.Date(default=lambda self: fields.Datetime.now())
    to_date = fields.Date(default=lambda self: fields.Datetime.now())

    def action_print_report(self):
        report_domain = []
        from_date = self.from_date
        to_date = self.to_date
        if from_date:
            report_domain.append(('date_order', '>=', from_date))
        if to_date:
            report_domain.append(('date_order', '<=', to_date))

        report_domain.append(('is_booking', '=', True))

        finished_report = self.env['sale.order'].search(report_domain)

        data = {
            'form': self.read()[0],
            'docs': finished_report,
        }

        report_action = self.env.ref('final_exam_hashmicro.report_sale_order_booking_order_pdf').report_action(
            self, data=data)
        report_action['close_on_report_download'] = True

        return report_action
