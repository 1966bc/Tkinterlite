#!/usr/bin/python3
#-----------------------------------------------------------------------------
# project:  tkinterlite
# authors:  1966bc
# mailto:   [giuseppe.costanzi@gmail.com]
# modify:   2018-12-23
# version:  0.2                                                                 
#-----------------------------------------------------------------------------
import tkinter as tk
from tkinter import messagebox

import frames.supplier

class Dialog(tk.Toplevel):     
    def __init__(self,parent,engine,):
        super().__init__(name='suppliers')

        self.transient(parent)
        self.resizable(0,0)
        self.parent = parent
        self.engine = engine
        self.obj = None
        self.center_me()
        self.init_ui()

    def center_me(self):

        #center window
        x = (self.master.winfo_screenwidth() - self.master.winfo_reqwidth()) / 2
        y = (self.master.winfo_screenheight() - self.master.winfo_reqheight()) / 2
        self.master.geometry("+%d+%d" % (x, y))
        
    def init_ui(self):

        f0 = self.engine.get_frame(self)
        f1 = tk.Frame(f0,)
        self.lstItems = self.engine.get_listbox(f1,width=40)
        self.lstItems.bind("<<ListboxSelect>>", self.on_item_selected)
        self.lstItems.bind("<Double-Button-1>", self.on_item_activated)
        f1.pack(side=tk.LEFT, fill=tk.BOTH, padx=5, pady=5, expand=1)
        self.engine.get_add_edit_cancel(self,f0)
        f0.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

    def on_open(self,):

        sql = "SELECT * FROM suppliers"

        rs = self.engine.read(True, sql, ())

        index = 0
        self.dict_items={}

        if rs:
            self.lstItems.delete(0, tk.END)
            for i in rs:
                self.lstItems.insert(tk.END, i[1])
                if i[2] != 1:
                    self.lstItems.itemconfig(index, {'bg':'light gray'})
                self.dict_items[index]=i[0]
                index+=1
                
        self.title("Suppliers")

    def on_add(self, evt):

        obj = frames.supplier.Dialog(self,self.engine)
        obj.on_open()

    def on_edit(self, evt):

        if self.lstItems.curselection():
            index = self.lstItems.curselection()[0]
            self.obj = frames.supplier.Dialog(self, self.engine, index)
            self.obj.transient(self)
            self.obj.on_open(self.selected_item,)

        else:
            msg = "Please select an item."
            messagebox.showwarning(self.engine.title,msg)

    def on_item_activated(self, evt):

        self.on_edit(self)

    def on_item_selected(self, evt):

        if self.lstItems.curselection():

            index = self.lstItems.curselection()[0]
            pk = self.dict_items.get(index)
            self.selected_item = self.engine.get_selected('suppliers','supplier_id', pk)
                  
    def on_cancel(self, evt=None):
        if self.obj is not None:
            self.obj.destroy()
        self.destroy()
