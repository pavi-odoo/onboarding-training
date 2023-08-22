from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = "sale.order"

    is_factoring = fields.Boolean(string="Is Factoring")

    @api.onchange("partner_id")
    def _onchange_partner_id(self):
        for rec in self:
            rec.is_factoring = rec.partner_id.is_factoring

    def _prepare_invoice(self):
        res = super(SaleOrder, self)._prepare_invoice()
        res["is_factoring"] = self.is_factoring
        return res
