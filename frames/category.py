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


class UI(tk.Toplevel):
    def __init__(self, parent, index=None):
        super().__init__(name="category")

        self.parent = parent
        self.index = index
        self.transient(parent)
        self.resizable(0, 0)
        self.category = tk.StringVar()
        self.description = tk.StringVar()
        self.enable = tk.BooleanVar()
        self.init_ui()
        self.nametowidget(".").engine.center_me(self)

    def init_ui(self):

        w = self.nametowidget(".").engine.get_init_ui(self)

        r = 0
        c = 1
        ttk.Label(w, text="Category:",).grid(row=r, sticky=tk.W)
        self.txtCategory = ttk.Entry(w, textvariable=self.category)
        self.txtCategory.grid(row=r, column=c, sticky=tk.W, padx=5, pady=5)

        r += 1
        ttk.Label(w, text="Description:").grid(row=r, sticky=tk.W)
        wdg = ttk.Entry(w, textvariable=self.description)
        wdg.grid(row=r, column=c, sticky=tk.W, padx=5, pady=5)

        r += 1
        ttk.Label(w, text="Enable:").grid(row=r, sticky=tk.W)
        chk = ttk.Checkbutton(w, onvalue=1, offvalue=0, variable=self.enable,)
        chk.grid(row=r, column=c, sticky=tk.W)

        self.nametowidget(".").engine.get_save_cancel_bts(self, w)

    def on_open(self, selected_item=None):

        if self.index is not None:
            self.selected_item = selected_item
            msg = "Edit {0}".format(self.winfo_name().title())
            self.set_values()
        else:
            msg = "Add {0}".format(self.winfo_name().title())
            self.enable.set(1)

        self.title(msg)
        self.txtCategory.focus()

    def set_values(self,):

        self.category.set(self.selected_item[1])
        self.description.set(self.selected_item[2])
        self.enable.set(self.selected_item[3])

    def get_values(self,):

        return [self.category.get(),
                self.description.get(),
                self.enable.get()]

    def on_save(self, evt=None):

        if self.nametowidget(".").engine.on_fields_control(self) == False: return

        if messagebox.askyesno(self.nametowidget(".").title(),
                               self.nametowidget(".").engine.ask_to_save,
                               parent=self) == True:

            args = self.get_values()

            if self.index is not None:

                sql = self.nametowidget(".").engine.get_update_sql(self.parent.table, self.parent.primary_key)

                args.append(self.selected_item[0])

            else:

                sql = self.nametowidget(".").engine.get_insert_sql(self.parent.table, len(args))

            last_id = self.nametowidget(".").engine.write(sql, args)
            self.parent.on_open()

            if self.index is not None:
                self.parent.lstItems.see(self.index)
                self.parent.lstItems.selection_set(self.index)
            else:
                #force focus on listbox
                idx = list(self.parent.dict_items.keys())[list(self.parent.dict_items.values()).index(last_id)]
                self.parent.lstItems.selection_set(idx)
                self.parent.lstItems.see(idx)

            self.on_cancel()

        else:
            messagebox.showinfo(self.nametowidget(".").title(),
                                self.nametowidget(".").engine.abort,
                                parent=self)

    def on_cancel(self, evt=None):
        self.destroy()
