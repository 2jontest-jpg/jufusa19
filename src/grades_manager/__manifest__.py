# -*- coding: utf-8 -*-
{
    "name": "Grades Manager",
    "summary": "Handles grades among students and courses",
    "description": "Handles grades among students and courses, full description",
    "author": "Jonathan Hidalgo",
    "category": "Base",
    "version": "19.0.0.1",
    "depends": ["base", "crm", "project", "account"],
    "data": [
        "security/ir.model.access.csv",
        "views/res_partner_views.xml",
        "views/grades_course_views.xml",
        "views/grades_evaluation_views.xml",
        "views/grades_grade_views.xml",
        "views/crm_lead_views.xml",
        "views/grades_manager_menus.xml",
    ],
    "license": "AGPL-3",
    "application": True,  # Esto es para que aparezca en las apps
    "installable": True,
    "auto_install": False,
}
