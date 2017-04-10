#!/usr/bin/python3
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

from engine import Engine


class Frame(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        
        self.master = master
        self.master.resizable(800,800)
        self.init_style()
        self.InitResizing()
        self.init_window()

    def InitResizing(self):
        top = self.winfo_toplevel()
        top.rowconfigure(0, weight=1)
        top.columnconfigure(0, weight=1)
        top.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)        

    def init_style(self,):

        self.s = ttk.Style()
        self.s.theme_use('clam')
        self.s.configure('TLabelframe.Label', font=('courier', 15, 'bold'))
        
    def init_window(self):

        self.master.title('Products')
        self.create_widgets()
       
    def create_widgets(self):

        self.label_frame_lst_products = ttk.Frame()
        self.frame_buttons = ttk.Frame(pad=10)

        #begin creating ttk.Treeview
        #-----------------------------------------------------------------------
        self.lstProducts = ttk.Treeview(self.label_frame_lst_products,
                                        columns=('ID','Product', 'Description', 'Stock'),
                                        selectmode='browse')
        #bind TreeviewSelect
        self.lstProducts.bind("<<TreeviewSelect>>", self.get_selected_product)
        
        self.lstProducts.heading('#0', text='ID',)
        self.lstProducts.heading('#1', text='Product',)
        self.lstProducts.heading('#2', text='Description')
        self.lstProducts.heading('#3', text='Stock')
        self.lstProducts.column('#0', stretch=tk.NO,width=0)
        self.lstProducts.column('#1', stretch=tk.YES)
        self.lstProducts.column('#2', stretch=tk.YES)
        self.lstProducts.column('#3', stretch=tk.NO,width=50)
        #add ttk.Scrollbar to ttk.Treeview
        treeScroll = ttk.Scrollbar(self.label_frame_lst_products)
        treeScroll.configure(command=self.lstProducts.yview)
        self.lstProducts.configure(yscrollcommand=treeScroll.set)
        #packing
        self.lstProducts.pack(side=LEFT,fill=tk.BOTH, expand=1)
        treeScroll.pack(fill=tk.Y,expand=1)
        #-----------------------------------------------------------------------
    
       
        #creating and packing tk.Button
        #-----------------------------------------------------------------------
        self.btnRefresh = tk.Button(self.frame_buttons, text="Refresh", command=self.on_open)
        self.btnRefresh.pack(fill = X,anchor=W, pady=10)

        self.btClose = tk.Button(self.frame_buttons, text="Close", command=self.on_exit)
        self.btClose.pack(fill = X,anchor=W, pady=10)
        #-----------------------------------------------------------------------

        #positioning all
        #-----------------------------------------------------------------------
        self.label_frame_lst_products.grid(row=0,column=0, sticky=N+E+S+W)
        self.frame_buttons.grid(row = 0, column = 1, sticky=N+S,)
        #-----------------------------------------------------------------------

    def get_selected_product(self, event):

        pk = int(self.lstProducts.item(self.lstProducts.focus())['text'])

        self.selected_dict_product = self.master.engine.get_selected('Products','ProductID', pk)
            
    def set_tree_values(self,sql,args):

        for i in self.lstProducts.get_children():
            self.lstProducts.delete(i)

        index = 0
        self.dict_products={}            

        rs  = self.master.engine.read(True, sql, args)
        
        for i in rs:
            self.lstProducts.insert('', 0, text=i[0],values=(i[1],i[4],i[6]))
            self.dict_products[index]=i[0]
            index+=1

          
    def on_open(self):

        sql = "SELECT * FROM Products ORDER BY ProductName DESC"
        self.set_tree_values(sql,())
        
        
    def on_exit(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.master.destroy()

def main():
    root = tk.Tk()
    root.engine = Engine()
    app = Frame(master=root)
    app.on_open()
    app.master.protocol("WM_DELETE_WINDOW",app.on_exit)
    app.mainloop()
  
if __name__ == '__main__':
    main()
