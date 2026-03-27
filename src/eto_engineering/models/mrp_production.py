from odoo import models, fields


class MrpProduction(models.Model):
    _inherit = "mrp.production"

    engineering_design_id = fields.Many2one(
        "engineering.design",
        string="Engineering Design",
    )

    sale_order_id = fields.Many2one(
        "sale.order",
        string="Sales Order",
    )

    def action_view_engineering_design(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": "Engineering Design",
            "res_model": "engineering.design",
            "view_mode": "form",
            "res_id": self.engineering_design_id.id,
        }

    def action_view_sale_order(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": "Sales Order",
            "res_model": "sale.order",
            "view_mode": "form",
            "res_id": self.sale_order_id.id,
        }
