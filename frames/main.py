""" This is the main module of Tkinterlite."""
import sys
import threading
import queue
import datetime
import time
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

import frames.product
import frames.categories
import frames.suppliers

from engine import Engine

__author__ = "1966bc aka giuseppe costanzi"
__copyright__ = "Copyleft"
__credits__ = ["hal9000",]
__license__ = "GNU GPL Version 3, 29 June 2007"
__version__ = "42"
__maintainer__ = "1966bc"
__email__ = "giuseppecostanzi@gmail.com"
__date__ = "2020-02-29"
__status__ = "Production"


class ClockThread(threading.Thread):

    def __init__(self, queue, engine):
        threading.Thread.__init__(self)

        self.queue = queue
        self.check = True
        self.engine = engine

    def stop(self):
        self.check = False

    def run(self):

        while self.check:
            s = "Astral date: "
            t = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            #print(t)
            msg = s+t
            time.sleep(1)
            self.queue.put(msg)


class Tkinterlite(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__()

        self.parent = parent
        self.engine = kwargs["engine"]
        self.info = kwargs["info"]
        self.args = args
        self.queue = queue.Queue()
        self.clock = None

        self.ops = ("Categories", "Suppliers")
        self.status_bar_text = tk.StringVar()
        self.filter_id = tk.IntVar()

        self.cols = (["#0", "id", "w", False, 0, 0],
                     ["#1", "Product", "w", True, 100, 100],
                     ["#2", "Description", "w", True, 100, 100],
                     ["#3", "Stock", "center", True, 20, 20],
                     ["#4", "Price", "center", True, 20, 20],)

        self.init_menu()
        self.init_toolbar()
        self.init_ui()
        self.init_status_bar()
        self.center_ui()

    def init_menu(self):

        m_main = tk.Menu(self, bd=1)

        m_file = tk.Menu(m_main, tearoff=0, bd=1)
        s_menu = tk.Menu(m_file)

        m_about = tk.Menu(m_main, tearoff=0, bd=1)

        m_main.add_cascade(label="File", underline=0, menu=m_file)
        m_main.add_cascade(label="?", underline=0, menu=m_about)

        m_file.add_cascade(label="Tools", menu=s_menu, underline=0)

        items = (("Categories", self.on_categories),
                 ("Suppliers", self.on_suppliers),)

        for i in items:
            s_menu.add_command(label=i[0], underline=0, command=i[1])

        m_file.add_separator()

        m_file.add_command(label="Exit", underline=0, command=self.parent.on_exit)

        m_about.add_command(label="About", underline=0, command=self.on_about)

        self.master.config(menu=m_main)

    def init_toolbar(self):

        toolbar = tk.Frame(self, bd=1, relief=tk.RAISED)

        img_exit = tk.PhotoImage(data=self.engine.get_exit__icon())
        img_info = tk.PhotoImage(data=self.engine.get_info_icon())

        exitButton = tk.Button(toolbar, width=20, image=img_exit,
                               relief=tk.FLAT, command=self.parent.on_exit)
        infoButton = tk.Button(toolbar, width=20, image=img_info,
                               relief=tk.FLAT, command=self.on_about)

        exitButton.image = img_exit
        infoButton.image = img_info

        exitButton.pack(side=tk.LEFT, padx=2, pady=2)
        infoButton.pack(side=tk.LEFT, padx=2, pady=2)

        toolbar.pack(side=tk.TOP, fill=tk.X)

    def init_status_bar(self):

        self.status = tk.Label(self.master,
                               textvariable=self.status_bar_text,
                               bd=1,
                               relief=tk.SUNKEN,
                               anchor=tk.W)
        self.status.pack(side=tk.BOTTOM, fill=tk.X)

    def init_ui(self):

        """create widgets"""

        self.pack(fill=tk.BOTH, expand=1)

        #products
        #-----------------------------------------------------------------------
        w = self.engine.get_frame(self, 8)

        self.lblProdutcs = ttk.LabelFrame(w, text="Products",)
        self.lstProducts = self.engine.get_tree(self.lblProdutcs, self.cols,)
        self.lstProducts.bind("<<TreeviewSelect>>", self.get_selected_product)
        self.lstProducts.bind("<Double-1>", self.on_double_click)
        self.lblProdutcs.pack(fill=tk.BOTH, expand=1)
        
        #categories
        #-----------------------------------------------------------------------
        self.lblCombo = ttk.LabelFrame(w,)

        self.cbCombo = ttk.Combobox(self.lblCombo)
        self.cbCombo.bind("<<ComboboxSelected>>", self.get_selected_combo_item)
        self.cbCombo.pack(side=tk.TOP, anchor=tk.W, fill=tk.X, expand=1)

        self.lblCombo.pack(side=tk.TOP, anchor=tk.W, fill=tk.X, pady=5, expand=0)

        w.pack(side=tk.LEFT, fill=tk.BOTH, anchor=tk.W, expand=1)

        #buttons and radio
        #-----------------------------------------------------------------------
        f = self.engine.get_frame(self, 8)

        bts = (("Reset", self.on_reset, "<Alt-r>"),
               ("New", self.on_add, "<Alt-n>"),
               ("Edit", self.on_edit, "<Alt-e>"),
               ("Close", self.parent.on_exit, "<Alt-c>"))

        for btn in bts:
            self.engine.get_button(f, btn[0]).bind("<Button-1>", btn[1])
            self.parent.bind(btn[2], btn[1])

        self.engine.get_radio_buttons(f,
                                      "Combo data",
                                      self.ops,
                                      self.filter_id,
                                      self.set_combo_values).pack()

        f.pack(side=tk.RIGHT, fill=tk.Y, expand=0)

    def center_ui(self):

        ws = self.master.winfo_screenwidth()
        hs = self.master.winfo_screenheight()
        # calculate position x, y
        d = self.engine.get_dimensions()
        w = int(d["w"])
        h = int(d["h"])
        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)
        self.master.geometry("%dx%d+%d+%d" % (w, h, x, y))

    def on_open(self, evt=None):

        self.on_reset()
        
        self.clock = ClockThread(self.queue, engine=self.engine)
        #notice this, we use it on exit function that is in App class....just to remember it.
        self.parent.clock = self.clock
        self.clock.start()
        self.periodic_call()

    def on_reset(self, evt=None):

        self.selected_product = None
        sql = "SELECT * FROM products ORDER BY product ASC"
        self.set_tree_values(sql, ())
        self.set_combo_values()
            
        
    def on_add(self, evt):
        frames.product.UI(self, engine=self.engine, index=None).on_open()

    def on_categories(self):
        frames.categories.UI(self, engine=self.engine).on_open()

    def on_suppliers(self):
        frames.suppliers.UI(self, engine=self.engine).on_open()

    def on_edit(self, evt):

        if self.lstProducts.focus():

            item_iid = self.lstProducts.selection()

            frames.product.UI(self,
                              engine=self.engine,
                              index=item_iid).on_open(self.selected_product,)

        else:
            messagebox.showwarning(self.master.title(),
                                   self.engine.no_selected,
                                   parent=self)

    def on_double_click(self, evt):

        self.on_edit(self)

    def get_selected_product(self, evt):

        if self.lstProducts.focus():
            item_iid = self.lstProducts.selection()
            pk = int(item_iid[0])
            self.selected_product = self.engine.get_selected("products",
                                                             "product_id",
                                                             pk)

    def get_selected_combo_item(self, evt):

        if self.cbCombo.current() != -1:

            index = self.cbCombo.current()
            selected_id = self.dict_combo_values[index]

            if self.filter_id.get() != 1:
                sql = "SELECT * FROM products WHERE supplier_id =? ORDER BY product"
            else:
                sql = "SELECT * FROM products WHERE category_id =? ORDER BY product"

            args = (selected_id,)
            self.set_tree_values(sql, args)
        else:
            self.on_open()

    def set_tree_values(self, sql, args):

        self.lstProducts.tag_configure("is_enable",
                                       background="light gray")
        self.lstProducts.tag_configure("is_zero",
                                       background=self.engine.get_rgb(255, 160, 122))

        for i in self.lstProducts.get_children():
            self.lstProducts.delete(i)

        rs = self.engine.read(True, sql, args)

        if rs:
            
            self.lblProdutcs["text"] = "Products %s"%len(rs)
            
            for i in rs:
                self.lstProducts.insert("",
                                        tk.END,
                                        iid=i[0],
                                        text=i[0],
                                        values=(i[1], i[4], i[6], i[5]))
                if i[7] == 0:
                    self.lstProducts.item(i[0], tags=("is_enable"))
                elif i[6] < 1:
                    self.lstProducts.item(i[0], tags=("is_zero"))
                      
        else:
            self.lblProdutcs["text"] = "Products 0"

    def set_combo_values(self):

        self.cbCombo.set("")

        index = 0
        self.dict_combo_values = {}
        values = []

        if self.filter_id.get() != 1:
            self.lblCombo["text"] = "Categories"
            sql = "SELECT category_id, category\
                   FROM categories\
                   WHERE enable =1\
                   ORDER BY category"
        else:
            self.lblCombo["text"] = "Suppliers"
            sql = "SELECT supplier_id, company\
                   FROM suppliers\
                   WHERE enable =1\
                   ORDER BY company"

        rs = self.engine.read(True, sql, ())

        for i in rs:
            self.dict_combo_values[index] = i[0]
            index += 1
            values.append(i[1])

        self.cbCombo.set("")
        self.cbCombo["values"] = values

    def on_about(self,):
        messagebox.showinfo(self.master.title(), self.info, parent=self)

    def periodic_call(self):

        self.check_queue()
        if self.clock.is_alive():
            self.after(1, self.periodic_call)
        else:
            pass

    def check_queue(self):

        while self.queue.qsize():
            try:
                x = self.queue.get(0)
                msg = "{0}".format(x)
                self.status_bar_text.set(msg)
            except queue.Empty:
                pass


class App(tk.Tk):
    """Tkinterlite Main Application start here"""
    def __init__(self, *args, **kwargs):
        super().__init__()

        self.protocol("WM_DELETE_WINDOW", self.on_exit)
        self.style = ttk.Style()
        self.engine = kwargs["engine"]
        self.set_title(kwargs["title"])
        self.set_icon()
        self.set_style(kwargs["style"])
        self.engine.title = self.title()

        w = Tkinterlite(self, *args, **kwargs)
        w.on_open()
        w.pack(fill=tk.BOTH, expand=1)

    def set_title(self, title):
        s = "{0} {1}".format(title, __version__)
        self.title(s)

    def set_style(self, style):
        self.style.theme_use(style)
        self.style.configure(".", background=self.engine.get_rgb(240, 240, 237))

    def set_icon(self):
        icon = tk.PhotoImage(data=self.engine.get_icon())
        self.call("wm", "iconphoto", self._w, "-default", icon)

    def on_exit(self, evt=None):
        if messagebox.askokcancel(self.title(), "Do you want to quit?", parent=self):
            self.engine.con.close()
            if self.clock is not None:
                self.clock.stop()
            self.destroy()


def main():

    args = []

    for i in sys.argv:
        args.append(i)

    kwargs = {"style":"clam", "title":"Tkinterlite", "engine":Engine(*args,)}

    msg = "{0}\nauthor: {1}\ncopyright: {2}\ncredits: {3}\nlicense: {4}\nversion: {5}\
           \nmaintainer: {6}\nemail: {7}\ndate: {8}\nstatus: {9}"
    info = msg.format(kwargs["title"], __author__, __copyright__, __credits__, __license__,
                      __version__, __maintainer__, __email__, __date__, __status__)

    kwargs["info"] = info

    app = App(*args, **kwargs)

    app.mainloop()

if __name__ == "__main__":
    main()
