from odoo import models, fields
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    engineering_design_ids = fields.One2many(
        "engineering.design", "sale_order_id", string="Engineering Designs"
    )

    engineering_design_count = fields.Integer(
        compute="_compute_engineering_design_count"
    )

    def _compute_engineering_design_count(self):
        for order in self:
            order.engineering_design_count = len(order.engineering_design_ids)

    def action_create_engineering_design(self):
        self.ensure_one()

        if not self.order_line:
            raise UserError("Add a product before creating engineering design")

        line = self.order_line[0]

        family = line.product_id.product_tmpl_id.engineering_family_id

        if not family:
            raise UserError("This product has no engineering family assigned")

        design = self.env["engineering.design"].create(
            {
                "name": "New",
                "sale_order_line_id": line.id,
                "family_id": family.id,
            }
        )

        return {
            "type": "ir.actions.act_window",
            "name": "Engineering Design",
            "res_model": "engineering.design",
            "view_mode": "form",
            "res_id": design.id,
            "target": "current",
        }

    def action_view_engineering_design(self):
        self.ensure_one()

        if not self.engineering_design_ids[0]:
            raise UserError("No Engineering Design associated with order")

        return {
            "type": "ir.actions.act_window",
            "name": "Engineering Design",
            "res_model": "engineering.design",
            "view_mode": "form",
            "res_id": self.engineering_design_ids[0].id,
        }
