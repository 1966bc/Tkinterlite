#!/usr/bin/python3
#-----------------------------------------------------------------------------
# project:  tkinterlite
# authors:  1966bc
# mailto:   [giuseppe.costanzi@gmail.com]
# modify:   2018-12-23
# version:  0.2                                                             
#-----------------------------------------------------------------------------

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox


class Dialog(tk.Toplevel):     
    def __init__(self, parent, engine, item_iid=None):
        super().__init__(name='product')

        self.transient(parent)
        self.resizable(0,0)
        self.parent = parent
        self.engine = engine
        self.item_iid = item_iid
        self.vcmd = self.engine.get_validate_float(self)

        self.product = tk.StringVar()
        self.stock = tk.IntVar()
        self.package = tk.StringVar()
        self.price = tk.DoubleVar() 
        self.enable = tk.BooleanVar()

        self.set_style()
        self.engine.center_me(self)
        self.init_ui()

    def set_style(self):
        s = ttk.Style()
        s.configure('Product.TLabel',
                    foreground=self.engine.get_rgb(0,0,255),
                    background=self.engine.get_rgb(255,255,255))
         
        s.configure('Package.TLabel',
                    foreground=self.engine.get_rgb(255,0,0),
                    background=self.engine.get_rgb(255,255,255))

        

    def init_ui(self):

        w = self.engine.get_init_ui(self)

        r =0
        ttk.Label(w, text="Product:",).grid(row=r, sticky=tk.W)
        self.txtProduct = ttk.Entry(w,
                                    style='Product.TLabel',
                                    textvariable=self.product)
        self.txtProduct.grid(row=r, column=1, padx=5, pady=5)

        r +=1
        ttk.Label(w, text="Suppliers:",).grid(row=r, sticky=tk.W)
        self.cbSuppliers = ttk.Combobox(w,)
        self.cbSuppliers.grid(row=r, column=1)

        r +=1
        ttk.Label(w, text="Categories:",).grid(row=r, sticky=tk.W)
        self.cbCategories = ttk.Combobox(w,)
        self.cbCategories.grid(row=r, column=1)

        r +=1
        ttk.Label(w, text="Package:").grid(row=r, sticky=tk.W)
        self.txtPackage = ttk.Entry(w,
                                    style='Package.TLabel',
                                    textvariable=self.package)
        self.txtPackage.grid(row=r, column=1, padx=5, pady=5)

        r +=1
        ttk.Label(w, text="Price:").grid(row=r, sticky=tk.W)
        self.txtPrice = ttk.Entry(w,
                                  validate = 'key',
                                  validatecommand = self.vcmd,
                                  textvariable=self.price)
        self.txtPrice.grid(row=r, column=1, padx=5, pady=5)

        r +=1
        ttk.Label(w, text="Stock:").grid(row=r, sticky=tk.W)
        self.txtStock = ttk.Entry(w,
                           validate = 'key',
                           validatecommand = self.vcmd,
                           textvariable=self.stock)
        self.txtStock.grid(row=r, column=1, padx=5, pady=5)

       
        r +=1
        ttk.Label(w, text="Enable:").grid(row=r, sticky=tk.W)
        ttk.Checkbutton(w,
                       onvalue=1,
                       offvalue=0,
                       variable = self.enable,).grid(row=r,
                                                    column=1,
                                                    sticky=tk.W)

        self.engine.get_save_cancel(self, w)

    def on_open(self, selected_product=None):

        
        self.set_categories()
        self.set_suppliers()

        if self.item_iid is not None:
            self.selected_product = selected_product
            msg = "Update  %s" % (self.selected_product[1],)
            self.set_values()
        else:
            msg = "Insert new product"
            self.enable.set(1)

        self.title(msg)
        self.txtProduct.focus()

    def set_values(self,):


        self.product.set(self.selected_product[1])

        key = next(key for key, value in self.dict_suppliers.items() if value == self.selected_product[2])
        self.cbSuppliers.current(key)

        key = next(key for key, value in self.dict_categories.items() if value == self.selected_product[3])
        self.cbCategories.current(key)

        self.package.set(self.selected_product[4])
        self.price.set(self.selected_product[5])
        self.stock.set(self.selected_product[6])
        self.enable.set(self.selected_product[7])

    def get_values(self,):

        return [self.product.get(),
                self.dict_suppliers[self.cbSuppliers.current()],
                self.dict_categories[self.cbCategories.current()],
                self.package.get(),
                self.price.get(),
                self.stock.get(),
                self.enable.get()]
        
    def on_save(self, evt):

        if self.engine.on_fields_control(self)==False:return
        if messagebox.askyesno(self.engine.title, self.engine.ask_to_save, parent=self) == True:

            args =  self.get_values()

            if self.item_iid is not None:

                sql = self.engine.get_update_sql('products','product_id')
                args.append(self.selected_product[0])
                       
            else:
                sql = self.engine.get_insert_sql('products',len(args))

            self.engine.write(sql,args)
            self.parent.on_open()

            if self.item_iid is not None:
                self.parent.lstProducts.selection_set(self.item_iid)
                self.parent.lstProducts.see(self.item_iid)
                
            self.on_cancel()
    
    def set_categories(self):

        index = 0
        self.dict_categories={}
        values = []

        sql = "SELECT category_id, category FROM categories ORDER BY category ASC"
        rs = self.engine.read(True, sql, ())
            
        for i in rs:
            self.dict_categories[index]=i[0]
            index+=1
            values.append(i[1])

        self.cbCategories['values']=values
            
    def set_suppliers(self,):

        index = 0
        self.dict_suppliers={}
        values = []

        sql = "SELECT supplier_id, company FROM suppliers ORDER BY company ASC"
        rs = self.engine.read(True, sql, ())
            
        for i in rs:
            self.dict_suppliers[index]=i[0]
            index+=1
            values.append(i[1])

        self.cbSuppliers['values']=values

    def on_cancel(self,evt=None):
        self.destroy()
        
