from odoo import models, fields

class ResPartner(models.Model):
    _inherit = 'res.partner'

    customer_priority = fields.Selection([
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ], string='Customer Priority', default='medium')