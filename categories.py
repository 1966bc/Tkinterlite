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
import category

class Dialog(tk.Toplevel):     
    def __init__(self,parent,engine):
        tk.Toplevel.__init__(self,)

        self.resizable(0,0)
        self.parent = parent
        self.engine = engine
    
        self.enable =  BooleanVar()
        self.selected_category = None

        self.panel = Frame(self)
        self.label_frame_lst_categories = LabelFrame(self.panel,text='Categories',)      
        self.label_frame_buttons = LabelFrame(self.panel,text='Buttons', relief=FLAT)
       
        #widgets
        self.scroll_bar_lst_categories = Scrollbar(self.label_frame_lst_categories,orient=VERTICAL)
        self.lstCategories = Listbox(self.label_frame_lst_categories,width=30, selectmode=BROWSE,
                                   yscrollcommand=self.scroll_bar_lst_categories.set,
                                   relief=GROOVE,bg='lightyellow')
        self.lstCategories.bind("<<ListboxSelect>>", self.on_selected)
        self.lstCategories.bind("<Double-Button-1>", self.on_double_click)
        self.scroll_bar_lst_categories.config(command=self.lstCategories.yview)

        self.btnAdd = Button(self.label_frame_buttons, text="Add", command=self.on_add)
        self.btnAdd.pack(fill = X, padx = 3, pady = 4)

        self.btnEdit = Button(self.label_frame_buttons, text="Edit", command=self.on_edit)
        self.btnEdit.pack(fill = X, padx = 3, pady = 4)

        self.btClose = Button(self.label_frame_buttons, text="Close", command = self.on_cancel)
        self.btClose.pack(fill = X, padx = 3, pady = 4)
 
        #panel packing
        self.panel.pack(expand=1,fill=Y,)
        self.label_frame_lst_categories.pack(fill=BOTH,side=LEFT,)
        self.lstCategories.pack(side=LEFT,fill=Y) 
        self.scroll_bar_lst_categories.pack(expand=1, fill=Y)
        self.label_frame_buttons.pack(fill=BOTH,side=LEFT,padx = 10,)
        

    def on_open(self,):

        sql = "SELECT * FROM categories"

        rs = self.engine.read(True, sql, ())

        index = 0
        self.dict_categories={}

        if rs:
            self.lstCategories.delete(0, END)
            for i in rs:
                self.lstCategories.insert(END, i[1])
                self.dict_categories[index]=i[0]
                index+=1
                
        self.title("Categories")

    def on_add(self,):

        obj = category.Dialog(self,self.engine)
        obj.on_open()

    def on_edit(self,):
        
        if self.selected_category is not None:
            obj = category.Dialog(self,self.engine)
            obj.on_open(self.selected_category)
        else:
            msg = "Please select an item."
            messagebox.showwarning(self.engine.title,msg)

    def on_double_click(self,event):

        self.on_edit()

    def on_selected(self,event):

        index = self.lstCategories.curselection()[0]
        pk = self.dict_categories.get(index)
        self.selected_category = self.engine.get_selected('categories','category_id', pk)

       
    def on_cancel(self,):
        self.destroy()
    
