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
import shelve

class Dialog(tk.Toplevel):     
    def __init__(self,parent,engine):
        tk.Toplevel.__init__(self,)

        self.resizable(0,0)
        
        self.parent = parent
        self.engine = engine

        self.stock_min = IntVar()
        self.stock_max = IntVar()


        Label(self, text="Stock Min:").grid(row=0)
        Label(self, text="Stock Max:").grid(row=1)

        self.spStockMin = Spinbox(self,bg='white',width=5,
                                  from_=1, to=10000,
                                  textvariable=self.stock_min)
        self.spStockMax = Spinbox(self,bg='white',width=5,
                                  from_=1, to=10000,
                                  textvariable=self.stock_max)
     
        self.spStockMin.grid(row=0, column=1)
        self.spStockMax.grid(row=1, column=1)
       
        self.btnSave = tk.Button(self,text="Save",padx=10, pady=10, command=self.on_save)
        self.btnSave.grid(row=0, column=2)
        
        self.btCancel = tk.Button(self, text="Cancel",padx=10,pady=10, command=self.on_cancel)
        self.btCancel.grid(row=1, column=2)


    def on_open(self,):
        
        self.title('Parameters')

        self.engine.parameters = self.engine.get_parameters()
        
        self.set_values()
        
        
    def on_save(self,):

        if self.on_check_values()==False:

            msg = "Min stock value is equal or major of Max stock value."
            messagebox.showwarning(self.engine.title,msg)

        else:            

            if messagebox.askquestion(self.engine.title, "Do you want to save?"):

                try:
                    db = shelve.open('parameters')
                    db['spinbox_min_value'] = self.stock_min.get()
                    db['spinbox_max_value'] = self.stock_max.get()
                    db.close()
                    self.on_cancel()
                except:
                    print (sys.exc_info()[0])
                    print (sys.exc_info()[1])
                    print (sys.exc_info()[2])

    def on_cancel(self,):
        self.destroy()
    
    def set_values(self,):
        self.stock_min.set(self.engine.parameters['spinbox_min_value'])
        self.stock_max.set(self.engine.parameters['spinbox_max_value'])

    def on_check_values(self):

        if self.stock_min.get() >= self.stock_max.get():
            return False
        else:
            return True           

                 
        
