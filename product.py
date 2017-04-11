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
    def __init__(self,parent,engine):
        tk.Toplevel.__init__(self,)
       
        self.parent = parent
        self.engine = engine
    
        self.resizable(0,0)
        self.enable =  BooleanVar()
        self.stock =  IntVar()

        Label(self, text="Product:").grid(row=0)
        Label(self, text="Suppliers:").grid(row=1)
        Label(self, text="Categories:").grid(row=2)
        Label(self, text="Package:").grid(row=3)
        Label(self, text="Price:").grid(row=4)
        Label(self, text="Stock:").grid(row=5)
        
        self.txtProduct = Entry(self)
        self.cbSuppliers =  ttk.Combobox(self)
        self.cbCategories =  ttk.Combobox(self)
        self.txtPackage = Entry(self)
        self.txtPrice = Entry(self)
        self.spStock = Spinbox(self,
                               from_=self.engine.parameters['spinbox_min_value'],
                               to=self.engine.parameters['spinbox_max_value'],
                               textvariable=self.stock)
        self.txtProduct.grid(row=0, column=1)
        self.cbSuppliers.grid(row=1, column=1)
        self.cbCategories.grid(row=2, column=1)
        self.txtPackage.grid(row=3, column=1)
        self.txtPrice.grid(row=4, column=1)
        self.spStock.grid(row=5, column=1)
       
        #creating and packing tk.Button and tk.Checkbutton
        #-----------------------------------------------------------------------
        self.btnSave = tk.Button(self,text="Save", command=self.on_save)
        self.btnSave.grid(row=0, column=2)
        
        self.btCancel = tk.Button(self, text="Cancel", command=self.on_cancel)
        self.btCancel.grid(row=1, column=2)

        self.ckEnable = tk.Checkbutton(self, text="Enable",onvalue=1, offvalue=0,variable = self.enable, )
        self.ckEnable.grid(row=2, column=2)
        #-----------------------------------------------------------------------


    def on_open(self,selected_product = None):

        self.selected_product  = selected_product
        self.set_categories_values()
        self.set_suppliers_values()
        
        if selected_product is not None:
            self.insert_mode = False
            self.selected_product = selected_product
            msg = "Update  %s" % (self.selected_product[1],)
            self.set_values()
        else:
            self.insert_mode = True
            msg = "Insert new product"
            self.stock.set(self.engine.parameters['spinbox_min_value'])
            self.enable.set(1)

        self.title(msg)
        self.txtProduct.focus()

    def set_values(self,):

        key = next(key for key, value in self.dict_categories.items() if value == self.selected_product[3])
        self.cbCategories.current(key)

        key = next(key for key, value in self.dict_suppliers.items() if value == self.selected_product[2])
        self.cbSuppliers.current(key)

        self.txtProduct.insert(0, self.selected_product[1])
        self.txtPackage.insert(0, self.selected_product[4])
        self.txtPrice.insert(0, self.selected_product[5])
        
        self.stock.set(self.selected_product[6])        
        self.enable.set(self.selected_product[7])        
        
    def on_save(self,):

        if self.on_fields_control()==False:

            msg = "Please fill all fields."
            messagebox.showwarning(self.engine.title,msg)

        else:
       
            if messagebox.askquestion("Save", "Do you want to save?"):

                args =  self.get_values()

                if self.insert_mode == False:

                    sql = self.engine.get_update_sql('products','product_id')

                    args = self.engine.get_update_sql_args(args, self.selected_product[0])
                       
                elif self.insert_mode == True:

                        sql = self.engine.get_insert_sql('products',len(args))

                self.engine.write(sql,args)
                self.parent.on_open()
                self.on_cancel()
           
    def on_cancel(self,):
        self.destroy()

    def get_values(self,):

        return (self.txtProduct.get(),
                self.dict_suppliers[self.cbSuppliers.current()],
                self.dict_categories[self.cbCategories.current()],
                self.txtPackage.get(),
                self.txtPrice.get(),
                self.stock.get(),
                self.enable.get())

    def get_selected_category(self, event):
        
        index = self.cbCategories.current()
        category_id = self.dict_categories[index]
        sql = "SELECT * FROM products WHERE category_id =? ORDER BY product DESC"
        args = (category_id,)
        self.set_tree_values(sql, args)            
        
    def set_categories_values(self):

        index = 0
        self.dict_categories={}
        l = []

        sql = "SELECT category_id, category FROM categories ORDER BY category ASC"
        rs = self.engine.read(True, sql, ())
            
        for i in rs:
            self.dict_categories[index]=i[0]
            index+=1
            l.append(i[1])

        self.cbCategories['values']=l
        
        
    def set_suppliers_values(self,):

        index = 0
        self.dict_suppliers={}
        l = []

        sql = "SELECT supplier_id, company FROM suppliers ORDER BY company ASC"
        rs = self.engine.read(True, sql, ())
            
        for i in rs:
            self.dict_suppliers[index]=i[0]
            index+=1
            l.append(i[1])

        self.cbSuppliers['values']=l

    def on_fields_control(self):

        objs =  (self.txtProduct,
                 self.cbSuppliers,
                 self.cbCategories,
                 self.txtPackage,
                 self.txtPrice,)

        for obj in objs:
            if not obj.get():
                ret = False
                break   
            else:
                ret = True
        return ret           


      
       
