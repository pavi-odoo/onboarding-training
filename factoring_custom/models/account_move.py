from odoo import models, fields, api


class AccountMove(models.Model):
    _inherit = "account.move"

    is_factoring = fields.Boolean(string="Is Factoring")

    @api.model
    def create(self, vals):
        res = super(AccountMove, self).create(vals)
        for rec in res:
            if rec.is_factoring:
                res["narration"] = (
                    self.env["ir.config_parameter"]
                    .sudo().get_param("factoring_custom.assignment_clause")
                )
        return res
