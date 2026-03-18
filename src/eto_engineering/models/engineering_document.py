from odoo import models, fields


class EngineeringDocument(models.Model):
    _name = "engineering.document"
    _description = "Engineering Document"

    name = fields.Char(string="Document Name", required=True)

    design_id = fields.Many2one(
        "engineering.design", string="Engineering Design", ondelete="cascade"
    )

    document_type = fields.Selection(
        [
            ("drawing", "Drawing"),
            ("technical_pdf", "Technical PDF"),
            ("material_certificate", "Material Certificate"),
            ("inspection_report", "Inspection Report"),
        ],
        string="Document Type",
    )

    file = fields.Binary(string="File")

    filename = fields.Char(string="Filename")

    uploaded_by = fields.Many2one("res.users", string="Uploaded By")

    uploaded_date = fields.Datetime(string="Uploaded Date", default=fields.Datetime.now)
