#!/usr/bin/python3
#-----------------------------------------------------------------------------
# project:  tkinterlite
# authors:  1966bc
# mailto:   [giuseppe.costanzi@gmail.com]
# modify:   2018-12-23
# version:  0.1                                                                
#-----------------------------------------------------------------------------

import tkinter as tk
from tkinter import messagebox

class Dialog(tk.Toplevel):     
    def __init__(self, parent, engine, index=None):
        super().__init__(name='supplier')

        self.transient(parent)
        self.resizable(0,0)
        self.parent = parent
        self.engine = engine
        self.index = index

        self.company = tk.StringVar()
        self.enable =  tk.BooleanVar()

        self.init_ui()

    def init_ui(self):

        w = self.engine.get_init_ui(self)

        r =0
        tk.Label(w, text="Company:",).grid(row=r, sticky=tk.W)
        self.txtCompany = tk.Entry(w, bg='white', textvariable=self.company)
        self.txtCompany.grid(row=r, column=1, padx=5, pady=5)

        r =1
        tk.Label(w, text="Enable:").grid(row=r, sticky=tk.W)
        tk.Checkbutton(w,
                       onvalue=1,
                       offvalue=0,
                       variable = self.enable,).grid(row=r,
                                                    column=1,
                                                    sticky=tk.W)

        self.engine.get_save_cancel(self, self)
       

    def on_open(self, selected_item=None):

        if self.index is not None:
            self.selected_item = selected_item
            msg = "Update  %s" % (self.selected_item[1],)
            self.set_values()
        else:
            self.insert_mode = True
            msg = "Insert new supplier"
            self.enable.set(1)

        self.title(msg)
        self.txtCompany.focus()

    def on_save(self, evt):

        fields =(self.txtCompany,)
        
        if self.engine.on_fields_control(fields)==False:return
        if messagebox.askyesno(self.engine.title, self.engine.ask_to_save, parent=self) == True:

            args =  self.get_values()

            if self.index is not None:

                sql = self.engine.get_update_sql('suppliers','supplier_id')
                args.append(self.selected_item[0])
                       
            else:
                sql = self.engine.get_insert_sql('suppliers',len(args))

            self.engine.write(sql,args)
            self.parent.on_open()


            if self.index is not None:
                self.parent.lstItems.see(self.index)
                self.parent.lstItems.selection_set(self.index)
                    
            self.on_cancel()
            
    def get_values(self,):

        return [self.company.get(),
                self.enable.get()]
    
    def set_values(self,):

        self.company.set(self.selected_item[1])
        self.enable.set(self.selected_item[2])

    def on_cancel(self, evt=None):
        self.destroy()        
