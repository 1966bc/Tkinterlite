# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# project:  Tkinterlite
# authors:  Giuseppe Costanzi (1966bc)
# licence:  GPL-3.0-or-later, see LICENSE
# -----------------------------------------------------------------------------
"""One supplier: added, or edited."""

import tkinter as tk

from ui.base import Dialog


class UI(Dialog):
    NAME = "supplier"
    TABLE = "suppliers"

    def init_fields(self):

        self.company = tk.StringVar()

        self.add_field("Company:", self.engine.tools.get_entry(self.frm_fields, self.company))

    def set_values(self, row):

        self.company.set(row["company"])

    def get_values(self):

        return {"company": self.company.get()}
