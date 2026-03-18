from odoo import models, fields


class EngineeringBomLine(models.Model):
    _name = "engineering.bom.line"
    _description = "Engineering BOM Line"

    design_id = fields.Many2one(
        "engineering.design", string="Design", required=True, ondelete="cascade"
    )

    product_id = fields.Many2one("product.product", string="Component", required=True)

    quantity = fields.Float(string="Quantity", default=1)

    uom_id = fields.Many2one("uom.uom", string="Unit of Measure")

    notes = fields.Text(string="Notes")
