# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# project:  Tkinterlite
# authors:  Giuseppe Costanzi (1966bc)
# licence:  GPL-3.0-or-later, see LICENSE
# -----------------------------------------------------------------------------
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox


class UI(tk.Toplevel):
    def __init__(self, parent, row_id=None):
        super().__init__(name="category")

        self.parent = parent
        self.engine = parent.engine
        #: The category being edited, None for a new one. The row itself is
        #: read from the database when the window opens, never taken from a
        #: copy held by the list: a copy is what showed the old values.
        self.row_id = row_id
        self.transient(parent)
        self.resizable(0, 0)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=2)
        self.columnconfigure(2, weight=1)
        
        self.category = tk.StringVar()
        self.description = tk.StringVar()
        self.enable = tk.BooleanVar()

        self.init_ui()
        self.engine.tools.center_me(self)

    def init_ui(self):

        paddings = {"padx": 5, "pady": 5}
        
        self.frm_main = ttk.Frame(self, style="App.TFrame")
        self.frm_main.grid(row=0, column=0)

        frm_left = ttk.Frame(self.frm_main, style="App.TFrame")
        frm_left.grid(row=0, column=0, sticky=tk.NS, **paddings)

        r = 0
        c = 1
        ttk.Label(frm_left, style="App.TLabel", text="Category:",).grid(row=r, sticky=tk.W)
        self.txtCategory = ttk.Entry(frm_left, textvariable=self.category)
        self.txtCategory.grid(row=r, column=c, sticky=tk.EW, **paddings)

        r += 1
        ttk.Label(frm_left, style="App.TLabel", text="Description:").grid(row=r, sticky=tk.W)
        ent_description = ttk.Entry(frm_left, textvariable=self.description)
        ent_description.grid(row=r, column=c, sticky=tk.EW, **paddings)

        r += 1
        ttk.Label(frm_left, style="App.TLabel", text="Enable:").grid(row=r, sticky=tk.W)
        chk_enable = ttk.Checkbutton(frm_left, onvalue=1, offvalue=0, variable=self.enable,)
        chk_enable.grid(row=r, column=c, sticky=tk.W)

        frm_right = ttk.Frame(self.frm_main, style="App.TFrame")
        frm_right.grid(row=0, column=1, sticky=tk.NS, **paddings)

        r = 0
        c = 0
        btn_save = ttk.Button(frm_right, style="App.TButton", text="Save", underline=0, command=self.on_save,)
        self.bind("<Alt-s>", self.on_save)
        btn_save.grid(row=r, column=c, sticky=tk.EW, **paddings)

        r += 1
        btn_cancel = ttk.Button(frm_right, style="App.TButton", text="Cancel", underline=0, command=self.on_cancel)
        self.bind("<Alt-c>", self.on_cancel)
        btn_cancel.grid(row=r, column=c, sticky=tk.EW, **paddings)

    def on_open(self):

        if self.row_id is not None:
            msg = "Edit {0}".format(self.winfo_name().title())
            self.set_values()
        else:
            msg = "Add {0}".format(self.winfo_name().title())
            self.enable.set(1)

        self.title(msg)
        self.txtCategory.focus()

    def set_values(self,):

        row = self.engine.db.get_selected(self.parent.table, self.parent.primary_key, self.row_id)
        self.category.set(row["category"])
        self.description.set(row["description"])
        self.enable.set(row["enable"])

    def get_values(self,):

        return {"category": self.category.get(),
                "description": self.description.get(),
                "enable": self.enable.get()}

    def on_save(self, evt=None):

        if self.engine.tools.on_fields_control(self.frm_main, self.nametowidget(".").title()):
            if messagebox.askyesno(self.nametowidget(".").title(),
                                   self.engine.ask_to_save,
                                   parent=self):
                self.save()
            else:
                messagebox.showinfo(self.nametowidget(".").title(),
                                    self.engine.abort,
                                    parent=self)

    def save(self):
        """Write the row, close, and tell whoever shows categories which one.

        The id of the saved row is known two ways: an INSERT returns the id
        it made, an UPDATE had it before the window opened. lastrowid after
        an UPDATE still holds the last row inserted on the connection, a
        plausible number that belongs to something else.
        """
        values = self.get_values()

        if self.row_id is not None:
            sql, args = self.engine.db.get_update(self.parent.table, self.row_id, values)
            self.engine.db.write(sql, args)
            saved_id = self.row_id
        else:
            sql, args = self.engine.db.get_insert(self.parent.table, values)
            saved_id = self.engine.db.write(sql, args)

        self.on_cancel()
        self.engine.events.notify("categories", saved_id)

    def on_cancel(self, evt=None):
        self.destroy()
