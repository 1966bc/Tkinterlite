#!/usr/bin/python3
# -----------------------------------------------------------------------------
# project:  tkinterlite
# authors:  1966bc
# mailto:   [giuseppecostanzi@gmail.com]
# modify:   hiems MMXX
# -----------------------------------------------------------------------------
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import frames.category as ui

SQL = "SELECT * FROM categories ORDER BY category ASC;"


class UI(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(name="categories")

        self.parent = parent
        self.attributes("-topmost", True)
        self.protocol("WM_DELETE_WINDOW", self.on_cancel)
        self.table = "categories"
        self.primary_key = "category_id"
        self.obj = None
        self.init_ui()
        self.master.engine.center_me(self)

    def init_ui(self):

        self.lblFrame = ttk.LabelFrame(self, text="Items",)
        self.lstItems = self.master.engine.get_listbox(self.lblFrame,)
        self.lstItems.bind("<<ListboxSelect>>", self.on_item_selected)
        self.lstItems.bind("<Double-Button-1>", self.on_item_activated)
        self.lblFrame.pack(side=tk.LEFT, fill=tk.BOTH, expand=1, padx=5, pady=5)

        w = ttk.Frame(self, style='W.TFrame', padding=2)

        bts = (("Add", 0, self.on_add, "<Alt-a>"),
               ("Edit", 0, self.on_edit, "<Alt-e>"),
               ("Close", 0, self.on_cancel, "<Alt-c>"))

        for btn in bts:
            ttk.Button(w,
                       text=btn[0],
                       underline=btn[1],
                       command=btn[2],
                       style='W.TButton',).pack(fill=tk.X, padx=5, pady=5)
            self.bind(btn[3], btn[2])

        w.pack(fill=tk.BOTH, expand=1)

    def on_open(self,):

        msg = "{0}".format(self.winfo_name().title())
        self.title(msg)
        self.set_values()

    def set_values(self):

        self.lstItems.delete(0, tk.END)
        index = 0
        self.dict_items = {}

        rs = self.master.engine.read(True, SQL, ())

        if rs:
            self.lstItems.delete(0, tk.END)

            for i in rs:
                s = "{:}".format(i[1])
                self.lstItems.insert(tk.END, s)
                if i[3] != 1:
                    self.lstItems.itemconfig(index, {"bg":"light gray"})
                self.dict_items[index] = i[0]
                index += 1

            msg = ("Items: {0}".format(self.lstItems.size()))
            self.lblFrame['text'] = msg

    def on_add(self, evt=None):

        self.obj = ui.UI(self)
        self.obj.on_open()

    def on_edit(self, evt=None):
        self.on_item_activated()

    def on_item_selected(self, evt=None):

        if self.lstItems.curselection():
            index = self.lstItems.curselection()[0]
            pk = self.dict_items.get(index)
            self.selected_item = self.master.engine.get_selected(self.table,
                                                                 self.primary_key,
                                                                 pk)
            
    def on_item_activated(self, evt=None):

        if self.lstItems.curselection():
            index = self.lstItems.curselection()[0]
            self.obj = ui.UI(self, index)
            self.obj.on_open(self.selected_item,)

        else:
            messagebox.showwarning(self.master.title(),
                                   self.master.engine.no_selected,
                                   parent=self)

    def on_cancel(self, evt=None):
        if self.obj is not None:
            self.obj.destroy()
        self.destroy()
