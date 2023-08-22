from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = "res.partner"

    is_factoring = fields.Boolean(string="Is factoring")
    factoring_partner = fields.Boolean(string="Factoring Partner")
