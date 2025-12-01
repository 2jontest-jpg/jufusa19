from odoo import models, fields


class GradesGrade(models.Model):
    _name = 'grades.grade'
    _description = 'Grades Grade'
    #_order = '' #Como aparecen ordenados los registros, generalmente lo hace por el primer campo
    #_rec_name = '' se utilizan para mas migajas de pan, generalmente es el field name

    student_id = fields.Many2one('res.partner', string='Student')
    evaluation_id = fields.Many2one('grades.evaluation', string='Evaluation',readonly=True, required=True)
    grade = fields.Float(string='Grade')
    date = fields.Date(string='Date' , default=fields.Date.today())
