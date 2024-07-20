{
    'name': "Final Exam Hashmicro",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,
    'author': "My Company",
    'website': "http://www.yourcompany.com",
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'product', 'stock', 'purchase','sale_management', 'report_xlsx'],

    # always loaded
    'data': [
        # "security/security.xml",
        "data/ir_sequence.xml",
        "security/ir.model.access.csv",
        "views/sale_order_views.xml",
        "views/purchase_order_views.xml",
        "views/product_views.xml",
        "views/menus.xml",
        "views/fitur_optional/webclient_template_extend.xml",
        "wizard/report_booking_order_pdf/booking_order_pdf_wizard.xml",
        "wizard/report_booking_order_pdf/booking_order_pdf_template.xml",
        "reports/report_action.xml",
        "reports/report_booking_order_customer.xml",
        "reports/payment_report_order/sale_report_wizard_xlsx.xml",
    ],

    'installable': True,
    'application': True,
}

