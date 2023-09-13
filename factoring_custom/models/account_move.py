import base64
from io import StringIO
from odoo import models, fields, api, Command
from datetime import datetime
from odoo.exceptions import ValidationError


class AccountMove(models.Model):
    _inherit = "account.move"

    is_factoring = fields.Boolean(string="Is Factoring")
    is_added_invoice = fields.Boolean(string="Is added in invoice file")
    is_added_debtor = fields.Boolean(string="Is added in debtor file")

    def create(self, vals):
        """
        if is_factoring enable narration automatic appear from
        res_setting.
        """
        res = super(AccountMove, self).create(vals)
        config_parameter = self.env["ir.config_parameter"]
        for rec in res:
            res["narration"] = (rec.is_factoring and config_parameter.sudo()
                                .get_param("factoring_custom.assignment_clause") or " ")
        return res

    def append_data_in_file(self, attachment_file, read_file_data):
        """
        it will append the data after existing data in both debtor
        and invoice files.
        """
        existing_data = base64.b64decode(attachment_file.datas).decode()
        new_data = existing_data + read_file_data
        encoded_new_data = base64.b64encode(new_data.encode()).decode()
        attachment_file.write({"datas": encoded_new_data})

    def account_record_filter(self, field_value):
        account_move_records = self.env["account.move"]
        domain = [("move_type", "in", ["out_invoice"])]
        company_ids = "allowed_company_ids" in self._context.keys() and self._context.get("allowed_company_ids") or [
            self.env.user.company_id.id]
        domain.append(field_value)
        domain.append(("company_id", "in", company_ids))
        records = account_move_records.search(domain=domain)
        return records

    def generate_debtor_file(self, file):
        '''
        it generates debtor file with the help of StringIO(buffer file)
        based on current company.
        '''
        attachment_debtor_file = file
        debtor_file = StringIO()
        field_value = ("is_added_debtor", "=", False)
        records = self.account_record_filter(field_value=field_value)
        debtor_records = records
        if debtor_records:
            for rec in debtor_records:
                rec.is_added_debtor = True
                line = ""
                transaction_code = "K"
                line += transaction_code
                version_number = "9409"
                line += version_number
                client_number = "1195"
                line += client_number
                debtor_number = (
                    f"{rec.partner_id.ref}".rjust(9, "0")[0:9]
                    if rec.partner_id.ref else "0" * 9)
                line += debtor_number
                org_no = (f"{rec.partner_id.company_id.l10n_no_bronnoysund_number}".rjust(11, "0")[0:11]
                          if rec.partner_id.company_id.l10n_no_bronnoysund_number else "0" * 11)
                line += org_no
                last_name = (f"{rec.partner_id.name}".rjust(35, " ")[0:35]
                             if rec.partner_id else " " * 35)
                line += last_name
                first_name = " " * 20
                line += first_name
                postal_address = (f"{rec.partner_id.street}".rjust(30, " ")[0:30]
                                  if rec.partner_id.street else " " * 30)
                line += postal_address
                zipcode = (f"{rec.partner_id.zip}".rjust(4, "0")[0:4]
                           if rec.partner_id.zip else "0" * 4)
                line += zipcode
                city = (f"{rec.partner_id.city}".rjust(23, " ")[0:23]
                        if rec.partner_id.city else " " * 23)
                line += city
                reference = " " * 20
                line += reference
                phone_number = (f"{rec.partner_id.phone}".rjust(12, " ")[0:12]
                                if rec.partner_id.phone else " " * 12)
                line += phone_number
                country = "Norge".rjust(20, " ")
                line += country
                country_code_alpha = "NO"
                line += country_code_alpha
                country_code_number = "578"
                line += country_code_number
                bank_acc_no = "0" * 11
                line += bank_acc_no
                seller_debtor_no = "0" * 4
                line += seller_debtor_no
                foreign_exchange_code = "NOK"
                name_2 = " " * 35
                line += name_2
                line += foreign_exchange_code
                debtor_file.write(line + "\r\n")

        debtor_file.seek(0)
        read_debtor_file_data = debtor_file.read()
        if attachment_debtor_file.datas:
            self.append_data_in_file(attachment_debtor_file, read_debtor_file_data)
        else:
            encoded_data = base64.b64encode(read_debtor_file_data.encode()).decode()
            values = {"datas": encoded_data}
            attachment_debtor_file.write(values)

    def generate_invoice_file(self, file):
        """
        it generates invoice file with the help of StringIO(buffer file)
        based on current company.
        """
        attachment_invoice_file = file
        invoice_file = StringIO()
        field_value = ("is_added_invoice", "=", False)
        records = self.account_record_filter(field_value=field_value)
        invoice_records = records
        for rec in invoice_records:
            rec.is_added_invoice = True
            line = ""
            transaction_code = "1" if rec.move_type == "out_invoice" else "9"
            line += transaction_code
            client_no = "1195"
            line += client_no
            customer_id = (str(rec.partner_id.ref).rjust(9, "0")[0:9]
                           if rec.partner_id.ref else "0" * 9)
            line += customer_id
            credit_note_no = rec.name[-8:] if rec.name else " " * 8
            line += credit_note_no
            credit_note_date = (
                f"{datetime.strptime(str(rec.invoice_date), '%Y-%m-%d').strftime('%y%m%d')}".rjust(
                    6, "0") if rec.invoice_date else "0" * 6)
            line += credit_note_date
            due_date = (f"{datetime.strptime(str(rec.invoice_date), '%Y-%m-%d').strftime('%y%m%d')}".rjust(
                6, "0") if rec.invoice_date else "0" * 6)
            line += due_date
            amount = (str(round(rec.amount_total_signed)).rjust(11, "0")
                      if rec.amount_total_signed else "0" * 11)
            line += amount
            discount_terms = f"{rec.invoice_payment_term_id.line_ids.months}".rjust(3, "0") + (
                str(round(rec.invoice_payment_term_id.line_ids.discount_percentage))
                if rec.invoice_payment_term_id.line_ids.discount_percentage else "0" * 2)
            line += discount_terms
            invoice_file.write(line + "\r\n")

        invoice_file.seek(0)
        read_invoice_file_data = invoice_file.read()
        if attachment_invoice_file.datas:
            self.append_data_in_file(attachment_invoice_file, read_invoice_file_data)
        else:
            encoded_data = base64.b64encode(read_invoice_file_data.encode()).decode()
            values = {"datas": encoded_data}
            attachment_invoice_file.write(values)

    def _cron_file_generator(self):
        self.generate_files()

    def create_file_vals(self, factoring_folder):
        """
        create attachments in folder and documents.
        for invoice==> faktura.sgf
        for debtor==> kunde.sgf
        """
        documents = self.env['documents.document']
        attachments = self.env['ir.attachment']
        debtor = attachments.create({
            "name": "kunde.sgf",
            "store_fname": "kunde.sgf",
            "type": "binary"
        })

        invoice = attachments.create({
            "name": "faktura.sgf",
            "store_fname": "faktura.sgf",
            "type": "binary"
        })
        files = documents.create(
            [{
                "folder_id": factoring_folder.id,
                "attachment_id": invoice.id
            }, {
                "folder_id": factoring_folder.id,
                "attachment_id": debtor.id
            }])

        return [rec for rec in files]

    def generate_files(self):
        """
        Check documents and folder. If not exist due to some uncertain behaviour
        it will generate and only append datas in existing files.
        """
        try:
            factoring_folder = self.env.ref('factoring_custom.documents_factoring_folder').document_ids
            if not factoring_folder.document_ids:
                self.create_file_vals(factoring_folder)

            debtor_file = factoring_folder.filtered(lambda file: file.name == 'kunde.sgf')
            invoice_file = factoring_folder.filtered(lambda file: file.name == 'faktura.sgf')
            if debtor_file:
                self.generate_debtor_file(debtor_file)
            if invoice_file:
                self.generate_invoice_file(invoice_file)

            else:
                if debtor_file:
                    self.generate_debtor_file(debtor_file)

                if invoice_file:
                    self.generate_invoice_file(invoice_file)

        except:
            ValidationError("Files kunde.sgf and faktura.sgf are not found.")
