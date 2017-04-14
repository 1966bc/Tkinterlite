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

class Dialog(tk.Toplevel):     
    def __init__(self,parent,engine,index=None):
        tk.Toplevel.__init__(self,)

        self.resizable(0,0)
        
        self.parent = parent
        self.engine = engine
        self.index = index

        self.enable =  BooleanVar()

        Label(self, text="Category:").grid(row=0)
        Label(self, text="Description:").grid(row=1)
        self.txtCategory = Entry(self, bg='white')
        self.txtDescription = Entry(self, bg='white')
        self.txtCategory.grid(row=0, column=1)
        self.txtDescription.grid(row=1, column=1)
       
        self.btnSave = tk.Button(self,text="Save", command=self.on_save)
        self.btnSave.grid(row=0, column=2)
        
        self.btCancel = tk.Button(self, text="Cancel", command=self.on_cancel)
        self.btCancel.grid(row=1, column=2)

        self.ckEnable = tk.Checkbutton(self, text="Enable",onvalue=1, offvalue=0,variable = self.enable, )
        self.ckEnable.grid(row=2, column=2)
       

    def on_open(self,selected_category = None):

        if selected_category is not None:
            self.insert_mode = False
            self.selected_category = selected_category
            msg = "Update  %s" % (self.selected_category[1],)
            self.set_values()
        else:
            self.insert_mode = True
            msg = "Insert new category"
            self.enable.set(1)

        self.title(msg)
        self.txtCategory.focus()
        
    def on_save(self,):

        if self.on_fields_control()==False:

            msg = "Please fill all fields."
            messagebox.showwarning(self.engine.title,msg)

        else:
       
            if messagebox.askquestion(self.engine.title, "Do you want to save?"):

                args =  self.get_values()

                if self.insert_mode == False:

                    sql = self.engine.get_update_sql('categories','category_id')

                    args = self.engine.get_update_sql_args(args, self.selected_category[0])
                       
                elif self.insert_mode == True:

                        sql = self.engine.get_insert_sql('categories',len(args))

                self.engine.write(sql,args)
                self.parent.on_open()

                if self.index is not None:
                    self.parent.lstCategories.see(self.index)
                    self.parent.lstCategories.selection_set(self.index)
                    
                self.on_cancel()
           
    def on_cancel(self,):
        self.destroy()

    def get_values(self,):

        return (self.txtCategory.get(),
                self.txtDescription.get(),
                self.enable.get())
    
    def set_values(self,):

        self.txtCategory.insert(0, self.selected_category[1])
        self.txtDescription.insert(0, self.selected_category[2])
        self.enable.set(self.selected_category[3])

    def on_fields_control(self):

        objs = (self.txtCategory,self.txtDescription)

        for obj in objs:
            if not obj.get():
                ret = False
                break   
            else:
                ret = True
        return ret               
        
