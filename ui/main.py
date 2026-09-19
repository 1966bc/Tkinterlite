# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# project:  Tkinterlite
# authors:  Giuseppe Costanzi (1966bc)
# licence:  GPL-3.0-or-later, see LICENSE
# -----------------------------------------------------------------------------
"""The main window: the products, filtered by category or supplier.

The module keeps the name it has had since 2017, a homage to C's main(); the
program itself starts from main() in tkinterlite.py.
"""

import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

import ui.about
import ui.categories
import ui.license
import ui.product
import ui.suppliers

#: One product with the names of its supplier and category, for the status bar.
SELECTED = ("SELECT p.product, s.company, c.category"
            "  FROM products AS p"
            "  LEFT JOIN suppliers AS s ON s.supplier_id = p.supplier_id"
            "  LEFT JOIN categories AS c ON c.category_id = p.category_id"
            " WHERE p.product_id = ?;")

#: The columns of the product list, as Tools.get_tree wants them:
#: (identifier, heading, anchor, stretch, minwidth, width).
COLUMNS = (("#0", "id", tk.W, False, 0, 0),
           ("#1", "Product", tk.W, True, 100, 100),
           ("#2", "Package", tk.W, True, 100, 100),
           ("#3", "Stock", tk.CENTER, True, 20, 20),
           ("#4", "Price", tk.CENTER, True, 20, 20))


class Main(ttk.Frame):
    """The products, a combo to filter them by category or supplier, and the menus."""

    TABLE = "products"

    #: A product with nothing in stock is drawn on this colour.
    OUT_OF_STOCK = (255, 160, 122)

    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent
        self.engine = parent.engine
        #: 0 filters by category, 1 by supplier.
        self.option_id = tk.IntVar()
        #: Position in the combo -> category_id or supplier_id, filled by set_combo_values.
        self.dict_combo_values = {}
        #: The status bar: the selected product on the left, the clock on the right.
        self.selected_text = tk.StringVar()
        self.clock_text = tk.StringVar()
        self.init_menu()
        self.init_toolbar()
        self.init_status_bar()
        self.init_ui()
        self.set_size()
        # The Observer at work: this window is told when a product is saved,
        # and when a category or a supplier is, because its combo shows them.
        # Whoever saves does not know this window exists.
        self.engine.events.subscribe("products", self.on_products_changed)
        self.engine.events.subscribe("categories", self.on_combo_changed)
        self.engine.events.subscribe("suppliers", self.on_combo_changed)
        self.check_clock()

    def init_menu(self):
        """The menu bar. Its colours come from Tools.set_classic, like every menu."""
        m_main = tk.Menu(self, bd=1)
        m_file = tk.Menu(m_main, tearoff=0, bd=1)
        m_database = tk.Menu(m_file, tearoff=0, bd=1)
        m_tools = tk.Menu(m_main, tearoff=0, bd=1)
        m_about = tk.Menu(m_main, tearoff=0, bd=1)

        for label, menu in (("File", m_file), ("Tools", m_tools), ("?", m_about)):
            m_main.add_cascade(label=label, underline=0, menu=menu)

        m_file.add_cascade(label="Database", underline=0, menu=m_database)
        for label, command in (("Dump", self.on_dump), ("Vacuum", self.on_vacuum)):
            m_database.add_command(label=label, underline=0, command=command)
        m_file.add_command(label="Log", underline=0, command=self.on_log)
        m_file.add_separator()
        m_file.add_command(label="Exit", underline=0, command=self.parent.on_exit)

        for label, command in (("Categories", self.on_categories),
                               ("Suppliers", self.on_suppliers)):
            m_tools.add_command(label=label, underline=0, command=command)

        for label, command in (("About", self.on_about),
                               ("License", self.on_license),
                               ("Python", self.on_python_version),
                               ("Tkinter", self.on_tkinter_version)):
            m_about.add_command(label=label, underline=0, command=command)

        self.parent.config(menu=m_main)

    def init_toolbar(self):

        background = self.engine.tools.get_rgb(*self.engine.tools.BACKGROUND)
        toolbar = tk.Frame(self, bd=1, relief=tk.RAISED, bg=background)

        # Kept on self: a PhotoImage that only a local variable points to is
        # collected, and the button goes blank.
        self.img_exit = tk.PhotoImage(data=self.engine.get_icon("exit"))
        self.img_info = tk.PhotoImage(data=self.engine.get_icon("info"))

        for image, command in ((self.img_exit, self.parent.on_exit),
                               (self.img_info, self.on_about)):
            tk.Button(toolbar, width=20, image=image, relief=tk.FLAT, bg=background,
                      command=command).pack(side=tk.LEFT, padx=2, pady=2)

        toolbar.pack(side=tk.TOP, fill=tk.X)

    def init_status_bar(self):
        """What changes on the left, the time on the right.

        The frame carries the sunken edge, as Tools.set_style asks: the style
        holds the colours, and what a strip looks like is written where it is
        built.
        """
        frm_status = ttk.Frame(self, style="StatusBar.TFrame", borderwidth=1, relief=tk.SUNKEN)
        ttk.Label(frm_status,
                  textvariable=self.selected_text,
                  style="StatusBar.TLabel",
                  anchor=tk.W).pack(side=tk.LEFT, fill=tk.X, expand=1)
        ttk.Label(frm_status,
                  textvariable=self.clock_text,
                  style="StatusBar.TLabel",
                  anchor=tk.E).pack(side=tk.RIGHT)
        frm_status.pack(side=tk.BOTTOM, fill=tk.X)

    def init_ui(self):

        frm_main = ttk.Frame(self, style="App.TFrame")
        frm_left = ttk.Frame(frm_main, style="App.TFrame", padding=8)

        self.lbl_products = ttk.LabelFrame(frm_left, style="App.TLabelframe", text="Products")
        self.lst_products = self.engine.tools.get_tree(self.lbl_products, COLUMNS)
        self.lst_products.tag_configure("out_of_stock",
                                        background=self.engine.tools.get_rgb(*self.OUT_OF_STOCK))
        self.lst_products.bind("<<TreeviewSelect>>", self.on_select)
        self.lst_products.bind("<Double-1>", self.on_edit)

        self.lbl_combo = ttk.LabelFrame(frm_left, style="App.TLabelframe", padding=2)
        self.cb_filter = self.engine.tools.get_combo(self.lbl_combo)
        self.cb_filter.bind("<<ComboboxSelected>>", self.on_filter)
        self.cb_filter.pack(side=tk.TOP, anchor=tk.W, fill=tk.X, expand=1)
        # Packed before the products, so a short window shortens the list
        # (which scrolls) instead of squeezing the combo out.
        self.lbl_combo.pack(side=tk.BOTTOM, anchor=tk.W, fill=tk.X, pady=5, expand=0)
        self.lbl_products.pack(fill=tk.BOTH, expand=1)

        frm_right = ttk.Frame(frm_main, style="App.TFrame", padding=4)

        # Add, as in the lists: windows that do the same thing say it the same way.
        buttons = self.engine.tools.get_button_column(frm_right,
                                                      (("Reset", self.on_reset),
                                                       ("Add", self.on_add),
                                                       ("Edit", self.on_edit),
                                                       ("Close", self.parent.on_exit)),
                                                      window=self.parent)
        buttons.pack(fill=tk.X)

        frm_filter = ttk.LabelFrame(frm_right, style="App.TLabelframe", text="Filter by")
        for value, text in enumerate(("Categories", "Suppliers")):
            ttk.Radiobutton(frm_filter,
                            style="App.TRadiobutton",
                            text=text,
                            variable=self.option_id,
                            command=self.set_combo_values,
                            value=value).pack(anchor=tk.W)
        frm_filter.pack()

        frm_right.pack(side=tk.RIGHT, fill=tk.Y, expand=0)
        frm_left.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        frm_main.pack(fill=tk.BOTH, expand=1)

    def set_size(self):
        """The size written in tkinterlite.ini, centred on the screen."""
        config = self.engine.config
        self.engine.tools.set_geometry(self.parent,
                                       config.get_int("window", "width"),
                                       config.get_int("window", "height"))

    def on_open(self, evt=None):

        self.on_reset()

    def on_reset(self, evt=None):
        """Every product, and the combo emptied."""
        self.set_products("SELECT * FROM products ORDER BY product ASC;", ())
        self.set_combo_values()

    def on_filter(self, evt=None):
        """The products of the category or supplier chosen in the combo."""
        row_id = self.engine.tools.get_combo_id(self.cb_filter, self.dict_combo_values)

        if row_id is not None:
            if self.option_id.get() == 0:
                field = "category_id"
            else:
                field = "supplier_id"
            sql = "SELECT * FROM products WHERE {0} = ? ORDER BY product ASC;".format(field)
            self.set_products(sql, (row_id,))
        else:
            self.on_reset()

    def set_products(self, sql, args):
        """Fill the list: disabled products in grey, those out of stock in salmon."""
        tools = self.engine.tools

        for item in self.lst_products.get_children():
            self.lst_products.delete(item)

        for row in self.engine.db.read(True, sql, args):
            tags = tools.get_enable_tags(row["enable"])
            if row["enable"] and row["stock"] < 1:
                tags = ("out_of_stock",)
            self.lst_products.insert("", tk.END,
                                     iid=row["product_id"], text=row["product_id"],
                                     values=(row["product"], row["package"],
                                             row["stock"], row["price"]),
                                     tags=tags)

        self.lbl_products["text"] = "Products {0}".format(len(self.lst_products.get_children()))
        self.on_select()

    def on_select(self, evt=None):
        """One click on a product: its supplier and category, in the status bar.

        Also called when the list is read again, and when the Observer lands on
        a row: selecting from code fires <<TreeviewSelect>> too. With nothing
        selected the status bar is left empty.
        """
        text = ""
        selection = self.lst_products.selection()

        if selection:
            row = self.engine.db.read(False, SELECTED, (int(selection[0]),))
            text = "{0}: {1}, {2}".format(row["product"], row["company"], row["category"])

        self.selected_text.set(text)

    def set_combo_values(self):
        """Fill the combo with the enabled categories, or suppliers."""
        if self.option_id.get() == 0:
            self.lbl_combo["text"] = "Categories"
            sql = ("SELECT category_id AS id, category AS caption"
                   "  FROM categories"
                   " WHERE enable = 1"
                   " ORDER BY category;")
        else:
            self.lbl_combo["text"] = "Suppliers"
            sql = ("SELECT supplier_id AS id, company AS caption"
                   "  FROM suppliers"
                   " WHERE enable = 1"
                   " ORDER BY company;")

        self.dict_combo_values.clear()
        captions = []
        for index, row in enumerate(self.engine.db.read(True, sql, ())):
            self.dict_combo_values[index] = row["id"]
            captions.append(row["caption"])

        self.cb_filter.set("")
        self.engine.tools.set_combo(self.cb_filter, captions)
        self.engine.log.trace("dict_combo_values = {0}".format(self.dict_combo_values))

    def on_products_changed(self, product_id):
        """A product was saved or deleted: read the list again and land on it."""
        self.on_reset()
        self.engine.tools.set_selected(self.lst_products, product_id)

    def on_combo_changed(self, row_id):
        """A category or a supplier was saved: the combo shows them."""
        self.set_combo_values()

    def on_add(self, evt=None):
        self.engine.windows.replace("product", lambda: ui.product.UI(self))

    def on_edit(self, evt=None):

        selection = self.lst_products.selection()

        if selection:
            product_id = int(selection[0])
            self.engine.windows.replace("product", lambda: ui.product.UI(self, product_id))
        else:
            messagebox.showwarning(self.parent.title(), self.engine.no_selected, parent=self)

    # Lists and information windows are shown, not built twice; a product
    # dialog replaces the one open (windows.py).

    def on_categories(self):
        self.engine.windows.show("categories", lambda: ui.categories.UI(self))

    def on_suppliers(self):
        self.engine.windows.show("suppliers", lambda: ui.suppliers.UI(self))

    def on_license(self):
        self.engine.windows.show("license", lambda: ui.license.UI(self))

    def on_about(self):
        self.engine.windows.show("about", lambda: ui.about.UI(self, self.parent.info))

    def on_python_version(self):
        messagebox.showinfo(self.parent.title(), self.engine.get_python_version(), parent=self)

    def on_tkinter_version(self):
        text = "Tkinter patchlevel\n{0}".format(self.tk.call("info", "patchlevel"))
        messagebox.showinfo(self.parent.title(), text, parent=self)

    def on_dump(self):
        self.engine.tools.busy(self)
        # Into dumps/, beside the program, not into whatever folder it was started from.
        path = self.engine.db.dump(self.engine.get_file("dumps"))
        self.engine.tools.not_busy(self)
        messagebox.showinfo(self.parent.title(), "Dump written to\n{0}".format(path), parent=self)

    def on_vacuum(self):
        self.engine.tools.busy(self)
        self.engine.db.write("VACUUM;")
        self.engine.tools.not_busy(self)
        messagebox.showinfo(self.parent.title(), "Vacuum executed.", parent=self)

    def on_log(self):
        # The log is born with the first error: until then there is nothing to open, and saying
        # so is better than a menu item that does nothing.
        if self.engine.log.is_empty():
            messagebox.showinfo(self.parent.title(),
                                "The log is empty: nothing has gone wrong so far.",
                                parent=self)
        else:
            self.engine.open_log()

    def check_clock(self):
        """Show what the clock thread has sent, and look again in 200 ms.

        This runs on the main loop, the only thread that may touch a widget:
        the clock thread only fills a queue, and this empties it. after(200)
        asks often enough for a clock and costs nothing in between - the old
        version asked every millisecond.
        """
        for message in self.parent.clock.drain():
            self.clock_text.set(message)
        self.after(200, self.check_clock)
