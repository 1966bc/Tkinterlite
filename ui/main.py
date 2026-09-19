# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# project:  Tkinterlite
# authors:  1966bc
# mailto:   [giuseppecostanzi@gmail.com]
# modify:   hiems MMXXI
# -----------------------------------------------------------------------------
""" This is the main module of Tkinterlite."""
import datetime
import os
import sys
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

import ui.license
import ui.product
import ui.categories
import ui.suppliers

from engine import Engine
from log import Log

#: The project directory, one level above ui/: the log lives there.
PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

__author__ = "1966bc"
__copyright__ = "Copyleft"
__credits__ = ["hal9000", ]
__license__ = "GNU GPL Version 3, 29 June 2007"
__version__ = "42"
__maintainer__ = "1966bc"
__email__ = "giuseppecostanzi@gmail.com"
__date__ = "hiems MMXXI"
__status__ = "production"


class Main(ttk.Frame):
    def __init__(self, parent):
        super().__init__()

        self.parent = parent
        self.engine = parent.engine
        self.table = "products"
        self.primary_key = "product_id"
        self.option_id = tk.IntVar()
        self.dict_combo_values = {}
        self.status_bar_text = tk.StringVar()
        self.init_menu()
        self.init_toolbar()
        self.init_status_bar()
        self.init_ui()
        self.center_ui()
        # The Observer at work: this window is told when a product is saved,
        # and when a category or a supplier is, because its combo shows them.
        # Whoever saves does not know this window exists.
        self.engine.events.subscribe("products", self.on_products_changed)
        self.engine.events.subscribe("categories", self.on_combo_changed)
        self.engine.events.subscribe("suppliers", self.on_combo_changed)
        self.update_clock()

    def init_menu(self):

        m_main = tk.Menu(self, bd=1)

        m_file = tk.Menu(m_main, tearoff=0, bd=1)
        m_tools = tk.Menu(m_main, tearoff=0, bd=1)
        s_databases = tk.Menu(m_file)
        m_about = tk.Menu(m_main, tearoff=0, bd=1)

        items = (("File", m_file),
                 ("Tools", m_tools),
                 ("?", m_about),)

        for i in items:
            m_main.add_cascade(label=i[0], underline=0, menu=i[1])

        m_file.add_cascade(label="Database", menu=s_databases, underline=0)

        items = (("Dump", self.on_dump),
                 ("Vacuum", self.on_vacuum),)

        for i in items:
            s_databases.add_command(label=i[0], underline=0, command=i[1])

        m_file.add_command(label="Log", underline=1, command=self.on_log)
        m_file.add_separator()

        m_file.add_command(label="Exit", underline=0, command=self.parent.on_exit)

        items = (("Categories", self.on_categories),
                 ("Suppliers", self.on_suppliers),)

        for i in items:
            m_tools.add_command(label=i[0], underline=0, command=i[1])

        items = (("About", self.on_about),
                 ("License", self.on_license),
                 ("Python", self.on_python_version),
                 ("Tkinter", self.on_tkinter_version),)

        for i in items:
            m_about.add_command(label=i[0], underline=0, command=i[1])

        for i in (m_main, m_file, s_databases, m_tools, m_about):
            i.config(bg=self.engine.tools.get_rgb(240, 240, 237),)
            i.config(fg="black")

        self.nametowidget(".").config(menu=m_main)

    def init_toolbar(self):

        toolbar = tk.Frame(self, bd=1, relief=tk.RAISED)

        img_exit = tk.PhotoImage(data=self.engine.get_icon("exit"))
        img_info = tk.PhotoImage(data=self.engine.get_icon("info"))

        exitButton = tk.Button(toolbar, width=20, image=img_exit,
                               relief=tk.FLAT, command=self.parent.on_exit)
        infoButton = tk.Button(toolbar, width=20, image=img_info,
                               relief=tk.FLAT, command=self.on_about)

        exitButton.image = img_exit
        infoButton.image = img_info

        exitButton.pack(side=tk.LEFT, padx=2, pady=2)
        infoButton.pack(side=tk.LEFT, padx=2, pady=2)

        toolbar.config(bg=self.engine.tools.get_rgb(240, 240, 237))
        toolbar.pack(side=tk.TOP, fill=tk.X)

    def init_status_bar(self):

        self.status = ttk.Label(self,
                                textvariable=self.status_bar_text,
                                style='StatusBar.TLabel',
                                anchor=tk.W)
        self.status.pack(side=tk.BOTTOM, fill=tk.X)

    def init_ui(self):

        """create widgets"""
        frm_main = ttk.Frame(self, style="App.TFrame")
        frm_left = ttk.Frame(frm_main, style="App.TFrame", padding=8)
        #products
        #-----------------------------------------------------------------------
        cols = (["#0", "id", "w", False, 0, 0],
                ["#1", "Product", "w", True, 100, 100],
                ["#2", "Description", "w", True, 100, 100],
                ["#3", "Stock", "center", True, 20, 20],
                ["#4", "Price", "center", True, 20, 20],)
        
        self.lblProdutcs = ttk.LabelFrame(frm_left, style="App.TLabelframe", text="Products",)
        self.lstProducts = self.engine.tools.get_tree(self.lblProdutcs, cols,)
        self.lstProducts.tag_configure("is_enable", background="light gray")
        self.lstProducts.tag_configure("is_zero", background=self.engine.tools.get_rgb(255, 160, 122))
        self.lstProducts.bind("<Double-1>", self.on_prduct_activated)

        #categories
        #-----------------------------------------------------------------------
        self.lblCombo = ttk.LabelFrame(frm_left, style="App.TLabelframe", padding=2)
        self.cbCombo = self.engine.tools.get_combo(self.lblCombo)
        self.cbCombo.bind("<<ComboboxSelected>>", self.get_selected_combo_item)
        self.cbCombo.pack(side=tk.TOP, anchor=tk.W, fill=tk.X, expand=1)
        # Packed before the products, so a short window shortens the list
        # (which scrolls) instead of squeezing the combo out.
        self.lblCombo.pack(side=tk.BOTTOM, anchor=tk.W, fill=tk.X, pady=5, expand=0)
        self.lblProdutcs.pack(fill=tk.BOTH, expand=1)

        #buttons and radio
        #-----------------------------------------------------------------------
        frm_right = ttk.Frame(frm_main, style="App.TFrame", padding=4)

        bts = (("Reset", 0, self.on_reset, "<Alt-r>"),
               ("New", 0, self.on_add, "<Alt-n>"),
               ("Edit", 0, self.on_prduct_activated, "<Alt-e>"),
               ("Close", 0, self.parent.on_exit, "<Alt-c>"))

        for btn in bts:
            ttk.Button(frm_right,
                       style="App.TButton",
                       text=btn[0],
                       underline=btn[1],
                       command=btn[2],).pack(fill=tk.X, padx=5, pady=5)
            self.parent.bind(btn[3], btn[2])

        w = ttk.LabelFrame(frm_right, style="App.TLabelframe", text="Combo data")
        voices = ("Categories", "Suppliers")
        for index, text in enumerate(voices):
            ttk.Radiobutton(w,
                            style="App.TRadiobutton",
                            text=text,
                            variable=self.option_id,
                            command=self.set_combo_values,
                            value=index,).pack(anchor=tk.W)

        w.pack()
        
        frm_right.pack(side=tk.RIGHT, fill=tk.Y, expand=0)
        frm_left.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        frm_main.pack(fill=tk.BOTH, expand=1)

    def center_ui(self):

        ws = self.nametowidget(".").winfo_screenwidth()
        hs = self.nametowidget(".").winfo_screenheight()
        # calculate position x, y
        config = self.engine.config
        w = config.get_int("window", "width")
        h = config.get_int("window", "height")
        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)
        self.nametowidget(".").geometry("%dx%d+%d+%d" % (w, h, x, y))

    def on_open(self, evt=None):

        self.on_reset()

    def on_reset(self, evt=None):

        sql = "SELECT * FROM {0} ORDER BY product ASC;".format(self.table)
        self.set_tree_values(sql, ())
        self.set_combo_values()

    def on_add(self, evt=None):
        ui.product.UI(self).on_open()

    def on_categories(self):
        ui.categories.UI(self).on_open()

    def on_suppliers(self):
        ui.suppliers.UI(self).on_open()

    def on_products_changed(self, product_id):
        """A product was saved or deleted: read the list again and land on it."""
        self.on_reset()
        self.engine.tools.set_selected(self.lstProducts, product_id)

    def on_combo_changed(self, row_id):
        """A category or a supplier was saved: the combo shows them."""
        self.set_combo_values()

    def on_prduct_activated(self, evt=None):

        selection = self.lstProducts.selection()

        if selection:
            ui.product.UI(self, int(selection[0])).on_open()
        else:
            messagebox.showwarning(self.nametowidget(".").title(),
                                   self.engine.no_selected,
                                   parent=self)

    
    def get_selected_combo_item(self, evt=None):

        if self.cbCombo.current() != -1:

            index = self.cbCombo.current()
            selected_id = self.dict_combo_values[index]

            if self.option_id.get() != 1:
                field = "category_id"
            else:
                field = "supplier_id"

            sql = "SELECT * FROM products WHERE  {0}=? ORDER BY product;".format(field)
            args = (selected_id,)
            self.set_tree_values(sql, args)
        else:
            self.on_open()

    def set_tree_values(self, sql, args):

        for i in self.lstProducts.get_children():
            self.lstProducts.delete(i)

        rs = self.engine.db.read(True, sql, args)

        if rs:

            for i in rs:

                if i["enable"] == 0:
                    tag_config = ("is_enable")
                elif i["stock"] < 1:
                    tag_config = ("is_zero")
                else:
                    tag_config = ("")

                self.lstProducts.insert("", tk.END,
                                        iid=i["product_id"], text=i["product_id"],
                                        values=(i["product"], i["package"],
                                                i["stock"], i["price"]),
                                        tags=tag_config)

        s = "{0} {1}".format("Products", len(self.lstProducts.get_children()))

        self.lblProdutcs["text"] = s

    def set_combo_values(self):

        self.cbCombo.set("")

        index = 0
        values = []

        if self.option_id.get() != 1:
            self.lblCombo["text"] = "Categories"
            sql = "SELECT category_id AS id, category AS caption\
                   FROM categories\
                   WHERE enable =1\
                   ORDER BY category;"
        else:
            self.lblCombo["text"] = "Suppliers"
            sql = "SELECT supplier_id AS id, company AS caption\
                   FROM suppliers\
                   WHERE enable =1\
                   ORDER BY company;"

        rs = self.engine.db.read(True, sql, ())

        for i in rs:
            self.dict_combo_values[index] = i["id"]
            index += 1
            values.append(i["caption"])

        self.cbCombo.set("")
        self.cbCombo["values"] = values

    def on_license(self):
        ui.license.UI(self).on_open()

    def on_python_version(self):
        s = self.engine.get_python_version()
        messagebox.showinfo(self.nametowidget(".").title(), s, parent=self)

    def on_tkinter_version(self):
        s = "Tkinter patchlevel\n{0}".format(self.nametowidget(".").tk.call("info", "patchlevel"))
        messagebox.showinfo(self.nametowidget(".").title(), s, parent=self)

    def on_about(self,):
        messagebox.showinfo(self.nametowidget(".").title(),
                            self.nametowidget(".").info,
                            parent=self)

    def on_dump(self):
        self.engine.tools.busy(self)
        # Into dumps/, beside the program, not into whatever folder it was started from.
        path = self.engine.db.dump(self.engine.get_file("dumps"))
        self.engine.tools.not_busy(self)
        messagebox.showinfo(self.nametowidget(".").title(),
                            "Dump written to\n{0}".format(path),
                            parent=self)

    def on_vacuum(self):
        sql = "VACUUM;"
        self.engine.tools.busy(self)
        self.engine.db.write(sql)
        self.engine.tools.not_busy(self)
        messagebox.showinfo(self.nametowidget(".").title(), "Vacuum executed.", parent=self)

    def on_log(self,):
        self.engine.open_log()

    def update_clock(self):
        """Write the time on the status bar, then ask Tk to do it again in a second.

        after() puts the next call in Tk's own queue of events, so there is no
        thread, no queue.Queue and no polling every millisecond: the main loop
        is the only thread there is, and the only one that touches widgets.
        """
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.status_bar_text.set("Astral date: {0}".format(now))
        self.after(1000, self.update_clock)


class App(tk.Tk):
    """Application start here"""
    def __init__(self, *args, **kwargs):
        super().__init__()

        self.engine = Engine(kwargs["log"])

        self.protocol("WM_DELETE_WINDOW", self.on_exit)
        self.set_title(kwargs["title"])
        self.engine.tools.set_style(self.engine.config.get("window", "theme"))
        self.set_icon()
        self.set_info()

        w = Main(self)
        w.on_open()
        w.pack(fill=tk.BOTH, expand=1)

    def set_title(self, title):
        s = "{0}".format(title)
        self.title(s)

    def set_icon(self):
        # The icon in 16, 32 and 48 pixels: the window manager picks the
        # size each place needs, so it is never scaled up and blurred.
        icons = [tk.PhotoImage(data=data) for data in self.engine.get_icons("app")]
        self.iconphoto(True, *icons)

    def set_info(self,):
        msg = "{0}\nauthor: {1}\ncopyright: {2}\ncredits: {3}\nlicense: {4}\nversion: {5}\
               \nmaintainer: {6}\nemail: {7}\ndate: {8}\nstatus: {9}"
        info = msg.format(self.title(), __author__, __copyright__, __credits__, __license__, __version__, __maintainer__, __email__, __date__, __status__)
        self.info = info

    def report_callback_exception(self, exc, val, tb):
        """Tkinter calls this for an exception raised in a callback.

        A button, a menu, an after(): every error coming out of the interface
        ends up here, the one place where it is handled. It is written to
        the log with its traceback and shown, so the application goes on and
        nothing fails in silence. Tkinter calls this from inside its own
        except block, which is what log.exception() needs.
        """
        self.engine.log.exception("{0}: {1}".format(exc.__name__, val))
        messagebox.showerror(self.title(),
                             "{0}\n\nDetails in {1}".format(val, self.engine.log.path),
                             parent=self)

    def on_exit(self, evt=None):
        if messagebox.askokcancel(self.title(), "Do you want to quit?", parent=self):
            self.engine.db.con.close()
            self.destroy()

def main():
    #if you want pass a number of arbitrary args or kwargs...
    args = []

    for i in sys.argv:
        args.append(i)

    # The log comes first, so that even a failure to start is written down.
    log = Log(os.path.join(PROJECT_DIR, "tkinterlite.log"))

    # Before the main loop there is no report_callback_exception yet:
    # a failure here is written to the log, shown, and raised again.
    try:
        kwargs = {"title": "Tkinterlite", "log": log}
        app = App(*args, **kwargs)
    except Exception as exc:
        log.exception("start failed: {0}".format(exc))
        messagebox.showerror("Tkinterlite", "{0}\n\nDetails in {1}".format(exc, log.path))
        raise

    app.mainloop()


if __name__ == "__main__":
    main()
