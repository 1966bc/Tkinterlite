# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# authors:  1966bc
# mailto:   [giuseppecostanzi@gmail.com]
# modify:   hiems MMXXI
# -------------------------------------------------------------------------------
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk


class Tools:
    """
    Tools is a class to set, get some usefull things about app widgets.
    """

    def __str__(self):
        return "class: {0}".format((self.__class__.__name__, ))

    def set_style(self, theme):
        """
        Recive theme name and set style for all widgets.
        """

        self.style = ttk.Style()

        self.style.theme_use(theme)

        self.style.configure(".",
                             background=self.get_rgb(240, 240, 237),
                             font=("TkFixedFont"))
        
        self.style.configure("App.TFrame")

        self.style.configure("Product.TEntry",
                             foreground=self.get_rgb(0, 0, 255),
                             background=self.get_rgb(255, 255, 255))

        self.style.configure("Package.TEntry",
                             foreground=self.get_rgb(255, 0, 0),
                             background=self.get_rgb(255, 255, 255))

        self.style.configure("App.TLabelframe",
                             relief=tk.GROOVE,
                             padding=2)

        self.style.configure("App.TButton",
                             padding=5,
                             border=1,
                             relief=tk.RAISED)

        self.style.configure("App.TLabel",
                             padding=2,
                             anchor=tk.W)

        self.style.configure("App.TRadiobutton",
                             padding=4)

        self.style.configure("App.TCombobox")

        self.style.configure("StatusBar.TLabel",
                             padding=2,
                             border=1,
                             relief=tk.SUNKEN)

        self.style.map("Treeview",
                       foreground=self.fixed_map("foreground"),
                       background=self.fixed_map("background"))

        self.style.configure("Treeview.Heading",
                             background=self.get_rgb(240, 240, 237),
                             font=("TkHeadingFont", 10))

        self.style.layout("Treeview", [("Treeview.treearea", {"sticky": "nswe"})])

        self.style.configure("Mandatory.TLabel",
                             foreground=self.get_rgb(0, 0, 255),
                             background=self.get_rgb(255, 255, 255))

    def get_rgb(self, r, g, b):
        """Translates an rgb tuple of int to a tkinter friendly color code"""
        return "#%02x%02x%02x" % (r, g, b)

    def center_me(self, container):
        """Center window on the screen"""
        x = (container.winfo_screenwidth() - container.winfo_reqwidth()) / 2
        y = (container.winfo_screenheight() - container.winfo_reqheight()) / 2
        container.geometry("+%d+%d" % (x, y))


    def on_fields_control(self, container, title):
        """Ceck if all entry widget are empty
            Chek even if a value set in a combobox is legal"""

        msg = "Please fill all fields."

        for w in container.winfo_children():
            for field in w.winfo_children():
                if type(field) in(ttk.Entry, tk.Entry, ttk.Combobox):
                    if not field.get():
                        messagebox.showwarning(title, msg, parent=container)
                        field.focus()
                        return 0
                    elif type(field) == ttk.Combobox:
                        if field.get() not in field.cget("values"):
                            msg = "You can choice only a value of the list."
                            messagebox.showwarning(container.master.title(), msg, parent=container)
                            field.focus()
                            return 0

    def get_tree(self, container, cols, size=None, show=None):
        """Get a treeview"""
        #this is a patch because with tkinter version
        #with Tk 8.6.9 the color assignment with tags dosen't work
        #https://bugs.python.org/issue36468
        #style = ttk.Style()

        if size is not None:
            self.style.configure("Treeview",
                                 highlightthickness=0,
                                 bd=0,
                                 font=("TkHeadingFont", size)) # Modify the font of the body
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

        w["columns"] = headers

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
        return [elm for elm in style.map("Treeview", query_opt=option) if
                elm[:2] != ("!disabled", "!selected")]


    def get_validate_integer(self, caller):
        return (caller.register(self.validate_integer),
                "%d", "%i", "%P", "%s", "%S", "%v", "%V", "%W")

    def get_validate_float(self, caller):
        return (caller.register(self.validate_float),
                "%d", "%i", "%P", "%s", "%S", "%v", "%V", "%W")

    def validate_integer(self, action, index, value_if_allowed,
                         prior_value, text, validation_type,
                         trigger_type, widget_name):
    
        # action=1 -> insert
        if action == "1":
            if text in "0123456789":
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
            if text in "0123456789.-+":
                try:
                    float(value_if_allowed)
                    return True
                except ValueError:
                    return False
            else:
                return False
        else:
            return True

def main():

    foo = Tools()
    print(foo)
    input("end")

if __name__ == "__main__":
    main()
