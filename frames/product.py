# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# project:  tkinterlite
# authors:  1966bc
# mailto:   [giuseppecostanzi@gmail.com]
# modify:   hiems MMXX
# -----------------------------------------------------------------------------
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox


class UI(tk.Toplevel):
    def __init__(self, parent, index=None):
        super().__init__(name="product")

        self.parent = parent
        self.index = index
        self.resizable(0, 0)
        self.transient(parent)

        self.product = tk.StringVar()
        self.stock = tk.IntVar()
        self.package = tk.StringVar()
        self.price = tk.DoubleVar()
        self.enable = tk.BooleanVar()

        self.val_int = self.nametowidget(".").engine.get_validate_integer(self)
        self.val_float = self.nametowidget(".").engine.get_validate_float(self)
        self.nametowidget(".").engine.center_me(self)
        self.init_ui()

    def init_ui(self):

        f = self.nametowidget(".").engine.get_init_ui(self)

        r = 0
        c = 1
        ttk.Label(f, style='W.TLabel', text="Product:",).grid(row=r, sticky=tk.W)
        self.txtProduct = ttk.Entry(f,
                                    style="Product.TEntry",
                                    textvariable=self.product)
        self.txtProduct.grid(row=r, column=c, sticky=tk.W, padx=5, pady=5)

        r += 1
        ttk.Label(f, style='W.TLabel', text="Suppliers:",).grid(row=r, sticky=tk.W)
        self.cbSuppliers = ttk.Combobox(f,)
        self.cbSuppliers.grid(row=r, column=c, sticky=tk.W, padx=5, pady=5)

        r += 1
        ttk.Label(f, style='W.TLabel', text="Categories:",).grid(row=r, sticky=tk.W)
        self.cbCategories = ttk.Combobox(f,)
        self.cbCategories.grid(row=r, column=c, sticky=tk.W, padx=5, pady=5)

        r += 1
        ttk.Label(f, style='W.TLabel', text="Package:").grid(row=r, sticky=tk.W)
        w = ttk.Entry(f, style="Package.TEntry", textvariable=self.package)
        w.grid(row=r, column=c, sticky=tk.W, padx=5, pady=5)

        r += 1
        ttk.Label(f, style='W.TLabel', text="Price:").grid(row=r, sticky=tk.W)
        w = ttk.Entry(f, justify=tk.CENTER, width=8, validate="key",
                      validatecommand=self.val_float, textvariable=self.price)
        w.grid(row=r, column=c, sticky=tk.W, padx=5, pady=5)

        r += 1
        ttk.Label(f, style='W.TLabel', text="Stock:").grid(row=r, sticky=tk.W)
        w = ttk.Entry(f, justify=tk.CENTER, width=8, validate="key",
                      validatecommand=self.val_int, textvariable=self.stock)
        w.grid(row=r, column=c, sticky=tk.W, padx=5, pady=5)

        r += 1
        ttk.Label(f, style='W.TLabel', text="Enable:").grid(row=r, sticky=tk.W)
        w = ttk.Checkbutton(f, onvalue=1, offvalue=0, variable=self.enable,)
        w.grid(row=r, column=c, sticky=tk.W, padx=5, pady=5)

        r = 0
        c = 2
        btn = ttk.Button(f, style='W.TButton', text="Save", underline=0, command=self.on_save,)
        self.bind("<Alt-s>", self.on_save)
        btn.grid(row=r, column=c, sticky=tk.W, padx=5, pady=5)

        if self.index is not None:
            r += 1
            btn = ttk.Button(f, style='W.TButton', text="Delete", underline=0, command=self.on_delete,)
            self.bind("<Alt-c>", self.on_delete)
            btn.grid(row=r, column=c, sticky=tk.W, padx=5, pady=5)

        r += 1
        btn = ttk.Button(f, style='W.TButton', text="Cancel", underline=0, command=self.on_cancel,)
        self.bind("<Alt-c>", self.on_cancel)
        btn.grid(row=r, column=c, sticky=tk.W, padx=5, pady=5)

       
    def on_open(self, selected_item=None):

        self.set_categories()
        self.set_suppliers()

        if self.index is not None:
            self.selected_item = selected_item
            msg = "Update {0}".format(self.winfo_name().capitalize())
            self.set_values()
        else:
            msg = "Insert {0}".format(self.winfo_name().capitalize())
            self.enable.set(1)

        self.title(msg)
        self.txtProduct.focus()

    def set_values(self,):

        self.product.set(self.selected_item[1])

        key = next(key
                   for key, value
                   in self.dict_suppliers.items()
                   if value == self.selected_item[2])
        self.cbSuppliers.current(key)

        key = next(key
                   for key, value
                   in self.dict_categories.items()
                   if value == self.selected_item[3])
        self.cbCategories.current(key)

        self.package.set(self.selected_item[4])
        self.price.set(self.selected_item[5])
        self.stock.set(self.selected_item[6])
        self.enable.set(self.selected_item[7])

    def get_values(self,):

        return [self.product.get(),
                self.dict_suppliers[self.cbSuppliers.current()],
                self.dict_categories[self.cbCategories.current()],
                self.package.get(),
                self.price.get(),
                self.stock.get(),
                self.enable.get()]

    def on_save(self, evt=None):

        if self.nametowidget(".").engine.on_fields_control(self) == False: return

        if messagebox.askyesno(self.nametowidget(".").title(),
                               self.nametowidget(".").engine.ask_to_save,
                               parent=self) == True:

            args = self.get_values()

            if self.index is not None:

                sql = self.nametowidget(".").engine.get_update_sql(self.parent.table, self.parent.primary_key)

                args.append(self.selected_item[0])

            else:

                sql = self.nametowidget(".").engine.get_insert_sql(self.parent.table, len(args))

            product_id = self.nametowidget(".").engine.write(sql, args)
            self.parent.on_reset()

            if self.index is not None:
                self.parent.lstProducts.selection_set(self.index)
                self.parent.lstProducts.see(self.index)
            else:
                self.parent.lstProducts.selection_set(product_id)
                self.parent.lstProducts.see(product_id)

            self.on_cancel()

    def on_delete(self, evt=None):

        sql = "DELETE FROM products WHERE product_id=?;"

        if messagebox.askyesno(self.nametowidget(".").title(),
                               self.nametowidget(".").engine.ask_to_delete,
                               parent=self) == True:

            args = (self.selected_item[0],)
            self.nametowidget(".").engine.write(sql, args)
            self.parent.get_selected_combo_item()
            self.on_cancel()
        else:
            messagebox.showinfo(self.nametowidget(".").title(),
                                self.nametowidget(".").engine.abort,
                                parent=self)

    def set_categories(self):

        sql = "SELECT category_id, category FROM categories ORDER BY category ASC;"
        index = 0
        self.dict_categories = {}
        values = []
        rs = self.nametowidget(".").engine.read(True, sql, ())

        for i in rs:
            self.dict_categories[index] = i[0]
            index += 1
            values.append(i[1])

        self.cbCategories["values"] = values

    def set_suppliers(self,):

        sql = "SELECT supplier_id, company FROM suppliers ORDER BY company ASC;"
        index = 0
        self.dict_suppliers = {}
        values = []

        rs = self.nametowidget(".").engine.read(True, sql, ())

        for i in rs:
            self.dict_suppliers[index] = i[0]
            index += 1
            values.append(i[1])

        self.cbSuppliers["values"] = values

    def on_cancel(self, evt=None):
        self.destroy()
