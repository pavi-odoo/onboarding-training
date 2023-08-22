from odoo import models, fields, api
from datetime import datetime


class AccountMove(models.Model):
    _inherit = "account.move"

    is_factoring = fields.Boolean(string="Is Factoring")

    @api.model
    def create(self, vals):
        res = super(AccountMove, self).create(vals)
        for rec in res:
            if rec.is_factoring:
                res["narration"] = (
                    self.env["ir.config_parameter"].sudo()
                    .get_param("factoring_custom.assignment_clause"))
        return res

    def generate_invoice_debtor(self):
        file1 = open("/home/odoo/Desktop/test/new_text.txt", "a+")
        all_account_records = self.search([("move_type", "=", "out_invoice")])
        for rec in all_account_records:
            transaction_code = 1
            client_no = "{:04d}".format(1195)
            customer_id = "{:09d}".format(rec.partner_id.id) if rec.partner_id else "         "
            credit_note_no = "{:8s}".format(rec.name) if rec.name else "        "
            credit_note_date = (
                "{:6d}".format(
                    int(datetime.strptime(str(rec.invoice_date), "%Y-%m-%d").strftime("%y%m%d")))
                if rec.invoice_date
                else "      ")
            due_date = (
                "{:6d}".format(
                    int(datetime.strptime(str(rec.invoice_date), "%Y-%m-%d").strftime("%y%m%d")))
                if rec.invoice_date
                else "      ")
            amount = ("{:08.3f}".format(rec.amount_total_signed)
                if rec.amount_total_signed
                else "           ")
            discount_terms = "03011"

            file1.write(
                f"{transaction_code}{client_no}{customer_id}{credit_note_no}{credit_note_date}{due_date}"
                f"{amount}{discount_terms}" + "\r\n"
            )
