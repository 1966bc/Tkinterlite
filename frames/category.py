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

        paddings = {"padx": 5, "pady": 5}

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=2)
        self.columnconfigure(2, weight=1)
        
        self.frm_main = ttk.Frame(self)
        self.frm_main.grid(row=0, column=0)

        frm_left = ttk.Frame(self.frm_main)
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

        frm_right = ttk.Frame(self.frm_main)
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

        if self.index is not None:
            msg = "Edit {0}".format(self.winfo_name().title())
            self.set_values()
        else:
            msg = "Add {0}".format(self.winfo_name().title())
            self.enable.set(1)

        self.title(msg)
        self.txtCategory.focus()

    def set_values(self,):

        self.category.set(self.parent.selected_item[1])
        self.description.set(self.parent.selected_item[2])
        self.enable.set(self.parent.selected_item[3])

    def get_values(self,):

        return [self.category.get(),
                self.description.get(),
                self.enable.get()]

    def on_save(self, evt=None):

        if self.nametowidget(".").engine.on_fields_control(self.frm_main, self.nametowidget(".").title()) == False: return

        if messagebox.askyesno(self.nametowidget(".").title(),
                               self.nametowidget(".").engine.ask_to_save,
                               parent=self) == True:

            args = self.get_values()

            if self.index is not None:

                sql = self.nametowidget(".").engine.get_update_sql(self.parent.table, self.parent.primary_key)

                args.append(self.parent.selected_item[0])

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
