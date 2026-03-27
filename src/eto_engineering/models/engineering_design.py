from odoo import models, fields, api
from odoo.exceptions import UserError


class EngineeringDesign(models.Model):
    _name = "engineering.design"
    _description = "Engineering Design"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    product_id = fields.Many2one(
        "product.product", string="Generated Product", readonly=True
    )

    name = fields.Char(
        string="Design Reference", required=True, copy=False, default="New"
    )

    sale_order_id = fields.Many2one("sale.order", string="Sales Order", required=True)
    production_id = fields.Many2one("mrp.production", string="Manufacturing Order")

    family_id = fields.Many2one(
        "engineering.family", string="Product Family", required=True
    )

    diameter = fields.Float(string="Diameter")
    length = fields.Float(string="Length")

    material_inner = fields.Char(string="Inner Material")
    material_outer = fields.Char(string="Outer Material")

    pressure_rating = fields.Char(string="Pressure Rating")

    notes = fields.Text()

    bom_line_ids = fields.One2many(
        "engineering.bom.line", "design_id", string="Engineering BOM"
    )

    document_ids = fields.One2many(
        "engineering.document", "design_id", string="Documents"
    )

    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("review", "In Review"),
            ("approved", "Approved"),
            ("released", "Released"),
        ],
        default="draft",
    )

    def action_view_sale_order(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": "Sales Order",
            "res_model": "sale.order",
            "view_mode": "form",
            "res_id": self.sale_order_id.id,
        }

    def action_view_manufacturing_order(self):
        self.ensure_one()

        if not self.production_id:
            raise UserError("No Manufacturing Order associated with design")

        return {
            "type": "ir.actions.act_window",
            "name": "Manufacturing Order",
            "res_model": "mrp.production",
            "view_mode": "form",
            "res_id": self.production_id.id,
        }

    def action_release_design(self):
        for rec in self:

            rec._validate_before_release()

            # 1. Crear producto dinámico
            rec._create_product_from_design()

            # 2. Generar BOM
            bom = rec._generate_bom()

            # 3. Crear MO
            rec._create_manufacturing_order(bom)

            # 4. Cambiar estado
            rec.state = "released"

    def action_set_review(self):
        for rec in self:
            rec.state = "review"

    def action_approve_design(self):
        for rec in self:
            rec.state = "approved"

    def _create_product_from_design(self):
        ProductTemplate = self.env["product.template"]

        for rec in self:
            if rec.product_id:
                continue

            name = f'{rec.family_id.name} Ø{rec.diameter}" L{rec.length}"'

            template = ProductTemplate.create(
                {
                    "name": name,
                    "detailed_type": "product",
                    "tracking": "lot",
                }
            )

            rec.product_id = template.product_variant_id.id

    def _generate_bom(self):
        self.ensure_one()

        Bom = self.env["mrp.bom"]
        BomLine = self.env["mrp.bom.line"]

        if not self.product_id:
            raise UserError("No product associated with design")

        if not self.bom_line_ids:
            raise UserError("EBOM vacía")

        bom = Bom.create(
            {
                "product_tmpl_id": self.product_id.product_tmpl_id.id,
                "product_qty": 1,
                "type": "normal",
            }
        )

        for line in self.bom_line_ids:
            BomLine.create(
                {
                    "bom_id": bom.id,
                    "product_id": line.product_id.id,
                    "product_qty": line.quantity,
                }
            )

        return bom

    def _create_manufacturing_order(self, bom):
        self.ensure_one()

        Production = self.env["mrp.production"]

        if not bom:
            raise UserError("No BOM provided")

        production = Production.create(
            {
                "product_id": self.product_id.id,
                "product_qty": 1,
                "bom_id": bom.id,
                "origin": self.sale_order_id.name,  # 🔥 mejor que self.name
                "engineering_design_id": self.id,
                "sale_order_id": self.sale_order_id.id,
            }
        )

        self.production_id = production.id

        return production

    def _validate_before_release(self):
        if not self.family_id:
            raise UserError("Product family is required")

        if not self.bom_line_ids:
            raise UserError("EBOM is empty")
