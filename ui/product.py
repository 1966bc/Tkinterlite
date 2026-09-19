# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# project:  Tkinterlite
# authors:  Giuseppe Costanzi (1966bc)
# licence:  GPL-3.0-or-later, see LICENSE
# -----------------------------------------------------------------------------
"""One product: added, edited, or deleted.

The only table whose rows are deleted rather than disabled, so the only
dialog with a Delete button.
"""

import tkinter as tk
from tkinter import messagebox

from ui.dialog import Dialog


class UI(Dialog):
    NAME = "product"
    TABLE = "products"

    def init_fields(self):

        tools = self.engine.tools

        self.product = tk.StringVar()
        self.package = tk.StringVar()
        self.price = tk.DoubleVar()
        self.stock = tk.IntVar()
        #: Position in each combo -> primary key, filled below.
        self.dict_suppliers = {}
        self.dict_categories = {}

        txt_product = tools.get_entry(self.frm_fields, self.product)
        txt_product.configure(style="Product.TEntry")
        self.add_field("Product:", txt_product)

        self.cb_suppliers = tools.get_combo(self.frm_fields)
        self.add_field("Supplier:", self.cb_suppliers)

        self.cb_categories = tools.get_combo(self.frm_fields)
        self.add_field("Category:", self.cb_categories)

        txt_package = tools.get_entry(self.frm_fields, self.package)
        txt_package.configure(style="Package.TEntry")
        self.add_field("Package:", txt_package)

        self.add_field("Price:", tools.get_entry(self.frm_fields, self.price, "float"), tk.W)
        self.add_field("Stock:", tools.get_entry(self.frm_fields, self.stock, "integer"), tk.W)

        self.set_suppliers()
        self.set_categories()

    def get_buttons(self):
        """Delete as well, but only for a product that exists."""
        buttons = super().get_buttons()

        if self.row_id is not None:
            buttons = (("Save", self.on_save),
                       ("Delete", self.on_delete),
                       ("Cancel", self.on_cancel))

        return buttons

    def set_values(self, row):

        tools = self.engine.tools

        self.product.set(row["product"])
        tools.set_combo_id(self.cb_suppliers, self.dict_suppliers, row["supplier_id"])
        tools.set_combo_id(self.cb_categories, self.dict_categories, row["category_id"])
        self.package.set(row["package"])
        self.price.set(row["price"])
        self.stock.set(row["stock"])

    def get_values(self):

        tools = self.engine.tools

        return {"product": self.product.get(),
                "supplier_id": tools.get_combo_id(self.cb_suppliers, self.dict_suppliers),
                "category_id": tools.get_combo_id(self.cb_categories, self.dict_categories),
                "package": self.package.get(),
                "price": self.price.get(),
                "stock": self.stock.get()}

    def on_delete(self, evt=None):

        if messagebox.askyesno(self.nametowidget(".").title(),
                               self.engine.ask_to_delete,
                               parent=self):
            self.engine.db.write("DELETE FROM products WHERE product_id = ?;", (self.row_id,))
            self.on_cancel()
            # No row to land on: it is gone.
            self.engine.events.notify(self.TABLE, None)
        else:
            messagebox.showinfo(self.nametowidget(".").title(),
                                self.engine.abort,
                                parent=self)

    def set_suppliers(self):

        sql = "SELECT supplier_id, company FROM suppliers ORDER BY company ASC;"
        rs = self.engine.db.read(True, sql, ())

        self.dict_suppliers.clear()
        captions = []
        for index, row in enumerate(rs):
            self.dict_suppliers[index] = row["supplier_id"]
            captions.append(row["company"])

        self.engine.tools.set_combo(self.cb_suppliers, captions)

    def set_categories(self):

        sql = "SELECT category_id, category FROM categories ORDER BY category ASC;"
        rs = self.engine.db.read(True, sql, ())

        self.dict_categories.clear()
        captions = []
        for index, row in enumerate(rs):
            self.dict_categories[index] = row["category_id"]
            captions.append(row["category"])

        self.engine.tools.set_combo(self.cb_categories, captions)
