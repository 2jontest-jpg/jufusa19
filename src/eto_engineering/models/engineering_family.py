from odoo import models, fields


class EngineeringFamily(models.Model):
    _name = "engineering.family"
    _description = "Engineering Product Family"

    name = fields.Char(string="Family Name", required=True)

    code = fields.Char(string="Code")

    description = fields.Text()
