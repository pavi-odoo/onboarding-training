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
                    self.env["ir.config_parameter"]
                    .sudo()
                    .get_param("factoring_custom.assignment_clause")
                )
        return res

    def generate_debtor_file(self):
        debtor_file = open("/home/odoo/Desktop/test/kunde.sgf", "a+")
        debtor_records = self.search([("move_type", "=", "out_invoice")])
        for rec in debtor_records:
            transaction_code = "{}".format("K")
            version_number = "{:04d}".format(9409)
            client_number = "{:04d}".format(1195)
            debtor_number = (
                "{:09d}".format(rec.partner_id.ref) if rec.partner_id.ref else " " * 9
            )
            org_no = (
                "{:11d}".format(rec.partner_id.company_id.l10n_no_bronnoysund_number)
                if (rec.partner_id.company_id.l10n_no_bronnoysund_number)
                else " " * 11
            )
            last_name = (
                f"{rec.partner_id.name}".rjust(35) if rec.partner_id else " " * 35
            )
            first_name = " " * 20
            postal_address = (
                f"{rec.partner_id.street}".rjust(30)
                if rec.partner_id.street
                else " " * 30
            )
            zipcode = (
                f"{rec.partner_id.zip}".rjust(4) if rec.partner_id.zip else "0" * 4
            )
            city = (
                f"{rec.partner_id.city}".rjust(23) if rec.partner_id.city else " " * 23
            )
            reference = " " * 20
            phone_number = (
                f"{rec.partner_id.phone}".rjust(12)
                if rec.partner_id.phone
                else " " * 12
            )
            country = "Norge"
            country_code_alpha = "NO"
            country_code_number = 578
            bank_acc_no = "{:11d}".format(0)
            seller_debtor_no = "{:4d}".format(0)
            foreign_exchange_code = "NOK"

            debtor_file.write(
                f"{transaction_code}{version_number}{client_number}{debtor_number}{org_no}{last_name}"
                f"{first_name}{postal_address}{zipcode}{city}{reference}{phone_number}{country}"
                f"{country_code_alpha}{country_code_number}{bank_acc_no}{seller_debtor_no}"
                f"{foreign_exchange_code}" + "\r\n"
            )

    def generate_invoice_file(self):
        invoice_file = open("/home/odoo/Desktop/test/faktura.sgf", "a+")
        invoice_records = self.search([("move_type", "=", "out_invoice")])
        for rec in invoice_records:
            transaction_code = 1
            client_no = "{:04d}".format(1195)
            customer_id = (
                "{:09d}".format(rec.partner_id.id) if rec.partner_id else " " * 9
            )
            credit_note_no = f"{rec.name}".rjust(8) if rec.name else " " * 8
            credit_note_date = (
                "{:6d}".format(
                    int(
                        datetime.strptime(str(rec.invoice_date), "%Y-%m-%d").strftime(
                            "%y%m%d"
                        )
                    )
                )
                if rec.invoice_date
                else " " * 6
            )
            due_date = (
                "{:6d}".format(
                    int(
                        datetime.strptime(str(rec.invoice_date), "%Y-%m-%d").strftime(
                            "%y%m%d"
                        )
                    )
                )
                if rec.invoice_date
                else " " * 6
            )
            amount = (
                "{:08.3f}".format(rec.amount_total_signed)
                if rec.amount_total_signed
                else "0" * 11
            )
            discount_terms = f"{rec.invoice_payment_term_id.line_ids.months}".rjust(3)+{}

            invoice_file.write(
                f"{transaction_code}{client_no}{customer_id}{credit_note_no}{credit_note_date}{due_date}"
                f"{amount}{discount_terms}" + "\r\n"
            )

    def _cron_file_generator(self):
        self.generate_invoice_file()
        self.generate_debtor_file()
