{
    "name": "Factoring Custom",
    "summary": "Factoring task",
    "description": "",
    "version": "16.0.1.0",
    "category": "Management",
    "depends": [
        "sale_management",
        "account",
        "account_accountant",
        "contacts",
        "stock",
    ],
    "data": [
        "views/res_partner_views.xml",
        "views/sale_order_views.xml",
        "views/account_move_views.xml",
        "views/res_config_settings_views.xml",
        "views/res_partner_bank_views.xml",
    ],
    "installable": True,
    "application": True,
    "auto_install": False,
}
