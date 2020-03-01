#-----------------------------------------------------------------------------
# project:  tkinterlite
# authors:  1966bc
# mailto:   [giuseppe.costanzi@gmail.com]
# modify:   2020-03-01
#-----------------------------------------------------------------------------
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import frames.supplier as ui

class UI(tk.Toplevel):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(name="suppliers")

        self.attributes("-topmost", True)
        self.parent = parent
        self.engine = kwargs["engine"]
        self.table = "suppliers"
        self.field = "supplier_id"
        self.obj = None
        self.init_ui()
        self.engine.center_me(self)

    def init_ui(self):

        f0 = self.engine.get_frame(self, 8)
        f1 = ttk.Frame(f0,)
        self.lstItems = self.engine.get_listbox(f1, width=40)
        self.lstItems.bind("<<ListboxSelect>>", self.on_item_selected)
        self.lstItems.bind("<Double-Button-1>", self.on_item_activated)
        f1.pack(side=tk.LEFT, fill=tk.BOTH, padx=5, pady=5, expand=1)
        self.engine.get_add_edit_cancel(self, f0)
        f0.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

    def on_open(self,):

        sql = "SELECT * FROM suppliers"
        rs = self.engine.read(True, sql, ())
        index = 0
        self.dict_items = {}

        if rs:
            self.lstItems.delete(0, tk.END)

            for i in rs:
                self.lstItems.insert(tk.END, i[1])

                if i[2] != 1:
                    self.lstItems.itemconfig(index, {"bg":"light gray"})

                self.dict_items[index] = i[0]
                index += 1

        self.title("Suppliers")

    def on_add(self, evt):

        self.obj = ui.UI(self,
                         engine=self.engine,
                         table=self.table,
                         field=self.field,
                         index=None)
        self.obj.on_open()


    def on_edit(self, evt):
        self.on_item_activated()


    def on_item_activated(self, evt=None):

        if self.lstItems.curselection():
            index = self.lstItems.curselection()[0]
            self.obj = ui.UI(self,
                             engine=self.engine,
                             table=self.table,
                             field=self.field,
                             index=index)
            self.obj.on_open(self.selected_item,)

        else:
            messagebox.showwarning(self.master.title(),
                                   self.engine.no_selected,
                                   parent=self)


    def on_item_selected(self, evt):

        if self.lstItems.curselection():
            index = self.lstItems.curselection()[0]
            pk = self.dict_items.get(index)
            self.selected_item = self.engine.get_selected(self.table,
                                                          self.field,
                                                          pk)

    def on_cancel(self, evt=None):

        if self.obj is not None:
            self.obj.destroy()
        self.destroy()
