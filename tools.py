# -*- coding: utf-8 -*-
"""
project:  general purpose
mailto:   [giuseppecostanzi@gmail.com]
modify:   aestas MMXXI
@author:  1966bc
"""
import tkinter as tk
from tkinter import messagebox
from tkinter import font
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText


class Tools:
    def __init__(self,):
        super().__init__()

    def __str__(self):
        return "class: {0}".format((self.__class__.__name__, ))

    def set_style(self, theme):

        self.style = ttk.Style()

        self.style.theme_use(theme)

        self.style.configure(".", background=self.get_rgb(240, 240, 237),
                             font=('TkFixedFont'))
        
        self.style.configure("Product.TEntry",
                    foreground=self.get_rgb(0, 0, 255),
                    background=self.get_rgb(255, 255, 255))

        self.style.configure("Package.TEntry",
                    foreground=self.get_rgb(255, 0, 0),
                    background=self.get_rgb(255, 255, 255))
        
        self.style.configure('W.TFrame', background=self.get_rgb(240, 240, 237))

        self.style.configure('W.TButton',
                             background=self.get_rgb(240, 240, 237),
                             padding=5,
                             border=1,
                             relief=tk.RAISED,
                             font="TkFixedFont")

        self.style.configure('W.TLabel',
                             background=self.get_rgb(240, 240, 237),
                             padding=2,
                             font="TkFixedFont")

        self.style.configure('W.TRadiobutton',
                             background=self.get_rgb(240, 240, 237),
                             padding=4,
                             font="TkFixedFont")

        self.style.map('W.TCheckbutton',
        indicatoron=[('pressed', '#ececec'), ('selected', '#4a6984')])

        self.style.configure('W.TCombobox',
                             background=self.get_rgb(240, 240, 237),
                             font="TkFixedFont")

        self.style.configure('W.TLabelframe',
                             background=self.get_rgb(240, 240, 237),
                             relief=tk.GROOVE,
                             padding=2,
                             font="TkFixedFont")

        self.style.configure('StatusBar.TLabel',
                             background=self.get_rgb(240, 240, 237),
                             padding=2,
                             border=1,
                             relief=tk.SUNKEN,
                             font="TkFixedFont")

        self.style.map('Treeview', foreground=self.fixed_map('foreground'), background=self.fixed_map('background'))
        self.style.configure("Treeview.Heading", background=self.get_rgb(240, 240, 237), font=('TkHeadingFont', 10))
        self.style.layout("Treeview", [('Treeview.treearea', {'sticky': 'nswe'})]) 

        self.style.configure("Mandatory.TLabel",
                             foreground=self.get_rgb(0, 0, 255),
                             background=self.get_rgb(255, 255, 255))

    def get_rgb(self, r, g, b):
        """translates an rgb tuple of int to a tkinter friendly color code"""
        return "#%02x%02x%02x" % (r, g, b)

    def center_me(self, container):

        """center window on the screen"""
        x = (container.winfo_screenwidth() - container.winfo_reqwidth()) / 2
        y = (container.winfo_screenheight() - container.winfo_reqheight()) / 2
        container.geometry("+%d+%d" % (x, y))

    def cols_configure(self, w):

        w.columnconfigure(0, weight=4)
        w.columnconfigure(1, weight=1)
        w.rowconfigure(0, weight=0)
        w.rowconfigure(1, weight=0)
        #w.rowconfigure(2, weight=1)
        #w.rowconfigure(0, pad=8)

    def get_init_ui(self, container):
        """All insert,update modules have this same configuration on init_ui.
           A Frame, a columnconfigure and a grid method.
           So, why rewrite every time?"""
        w = ttk.Frame(container, style='W.TFrame')
        self.cols_configure(w)
        w.grid(row=0, column=0, sticky=tk.N+tk.W+tk.S+tk.E, padx=3, pady=6)

        return w

    def get_text_box(self, container, height=None, width=None, row=None, col=None):

        w = ScrolledText(container,
                         wrap=tk.WORD,
                         bg='light yellow',
                         relief=tk.GROOVE,
                         height=height,
                         width=width,
                         font='TkFixedFont',)

        if row is not None:
            #print(row,col)
            w.grid(row=row, column=1, sticky=tk.W)
        else:
            w.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

        return w

    def get_listbox(self, container, height=None, width=None, color=None):

        sb = ttk.Scrollbar(container, orient=tk.VERTICAL)

        w = tk.Listbox(container,
                       relief=tk.GROOVE,
                       selectmode=tk.BROWSE,
                       exportselection=0,
                       height=height,
                       width=width,
                       background=color,
                       font='TkFixedFont',
                       #bg="white",
                       #fg="black",
                       yscrollcommand=sb.set,)

        sb.config(command=w.yview)

        w.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        sb.pack(fill=tk.Y, expand=1)

        return w

    def on_fields_control(self, container):

        msg = "Please fill all fields."

        for w in container.winfo_children():
            for field in w.winfo_children():
                if type(field) in(ttk.Entry, tk.Entry, ttk.Combobox):
                    if not field.get():
                        messagebox.showwarning(container.master.title(), msg, parent=container)
                        field.focus()
                        return 0
                    elif type(field) == ttk.Combobox:
                        if field.get() not in field.cget('values'):
                            msg = "You can choice only a value of the list."
                            messagebox.showwarning(container.master.title(), msg, parent=container)
                            field.focus()
                            return 0

    def get_tree(self, container, cols, size=None, show=None):

        #this is a patch because with tkinter version with Tk 8.6.9 the color assignment with tags dosen't work
        #https://bugs.python.org/issue36468
        #style = ttk.Style()

        if size is not None:
            self.style.configure("Treeview",
                                 highlightthickness=0,
                                 bd=0,
                                 font=('TkHeadingFont', size)) # Modify the font of the body
        else:
            pass

        headers = []

        for col in cols:
            headers.append(col[1])
        del headers[0]

        if show is not None:
            w = ttk.Treeview(container, show=show)

        else:
            w = ttk.Treeview(container,)

        w['columns'] = headers
        w.tag_configure('is_enable', background='light gray')

        for col in cols:
            w.heading(col[0], text=col[1], anchor=col[2],)
            w.column(col[0], anchor=col[2], stretch=col[3], minwidth=col[4], width=col[5])

        sb = ttk.Scrollbar(container)
        sb.configure(command=w.yview)
        w.configure(yscrollcommand=sb.set)

        w.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        sb.pack(fill=tk.Y, expand=1)

        return w

    def fixed_map(self, option):

        style = ttk.Style()
        # Fix for setting text colour for Tkinter 8.6.9
        # From: https://core.tcl.tk/tk/info/509cafafae
        #
        # Returns the style map for 'option' with any styles starting with
        # ('!disabled', '!selected', ...) filtered out.

        # style.map() returns an empty list for missing options, so this
        # should be future-safe.
        return [elm for elm in style.map('Treeview', query_opt=option) if
                elm[:2] != ('!disabled', '!selected')]

    def get_validate_text(self, caller,):

        return (caller.register(self.validate_text),
                '%i', '%P', )

    def get_validate_integer(self, caller):
        return (caller.register(self.validate_integer),
                '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')

    def get_validate_float(self, caller):
        return (caller.register(self.validate_float),
                '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')


    def limit_chars(self, c, v, *args):
        #print(x,args)
        if len(v.get()) > c:
            v.set(v.get()[:-1])

    def validate_text(self, index, value_if_allowed):

        try:
            str(value_if_allowed)
            return True
        except ValueError:
            return False

    def validate_integer(self, action, index, value_if_allowed,
                         prior_value, text, validation_type,
                         trigger_type, widget_name):
        # action=1 -> insert
        if action == '1':
            if text in '0123456789':
                try:
                    int(value_if_allowed)
                    return True
                except ValueError:
                    return False
            else:
                return False
        else:
            return True

    def validate_float(self, action, index, value_if_allowed,
                       prior_value, text, validation_type,
                       trigger_type, widget_name):
        # action=1 -> insert
        if action == "1":
            if text in '0123456789.-+':
                try:
                    float(value_if_allowed)
                    return True
                except ValueError:
                    return False
            else:
                return False
        else:
            return True

    def on_to_assign(self, caller, evt=None):

        msg = "To do!"
        messagebox.showwarning(self.title, msg, )

    def get_widget_attributes(self, container):
        all_widgets = container.winfo_children()
        for widg in all_widgets:
            print('\nWidget Name: {}'.format(widg.winfo_class()))
            keys = widg.keys()
            for key in keys:
                print("Attribute: {:<20}".format(key), end=' ')
                value = widg[key]
                vtype = type(value)
                print('Value: {:<30} Type: {}'.format(value, str(vtype)))

    def get_widgets(self, container):
        all_widgets = container.winfo_children()
        for widg in all_widgets:
            print(widg)
            print('\nWidget Name: {}'.format(widg.winfo_class()))
            #keys = widg.keys()


def main():

    foo = Tools()
    print(foo)
    input('end')

if __name__ == "__main__":
    main()
