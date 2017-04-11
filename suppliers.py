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

        self.frame = Frame(self)

        self.label_frame_lst_suplpiers = LabelFrame(self.frame,text='Suppliers',)      
   
        self.label_frame_buttons = LabelFrame(self.frame,text='Buttons', relief=FLAT)
       
        #widgets
        self.lst_vs = Scrollbar(self.label_frame_lst_suplpiers,orient=VERTICAL)
        self.lstSuppliers = Listbox(self.label_frame_lst_suplpiers,width=30, selectmode=BROWSE,
                                   yscrollcommand=self.lst_vs.set,
                                   relief=GROOVE,bg='lightyellow')
        self.lstSuppliers.bind("<<ListboxSelect>>", self.on_selected)
        self.lstSuppliers.bind("<Double-Button-1>", self.on_double_click)
        self.lst_vs.config(command=self.lstSuppliers.yview)

        self.btnAdd = Button(self.label_frame_buttons, text="Add", command=self.on_add)
        self.btnAdd.pack(fill = X, padx = 3, pady = 4)

        self.btnEdit = Button(self.label_frame_buttons, text="Edit", command=self.on_edit)
        self.btnEdit.pack(fill = X, padx = 3, pady = 4)

        self.btClose = Button(self.label_frame_buttons, text="Close", command = self.on_cancel)
        self.btClose.pack(fill = X, padx = 3, pady = 4)
 
        #frame packing
        self.frame.pack(expand=1,fill=Y,)
        self.label_frame_lst_suplpiers.pack(fill=BOTH,side=LEFT,)
        self.lstSuppliers.pack(side=LEFT,fill=Y) 
        self.lst_vs.pack(expand=1, fill=Y)
        self.label_frame_buttons.pack(fill=BOTH,side=LEFT,padx = 10,)
        

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
    
