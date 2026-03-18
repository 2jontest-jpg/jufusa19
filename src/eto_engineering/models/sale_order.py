from odoo import models, fields


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

        design = self.env["engineering.design"].create(
            {
                "name": f"Design for {self.name}",
                "sale_order_id": self.id,
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
