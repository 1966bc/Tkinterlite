# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# project:  Tkinterlite
# authors:  Giuseppe Costanzi (1966bc)
# licence:  GPL-3.0-or-later, see LICENSE
# -----------------------------------------------------------------------------
"""A list of the rows of one table, with Add, Edit and Close.

categories and suppliers were the same list written twice. What they share
lives here; each module says only which table, which column, which dialog.

This is inheritance used where it belongs: a list of categories *is a* list
window. Compare Engine, which is not a database but has one (ARCHITECTURE.md).
"""

import tkinter as tk
from tkinter import messagebox
from tkinter import ttk


class ListWindow(tk.Toplevel):
    """The rows of one table in a list, with Add, Edit and Close.

    A subclass names three things:

        TABLE    the table, which is also the name of its event
        CAPTION  the column shown in the list, and the order
        DIALOG   the dialog class that adds or edits one row
    """

    TABLE = None
    CAPTION = None
    DIALOG = None

    def __init__(self, parent):
        super().__init__(name=self.TABLE)

        self.parent = parent
        self.engine = parent.engine
        self.attributes("-topmost", True)
        self.protocol("WM_DELETE_WINDOW", self.on_cancel)
        self.items = tk.StringVar()
        #: Position in the list -> primary key, filled by set_values.
        self.dict_items = {}
        self.dialog = None
        self.init_ui()
        self.engine.tools.center_me(self)
        # Told when a row of this table is saved, here or anywhere else.
        self.engine.events.subscribe(self.TABLE, self.on_changed)

    def init_ui(self):

        frm_main = ttk.Frame(self, style="App.TFrame", padding=8)

        frm_list = ttk.Frame(frm_main, style="App.TFrame")
        ttk.Label(frm_list, style="App.TLabel", textvariable=self.items).pack(fill=tk.X)
        self.lst_items = self.engine.tools.get_listbox(frm_list)
        self.lst_items.bind("<Double-Button-1>", self.on_edit)

        buttons = self.engine.tools.get_button_column(frm_main,
                                                      (("Add", self.on_add),
                                                       ("Edit", self.on_edit),
                                                       ("Close", self.on_cancel)),
                                                      window=self)

        frm_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        buttons.pack(side=tk.RIGHT, fill=tk.Y)
        frm_main.pack(fill=tk.BOTH, expand=1)

    def on_open(self):

        self.title(self.TABLE.title())
        self.set_values()

    def set_values(self):
        """Read the list again: every row, disabled ones in grey."""
        key = self.engine.db.get_primary_key(self.TABLE)
        sql = "SELECT * FROM {0} ORDER BY {1} ASC;".format(self.TABLE, self.CAPTION)
        rs = self.engine.db.read(True, sql, ())

        self.dict_items.clear()
        captions = []
        enabled = []
        for index, row in enumerate(rs):
            self.dict_items[index] = row[key]
            captions.append(row[self.CAPTION])
            enabled.append(row["enable"])

        self.engine.tools.set_list(self.lst_items, captions, enabled)
        self.engine.tools.set_count(self.items, len(rs))

    def on_changed(self, row_id):
        """A row was saved: read the list again and land on it."""
        self.set_values()
        self.engine.tools.set_list_id(self.lst_items, self.dict_items, row_id)
        self.lst_items.focus_set()

    def on_add(self, evt=None):

        self.dialog = self.DIALOG(self)
        self.dialog.on_open()

    def on_edit(self, evt=None):

        row_id = self.engine.tools.get_list_id(self.lst_items, self.dict_items)

        if row_id is not None:
            self.dialog = self.DIALOG(self, row_id)
            self.dialog.on_open()
        else:
            messagebox.showwarning(self.nametowidget(".").title(),
                                   self.engine.no_selected,
                                   parent=self)

    def on_cancel(self, evt=None):

        self.engine.events.unsubscribe(self.TABLE, self.on_changed)
        if self.dialog is not None and self.dialog.winfo_exists():
            self.dialog.destroy()
        self.destroy()
