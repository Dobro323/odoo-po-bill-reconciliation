from odoo import models, fields, api

class PoReconciliationLine(models.Model):
    _name = 'po.reconciliation.line'
    _description = 'PO Reconciliation Line'

    # Link to the original Purchase Order
    purchase_order_id = fields.Many2one('purchase.order', string='Purchase Order')
    
    # Product being compared
    product_id = fields.Many2one('product.product', string='Product')
    
    # Quantities and prices from the Purchase Order
    po_qty = fields.Float(string='PO Quantity')
    po_price = fields.Float(string='PO Unit Price')
    
    # Quantities and prices from the supplier bill
    bill_qty = fields.Float(string='Bill Quantity')
    bill_price = fields.Float(string='Bill Unit Price')
    
    # Computed discrepancy fields — auto-calculated when qty/price change
    qty_diff = fields.Float(string='Qty Difference', compute='_compute_diff', store=True)
    price_diff = fields.Float(string='Price Difference', compute='_compute_diff', store=True)
    amount_diff = fields.Float(string='Amount Difference', compute='_compute_diff', store=True)

    @api.depends('po_qty', 'bill_qty', 'po_price', 'bill_price')
    def _compute_diff(self):
        for rec in self:
            # Negative = received less than ordered
            rec.qty_diff = rec.bill_qty - rec.po_qty
            rec.price_diff = rec.bill_price - rec.po_price
            # Total financial impact of the discrepancy
            rec.amount_diff = (rec.bill_qty * rec.bill_price) - (rec.po_qty * rec.po_price)