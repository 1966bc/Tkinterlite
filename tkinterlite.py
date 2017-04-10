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

from engine import Engine
import product
import categories
import suppliers

class App(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)

        self.engine = Engine()
        self.master = master
        self.master.resizable(800,800)
        self.init_style()
        self.InitResizing()
        self.init_menu()
        self.init_status_bar()
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
        self.s.configure('TLabelframe.Label', font=('courier', 15, 'bold'),)
        
    def init_menu(self):

        mnuMain = Menu(self.master, bd = 1)
        
        mFile = Menu(mnuMain, tearoff=0, bd = 1)
        mTools = Menu(mnuMain, tearoff=0, bd = 1)
        mAbout = Menu(mnuMain, tearoff=0, bd = 1)
        
        mnuMain.add_cascade(label="File", menu=mFile)
        mnuMain.add_cascade(label="Tools", menu=mTools)
        mnuMain.add_cascade(label="Info", menu=mAbout)
        
       
        mFile.add_command(label="Exit", command=self.on_exit)
        mTools.add_command(label="Categories", command=self.on_categories)
        mTools.add_command(label="Suppliers", command=self.on_suppliers)
        mAbout.add_command(label="About", command=self.on_about)
             
        self.master.config(menu=mnuMain)

    def init_status_bar(self):

        self.status = tk.Label(self.master, text = 'Ready', bd=1, relief=SUNKEN, anchor=W)
        self.status.grid(row = 3, column = 0, columnspan = 2, sticky = N+E+W+S)

    def init_window(self):

        self.master.title(self.engine.title)
        self.create_widgets()
       
    def create_widgets(self):

        self.label_frame_lst_products = ttk.LabelFrame(text='Products list')
        self.label_frame_cb_categories = ttk.LabelFrame(text='Categories')
        self.frame_buttons = ttk.Frame(pad=10)

        #begin creating ttk.Treeview
        #-----------------------------------------------------------------------
        self.lstProducts = ttk.Treeview(self.label_frame_lst_products,
                                        columns=('ID','Product', 'Description', 'Stock','Price'),
                                        selectmode='browse',
                                        padding = 5,
                                        show='headings',
                                        displaycolumns=('#all',))
        #bind TreeviewSelect
        self.lstProducts.bind("<<TreeviewSelect>>", self.get_selected_product)
        self.lstProducts.bind("<Double-1>", self.on_double_click)
        
        self.lstProducts.heading('#0', text='ID',)
        self.lstProducts.heading('#1', text='Product',)
        self.lstProducts.heading('#2', text='Description')
        self.lstProducts.heading('#3', text='Stock')
        self.lstProducts.heading('#4', text='Price')
        self.lstProducts.column('#0', stretch=tk.NO,width=0)
        self.lstProducts.column('#1', stretch=tk.YES,width=300)
        self.lstProducts.column('#2', stretch=tk.YES)
        self.lstProducts.column('#3', stretch=tk.YES,width=50)
        self.lstProducts.column('#4', stretch=tk.YES,width=50)
        #add ttk.Scrollbar to ttk.Treeview
        treeScroll = ttk.Scrollbar(self.label_frame_lst_products)
        treeScroll.configure(command=self.lstProducts.yview)
        self.lstProducts.configure(yscrollcommand=treeScroll.set)
        #packing
        self.lstProducts.pack(side=LEFT,fill=tk.BOTH, expand=1)
        treeScroll.pack(fill=tk.Y,expand=1)
        #-----------------------------------------------------------------------
    
        #begin creating ttk.Combobox
        #-----------------------------------------------------------------------
        self.cbCategories =  ttk.Combobox(self.label_frame_cb_categories,)
        self.cbCategories.bind("<<ComboboxSelected>>", self.get_selected_category)
        #packing
        self.cbCategories.pack(fill=BOTH, expand =1)
        #-----------------------------------------------------------------------

        #creating and packing tk.Button
        #-----------------------------------------------------------------------
        self.btnRefresh = tk.Button(self.frame_buttons, text="Refresh", command=self.on_open)
        self.btnRefresh.pack(fill = X,anchor=W, pady=10)
        
        self.btnNew = tk.Button(self.frame_buttons, text="New", command=self.on_add_product)
        self.btnNew.pack(fill = X,anchor=W, pady=10)

        self.btnEdit = tk.Button(self.frame_buttons, text="Edit", command=self.on_edit)
        self.btnEdit.pack(fill = X,anchor=W, pady=10)

        self.btClose = tk.Button(self.frame_buttons, text="Close", command=self.on_exit)
        self.btClose.pack(fill = X,anchor=W, pady=10)
        #-----------------------------------------------------------------------

        #positioning all
        #-----------------------------------------------------------------------
        self.label_frame_lst_products.grid(row=0,column=0, sticky=N+E+S+W)
        self.label_frame_cb_categories.grid(row=1, column=0,sticky=W+E)
        self.frame_buttons.grid(row = 0, column = 1, sticky=N+S)
        #-----------------------------------------------------------------------

    def on_open(self):

        self.selected_product = None
        sql = "SELECT * FROM products ORDER BY product DESC"
        self.set_tree_values(sql,())
        self.set_combo_values()

    def on_add_product(self):

        obj = product.Dialog(self,self.engine)
        obj.on_open()
        obj.wait_visibility()
        obj.grab_set()
        self.master.wait_window(obj)

    def on_categories(self):

        obj = categories.Dialog(self,self.engine)
        obj.on_open()
      
    def on_suppliers(self):

        obj = suppliers.Dialog(self,self.engine)
        obj.on_open()

    def on_edit(self,):

        if self.selected_product is not None:
            obj = product.Dialog(self,self.engine)
            obj.on_open(self.selected_product)
            obj.wait_visibility()
            obj.grab_set()
            self.master.wait_window(obj)
        else:
            msg = "Please select an item."
            messagebox.showwarning(self.engine.title,msg)

      
    def on_double_click(self,event):

        self.on_edit()
 
    def get_selected_product(self, event):
        
        pk = int(self.lstProducts.item(self.lstProducts.focus())['text'])
        self.selected_product = self.engine.get_selected('products','product_id', pk)

    def get_selected_category(self, event):
        
        index = self.cbCategories.current()
        category_id = self.dict_categories[index]
        sql = "SELECT * FROM products WHERE category_id =? ORDER BY product DESC"
        args = (category_id,)
        self.set_tree_values(sql, args)
        
    def set_tree_values(self,sql,args):

        for i in self.lstProducts.get_children():
            self.lstProducts.delete(i)

        index = 0
        self.dict_products={}            

        rs  = self.engine.read(True, sql, args)
        
        for i in rs:
            self.lstProducts.insert('', 0, text=i[0],values=(i[1],i[4],i[6],i[5]))
            self.dict_products[index]=i[0]
            index+=1

    def set_combo_values(self):

        index = 0
        self.dict_categories={}
        l = []

        sql = "SELECT category_id, category FROM categories ORDER BY category"
        rs = self.engine.read(True, sql, ())
            
        for i in rs:
            self.dict_categories[index]=i[0]
            index+=1
            l.append(i[1])

        self.cbCategories['values']=l

    def on_about(self,):
        messagebox.showinfo(self.engine.title, self.engine.about)   
        
        
    def on_exit(self):
        if messagebox.askokcancel(self.engine.title, "Do you want to quit?"):
            self.master.destroy()

def main():
    root = tk.Tk()
    app = App(master=root)
    app.on_open()
    app.master.protocol("WM_DELETE_WINDOW",app.on_exit)
    app.mainloop()
  
if __name__ == '__main__':
    main()
