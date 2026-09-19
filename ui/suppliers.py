# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# project:  tkinterlite
# authors:  1966bc
# mailto:   [giuseppecostanzi@gmail.com]
# modify:   hiems MMXXI
# -----------------------------------------------------------------------------
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import ui.supplier

SQL = "SELECT * FROM suppliers ORDER BY company ASC;"


class UI(tk.Toplevel):
    def __init__(self, parent,):
        super().__init__(name="suppliers")

        self.parent = parent
        self.engine = parent.engine
        self.attributes("-topmost", True)
        self.protocol("WM_DELETE_WINDOW", self.on_cancel)
        self.table = "suppliers"
        self.primary_key = "supplier_id"
        self.items = tk.StringVar()
        #: Position in the list -> supplier_id, filled by set_values.
        self.dict_items = {}
        self.obj = None
        self.init_ui()
        self.engine.tools.center_me(self)
        # Told when a supplier is saved, here or anywhere else.
        self.engine.events.subscribe("suppliers", self.on_changed)

    def init_ui(self):

        frm_main = ttk.Frame(self, style="App.TFrame")
        
        frm_left = ttk.Frame(frm_main, style="App.TFrame", padding=8)

        ttk.Label(frm_left, style="App.TLabel", textvariable=self.items,).pack(fill=tk.X, expand=0)

        self.lstItems = self.engine.tools.get_listbox(frm_left)
        self.lstItems.bind("<Double-Button-1>", self.on_item_activated)

        frm_right = ttk.Frame(frm_main, style="App.TFrame", padding=4)
       
        bts = (("Add", 0, self.on_add, "<Alt-a>"),
               ("Edit", 0, self.on_item_activated, "<Alt-e>"),
               ("Close", 0, self.on_cancel, "<Alt-c>"))

        for btn in bts:
            ttk.Button(frm_right,
                       style="App.TButton",
                       text=btn[0],
                       underline=btn[1],
                       command=btn[2],).pack(fill=tk.X, padx=5, pady=5)
            self.bind(btn[3], btn[2])
        
        frm_main.pack(fill=tk.BOTH, expand=1)
        frm_left.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        frm_right.pack(side=tk.RIGHT, fill=tk.Y, expand=0)

    def on_open(self,):

        msg = "{0}".format(self.winfo_name().title())
        self.title(msg)
        self.set_values()

    def set_values(self):
        """Read the list again, through the helpers of tools.py."""
        rs = self.engine.db.read(True, SQL, ())

        self.dict_items.clear()
        captions = []
        enabled = []
        for index, row in enumerate(rs):
            self.dict_items[index] = row["supplier_id"]
            captions.append(row["company"])
            enabled.append(row["enable"])

        self.engine.tools.set_list(self.lstItems, captions, enabled)
        self.engine.tools.set_count(self.items, len(rs))

    def on_changed(self, supplier_id):
        """A supplier was saved: read the list again and land on it."""
        self.set_values()
        self.engine.tools.set_list_id(self.lstItems, self.dict_items, supplier_id)
        self.lstItems.focus_set()

    def on_add(self, evt=None):

        self.obj = ui.supplier.UI(self)
        self.obj.on_open()

    def on_item_activated(self, evt=None):

        supplier_id = self.engine.tools.get_list_id(self.lstItems, self.dict_items)

        if supplier_id is not None:
            self.obj = ui.supplier.UI(self, supplier_id)
            self.obj.on_open()
        else:
            messagebox.showwarning(self.nametowidget(".").title(),
                                   self.engine.no_selected,
                                   parent=self)

    def on_cancel(self, evt=None):
        self.engine.events.unsubscribe("suppliers", self.on_changed)
        if self.obj is not None:
            self.obj.destroy()
        self.destroy()
