{
    "name": "ETO Engineering",
    "version": "1.0",
    "summary": "Engineering-to-Order workflow integration",
    "description": """
ETO Engineering module
Handles engineering design linked to sales orders
""",
    "author": "Your Company",
    "depends": ["sale", "mrp", "stock"],
    "data": [
        "security/ir.model.access.csv",
        "security/security.xml",
        "views/engineering_family_views.xml",
        "views/engineering_design_views.xml",
        "views/engineering_menu.xml",
        "views/sale_order_views.xml",
        "views/mrp_production_views.xml",
        "views/product_template_views.xml",
    ],
    "installable": True,
    "application": True,
}
