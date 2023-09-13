from odoo import api, fields, models, _


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    assignment_clause = fields.Html(string="Assignment Clause")

    @api.model
    def set_values(self):
        """
        Set value in res config setting.
        """
        super(ResConfigSettings, self).set_values()
        config_parameter = self.env["ir.config_parameter"]
        config_parameter.sudo().set_param("factoring_custom.assignment_clause", self.assignment_clause)
        return

    @api.model
    def get_values(self):
        """
        Get value after save the settings.
        """
        res = super(ResConfigSettings, self).get_values()
        config_parameter = self.env["ir.config_parameter"]
        res.update(
            assignment_clause=config_parameter.sudo().
                              get_param("factoring_custom.assignment_clause", self.assignment_clause) or " ")
        return res
