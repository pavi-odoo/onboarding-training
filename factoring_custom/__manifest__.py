{
    "name": "Factoring Custom",
    "summary": "Factoring task",
    "description": "",
    "version": "16.0.1.0",
    "category": "Management",
    "depends": [
        "documents",
        "account_accountant",
        "account",
        "l10n_no",
        "sale_management",
        "contacts",
        "stock",
    ],
    "data": [
        "data/factoring_files_generator_cron.xml",
        "views/res_partner_views.xml",
        "views/sale_order_views.xml",
        "views/account_move_views.xml",
        "views/res_config_settings_views.xml",
        "views/res_partner_bank_views.xml",
    ],
    "demo": [
        "demo/factoring_document_folder.xml"
    ],
    "installable": True,
    "application": True,
    "auto_install": False,
}
