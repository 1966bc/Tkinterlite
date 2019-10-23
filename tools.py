#!/usr/bin/python3
#-----------------------------------------------------------------------------
# project:  tkinterlite
# authors:  1966bc
# mailto:   [giuseppe.costanzi@gmail.com]
# modify:   10/04/2017
#-----------------------------------------------------------------------------
import datetime
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import font

class Tools:
    def __init__(self, *args, **kwargs):

        self.args = args
        self.kwargs = kwargs

    def __str__(self):
        return "class: %s" % (self.__class__.__name__, )

    def on_log(self, container, function, exc_value, exc_type, module):

        now = datetime.datetime.now()
        log_text = "{0}\n {1}\n{2}\n{3}\n{4}\n\n".format(now, function, exc_value, exc_type, module)
        log_file = open('log.txt', 'a')
        log_file.write(log_text)
        log_file.close()

        msg = "Except type: {0}\n\nModule:{1}\n\nFunction{2}\n\n{3}".format(exc_type, module, function, exc_value)
        messagebox.showwarning(self.title, msg, parent=container)



    def get_rgb(self, r, g, b):
        """translates an rgb tuple of int to a tkinter friendly color code"""
        return "#%02x%02x%02x" % (r, g, b)

    def center_me(self, container):

        """center window on the screen"""
        x = (container.winfo_screenwidth() - container.winfo_reqwidth()) / 2
        y = (container.winfo_screenheight() - container.winfo_reqheight()) / 2
        container.geometry("+%d+%d" % (x, y))


    def cols_configure(self, w):

        w.columnconfigure(0, weight=1)
        w.columnconfigure(1, weight=1)
        w.columnconfigure(2, weight=1)

    def get_init_ui(self, container):
        """All insert,update modules have this same configuration on init_ui.
           A Frame, a columnconfigure and a grid method.
           So, why rewrite every time?"""
        w = self.get_frame(container)
        self.cols_configure(w)
        w.grid(row=0, column=0, sticky=tk.N+tk.W+tk.S+tk.E)

        return w

    def get_frame(self, container, padding=None):
        return ttk.Frame(container, padding=padding)


    def get_label_frame(self, container, text=None, ):
        return ttk.LabelFrame(container, text=text,)

    def get_button(self, container, text, row=None, col=None):

        w = ttk.Button(container, text=text, underline=0)

        if row is not None:
            w.grid(row=row, column=col, sticky=tk.W+tk.E, padx=5, pady=5)
        else:
            w.pack(fill=tk.X, padx=5, pady=5)

        return w

    def get_radio_buttons(self, container, text, ops, v, callback=None):

        w = self.get_label_frame(container, text=text)

        for index, text in enumerate(ops):
            ttk.Radiobutton(w,
                            text=text,
                            variable=v,
                            command=callback,
                            value=index,).pack(anchor=tk.W)
        return w

    def get_label(self, container, text, textvariable=None, anchor=None, args=()):

        w = ttk.Label(container,
                      text=text,
                      textvariable=textvariable,
                      anchor=anchor)

        if args:
            w.grid(row=args[0], column=args[1], sticky=args[2])
        else:
            w.pack(fill=tk.X, padx=5, pady=5)

        return w

    def get_spin_box(self, container, text, frm, to, width, var=None, callback=None):

        w = self.get_label_frame(container, text=text,)

        tk.Spinbox(w, bg='white',
                   from_=frm,
                   to=to,
                   justify=tk.CENTER,
                   width=width,
                   wrap=False,
                   insertwidth=1,
                   textvariable=var).pack(anchor=tk.CENTER)
        return w



    def set_font(self, family, size, weight=None):

        if weight is not None:
            weight = weight
        else:
            weight = tk.NORMAL

        return font.Font(family=family, size=size, weight=weight)

    def get_listbox(self, container, height=None, width=None):


        sb = ttk.Scrollbar(container, orient=tk.VERTICAL)

        w = tk.Listbox(container,
                       relief=tk.GROOVE,
                       selectmode=tk.BROWSE,
                       exportselection=0,
                       height=height,
                       width=width,
                       background='white',
                       font='TkFixedFont',
                       yscrollcommand=sb.set,)

        sb.config(command=w.yview)

        w.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        sb.pack(fill=tk.Y, expand=1)

        return w

    def get_save_cancel(self, caller, container):

        caller.btnSave = self.get_button(container, "Save", 0, 2)
        caller.btnSave.bind("<Button-1>", caller.on_save)
        caller.btnSave.bind("<Return>", caller.on_save)
        caller.btCancel = self.get_button(container, "Close", 1, 2)
        caller.btCancel.bind("<Button-1>", caller.on_cancel)

        caller.bind("<Alt-s>", caller.on_save)
        caller.bind("<Alt-c>", caller.on_cancel)


    def get_export_cancel(self, caller, container):

        w = self.get_frame(container, 5)

        caller.btnExport = self.get_button(w, "Export", 0, 1,)
        caller.btnExport.bind("<Button-1>", caller.on_export)
        caller.btnExport.bind("<Return>", caller.on_export)

        caller.btCancel = self.get_button(w, "Close", 1, 1)
        caller.btCancel.bind("<Button-1>", caller.on_cancel)

        caller.bind("<Alt-e>", caller.on_export)
        caller.bind("<Alt-c>", caller.on_cancel)


        w.grid(row=0, column=2, sticky=tk.N+tk.E, padx=5, pady=5)


    def get_save_cancel_delete(self, caller, container):

        caller.btnSave = self.get_button(container, "Save", 0, 2)
        caller.btnSave.bind("<Button-1>", caller.on_save)
        caller.btnSave.bind("<Return>", caller.on_save)

        caller.btDelete = self.get_button(container, "Delete", 1, 2)
        caller.btDelete.bind("<Button-1>", caller.on_delete)

        caller.btCancel = self.get_button(container, "Close", 2, 2)
        caller.btCancel.bind("<Button-1>", caller.on_cancel)

        caller.bind("<Alt-s>", caller.on_save)
        caller.bind("<Alt-d>", caller.on_delete)
        caller.bind("<Alt-c>", caller.on_cancel)


    def get_add_edit_cancel(self, caller, container):

        caller.btnAdd = self.get_button(container, "Add")
        caller.btnAdd.bind("<Return>", caller.on_add)
        caller.btnAdd.bind("<Button-1>", caller.on_add)
        caller.btnEdit = self.get_button(container, "Edit")
        caller.btnEdit.bind("<Button-1>", caller.on_edit)
        caller.btCancel = self.get_button(container, "Close")
        caller.btCancel.bind("<Button-1>", caller.on_cancel)

        caller.bind("<Alt-a>", caller.on_add)
        caller.bind("<Alt-e>", caller.on_edit)
        caller.bind("<Alt-c>", caller.on_cancel)


    def on_fields_control(self, container):

        msg = "Please fill all fields."

        for w in container.winfo_children():
            for field in w.winfo_children():
                if type(field) in(ttk.Entry, ttk.Combobox):
                    #print(type(field),)
                    #for i in field.keys():
                    #    print (i)
                    if not field.get():
                        messagebox.showwarning(self.title, msg, parent=container)
                        field.focus()
                        return 0
                    elif type(field) == ttk.Combobox:
                          if field.get() not in field.cget('values'):
                              msg = "You can choice only values in the list."
                              messagebox.showwarning(self.title, msg, parent=container)
                              field.focus()
                              return 0

    def get_tree(self, container, cols, size=None, show=None):


        #this is a patch because with tkinter version with Tk 8.6.9 the color assignment with tags dosen't work
        #https://bugs.python.org/issue36468
        style = ttk.Style()
        style.map('Treeview',
                  foreground=self.fixed_map('foreground'),
                  background=self.fixed_map('background'))


        ttk.Style().configure("Treeview.Heading", background=self.get_rgb(240, 240, 237))
        ttk.Style().configure("Treeview.Heading", font=('Helvetica', 10 ))

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


    def get_validate_integer(self, caller):
        return (caller.register(self.validate_integer), '%d', '%P', '%S')

    def get_validate_float(self, caller):
        return (caller.register(self.validate_float), '%d', '%P', '%S')


    def validate_integer(self, action, value_if_allowed, text,):
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

    def validate_float(self, action, value_if_allowed, text,):
        # action=1 -> insert
        if action == '1':
            if text in '0123456789.':
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
    input('end')

if __name__ == "__main__":
    main()
