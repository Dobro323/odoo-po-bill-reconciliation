from odoo import models, fields, api

class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    # Total billed quantity from all vendor bills linked to this PO line
    billed_qty = fields.Float(
        string='Billed Qty',
        compute='_compute_bill_reconciliation',
        store=True
    )

    # Unit price from the vendor bill
    billed_price = fields.Float(
        string='Billed Price',
        compute='_compute_bill_reconciliation',
        store=True
    )

    # Quantity discrepancy: negative = received less than ordered
    qty_discrepancy = fields.Float(
        string='Qty Discrepancy',
        compute='_compute_bill_reconciliation',
        store=True
    )

    # Financial impact of the discrepancy
    amount_discrepancy = fields.Float(
        string='Amount Discrepancy',
        compute='_compute_bill_reconciliation',
        store=True
    )

    # Status for quick visual check
    reconciliation_status = fields.Selection([
        ('ok', 'OK'),
        ('discrepancy', 'Discrepancy'),
        ('no_bill', 'No Bill'),
    ], string='Status', compute='_compute_bill_reconciliation', store=True)

    @api.depends('order_id.invoice_ids', 'product_qty', 'price_unit')
    def _compute_bill_reconciliation(self):
        for line in self:
            # Get all confirmed vendor bills linked to this PO
            bills = line.order_id.invoice_ids.filtered(
                lambda inv: inv.move_type == 'in_invoice'
                and inv.state == 'posted'
            )

            if not bills:
                line.billed_qty = 0
                line.billed_price = 0
                line.qty_discrepancy = -line.product_qty
                line.amount_discrepancy = -(line.product_qty * line.price_unit)
                line.reconciliation_status = 'no_bill'
                continue

            # Sum billed quantities for this product across all bills
            total_billed_qty = 0
            billed_price = 0

            for bill in bills:
                for bill_line in bill.invoice_line_ids:
                    if bill_line.product_id == line.product_id:
                        total_billed_qty += bill_line.quantity
                        billed_price = bill_line.price_unit

            line.billed_qty = total_billed_qty
            line.billed_price = billed_price
            line.qty_discrepancy = total_billed_qty - line.product_qty
            line.amount_discrepancy = (
                (total_billed_qty * billed_price) -
                (line.product_qty * line.price_unit)
            )

            # Determine status
            if total_billed_qty == line.product_qty and billed_price == line.price_unit:
                line.reconciliation_status = 'ok'
            else:
                line.reconciliation_status = 'discrepancy'