# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# project:  Tkinterlite
# authors:  Giuseppe Costanzi (1966bc)
# licence:  GPL-3.0-or-later, see LICENSE
# -----------------------------------------------------------------------------
"""A form for one row of one table: added, or edited.

category, supplier and product were the same dialog written three times. What
they share lives here; each module says only which table and which fields.

Inheritance where it belongs: a category form *is a* dialog.
"""

import tkinter as tk
from tkinter import messagebox
from tkinter import ttk


class Dialog(tk.Toplevel):
    """One row of one table: added, or edited.

    A subclass names the window and the table, and fills in three methods:

        init_fields()    the fields, each one placed with add_field()
        set_values(row)  a row read from the database into the fields
        get_values()     the fields as {column: value}

    The enable check box, the buttons, reading the row, saving it and
    telling the other windows are done here, once.
    """

    NAME = None
    TABLE = None

    def __init__(self, parent, row_id=None):
        super().__init__(name=self.NAME)

        self.parent = parent
        self.engine = parent.engine
        #: The row being edited, None for a new one. The row itself is read
        #: from the database when the window opens, never taken from a copy
        #: held by the list: a copy is what showed the old values.
        self.row_id = row_id
        self.enable = tk.BooleanVar()
        self.first_field = None
        self.next_row = 0
        self.transient(parent)
        self.resizable(0, 0)
        self.protocol("WM_DELETE_WINDOW", self.on_cancel)
        self.init_ui()
        self.engine.tools.center_me(self)

    def init_ui(self):

        self.frm_main = ttk.Frame(self, style="App.TFrame", padding=8)
        self.frm_fields = ttk.Frame(self.frm_main, style="App.TFrame")

        self.init_fields()
        chk_enable = ttk.Checkbutton(self.frm_fields, style="App.TCheckbutton",
                                     onvalue=1, offvalue=0, variable=self.enable)
        self.add_field("Enable:", chk_enable, tk.W)

        buttons = self.engine.tools.get_button_column(self.frm_main,
                                                      self.get_buttons(),
                                                      window=self)

        self.frm_fields.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        buttons.pack(side=tk.RIGHT, fill=tk.Y, padx=(8, 0))
        self.frm_main.pack(fill=tk.BOTH, expand=1)

    def add_field(self, label, widget, sticky=tk.EW):
        """Put a label and its field on the next row of the form."""
        ttk.Label(self.frm_fields, style="App.TLabel", text=label).grid(row=self.next_row,
                                                                         column=0,
                                                                         sticky=tk.W)
        widget.grid(row=self.next_row, column=1, sticky=sticky, padx=5, pady=5)

        if self.first_field is None:
            self.first_field = widget
        self.next_row += 1

    def get_buttons(self):
        """The buttons, as (label, command); a subclass may add its own."""
        return (("Save", self.on_save), ("Cancel", self.on_cancel))

    def on_open(self):

        if self.row_id is not None:
            self.title("Edit {0}".format(self.NAME.title()))
            row = self.get_row()
            self.set_values(row)
            self.enable.set(row["enable"])
        else:
            self.title("Add {0}".format(self.NAME.title()))
            self.enable.set(1)

        self.first_field.focus()

    def get_row(self):
        """The row being edited, read now from the database."""
        key = self.engine.db.get_primary_key(self.TABLE)
        return self.engine.db.get_selected(self.TABLE, key, self.row_id)

    def on_save(self, evt=None):

        if self.engine.tools.on_fields_control(self.frm_fields, self.nametowidget(".").title()):
            if messagebox.askyesno(self.nametowidget(".").title(),
                                   self.engine.ask_to_save,
                                   parent=self):
                self.save()
            else:
                messagebox.showinfo(self.nametowidget(".").title(),
                                    self.engine.abort,
                                    parent=self)

    def save(self):
        """Write the row, close, and tell whoever shows this table which row.

        The id of the saved row is known two ways: an INSERT returns the id
        it made, an UPDATE had it before the window opened. lastrowid after
        an UPDATE still holds the last row inserted on the connection, a
        plausible number that belongs to something else.
        """
        values = self.get_values()
        values["enable"] = self.enable.get()

        if self.row_id is not None:
            sql, args = self.engine.db.get_update(self.TABLE, self.row_id, values)
            self.engine.db.write(sql, args)
            saved_id = self.row_id
        else:
            sql, args = self.engine.db.get_insert(self.TABLE, values)
            saved_id = self.engine.db.write(sql, args)

        self.on_cancel()
        self.engine.events.notify(self.TABLE, saved_id)

    def on_cancel(self, evt=None):
        self.destroy()

    def init_fields(self):
        raise NotImplementedError("{0} must build its fields".format(self.__class__.__name__))

    def set_values(self, row):
        raise NotImplementedError("{0} must fill its fields".format(self.__class__.__name__))

    def get_values(self):
        raise NotImplementedError("{0} must read its fields".format(self.__class__.__name__))
