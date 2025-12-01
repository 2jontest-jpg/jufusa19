from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError
from markupsafe import Markup


class CrmLead(models.Model):
    _inherit = "crm.lead"

    require_engineering = fields.Boolean(string="Requiere Ingeniería")
    project_id = fields.Many2one(
        "project.project",
        string="Project",
        copy=False,
        help="Project related to this lead",
    )

    task_ids = fields.One2many(
        "project.task",
        compute="_compute_task_ids",
        inverse="_inverse_task_ids",
        string="Tasks",
        readonly=False,
    )

    def write(self, vals):
        # Manejar cambios en task_ids
        if vals and "project_id" in self and "task_ids" in vals:
            for command in vals["task_ids"]:
                if not isinstance(command, (list, tuple)):
                    continue

                cmd = command[0]
                message_body = ""

                # crear nueva tarea
                if cmd == 0 and len(command) >= 3:
                    task_vals = command[2]
                    if not task_vals.get("project_id"):
                        task_vals["project_id"] = self.project_id.id

                    # Asignar el primer stage del proyecto a la tarea (ordenado por secuencia)
                    first_stage = self.env["project.task.type"].search(
                        [("project_ids", "=", self.project_id.id)],
                        order="sequence",
                        limit=1,
                    )
                    if first_stage:
                        task_vals["stage_id"] = first_stage.id

                    self.env["project.task"].create(task_vals)
                    message_body = Markup(
                        f"<p>✅ Se agregó la nueva tarea: <br/> <strong>{task_vals.get('name')}</strong> al proyecto <strong>{self.project_id.name}</strong></p><br/>"
                    )

                # modificar tarea existente
                elif cmd == 1 and len(command) >= 3:
                    task_id = command[1]
                    task_vals = command[2]
                    task = self.env["project.task"].browse(task_id)

                    # Obtener cambios antes de aplicar
                    old_values = {}
                    for field, new_value in task_vals.items():
                        if hasattr(task, field):
                            old_value = getattr(task, field)
                            if old_value != new_value:
                                # formatear nombres de los campos
                                field_name = (
                                    self.env["project.task"]
                                    .fields_get([field])
                                    .get(field, {})
                                    .get("string", field)
                                )
                                old_values[field_name] = {
                                    "old": old_value,
                                    "new": new_value,
                                }

                    task.write(task_vals)

                    # Crear mensaje con los cambios
                    if old_values:
                        changes = []
                        for field_name, values in old_values.items():
                            changes.append(
                                f"<strong>{field_name}</strong>: {values['old']} -> {values['new']}"
                            )

                        message_body_temp = f"📝 Se modificó la tarea <strong>{task.name}</strong> del proyecto <strong>{self.project_id.name}</strong>:<br/>{'<br/>'.join(changes)}"
                        message_body = Markup(message_body_temp + "<br/><br/>")

                    else:
                        message_body = Markup(
                            f"✅ Se actualizó la tarea: <strong>{task.name}</strong><br/>"
                        )

                # borrar tarea
                elif cmd == 2 and len(command) >= 2:
                    task_id = command[1]
                    task_to_deleted = self.env["project.task"].browse(task_id)
                    message_body = Markup(
                        f"<p>❌ Se borró la tarea <b>{task_to_deleted.name}</b> del proyecto <strong>{self.project_id.name}</strong></p><br/>"
                    )
                    task_to_deleted.unlink()

                # link (4), unlink (3), etc. los puedes manejar igual si los necesitas

                if message_body:
                    self.message_post(body=message_body)

            # ⚠️ muy importante: ya no dejamos task_ids en vals
            vals.pop("task_ids")

        if ("require_engineering" in vals and vals["require_engineering"]) and (
            "project_id" not in self or not self.project_id.name
        ):
            message_body = ""
            self.action_create_project()
            message_body = Markup(
                f"<p>✅ Se creo el proyecto: <br/><strong>{self.project_id.name}</strong></p><br/>"
            )
            self.message_post(body=message_body)

        if ("require_engineering" in vals and not vals["require_engineering"]) and (
            "project_id" in self and self.project_id.name
        ):
            project_name = self.project_id.name
            message_body = ""
            self.project_id.unlink()
            message_body = Markup(
                f"<p>❌ Se borro el proyecto: <br/><strong>{project_name}</strong></p><br/>"
            )
            self.message_post(body=message_body)

        return super(CrmLead, self).write(vals)

    # Función para crear el proyecto si se necesita. Se podría usar un botón.
    def action_create_project(self):
        self.ensure_one()

        self = self.with_context(bypass_validation=True)
        # Seleccionar la plantilla de proyecto
        project_to_duplicate = self.env["project.project"].search(
            [("name", "=", "Plantilla ingeniería")], limit=1
        )

        if not project_to_duplicate:
            raise ValidationError(
                (
                    "No se encontró la plantilla de proyecto 'Plantilla ingeniería'. "
                    "Por favor, crea un proyecto con ese nombre para usarlo como plantilla."
                )
            )

        # Duplicar la plantilla
        project = project_to_duplicate.copy(
            {
                "name": "Consulta " + self.name,
                "partner_id": self.partner_id.id,
            }
        )

        self.project_id = project.id
        # Opcional: Mostrar una notificación al usuario
        return {
            "type": "ir.actions.client",
            "tag": "display_notification",
            "params": {
                "title": "Proyecto Creado",
                "message": f'El proyecto "{project.name}" se ha creado y asociado al lead.',
                "sticky": False,
            },
        }

    def _compute_task_ids(self):
        for lead in self:
            if lead.project_id:
                lead.task_ids = lead.project_id.task_ids
            else:
                lead.task_ids = self.env["project.task"]

    def _inverse_task_ids(self):
        """Este método se llama cuando se crean/editan tareas desde el lead."""

        for lead in self:
            if not lead.project_id:
                raise UserError(("You cannot add tasks to a lead without a project."))
        # Al crear una tarea desde aquí, Odoo ya asigna el project_id automaticamente
        # porque la tarea se guarda con el contexto del lead, pero asegurémonos
        lead = self["lead"]
        for task in lead.task_ids:
            if not task.project_id:
                task.project_id = lead.project_id
