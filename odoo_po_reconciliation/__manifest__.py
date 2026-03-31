{
    'name': 'PO Bill Reconciliation',
    'version': '17.0.1.0.0',
    'category': 'Purchase',
    'summary': 'Automated reconciliation of Purchase Orders with supplier bills',
    'depends': ['base', 'purchase', 'account'],
    'data': [
        'views/res_partner_views.xml',
        'report/partner_report.xml',
    ],
    'installable': True,
    'auto_install': False,
}