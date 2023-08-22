from odoo import fields, models, api
import codecs


class ResPartnerBank(models.Model):
    _inherit = "res.partner.bank"

    is_factoring = fields.Boolean(string="Is Factoring")

    @api.model
    def create(self, vals):
        res = super(ResPartnerBank, self).create(vals)
        for rec in res:
            res["is_factoring"] = rec.partner_id.is_factoring
        return res
