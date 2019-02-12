#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" This is the tools module. 
It helps to draw the windwos."""
import sys
import os
import datetime
from datetime import date
import tkinter as tk
from tkinter import messagebox
from tkinter import font
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
from PIL import Image, ImageTk


__author__ = "1966bc aka giuseppe costanzi"
__copyright__ = "Copyleft"
__credits__ = ["hal9000",]
__license__ = "GNU GPL Version 3, 29 June 2007"
__version__ = "4.2"
__maintainer__ = "1966bc"
__email__ = "giuseppecostanzi@gmail.com"
__date__ = "2018-12-25"
__status__ = "Production"

class Tools(object):

    def __init__(self,*args, **kwargs):

        super(Tools, self).__init__( *args, **kwargs)
        
    def __str__(self):
        return "class: %s\nMRO: %s" % (self.__class__.__name__,  [x.__name__ for x in Tools.__mro__])


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
            w.pack(fill =tk.X, padx=5, pady=5)
        
        return w

    def get_label(self, container, text ,textvariable=None, anchor=None, args=()):

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


    def get_scale(self, container, text, frm, to, width, var=None, callback=None):

        w = self.get_label_frame(container, text = text,)
        
        tk.Scale(w,
                 from_=frm,
                 to=to,
                 orient=tk.HORIZONTAL,
                 variable=var).pack(anchor=tk.N) 
        return w

    def get_radio_buttons(self, container, text, ops, v, callback=None):

        w = self.get_label_frame(container, text = text)
        
        for index, text in enumerate(ops):
            ttk.Radiobutton(w,
                            text=text,
                            variable=v,
                            command=callback,
                            value=index,).pack(anchor=tk.W)     
        return w

    def set_font(self,family,size,weight=None):

        if weight is not None:
            weight = weight
        else:
            weight =tk.NORMAL

        return font.Font(family=family,size=size,weight=weight)

    def get_listbox(self, container, height=None, width=None):


        sb = ttk.Scrollbar(container,orient=tk.VERTICAL)
       
        w = tk.Listbox(container,
                    relief=tk.GROOVE,
                    selectmode=tk.BROWSE,
                    height=height,
                    width=width,
                    background = 'white',
                    font='TkFixedFont',
                    yscrollcommand=sb.set,)
     
        sb.config(command=w.yview)
     
        w.pack(side=tk.LEFT,fill=tk.BOTH, expand =1) 
        sb.pack(fill=tk.Y, expand=1)

        return w

    def get_text_box(self, container, height=None, width=None, row=None, col=None):

        w = ScrolledText(container,
                    bg='white',
                    relief=tk.GROOVE,
                    height=height,
                    width=width,
                    font='TkFixedFont',)
     
        if row is not None:
            #print(row,col)
            w.grid(row=row, column=1,sticky=tk.W)
        else:
            w.pack(side=tk.LEFT,fill=tk.BOTH, expand =1)
           
        return w
        

    def get_save_cancel(self, caller, container):

        caller.btnSave = self.get_button(container, "Save",0,2)
        caller.btnSave.bind("<Button-1>", caller.on_save)
        caller.btnSave.bind("<Return>", caller.on_save)
    
        caller.btCancel = self.get_button(container, "Cancel", 1,2)
        caller.btCancel.bind("<Button-1>", caller.on_cancel)


    def get_export_cancel(self, caller, container):

        caller.btnExport = self.get_button(container, "Export",0,2)
        caller.btnExport.bind("<Button-1>", caller.on_export)
        caller.btnExport.bind("<Return>", caller.on_export)
    
        caller.btCancel = self.get_button(container, "Close", 1,2)
        caller.btCancel.bind("<Button-1>", caller.on_cancel)


    def get_save_cancel_delete(self, caller, container):
               
        caller.btnSave = self.get_button(container, "Save",0,2)
        caller.btnSave.bind("<Button-1>", caller.on_save)
        caller.btnSave.bind("<Return>", caller.on_save)

        caller.btDelete = self.get_button(container, "Delete", 1,2)
        caller.btDelete.bind("<Button-1>", caller.on_delete)
    
        caller.btCancel = self.get_button(container, "Close", 2,2)
        caller.btCancel.bind("<Button-1>", caller.on_cancel)


    def get_add_edit_cancel(self, caller, container):

        caller.btnAdd = self.get_button(container, "Add")
        caller.btnAdd.bind("<Return>", caller.on_add)
        caller.btnAdd.bind("<Button-1>", caller.on_add)
        caller.btnEdit = self.get_button(container, "Edit")
        caller.btnEdit.bind("<Button-1>", caller.on_edit)
        caller.btCancel = self.get_button(container, "Close")
        caller.btCancel.bind("<Button-1>", caller.on_cancel)

       


    def get_add_edit_delete_cancel(self, caller, container):

        bts = self.get_label_frame(container)

        caller.btnAdd = self.get_button(bts, "Add")
        caller.btnAdd.bind("<Return>", caller.on_add)
        caller.btnAdd.bind("<Button-1>", caller.on_add)
        caller.btnEdit = self.get_button(bts, "Edit")
        caller.btnEdit.bind("<Button-1>", caller.on_edit)
        caller.btnDelete = self.get_button(bts, "Delete")
        caller.btnDelete.bind("<Button-1>", caller.on_delete)
        caller.btCancel = self.get_button(bts, "Close")
        caller.btCancel.bind("<Button-1>", caller.on_cancel)

        bts.pack(side=tk.RIGHT, fill=tk.Y, expand=0)

        return bts

    def get_a_pic(self, filename=None):

        if filename is not None:
            if os.path.isfile(filename):
                pass
            else:
                filename = os.path.join('images', 'logo.jpg')
        else:
            filename = os.path.join('images', 'logo.jpg')
            
        image = Image.open(filename)
        image = image.resize((80, 80), Image.ANTIALIAS)
        return ImageTk.PhotoImage(image)
    

    def get_toolbar(self, caller, callbacks):

        toolbar = ttk.Frame(caller,)

        for k, v in enumerate(callbacks):
            
            img = tk.PhotoImage(file=os.path.join('icons', v[0]))
            btn =ttk.Button(toolbar,
                      width=20,
                      image=img,
                      command=v[1])
            btn.image = img
            btn.pack(side=tk.TOP, padx=2, pady=2)

        toolbar.pack(side=tk.LEFT, fill=tk.Y, expand=0)              
            

        return  toolbar


    def get_calendar(self, caller, container, row=None, column=None):

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
            w.grid(row = row, column = column,sticky=tk.W)
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
            msg = "Format data error:\n%s"%str(sys.exc_info()[1])
            messagebox.showerror(self.title, msg)
            return False

    def get_calendar_timestamp(self, caller):

        try:
            t = datetime.datetime.now()
            return datetime.datetime(caller.year.get(), caller.month.get(), caller.day.get(), t.hour , t.minute, t.second)
            
        except:
            msg = "Format data error:\n%s"%str(sys.exc_info()[1])
            messagebox.showerror(self.title, msg)
            return False

    def on_fields_control(self, container):

        msg = "Please fill all fields."

        for w in container.winfo_children():
            for field in w.winfo_children():
                if type(field) in(ttk.Entry,ttk.Combobox):
                    #print(type(field),)
                    #for i in field.keys():
                    #    print (i)
                    if not field.get():
                        messagebox.showwarning(self.title,msg)
                        field.focus()
                        return 0
                    elif type(field)==ttk.Combobox:
                          if field.get() not in field.cget('values'):
                              msg = "You can choice only values in the list."
                              messagebox.showwarning(self.title,msg)
                              field.focus()
                              return 0

    def get_tree(self, container, cols, size=None, show=None):

        ttk.Style().configure("Treeview.Heading",background = self.get_rgb(240,240,237))
        ttk.Style().configure("Treeview.Heading", font=('Helvetica', 10 ))

        headers = []

        for col in cols:
            headers.append(col[1])
        del headers[0]

        if show is not None:
            w = ttk.Treeview(container,show=show)

        else:
            w = ttk.Treeview(container,)
            
        
        w['columns']=headers
        w.tag_configure('is_enable', background='light gray')

        for col in cols:
            w.heading(col[0], text=col[1], anchor=col[2],)
            w.column(col[0], anchor=col[2], stretch=col[3],minwidth=col[4], width=col[5])
           
        sb = ttk.Scrollbar(container)
        sb.configure(command=w.yview)
        w.configure(yscrollcommand=sb.set)

        w.pack(side=tk.LEFT, fill=tk.BOTH, expand =1)
        sb.pack(fill=tk.Y, expand=1)

        return w

    def get_validate_text(self, caller, what=None ):

        if what is not None:
            callback = self.validate_integer
        else:
            callback = self.validate_float
            
        return (caller.register(callback),
             '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')

    def get_validate_integer(self, caller ):
        return (caller.register(self.validate_integer),
             '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')

    def get_validate_float(self, caller ):
        return (caller.register(self.validate_float),
             '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')


    def limit_chars(self, c, v, *args):
        
        if len(v.get())>c:
               v.set(v.get()[:-1])
         

    def validate_integer(self, action, index, value_if_allowed,
                 prior_value, text, validation_type,
                 trigger_type, widget_name):
        # action=1 -> insert
        if(action=='1'):
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
                       prior_value, text, validation_type, trigger_type, widget_name):
        # action=1 -> insert
        if(action=='1'):
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

    def get_widget_attributes(self,container):
        all_widgets = container.winfo_children()
        for widg in all_widgets:
            print('\nWidget Name: {}'.format(widg.winfo_class()))
            keys = widg.keys()
            for key in keys:
                print("Attribute: {:<20}".format(key), end=' ')
                value = widg[key]
                vtype = type(value)
                print('Value: {:<30} Type: {}'.format(value, str(vtype)))

    def get_widgets(self,container):
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
