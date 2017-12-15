#!/usr/bin/python
#-----------------------------------------------------------------------------
# project:  tkinterlite
# authors:  1966bc
# mailto:   [giuseppecostanzi@gmail.com]
# modify:   autumn 2017
# version:  0.1                                                                
#-----------------------------------------------------------------------------
from tkinter import *
from tkinter import ttk  
from tkinter import font


class Widgets(object):

    def __init__(self,*args, **kwargs):

        super(Widgets, self).__init__( *args, **kwargs)
        
    def __str__(self):
        return "class: %s\nMRO: %s" % (self.__class__.__name__,  [x.__name__ for x in Widgets.__mro__])

    def get_button(self, container, text, row=None, col=None):

        obj = Button(container, text=text, borderwidth=1,relief='raised',padx=5,pady=5,)

        if row is not None:
            obj.grid(row=row, column=col, sticky=W+E, padx=5, pady=5)
        else:
            obj.pack(fill =X, padx=5, pady=5)
        
        return obj


    def get_radio_buttons(self, container,text, ops, v, callback=None):

        obj = LabelFrame(container, borderwidth=1, text = text)

        for index, text in enumerate(ops):
            b = Radiobutton(obj,
                            text=text,
                            #fg='blue',
                            bd=0,
                            padx = 5,
                            pady = 5,
                            relief=GROOVE,
                            variable=v,
                            command=callback,
                            value=index).pack(anchor=W)

        obj.pack(fill=X, expand=0)            

        return obj            


    def get_buttons_label_frame(self, container):
        return LabelFrame(container, bd=1 ,padx=5, pady=5, relief=GROOVE)

    def get_panel_frame(self, container):
        return Frame(container, bd=1, padx = 5, pady = 5)

    def get_panel_label_frame(self, container,text):
        return LabelFrame(container,text=text, bd=1, padx = 5, pady = 5)


    def get_tree(self, container, cols,):

        #ttk.Style().configure("Treeview",
        #                      background="lightyellow",
        #                      fieldbackground="lightyellow",
        #                      foreground="black")
        
        headers = []

        for col in cols:
            headers.append(col[1])
        del headers[0]

        obj = ttk.Treeview(container,)
        
        obj['columns']=headers

        for col in cols:
            obj.heading(col[0], text=col[1], anchor=col[2],)
            obj.column(col[0], anchor=col[2], stretch=col[3],minwidth=col[4], width=col[5])
           
        sb = Scrollbar(container)
        sb.configure(command=obj.yview)
        obj.configure(yscrollcommand=sb.set)

        obj.pack(side=LEFT, fill=BOTH, expand =1)
        sb.pack(fill=Y, expand=1)

        return obj

    def get_listbox(self, container,):

        sb = Scrollbar(container,orient=VERTICAL)
        obj = Listbox(container,relief=GROOVE,selectmode=BROWSE,yscrollcommand=sb.set,)
        sb.config(command=obj.yview)
     
        obj.pack(side=LEFT,fill=BOTH, expand =1) 
        sb.pack(fill=Y, expand=1)

        return obj

    def get_save_cancel(self, caller, container):

        bts = self.get_buttons_label_frame(container)
        bts.grid(row = 0, column = 2, sticky=N+W+S+E)
       
        caller.btnSave = self.get_button(bts, "Save",0,2)
        caller.btnSave.bind("<Button-1>", caller.on_save)
        caller.btnSave.bind("<Return>", caller.on_save)
    
        caller.btCancel = self.get_button(bts, "Close", 1,2)
        caller.btCancel.bind("<Button-1>", caller.on_cancel)

        return bts


    def get_add_edit_cancel(self, caller, container):

        bts = self.get_buttons_label_frame(container)

        caller.btnAdd = self.get_button(bts, "Add")
        caller.btnAdd.bind("<Return>", caller.on_add)
        caller.btnAdd.bind("<Button-1>", caller.on_add)
        caller.btnEdit = self.get_button(bts, "Edit")
        caller.btnEdit.bind("<Button-1>", caller.on_edit)
        caller.btCancel = self.get_button(bts, "Close")
        caller.btCancel.bind("<Button-1>", caller.on_cancel)

        bts.pack(side=RIGHT, fill=Y, expand=0)

        return bts

                          
def main():
    
    foo = Widgets()
    print(foo)                
    input('end')
       
if __name__ == "__main__":
    main()
