from odoo import models, fields, api


class GradesEvaluation(models.Model):
    _name = "grades.evaluation"
    _description = "Grades Evaluation"
    # _order = '' #Como aparecen ordenados los registros, generalmente lo hace por el primer campo
    # _rec_name = '' se utilizan para mas migajas de pan, generalmente es el field name

    name = fields.Char(string="Name")
    date = fields.Date(string="Date")
    observations = fields.Text(string="Observations")
    course_id = fields.Many2one("grades.course", string="Course", ondelete="cascade")
    grade_ids = fields.One2many("grades.grade", "evaluation_id", string="Grades")

    @api.model_create_multi
    def create(self, vals):
        res = super(GradesEvaluation, self).create(vals)
        for student in res.course_id.student_ids:
            self.env["grades.grade"].create(
                {
                    "evaluation_id": res.id,
                    "date": fields.Date.today(),
                    "student_id": student.id,
                }
            )
        return res
