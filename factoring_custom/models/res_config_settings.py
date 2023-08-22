from odoo import api, fields, models, _


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    assignment_clause = fields.Html(string="Assignment Clause")

    @api.model
    def set_values(self):
        super(ResConfigSettings, self).set_values()
        self.env["ir.config_parameter"].sudo().set_param(
            "factoring_custom.assignment_clause", self.assignment_clause)
        return

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        res.update(
            assignment_clause=self.env["ir.config_parameter"].sudo()
            .get_param("factoring_custom.assignment_clause", self.assignment_clause)
            or "normal")
        return res
