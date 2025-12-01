from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = "res.partner"

    is_teacher = fields.Boolean(string="Is Teacher")
    is_freelance = fields.Boolean(string="Is Freelance")

    is_student = fields.Boolean(string="Is Student")
    # Esta es una manera de hacerlo pero le afecta a todas las vistas que hacen uso de res.partner
    # vat = fields.Char(required=True)

    def unlink(self):
        if self.email == "principal@gmail.com":
            courses = self.env["grades.course"].search([("teacher_id", "=", self.id)])
            seconadary = self.env["res.partner"].search(
                [("email", "=", "secundario@gmail.com")]
            )
            courses.write({"teacher_id": seconadary.id})
        result = super(ResPartner, self).unlink()
        return result
