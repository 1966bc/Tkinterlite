# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# project:  Main
# authors:  1966bc
# mailto:   [giuseppecostanzi@gmail.com]
# modify:   hiems MMXX
# -----------------------------------------------------------------------------
""" This is the main module of Main."""
import sys
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

import frames.license
import frames.product
import frames.categories
import frames.suppliers

from engine import Engine

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
        self.table = "products"
        self.primary_key = "product_id"
        self.combo_ops = ("Categories", "Suppliers")
        self.option_id = tk.IntVar()
        self.selected_product = None
        self.dict_combo_values = {}
        self.status_bar_text = tk.StringVar()

        self.cols = (["#0", "id", "w", False, 0, 0],
                     ["#1", "Product", "w", True, 100, 100],
                     ["#2", "Description", "w", True, 100, 100],
                     ["#3", "Stock", "center", True, 20, 20],
                     ["#4", "Price", "center", True, 20, 20],)

        self.init_menu()
        self.init_toolbar()
        self.init_status_bar()
        self.init_ui()
        self.center_ui()

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
            i.config(bg=self.nametowidget(".").engine.get_rgb(240, 240, 237),)
            i.config(fg="black")

        self.nametowidget(".").config(menu=m_main)


    def init_toolbar(self):

        toolbar = tk.Frame(self, bd=1, relief=tk.RAISED)

        img_exit = tk.PhotoImage(data=self.nametowidget(".").engine.get_icon("exit"))
        img_info = tk.PhotoImage(data=self.nametowidget(".").engine.get_icon("info"))

        exitButton = tk.Button(toolbar, width=20, image=img_exit,
                               relief=tk.FLAT, command=self.parent.on_exit)
        infoButton = tk.Button(toolbar, width=20, image=img_info,
                               relief=tk.FLAT, command=self.on_about)

        exitButton.image = img_exit
        infoButton.image = img_info

        exitButton.pack(side=tk.LEFT, padx=2, pady=2)
        infoButton.pack(side=tk.LEFT, padx=2, pady=2)

        toolbar.config(bg=self.nametowidget(".").engine.get_rgb(240, 240, 237))
        toolbar.pack(side=tk.TOP, fill=tk.X)

    def init_status_bar(self):

        self.status = ttk.Label(self,
                                textvariable=self.status_bar_text,
                                style='StatusBar.TLabel',
                                anchor=tk.W)
        self.status.pack(side=tk.BOTTOM, fill=tk.X)

    def init_ui(self):

        """create widgets"""
        f0 = ttk.Frame(self, style="App.TFrame")
        f1 = ttk.Frame(f0,
                       style="App.TFrame",
                       relief=tk.GROOVE,
                       borderwidth=1,
                       padding=8)
        #products
        #-----------------------------------------------------------------------
        self.lblProdutcs = ttk.LabelFrame(f1, text="Products",)
        self.lstProducts = self.nametowidget(".").engine.get_tree(self.lblProdutcs, self.cols,)
        self.lstProducts.tag_configure("is_enable", background="light gray")
        self.lstProducts.tag_configure("is_zero", background=self.nametowidget(".").engine.get_rgb(255, 160, 122))
        self.lstProducts.bind("<<TreeviewSelect>>", self.get_selected_product)
        self.lstProducts.bind("<Double-1>", self.on_double_click)
        self.lblProdutcs.pack(fill=tk.BOTH, expand=1)

        #categories
        #-----------------------------------------------------------------------
        self.lblCombo = ttk.LabelFrame(f1, style="W.TLabelframe", padding=2)
        self.cbCombo = ttk.Combobox(self.lblCombo, style="W.TCombobox")
        self.cbCombo.bind("<<ComboboxSelected>>", self.get_selected_combo_item)
        self.cbCombo.pack(side=tk.TOP, anchor=tk.W, fill=tk.X, expand=1)
        self.lblCombo.pack(side=tk.TOP, anchor=tk.W, fill=tk.X, pady=5, expand=0)

        #buttons and radio
        #-----------------------------------------------------------------------
        f2 = ttk.Frame(f0,
                       style="App.TFrame",
                       relief=tk.GROOVE,
                       borderwidth=1,
                       padding=8)

        bts = (("Reset", 0, self.on_reset, "<Alt-r>"),
               ("New", 0, self.on_add, "<Alt-n>"),
               ("Edit", 0, self.on_edit, "<Alt-e>"),
               ("Close", 0, self.parent.on_exit, "<Alt-c>"))

        for btn in bts:
            ttk.Button(f2,
                       style="W.TButton",
                       text=btn[0],
                       underline=btn[1],
                       command=btn[2],).pack(fill=tk.X, padx=5, pady=5)
            self.parent.bind(btn[3], btn[2])

        f4 = ttk.LabelFrame(f2, style="W.TLabelframe", text="Combo data", padding=2)

        for index, text in enumerate(self.combo_ops):
            ttk.Radiobutton(f4,
                            style="W.TRadiobutton",
                            text=text,
                            variable=self.option_id,
                            command=self.set_combo_values,
                            value=index,).pack(anchor=tk.W)

        f0.pack(fill=tk.BOTH, expand=1)
        f1.pack(side=tk.LEFT, fill=tk.BOTH, padx=5, pady=5, expand=1)
        f2.pack(side=tk.RIGHT, fill=tk.Y, padx=5, pady=5, expand=0)
        f4.pack()

    def center_ui(self):

        ws = self.nametowidget(".").winfo_screenwidth()
        hs = self.nametowidget(".").winfo_screenheight()
        # calculate position x, y
        d = self.nametowidget(".").engine.get_dimensions()
        w = int(d["w"])
        h = int(d["h"])
        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)
        self.nametowidget(".").geometry("%dx%d+%d+%d" % (w, h, x, y))

    def on_open(self, evt=None):

        self.on_reset()
        #Update clock
        self.periodic_call()

    def on_reset(self, evt=None):

        self.selected_product = None
        sql = "SELECT * FROM {0} ORDER BY product ASC;".format(self.table)
        self.set_tree_values(sql, ())
        self.set_combo_values()

    def on_add(self):
        frames.product.UI(self).on_open()

    def on_categories(self):
        frames.categories.UI(self).on_open()

    def on_suppliers(self):
        frames.suppliers.UI(self).on_open()

    def on_edit(self, evt=None):

        if self.lstProducts.focus():

            item_iid = self.lstProducts.selection()

            frames.product.UI(self, item_iid).on_open(self.selected_product,)

        else:
            messagebox.showwarning(self.nametowidget(".").title(),
                                   self.nametowidget(".").engine.no_selected,
                                   parent=self)

    def on_double_click(self, evt=None):

        self.on_edit(self)

    def get_selected_product(self, evt):

        if self.lstProducts.focus():
            item_iid = self.lstProducts.selection()
            pk = int(item_iid[0])
            self.selected_product = self.nametowidget(".").engine.get_selected(self.table, self.primary_key, pk)

    def get_selected_combo_item(self, evt=None):

        if self.cbCombo.current() != -1:

            index = self.cbCombo.current()
            selected_id = self.dict_combo_values[index]

            if self.option_id.get() != 1:
                sql = "SELECT * FROM products WHERE  category_id=? ORDER BY product;"
            else:
                sql = "SELECT * FROM products WHERE supplier_id =? ORDER BY product;"

            args = (selected_id,)
            self.set_tree_values(sql, args)
        else:
            self.on_open()

    def set_tree_values(self, sql, args):

        for i in self.lstProducts.get_children():
            self.lstProducts.delete(i)

        rs = self.nametowidget(".").engine.read(True, sql, args)

        if rs:

            for i in rs:

                if i[7] == 0:
                    tag_config = ("is_enable")
                elif i[6] < 1:
                    tag_config = ("is_zero")
                else:
                    tag_config = ("")

                self.lstProducts.insert("", tk.END, iid=i[0], text=i[0],
                                        values=(i[1], i[4], i[6], i[5]),
                                        tags=tag_config)

        s = "{0} {1}".format("Products", len(self.lstProducts.get_children()))

        self.lblProdutcs["text"] = s

    def set_combo_values(self):

        self.cbCombo.set("")

        index = 0
        values = []

        if self.option_id.get() != 1:
            self.lblCombo["text"] = "Categories"
            sql = "SELECT category_id, category\
                   FROM categories\
                   WHERE enable =1\
                   ORDER BY category;"
        else:
            self.lblCombo["text"] = "Suppliers"
            sql = "SELECT supplier_id, company\
                   FROM suppliers\
                   WHERE enable =1\
                   ORDER BY company;"

        rs = self.nametowidget(".").engine.read(True, sql, ())

        for i in rs:
            self.dict_combo_values[index] = i[0]
            index += 1
            values.append(i[1])

        self.cbCombo.set("")
        self.cbCombo["values"] = values

    def on_license(self):
        frames.license.UI(self).on_open()

    def on_python_version(self):
        s = self.nametowidget(".").engine.get_python_version()
        messagebox.showinfo(self.nametowidget(".").title(), s, parent=self)

    def on_tkinter_version(self):
        s = "Tkinter patchlevel\n{0}".format(self.nametowidget(".").tk.call("info", "patchlevel"))
        messagebox.showinfo(self.nametowidget(".").title(), s, parent=self)

    def on_about(self,):
        messagebox.showinfo(self.nametowidget(".").title(),
                            self.nametowidget(".").info,
                            parent=self)

    def on_dump(self):
        self.nametowidget(".").engine.busy(self)
        self.nametowidget(".").engine.dump()
        self.nametowidget(".").engine.not_busy(self)
        messagebox.showinfo(self.nametowidget(".").title(), "Dump executed.", parent=self)

    def on_vacuum(self):
        sql = "VACUUM;"
        self.nametowidget(".").engine.busy(self)
        self.nametowidget(".").engine.write(sql)
        self.nametowidget(".").engine.not_busy(self)
        messagebox.showinfo(self.nametowidget(".").title(), "Vacuum executed.", parent=self)

    def on_log(self,):
        self.nametowidget(".").engine.get_log_file()

    def periodic_call(self):

        self.parent.clock.check_queue(self.status_bar_text)

        if self.parent.clock.is_alive():
            self.after(1, self.periodic_call)


class App(tk.Tk):
    """Main Main Application start here"""
    def __init__(self, *args, **kwargs):
        super().__init__()

        self.engine = Engine()

        self.protocol("WM_DELETE_WINDOW", self.on_exit)
        self.set_title(kwargs["title"])
        self.engine.set_style(kwargs["theme"])
        self.set_icon()
        self.set_info()
        # set clock and start it.
        self.set_clock()

        w = Main(self)
        w.on_open()
        w.pack(fill=tk.BOTH, expand=1)

    def set_clock(self,):
        self.clock = self.engine.get_clock()
        self.clock.start()

    def set_title(self, title):
        s = "{0}".format(title)
        self.title(s)

    def set_icon(self):
        icon = tk.PhotoImage(data=self.engine.get_icon("app"))
        self.call("wm", "iconphoto", self._w, "-default", icon)

    def set_info(self,):
        msg = "{0}\nauthor: {1}\ncopyright: {2}\ncredits: {3}\nlicense: {4}\nversion: {5}\
               \nmaintainer: {6}\nemail: {7}\ndate: {8}\nstatus: {9}"
        info = msg.format(self.title(), __author__, __copyright__, __credits__, __license__, __version__, __maintainer__, __email__, __date__, __status__)
        self.info = info

    def on_exit(self, evt=None):
        if messagebox.askokcancel(self.title(), "Do you want to quit?", parent=self):
            self.engine.con.close()
            if self.clock is not None:
                self.clock.stop()
            self.destroy()

def main():
    #if you want pass a number of arbitrary args or kwargs...
    args = []

    for i in sys.argv:
        args.append(i)
    # ('clam', 'alt', 'default', 'classic')
    kwargs = {"title":"Tkinterlite", "theme":"default"}

    app = App(*args, **kwargs)

    app.mainloop()

if __name__ == "__main__":
    main()
