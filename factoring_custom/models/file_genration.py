import os
import codecs
from odoo import models, fields, api


class CustomFileGeneration(models.Model):
    _name = "custom.file.generation"
    _description = "Custom File Generation"

    name = fields.Char(string="Name")
    # Add other fields based on the provided fields

    @api.model
    def generate_files(self):
        # Retrieve data for invoice and debtor files
        invoice_data = self.env["custom.file.generation"].search([])
        debtor_data = self.env["custom.file.generation"].search([])

        # Generate invoice file
        with codecs.open("faktura.sgf", "w", "utf-16") as invoice_file:
            for data in invoice_data:
                # Format the data according to the provided rules
                line = f"{data.name}{data.field1:0>5}{data.field2:0>4}..."  # Format as needed
                invoice_file.write(line + "\r\n")

        # Generate debtor file
        with codecs.open("kunde.sgf", "w", "utf-16") as debtor_file:
            for data in debtor_data:
                # Format the data according to the provided rules
                line = (
                    f"{data.name} {data.field3} {data.field4} ..."  # Format as needed
                )
                debtor_file.write(line + "\r\n")
