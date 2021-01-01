# -*- coding: utf-8 -*-
#-----------------------------------------------------------------------------
# project:  tkinterlite
# authors:  1966bc
# mailto:   [giuseppecostanzi@gmail.com]
# modify:   hiems MMXX
#-------------------------------------------------------------------------------
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class UI(tk.Toplevel):
    def __init__(self, parent, index=None):
        super().__init__(name="supplier")

        self.attributes("-topmost", True)
        self.transient(parent)
        self.resizable(0, 0)
        self.parent = parent
        self.index = index

        self.company = tk.StringVar()
        self.enable = tk.BooleanVar()

        self.init_ui()
        self.master.engine.center_me(self)

    def init_ui(self):

        f = self.master.engine.get_init_ui(self)

        r = 0
        ttk.Label(f, text="Company:",).grid(row=r, sticky=tk.W)
        self.txtCompany = ttk.Entry(f, textvariable=self.company)
        self.txtCompany.grid(row=r, column=1, sticky=tk.W, padx=5, pady=5)

        r += 1
        ttk.Label(f, text="Enable:").grid(row=r, sticky=tk.W)
        w = ttk.Checkbutton(f, onvalue=1, offvalue=0, variable=self.enable,)
        w.grid(row=r, column=1, sticky=tk.W)

        self.master.engine.get_save_cancel(self, f)


    def on_open(self, selected_item=None):

        if self.index is not None:
            self.selected_item = selected_item
            msg = "Edit {0}".format(self.winfo_name().capitalize())
            self.set_values()
        else:
            msg = "Add {0}".format(self.winfo_name().capitalize())
            self.enable.set(1)

        self.title(msg)
        self.txtCompany.focus()

    def set_values(self,):

        self.company.set(self.selected_item[1])
        self.enable.set(self.selected_item[2])

    def get_values(self,):

        return [self.company.get(),
                self.enable.get()]

    def on_save(self, evt=None):

        if self.master.engine.on_fields_control(self) == False: return

        if messagebox.askyesno(self.master.title(),
                               self.master.engine.ask_to_save,
                               parent=self) == True:

            args = self.get_values()

            if self.index is not None:

                sql = self.master.engine.get_update_sql(self.parent.table, self.parent.field)

                args.append(self.selected_item[0])

            else:

                sql = self.engine.get_insert_sql(self.parent.table, len(args))

            last_id = self.master.engine.write(sql, args)
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

    def on_cancel(self, evt=None):
        self.destroy()
