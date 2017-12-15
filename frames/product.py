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
    def __init__(self,parent,engine,):
        super().__init__(name='product')
        
        self.resizable(0,0)
        self.parent = parent
        self.engine = engine
        self.vcmd = (self.register(self.validate), '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')

        self.stock = DoubleVar()
        self.price = DoubleVar() 
        self.enable = BooleanVar()
        
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

        Label(self.panel, text="Product:",anchor='w').grid(row=0, sticky='w')
        self.txtProduct = Entry(self.panel,)
        self.txtProduct.grid(row=0, column=1, sticky='w')

        Label(self.panel, text="Suppliers:",anchor='w').grid(row=1, sticky='w')
        self.cbSuppliers = ttk.Combobox(self.panel,)
        self.cbSuppliers.grid(row=1, column=1, sticky='w')

        Label(self.panel, text="Categories:",anchor='w').grid(row=2, sticky='w')
        self.cbCategories = ttk.Combobox(self.panel,)
        self.cbCategories.grid(row=2, column=1, sticky='w')

        Label(self.panel, text="Package:",anchor='w').grid(row=3, sticky='w')
        self.txtPackage = Entry(self.panel,)
        self.txtPackage.grid(row=3, column=1, sticky='w')

        Label(self.panel, text="Price:",anchor='w').grid(row=4, sticky='w')
        self.txtPrice = Entry(self.panel,
                              validate = 'key',
                              validatecommand = self.vcmd,
                              textvariable = self.price,
                              width=5)
        self.txtPrice.grid(row=4, column=1, sticky='w')

        Label(self.panel, text="Stock:",anchor='w').grid(row=5, sticky='w')
        self.txtStock = Entry(self.panel,
                              validate = 'key',
                              validatecommand = self.vcmd,
                              textvariable = self.stock,
                              width=5)
        self.txtStock.grid(row=5, column=1, sticky='w')

        Label(self.panel, text="Enable:").grid(row=6, sticky='w')
        self.ckEnable = Checkbutton(self.panel, onvalue=1, offvalue=0, variable = self.enable,)
        self.ckEnable.grid(row=6, column=1, sticky='w')

        self.engine.get_save_cancel(self, self)

    def on_open(self, selected_product = None):

        self.selected_product = selected_product
        self.set_categories()
        self.set_suppliers()
        
        if selected_product is not None:
            self.insert_mode = False
            self.selected_product = selected_product
            msg = "Update  %s" % (self.selected_product[1],)
            self.set_values()
        else:
            self.insert_mode = True
            msg = "Insert new product"
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
        self.price.set(self.selected_product[5])
        self.stock.set(self.selected_product[6])
        self.enable.set(self.selected_product[7])

    def get_values(self,):

        return (self.txtProduct.get(),
                self.dict_suppliers[self.cbSuppliers.current()],
                self.dict_categories[self.cbCategories.current()],
                self.txtPackage.get(),
                self.price.get(),
                self.stock.get(),
                self.enable.get())        
        
    def on_save(self, evt):

        if self.on_fields_control()==False:

            msg = "Please fill all fields."
            messagebox.showwarning(self.engine.title,msg)

        else:
       
            if messagebox.askyesno(self.engine.title, "Do you want to save?",parent=self) == True:

                args =  self.get_values()

                if self.insert_mode == False:

                    sql = self.engine.get_update_sql('products','product_id')

                    args = self.engine.get_update_sql_args(args, self.selected_product[0])
                       
                elif self.insert_mode == True:

                        sql = self.engine.get_insert_sql('products',len(args))

                self.engine.write(sql,args)
                self.parent.on_open()
                self.on_cancel()

            else:
                msg = "Operation aborted."
                messagebox.showinfo(self.engine.title,msg)                
           

    def on_cancel(self,evt=None):
        self.destroy()

    
    def get_selected_category(self, event):
        
        index = self.cbCategories.current()
        category_id = self.dict_categories[index]
        sql = "SELECT * FROM products WHERE category_id =? ORDER BY product DESC"
        args = (category_id,)
        self.set_tree_values(sql, args)            
        
    def set_categories(self):

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
        
        
    def set_suppliers(self,):

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

    def validate(self, action, index, value_if_allowed,
                 prior_value, text, validation_type,
                 trigger_type, widget_name):
        # action=1 -> insert
        if(action=='1'):
            if text in '.0123456789':
                try:
                    float(value_if_allowed)
                    return True
                except ValueError:
                    return False
            else:
                return False
        else:
            return True          

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
