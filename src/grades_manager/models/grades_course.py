from odoo import models, fields, api
from odoo.exceptions import ValidationError


class GradesCourse(models.Model):
    _name = "grades.course"
    _description = "Grades Course"
    # _order = '' #Como aparecen ordenados los registros, generalmente lo hace por el primer campo
    # _rec_name = '' se utilizan para mas migajas de pan, generalmente es el field name

    def _default_teacher(self):
        teacher = self.env["res.partner"].search(
            [("name", "ilike", "Profesor principal")], limit=1
        )
        return teacher.id

    name = fields.Char(string="Name")
    student_qty = fields.Integer(string="Student quantity")
    grades_average = fields.Float(string="Grades average")
    description = fields.Text(string="Description")
    is_active = fields.Boolean(string="Is Active")
    course_start = fields.Date(string="Course Start", default=fields.Date.today())
    course_end = fields.Date(string="Course End")
    last_evaluation_date = fields.Datetime(string="Last evaluation date")
    course_image = fields.Binary(string="Course image")
    course_shift = fields.Selection(
        [("day", "Day"), ("night", "Night")], string="Course shift"
    )
    teacher_id = fields.Many2one(
        "res.partner", string="Teacher", default=_default_teacher
    )

    teacher_email = fields.Char(string="Teacher email", related="teacher_id.email")

    evaluation_ids = fields.One2many(
        "grades.evaluation", "course_id", string="Evaluations"
    )
    # No dejar que odoo ponga el nombre de la tabla intermedia para esta relación. Entonces se agrega
    student_ids = fields.Many2many(
        "res.partner", "grades_course_student_rel", string="Students"
    )
    state = fields.Selection(
        [
            ("register", "Register"),
            ("in_progress", "In progress"),
            ("finished", "Finished"),
        ],
        string="State",
        default="register",
    )

    # _sql_constraints = [
    #     ("make_teacher_unique", "unique(teacher_id)", "The teacher must be unique")
    # ]

    @api.constrains("teacher_id")
    def _check_teacher_id(self):
        for record in self:
            if (
                self.search_count(
                    [("teacher_id", "=", record.teacher_id), ("id", "!=", record.id)]
                )
                > 0
            ):
                raise ValidationError("The teacher must be unique")

    # Funciones personalizadas
    # Antes de que se guarde este modelo

    def write(self, vals):
        if vals and "evaluation_ids" in vals and not self.student_ids:
            raise ValidationError(
                "The course must have at least one student for you add an evaluation"
            )
        res = super(GradesCourse, self).write(vals)
        return res
