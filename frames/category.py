#!/usr/bin/python3
#-----------------------------------------------------------------------------
# project:  tkinterlite
# authors:  1966bc
# mailto:   [giuseppe.costanzi@gmail.com]
# modify:   10/04/2017
# version:  0.1                                                                
#-----------------------------------------------------------------------------

from tkinter import *
from tkinter import ttk
from tkinter import messagebox

class Dialog(Toplevel):     
    def __init__(self,parent,engine,index=None):
        super().__init__(name='category')
        
        self.resizable(0,0)
        self.parent = parent
        self.engine = engine
        self.index = index
        
        self.enable =  BooleanVar()

        self.center_me()
        self.init_ui()

    def center_me(self):

        #center window
        x = (self.master.winfo_screenwidth() - self.master.winfo_reqwidth()) / 2
        y = (self.master.winfo_screenheight() - self.master.winfo_reqheight()) / 2
        self.master.geometry("+%d+%d" % (x, y))
        
    def init_ui(self):

        self.panel = self.engine.get_panel_frame(self)
        self.panel.grid(row = 0, column = 0, sticky=N+W+S+E)

        Label(self.panel, text="Category:",anchor='w').grid(row=0, sticky='w')
        self.txtCategory = Entry(self.panel,)
        self.txtCategory.grid(row=0, column=1, sticky='w')

        Label(self.panel, text="Description:",anchor='w').grid(row=1, sticky='w')
        self.txtDescription = Entry(self.panel,)
        self.txtDescription.grid(row=1, column=1, sticky='w')

        Label(self.panel, text="Enable:").grid(row=2, sticky='w')
        self.ckEnable = Checkbutton(self.panel, onvalue=1, offvalue=0, variable = self.enable,)
        self.ckEnable.grid(row=2, column=1, sticky='w')

        self.engine.get_save_cancel(self, self)
       

    def on_open(self, selected_category = None):

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
        
    def on_save(self, evt):

        if self.on_fields_control()==False:

            msg = "Please fill all fields."
            messagebox.showwarning(self.engine.title,msg)

        else:
       
            if messagebox.askyesno(self.engine.title, "Do you want to save?",parent=self) == True:

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

            else:
                msg = "Operation aborted."
                messagebox.showinfo(self.engine.title,msg)                    
           
    def on_cancel(self, evt=None):
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
        
