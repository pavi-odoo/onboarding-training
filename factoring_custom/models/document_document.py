from odoo import fields, models, api


class YourModule(models.Model):
    _inherit = "documents.document"

    def _create_initial_folder_and_files(self):
        # Create the folder
        folder = self.create(
            {
                "name": "viren",
                "res_model": "documents.document",
            }
        )

        # Create files within the folder
        self.create(
            {
                "name": "a.txt",
                "datas": b"Contents of a.txt",
                "res_id": folder.id,
                "res_model": "documents.document",
            }
        )

        self.create(
            {
                "name": "b.txt",
                "datas": b"Contents of b.txt",
                "res_id": folder.id,
                "res_model": "documents.document",
            }
        )
