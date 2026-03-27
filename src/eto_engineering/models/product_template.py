from odoo import models, fields


class ProductTemplate(models.Model):
    _inherit = "product.template"

    engineering_family_id = fields.Many2one(
        "engineering.family", string="Engineering Family"
    )
