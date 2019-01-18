#!/usr/bin/env python3
#-----------------------------------------------------------------------------
# project:  all
# authors:  1966bc
# mailto:   [giuseppecostanzi@gmail.com]
# modify:   winter 2018                                                          
#-----------------------------------------------------------------------------
import tkinter as tk
from tkinter import messagebox
from tkinter import font
from tkinter import ttk 
import datetime
from datetime import date
import sys

class Tools(object):

    def __init__(self,*args, **kwargs):

        super(Tools, self).__init__( *args, **kwargs)
        
    def __str__(self):
        return "class: %s\nMRO: %s" % (self.__class__.__name__,  [x.__name__ for x in Widgets.__mro__])


    def get_rgb(self, r,g,b):
        """translates an rgb tuple of int to a tkinter friendly color code"""
        return "#%02x%02x%02x" % (r,g,b)



    def center_me(self, container):
        
        """center window on the screen"""
        x = (container.winfo_screenwidth() - container.winfo_reqwidth()) / 2
        y = (container.winfo_screenheight() - container.winfo_reqheight()) / 2
        container.geometry("+%d+%d" % (x, y))


    def cols_configure(self,w):
        
        w.columnconfigure(0, weight=1)
        w.columnconfigure(1, weight=1)
        w.columnconfigure(2, weight=1)   

    def get_init_ui(self, container):

        w = self.get_frame(container)
        self.cols_configure(w)
        w.grid(row=0, column=0, sticky=tk.N+tk.W+tk.S+tk.E)

        return w
        
    def get_frame(self, container):
        return tk.Frame(container, bd=1, padx=5, pady=5)
    
    def get_label_frame(self, container, text=None, ):
        return tk.LabelFrame(container, text=text, relief=tk.GROOVE, bd=1, padx=5, pady=5,)    

    def get_button(self, container, text, row=None, col=None):
        w = tk.Button(container, text=text, borderwidth=1, relief=tk.RAISED, padx=5, pady=5,)

        if row is not None:
            w.grid(row=row, column=col, sticky=tk.W+tk.E, padx=5, pady=5)
        else:
            w.pack(fill =tk.X, padx=5, pady=5)
        
        return w

    def get_label(self, container, text, bg=None, foreground=None,textvariable=None, anchor=None, args=()):
        
        w = tk.Label(container,
                     text=text,
                     bg=bg,
                     foreground=foreground,
                     textvariable=textvariable,
                     anchor=anchor)

        if args:
            w.grid(row=args[0], column=args[1], sticky=tk.W+tk.E, padx=5, pady=5)
        else:
            w.pack(fill = tk.X, padx=5, pady=5)
        
        return w

    def get_spin_box(self, container, text, frm, to, width, var=None, callback=None):

        w = self.get_label_frame(container, text = text,)
        
        tk.Spinbox(w,
                    bg='white',
                    from_=frm,
                    to=to,
                    justify=tk.CENTER,
                    width=width,
                    wrap=False,
                    insertwidth=1,
                    textvariable=var).pack(anchor=tk.CENTER) 
        return w

    def get_radio_buttons(self, container,text, ops, v, callback=None):

        w = self.get_label_frame(container, text = text)
        
        for index, text in enumerate(ops):
            tk.Radiobutton(w,
                            text=text,
                            bd=0,
                            padx = 5,
                            pady = 5,
                            relief=tk.GROOVE,
                            variable=v,
                            command=callback,
                            value=index).pack(anchor=tk.W)     
        return w

    def set_font(self,family,size,weight=None):

        if weight is not None:
            weight = weight
        else:
            weight =tk.NORMAL

        return font.Font(family=family,size=size,weight=weight)

    def get_listbox(self, container, height=None, width=None):


        sb = tk.Scrollbar(container,orient=tk.VERTICAL)
       
        w = tk.Listbox(container,
                    relief=tk.GROOVE,
                    selectmode=tk.BROWSE,
                    height=height,
                    width=width,
                    font='TkFixedFont',
                    yscrollcommand=sb.set,)
     
        sb.config(command=w.yview)
     
        w.pack(side=tk.LEFT,fill=tk.BOTH, expand =1) 
        sb.pack(fill=tk.Y, expand=1)

        return w

    def get_save_cancel(self, caller, container):

        bts = self.get_label_frame(container)
        bts.grid(row = 0, column = 2, sticky=tk.N+tk.W+tk.S+tk.E)
       
        caller.btnSave = self.get_button(bts, "Save",0,2)
        caller.btnSave.bind("<Button-1>", caller.on_save)
        caller.btnSave.bind("<Return>", caller.on_save)
    
        caller.btCancel = self.get_button(bts, "Close", 1,2)
        caller.btCancel.bind("<Button-1>", caller.on_cancel)

        return bts

    def get_save_cancel_delete(self, caller, container):

        bts = self.get_label_frame(container)
        bts.grid(row = 0, column = 2, sticky=tk.N+tk.W+tk.S+tk.E)
       
        caller.btnSave = self.get_button(bts, "Save",0,2)
        caller.btnSave.bind("<Button-1>", caller.on_save)
        caller.btnSave.bind("<Return>", caller.on_save)

        caller.btDelete = self.get_button(bts, "Delete", 1,2)
        caller.btDelete.bind("<Button-1>", caller.on_delete)
    
        caller.btCancel = self.get_button(bts, "Close", 2,2)
        caller.btCancel.bind("<Button-1>", caller.on_cancel)

        return bts

    def get_add_edit_cancel(self, caller, container):

        bts = self.get_label_frame(container)

        caller.btnAdd = self.get_button(bts, "Add")
        caller.btnAdd.bind("<Return>", caller.on_add)
        caller.btnAdd.bind("<Button-1>", caller.on_add)
        caller.btnEdit = self.get_button(bts, "Edit")
        caller.btnEdit.bind("<Button-1>", caller.on_edit)
        caller.btCancel = self.get_button(bts, "Close")
        caller.btCancel.bind("<Button-1>", caller.on_cancel)

        bts.pack(side=tk.RIGHT, fill=tk.Y, expand=0)

        return bts

    def get_calendar(self, caller, container, row=None):

        w = tk.LabelFrame(container, borderwidth=2)

        d = tk.Spinbox(w, bg='white', fg='blue',width=2, from_=1, to=31, textvariable=caller.day,relief=tk.GROOVE,)
        
        m = tk.Spinbox(w, bg='white',fg='blue', width=2, from_=1, to=12, textvariable=caller.month,relief=tk.GROOVE,)

        y = tk.Spinbox(w, bg='white', fg='blue',width=4, from_=1900, to=3000, textvariable=caller.year,relief=tk.GROOVE,)

        for p,i in enumerate((d,m,y)):
             if row is not None:
                 i.grid(row=0, column=p, padx=5, pady=5,sticky=tk.W)
             else:
                 i.pack(side=tk.LEFT, fill=tk.X, padx=2)
                 
                 
        if row is not None:
            w.grid(row = row, column = 1,sticky=tk.W)
        else:
            w.pack()

        return w

    def set_calendar_date(self, caller):

        today = date.today()

        caller.day.set(today.day)
        caller.month.set(today.month)
        caller.year.set(today.year)

    def get_calendar_date(self, caller):

        try:
            return datetime.date(caller.year.get(), caller.month.get(), caller.day.get())
        except:
            msg = "Format date error:\n%s"%str(sys.exc_info()[1])
            messagebox.showerror(self.title, msg)
            return False

    def get_timestamp(self, caller):

        try:
            t = datetime.datetime.now()
            return datetime.datetime(caller.year.get(), caller.month.get(), caller.day.get(), t.hour , t.minute, t.second)
            
        except:
            msg = "Format date error:\n%s"%str(sys.exc_info()[1])
            messagebox.showerror(self.title, msg)
            return False        
        
    def on_fields_control(self, fields):

        msg = "Please fill all fields."

        for field in fields:
            if not field.get():
                messagebox.showwarning(self.title,msg)
                field.focus()
                return 0

    def get_tree(self, container, cols,):

        ttk.Style().configure("Treeview.Heading",background = self.get_rgb(240,240,237))
        ttk.Style().configure("Treeview.Heading", font=('Helvetica', 10 ))

        
        headers = []

        for col in cols:
            headers.append(col[1])
        del headers[0]

        w = ttk.Treeview(container,)
        
        w['columns']=headers

        for col in cols:
            w.heading(col[0], text=col[1], anchor=col[2],)
            w.column(col[0], anchor=col[2], stretch=col[3],minwidth=col[4], width=col[5])
           
        sb = tk.Scrollbar(container)
        sb.configure(command=w.yview)
        w.configure(yscrollcommand=sb.set)

        w.pack(side=tk.LEFT, fill=tk.BOTH, expand =1)
        sb.pack(fill=tk.Y, expand=1)

        return w            

    def get_widget_attributes(self,container):
        all_widgets = container.winfo_children()
        for widg in all_widgets:
            print('\nWidget Name: {}'.format(widg.winfo_class()))
            keys = widg.keys()
            for key in keys:
                print("Attribute: {:<20}".format(key), end=' ')
                value = widg[key]
                vtype = type(value)
                print('Type: {:<30} Value: {}'.format(str(vtype), value))               
                       
def main():
    
    foo = Widgets()
    print(foo)                
    input('end')
       
if __name__ == "__main__":
    main()
