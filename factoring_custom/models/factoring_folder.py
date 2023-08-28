from odoo import fields, models, api


class FactoringDocument(models.Model):
    _name = "factoring.document"

    name = fields.Char()

    def _cron_factoring_folder(self):
        vals = {"name": "Factoring folder"}
        context_dict = {}
        context_dict["hello"] = "hello"
        self.env["documents.folder"].create(vals).with_context(context_dict)
