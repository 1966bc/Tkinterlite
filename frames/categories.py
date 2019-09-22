#!/usr/bin/python3
#-----------------------------------------------------------------------------
# project:  tkinterlite
# authors:  1966bc
# mailto:   [giuseppe.costanzi@gmail.com]
# modify:   2019-09-22
# version:  0.3                                                              
#-----------------------------------------------------------------------------
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

import frames.category

class Categories(tk.Toplevel):     
    def __init__(self, parent, *args, **kwargs):
        super().__init__(name='categories')

        self.parent = parent
        self.engine = kwargs['engine']
        self.protocol("WM_DELETE_WINDOW", self.on_cancel)
        self.obj = None
        self.init_ui()
        self.engine.center_me(self)

    def init_ui(self):

        f0 = self.engine.get_frame(self, 8)
        f1 = ttk.Frame(f0,)
        self.lstItems = self.engine.get_listbox(f1,width=40)
        self.lstItems.bind("<<ListboxSelect>>", self.on_item_selected)
        self.lstItems.bind("<Double-Button-1>", self.on_item_activated)
        f1.pack(side=tk.LEFT, fill=tk.BOTH, padx=5, pady=5, expand=1)
        self.engine.get_add_edit_cancel(self,f0)
        f0.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

    def on_open(self,):

        index = 0
        self.dict_items={}
        sql = "SELECT * FROM categories"

        rs = self.engine.read(True, sql, ())

        if rs:
            self.lstItems.delete(0, tk.END)
            for i in rs:
                self.lstItems.insert(tk.END, i[1])
                if i[3] != 1:
                    self.lstItems.itemconfig(index, {'bg':'light gray'})
                self.dict_items[index]=i[0]
                index+=1
                
        self.title("Categories")

    def on_add(self, evt):

        frames.category.Category(self, engine=self.engine, index=None).on_open()

       
    def on_edit(self, evt):

        if self.lstItems.curselection():
            index = self.lstItems.curselection()[0]
            self.obj = frames.category.Category(self, engine=self.engine, index=index)
            self.obj.on_open(self.selected_item,)

        else:
            msg = "Please select an item."
            messagebox.showwarning(self.master.title(), msg)

    def on_item_activated(self, evt):

        self.on_edit(self)

    def on_item_selected(self, evt):

        if self.lstItems.curselection():

            index = self.lstItems.curselection()[0]
            pk = self.dict_items.get(index)
            self.selected_item = self.engine.get_selected('categories','category_id', pk)
                  
    def on_cancel(self, evt=None):
        if self.obj is not None:
            self.obj.destroy()
        self.destroy()
