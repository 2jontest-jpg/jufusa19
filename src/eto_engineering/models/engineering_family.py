from odoo import models, fields


class EngineeringFamily(models.Model):
    _name = "engineering.family"
    _description = "Engineering Family"

    name = fields.Char(string="Family Name", required=True)
    code = fields.Char(string="Code")
    description = fields.Text(string="Description")

    product_template_id = fields.Many2one(
        "product.template", string="Product Template", required=True
    )
