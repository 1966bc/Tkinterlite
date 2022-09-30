# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# project:  tkinterlite
# authors:  1966bc
# mailto:   [giuseppecostanzi@gmail.com]
# modify:   hiems MMXX
# -----------------------------------------------------------------------------
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import frames.supplier as ui

SQL = "SELECT * FROM suppliers ORDER BY company ASC;"


class UI(tk.Toplevel):
    def __init__(self, parent,):
        super().__init__(name="suppliers")

        self.parent = parent
        self.attributes("-topmost", True)
        self.protocol("WM_DELETE_WINDOW", self.on_cancel)
        self.table = "suppliers"
        self.primary_key = "supplier_id"
        self.counts = tk.IntVar()
        self.obj = None
        self.init_ui()
        self.nametowidget(".").engine.center_me(self)

    def init_ui(self):

        f0 = ttk.Frame(self,
                       style="App.TFrame",
                       relief=tk.RIDGE,
                       borderwidth=2,
                       padding=4)
        
        f1 = ttk.Frame(f0, style="App.TFrame", padding=4)

        ttk.Label(f1, style="App.TLabel", textvariable=self.counts,).pack(fill=tk.X, expand=0)

        sb = ttk.Scrollbar(f1, orient=tk.VERTICAL)
        self.lstItems = tk.Listbox(f1, yscrollcommand=sb.set,)
        self.lstItems.bind("<<ListboxSelect>>", self.on_item_selected)
        self.lstItems.bind("<Double-Button-1>", self.on_item_activated)
        sb.config(command=self.lstItems.yview)
        self.lstItems.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        sb.pack(fill=tk.Y, expand=1)

        f2 = ttk.Frame(f0,
                       style="App.TFrame",
                       relief=tk.RIDGE,
                       borderwidth=0,
                       padding=4)
       
        bts = (("Add", 0, self.on_add, "<Alt-a>"),
               ("Edit", 0, self.on_edit, "<Alt-e>"),
               ("Close", 0, self.on_cancel, "<Alt-c>"))

        for btn in bts:
            ttk.Button(f2,
                       style="App.TButton",
                       text=btn[0],
                       underline=btn[1],
                       command=btn[2],).pack(fill=tk.X, padx=5, pady=5)
            self.bind(btn[3], btn[2])
        
        f0.pack(fill=tk.BOTH, padx=5, pady=5, expand=1)
        f1.pack(side=tk.LEFT, fill=tk.BOTH, padx=5, pady=5, expand=1)
        f2.pack(side=tk.RIGHT, fill=tk.Y, padx=5, pady=5, expand=0)

    def on_open(self,):

        msg = "{0}".format(self.winfo_name().title())
        self.title(msg)
        self.set_values()

    def set_values(self):

        self.lstItems.delete(0, tk.END)
        index = 0
        self.dict_items = {}

        rs = self.nametowidget(".").engine.read(True, SQL, ())

        if rs:
            for i in rs:
                s = "{:}".format(i[1])
                self.lstItems.insert(tk.END, s)
                if i[2] != 1:
                    self.lstItems.itemconfig(index, {"bg": "light gray"})
                self.dict_items[index] = i[0]
                index += 1

            msg = ("Items: {0}".format(self.lstItems.size()))
            self.counts.set(msg)

    def on_add(self, evt=None):

        self.obj = ui.UI(self)
        self.obj.on_open()

    def on_edit(self, evt=None):
        self.on_item_activated()

    def on_item_selected(self, evt=None):

        if self.lstItems.curselection():
            index = self.lstItems.curselection()[0]
            pk = self.dict_items.get(index)
            self.selected_item = self.nametowidget(".").engine.get_selected(self.table,
                                                                            self.primary_key,
                                                                            pk)
    def on_item_activated(self, evt=None):

        if self.lstItems.curselection():
            index = self.lstItems.curselection()[0]
            self.obj = ui.UI(self, index)
            self.obj.on_open(self.selected_item,)

        else:
            messagebox.showwarning(self.nametowidget(".").title(),
                                   self.nametowidget(".").engine.no_selected,
                                   parent=self)

    def on_cancel(self, evt=None):
        if self.obj is not None:
            self.obj.destroy()
        self.destroy()
