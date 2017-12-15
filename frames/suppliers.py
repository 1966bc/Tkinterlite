#!/usr/bin/python3
#-----------------------------------------------------------------------------
# project:  tkinterlite
# authors:  1966bc
# mailto:   [giuseppe.costanzi@gmail.com]
# modify:   10/04/2017
# version:  0.1                                                                
#-----------------------------------------------------------------------------


from tkinter import *
from tkinter import messagebox

import frames.supplier

class Dialog(Toplevel):     
    def __init__(self,parent,engine,):
        super().__init__(name='suppliers')


        self.resizable(0,0)
        self.parent = parent
        self.engine = engine
        
        self.enable =  BooleanVar()
        self.selected_supplier = None

        self.center_me()
        self.init_ui()

    def center_me(self):

        #center window
        x = (self.master.winfo_screenwidth() - self.master.winfo_reqwidth()) / 2
        y = (self.master.winfo_screenheight() - self.master.winfo_reqheight()) / 2
        self.master.geometry("+%d+%d" % (x, y))
        
    def init_ui(self):
    
        self.panel = self.engine.get_panel_frame(self)

        wdg = LabelFrame(self.panel,text='Categories')
        self.lstSuppliers = self.engine.get_listbox(wdg,)
        self.lstSuppliers.bind("<<ListboxSelect>>", self.on_item_selected)
        self.lstSuppliers.bind("<Double-Button-1>", self.on_item_activated)
        wdg.pack(side=LEFT, fill=BOTH,padx=5, pady=5, expand =1)

        self.engine.get_add_edit_cancel(self,self.panel)
        
        self.panel.pack(side=LEFT, fill=BOTH, expand=1)
 
      
    def on_open(self,):

        sql = "SELECT * FROM suppliers"

        rs = self.engine.read(True, sql, ())

        index = 0
        self.dict_suppliers={}

        if rs:
            self.lstSuppliers.delete(0, END)
            for i in rs:
                self.lstSuppliers.insert(END, i[1])
                if i[2] != 1:
                    self.lstSuppliers.itemconfig(index, {'bg':'light gray'})
                self.dict_suppliers[index]=i[0]
                index+=1
                
        self.title("Suppliers")

    def on_add(self, evt):

        obj = frames.supplier.Dialog(self,self.engine)
        obj.transient(self)
        obj.on_open()

    def on_edit(self, evt):
        
        if self.selected_supplier is not None:
            obj = frames.supplier.Dialog(self,self.engine,self.index)
            obj.transient(self)
            obj.on_open(self.selected_supplier,)
        else:
            msg = "Please select an item."
            messagebox.showwarning(self.engine.title,msg)

    def on_item_activated(self,event):

        self.on_edit(self)

    def on_item_selected(self,event):

        try:
            self.index = self.lstSuppliers.curselection()[0]
            pk = self.dict_suppliers.get(self.index)
            self.selected_supplier = self.engine.get_selected('suppliers','supplier_id', pk)
        except:
            self.selected_supplier = None
            self.index = 0              

    def on_cancel(self, evt):
        self.destroy()
    
