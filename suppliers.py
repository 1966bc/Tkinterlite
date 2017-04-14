#!/usr/bin/python3
#-----------------------------------------------------------------------------
# project:  tkinterlite
# authors:  1966bc
# mailto:   [giuseppe.costanzi@gmail.com]
# modify:   10/04/2017
# version:  0.1                                                                
#-----------------------------------------------------------------------------

import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import supplier

class Dialog(tk.Toplevel):     
    def __init__(self,parent,engine):
        tk.Toplevel.__init__(self,)

        self.resizable(0,0)
        self.parent = parent
        self.engine = engine
    
        self.enable =  BooleanVar()
        self.selected_supplier = None

        self.panel = Frame(self)
        
        self.lf_suppliers = LabelFrame(self.panel,text='Suppliers',)      

        self.scroll_bar = Scrollbar(self.lf_suppliers,orient=VERTICAL)
        self.lstSuppliers = Listbox(self.lf_suppliers,
                                    relief=GROOVE,
                                    width=30,
                                    selectmode=BROWSE,
                                    bg='white',
                                    yscrollcommand=self.scroll_bar.set,)
        self.lstSuppliers.bind("<<ListboxSelect>>", self.on_selected)
        self.lstSuppliers.bind("<Double-Button-1>", self.on_double_click)
        self.scroll_bar.config(command=self.lstSuppliers.yview)

        self.lf_suppliers.pack(fill=BOTH, side=LEFT,)
        self.lstSuppliers.pack(side=LEFT,fill=Y) 
        self.scroll_bar.pack(fill=Y, expand=1)


        self.lf_buttons = Frame(self.panel, padx=8, pady=8)

        self.btnAdd = Button(self.lf_buttons, text="Add", command=self.on_add)
        self.btnAdd.pack(fill=X, pady=8)

        self.btnEdit = Button(self.lf_buttons, text="Edit", command=self.on_edit)
        self.btnEdit.pack(fill=X, pady=8)

        self.btClose = Button(self.lf_buttons, text="Close", command = self.on_cancel)
        self.btClose.pack(fill=X, pady=8)

        self.lf_buttons.pack(fill=BOTH, side=LEFT)

        self.panel.pack(expand=1,fill=Y,)
 
      
    def on_open(self,):

        sql = "SELECT * FROM suppliers"

        rs = self.engine.read(True, sql, ())

        index = 0
        self.dict_suppliers={}

        if rs:
            self.lstSuppliers.delete(0, END)
            for i in rs:
                self.lstSuppliers.insert(END, i[1])
                self.dict_suppliers[index]=i[0]
                index+=1
                
        self.title("Suppliers")

    def on_add(self,):

        obj = supplier.Dialog(self,self.engine)
        obj.on_open()

    def on_edit(self,):
        
        if self.selected_supplier is not None:
            obj = supplier.Dialog(self,self.engine,self.index)
            obj.on_open(self.selected_supplier,)
        else:
            msg = "Please select an item."
            messagebox.showwarning(self.engine.title,msg)

    def on_double_click(self,event):

        self.on_edit()

    def on_selected(self,event):

        self.index = self.lstSuppliers.curselection()[0]
        pk = self.dict_suppliers.get(self.index)
        self.selected_supplier = self.engine.get_selected('suppliers','supplier_id', pk)

    def on_cancel(self,):
        self.destroy()
    
