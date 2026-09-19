# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# project:  tkinterlite
# authors:  1966bc
# mailto:   [giuseppecostanzi@gmail.com]
# modify:   hiems MMXXI
# -----------------------------------------------------------------------------
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox


class UI(tk.Toplevel):
    def __init__(self, parent, row_id=None):
        super().__init__(name="product")

        self.parent = parent
        self.engine = parent.engine
        #: The product being edited, None for a new one. The row itself is
        #: read from the database when the window opens, never taken from a
        #: copy held by the list.
        self.row_id = row_id
        self.resizable(0, 0)
        self.transient(parent)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=2)
        self.columnconfigure(2, weight=1)

        self.product = tk.StringVar()
        self.stock = tk.IntVar()
        self.package = tk.StringVar()
        self.price = tk.DoubleVar()
        self.enable = tk.BooleanVar()

        self.val_int = self.engine.tools.get_validate_integer(self)
        self.val_float = self.engine.tools.get_validate_float(self)
        self.engine.tools.center_me(self)
        self.init_ui()

    def init_ui(self):

        paddings = {"padx": 5, "pady": 5}
        
        self.frm_main = ttk.Frame(self, style="App.TFrame")
        self.frm_main.grid(row=0, column=0)

        frm_left = ttk.Frame(self.frm_main, style="App.TFrame")
        frm_left.grid(row=0, column=0, sticky=tk.NS, **paddings)

        r = 0
        c = 1
        ttk.Label(frm_left, style="App.TLabel", text="Product:",).grid(row=r, sticky=tk.W)
        self.txtProduct = ttk.Entry(frm_left,
                                    style="Product.TEntry",
                                    textvariable=self.product)
        self.txtProduct.grid(row=r, column=c, sticky=tk.EW, **paddings)

        r += 1
        ttk.Label(frm_left, style="App.TLabel", text="Suppliers:",).grid(row=r, sticky=tk.W)
        self.cbSuppliers = ttk.Combobox(frm_left,)
        self.cbSuppliers.grid(row=r, column=c, sticky=tk.EW, **paddings)

        r += 1
        ttk.Label(frm_left, style="App.TLabel", text="Categories:",).grid(row=r, sticky=tk.W)
        self.cbCategories = ttk.Combobox(frm_left,)
        self.cbCategories.grid(row=r, column=c, sticky=tk.EW, **paddings)

        r += 1
        ttk.Label(frm_left, style="App.TLabel", text="Package:").grid(row=r, sticky=tk.W)
        ent_package = ttk.Entry(frm_left, style="Package.TEntry", textvariable=self.package)
        ent_package.grid(row=r, column=c, sticky=tk.EW, **paddings)

        r += 1
        ttk.Label(frm_left, style="App.TLabel", text="Price:").grid(row=r, sticky=tk.W)
        ent_price = ttk.Entry(frm_left, justify=tk.CENTER, width=8, validate="key",
                              validatecommand=self.val_float, textvariable=self.price)
        ent_price.grid(row=r, column=c, sticky=tk.W, **paddings)

        r += 1
        ttk.Label(frm_left, style="App.TLabel", text="Stock:").grid(row=r, sticky=tk.W)
        ent_stock = ttk.Entry(frm_left, justify=tk.CENTER, width=8, validate="key",
                              validatecommand=self.val_int, textvariable=self.stock)
        ent_stock.grid(row=r, column=c, sticky=tk.W, **paddings)

        r += 1
        ttk.Label(frm_left, style="App.TLabel", text="Enable:").grid(row=r, sticky=tk.W)
        chk_enable = ttk.Checkbutton(frm_left, onvalue=1, offvalue=0, variable=self.enable,)
        chk_enable.grid(row=r, column=c, sticky=tk.EW, **paddings)

        frm_right = ttk.Frame(self.frm_main, style="App.TFrame")
        frm_right.grid(row=0, column=1, sticky=tk.NS, **paddings)

        r = 0
        c = 0
        btn_save = ttk.Button(frm_right, style="App.TButton", text="Save", underline=0, command=self.on_save,)
        self.bind("<Alt-s>", self.on_save)
        btn_save.grid(row=r, column=c, sticky=tk.EW, **paddings)

        if self.row_id is not None:
            r += 1
            btn = ttk.Button(frm_right, style="App.TButton", text="Delete", underline=0, command=self.on_delete,)
            self.bind("<Alt-c>", self.on_delete)
            btn.grid(row=r, column=c, sticky=tk.EW, **paddings)

        r += 1
        btn_cancel = ttk.Button(frm_right, style="App.TButton", text="Cancel", underline=0, command=self.on_cancel)
        self.bind("<Alt-c>", self.on_cancel)
        btn_cancel.grid(row=r, column=c, sticky=tk.EW, **paddings)

    def on_open(self):

        self.set_categories()
        self.set_suppliers()

        if self.row_id is not None:
            msg = "Update {0}".format(self.winfo_name().capitalize())
            self.set_values()
        else:
            msg = "Insert {0}".format(self.winfo_name().capitalize())
            self.enable.set(1)

        self.title(msg)
        self.txtProduct.focus()

    def set_values(self,):

        row = self.engine.db.get_selected(self.parent.table, self.parent.primary_key, self.row_id)
        self.product.set(row["product"])
        self.engine.tools.set_combo_id(self.cbSuppliers, self.dict_suppliers, row["supplier_id"])
        self.engine.tools.set_combo_id(self.cbCategories, self.dict_categories, row["category_id"])
        self.package.set(row["package"])
        self.price.set(row["price"])
        self.stock.set(row["stock"])
        self.enable.set(row["enable"])

    def get_values(self,):

        return {"product": self.product.get(),
                "supplier_id": self.dict_suppliers[self.cbSuppliers.current()],
                "category_id": self.dict_categories[self.cbCategories.current()],
                "package": self.package.get(),
                "price": self.price.get(),
                "stock": self.stock.get(),
                "enable": self.enable.get()}

    def on_save(self, evt=None):

        if self.engine.tools.on_fields_control(self.frm_main, self.nametowidget(".").title()):
            if messagebox.askyesno(self.nametowidget(".").title(),
                                   self.engine.ask_to_save,
                                   parent=self):
                self.save()
            else:
                messagebox.showinfo(self.nametowidget(".").title(),
                                    self.engine.abort,
                                    parent=self)

    def save(self):
        """Write the row, close, and tell whoever shows products which one."""
        values = self.get_values()

        if self.row_id is not None:
            sql, args = self.engine.db.get_update(self.parent.table, self.row_id, values)
            self.engine.db.write(sql, args)
            saved_id = self.row_id
        else:
            sql, args = self.engine.db.get_insert(self.parent.table, values)
            saved_id = self.engine.db.write(sql, args)

        self.on_cancel()
        self.engine.events.notify("products", saved_id)

    def on_delete(self, evt=None):

        sql = "DELETE FROM products WHERE product_id=?;"

        if messagebox.askyesno(self.nametowidget(".").title(),
                               self.engine.ask_to_delete,
                               parent=self):
            self.engine.db.write(sql, (self.row_id,))
            self.on_cancel()
            # No row to land on: it is gone.
            self.engine.events.notify("products", None)
        else:
            messagebox.showinfo(self.nametowidget(".").title(),
                                self.engine.abort,
                                parent=self)

    def set_categories(self):

        sql = "SELECT category_id, category FROM categories ORDER BY category ASC;"
        index = 0
        self.dict_categories = {}
        values = []
        rs = self.engine.db.read(True, sql, ())

        for i in rs:
            self.dict_categories[index] = i["category_id"]
            index += 1
            values.append(i["category"])

        self.cbCategories["values"] = values

    def set_suppliers(self,):

        sql = "SELECT supplier_id, company FROM suppliers ORDER BY company ASC;"
        index = 0
        self.dict_suppliers = {}
        values = []

        rs = self.engine.db.read(True, sql, ())

        for i in rs:
            self.dict_suppliers[index] = i["supplier_id"]
            index += 1
            values.append(i["company"])

        self.cbSuppliers["values"] = values

    def on_cancel(self, evt=None):
        self.destroy()
