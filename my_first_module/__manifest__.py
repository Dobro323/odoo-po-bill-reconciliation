{
    'name': 'My First Module',
    'version': '17.0.1.0.0',
    'category': 'Custom',
    'summary': 'My first Odoo module',
    'depends': ['base'],
    'data': [
        'views/res_partner_views.xml',
        'report/partner_report.xml',
    ],
    'installable': True,
    'auto_install': False,
}