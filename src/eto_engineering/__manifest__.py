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
        "security/security.xml",
        "security/ir.model.access.csv",
        "views/engineering_design_views.xml",
        "views/engineering_menu.xml",
        "views/sale_order_views.xml",
    ],
    "installable": True,
    "application": True,
}
