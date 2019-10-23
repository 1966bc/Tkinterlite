#-----------------------------------------------------------------------------
# project:  tkinterlite
# authors:  1966bc
# mailto:   [giuseppe.costanzi@gmail.com]
# modify:   2019-09-22
#-----------------------------------------------------------------------------

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class UI(tk.Toplevel):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(name='category')

        self.attributes('-topmost', True)
        self.transient(parent)
        self.resizable(0, 0)

        self.parent = parent
        self.engine = kwargs['engine']
        self.table = kwargs['table']
        self.field = kwargs['field']
        self.index = kwargs['index']


        self.category = tk.StringVar()
        self.description = tk.StringVar()
        self.enable = tk.BooleanVar()

        self.init_ui()
        self.engine.center_me(self)

    def init_ui(self):

        w = self.engine.get_init_ui(self)

        r = 0
        ttk.Label(w, text="Category:",).grid(row=r, sticky=tk.W)
        self.txtCategory = ttk.Entry(w, textvariable=self.category)
        self.txtCategory.grid(row=r, column=1, sticky=tk.W, padx=5, pady=5)

        r += 1
        ttk.Label(w, text="Description:").grid(row=r, sticky=tk.W)
        self.txtDescription = ttk.Entry(w, textvariable=self.description)
        self.txtDescription.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)

        r += 1
        ttk.Label(w, text="Enable:").grid(row=r, sticky=tk.W)
        chk = ttk.Checkbutton(w, onvalue=1, offvalue=0, variable=self.enable,)
        chk.grid(row=r, column=1, sticky=tk.W)

        self.engine.get_save_cancel(self, w)


    def on_open(self, selected_item=None):

        if self.index is not None:
            self.selected_item = selected_item
            msg = "Update {0}".format(self.winfo_name())
            self.set_values()
        else:
            self.insert_mode = True
            msg = "Insert {0}".format(self.winfo_name())
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

        if self.engine.on_fields_control(self) == False: return

        if messagebox.askyesno(self.master.title(),
                               self.engine.ask_to_save,
                               parent=self) == True:

            args = self.get_values()

            if self.index is not None:

                sql = self.engine.get_update_sql(self.table, self.field)

                args.append(self.selected_item[0])

            else:

                sql = self.engine.get_insert_sql(self.table, len(args))

            self.engine.write(sql, args)
            self.parent.on_open()

            if self.index is not None:
                self.parent.lstItems.see(self.index)
                self.parent.lstItems.selection_set(self.index)

            self.on_cancel()


    def on_cancel(self, evt=None):
        self.destroy()
