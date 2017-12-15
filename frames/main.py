#!/usr/bin/python3
#-----------------------------------------------------------------------------
# project:  tkinterlite
# authors:  1966bc
# mailto:   [giuseppe.costanzi@gmail.com]
# modify:   10/04/2017
# version:  0.1                                                                
#-----------------------------------------------------------------------------
import os
import _thread
import datetime
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import Image 

from engine import Engine
import frames.product
import frames.categories
import frames.suppliers

class App(Frame):
    def __init__(self, engine):
        super().__init__()

        self.engine = engine
        self.status_bar_text = StringVar()
        #attention please, master is an attribute of self ergo root=Tk()
        self.master.title(self.engine.title)
        self.master.protocol("WM_DELETE_WINDOW",self.on_exit)

        self.ops = ('Cateogries','Suppliers')
        self.filter_id = IntVar()

        self.cols = (["#0",'id','w',False,0,0],
                      ["#1",'Product','w',True,200,200],
                      ["#2",'Description','w',True,200,200],
                      ["#3",'Stock','w',True,50,50],
                      ["#4",'Price','w',True,50,50],)

        self.init_menu()
        self.init_toolbar()
        self.init_status_bar()
        self.init_window()
        
    def init_menu(self):

        mnuMain = Menu(self)
        
        mFile = Menu(mnuMain, tearoff=0, bd = 1)
        mTools = Menu(mnuMain, tearoff=0, bd = 1)
        mAbout = Menu(mnuMain, tearoff=0, bd = 1)
        
        mnuMain.add_cascade(label="File", menu=mFile)
        mnuMain.add_cascade(label="Tools", menu=mTools)
        mnuMain.add_cascade(label="?", menu=mAbout)
        
        mFile.add_command(label="Exit", command=self.on_exit)
        
        mTools.add_command(label="Categories", command=self.on_categories)
        mTools.add_command(label="Suppliers", command=self.on_suppliers)
        mAbout.add_command(label="About", command=self.on_about)

        self.master.config(menu=mnuMain)

    def init_toolbar(self):

        toolbar = Frame(self, bd=1, relief=RAISED)

        img_exit = PhotoImage(file=os.path.join('icons', 'exit.png'))
        img_info = PhotoImage(file=os.path.join('icons', 'info.png'))

        exitButton = Button(toolbar,width=20, image=img_exit, relief=FLAT, command=self.on_exit)
        infoButton = Button(toolbar,width=20, image=img_info, relief=FLAT, command=self.on_about)
        
        exitButton.image = img_exit
        infoButton.image = img_info

        exitButton.pack(side=LEFT, padx=2, pady=2)
        infoButton.pack(side=LEFT, padx=2, pady=2)

        toolbar.pack(side=TOP, fill=X)
        

    def init_status_bar(self):

        self.status = Label(self.master, textvariable=self.status_bar_text, bd=1, relief=SUNKEN, anchor=W)
        self.status.pack(side=BOTTOM, fill=X)

    def init_window(self):

        """create widgets"""

        self.pack(fill=BOTH, expand=1)

        #products
        #-----------------------------------------------------------------------
        left_widgets = Frame(self,)

        self.tree_products = LabelFrame(left_widgets,text='Products',)
        self.lstProducts = self.engine.get_tree(self.tree_products, self.cols,)
        self.lstProducts.bind("<<TreeviewSelect>>", self.get_selected_product)
        #self.lstProducts.bind("<Double-1>", self.on_double_click)
        self.tree_products.pack(fill=BOTH, expand=1)
        #-----------------------------------------------------------------------

        #categories
        #-----------------------------------------------------------------------
        self.combo_label_frame = LabelFrame(left_widgets,)
        
        self.cbFilters =  ttk.Combobox(self.combo_label_frame)
        self.cbFilters.bind("<<ComboboxSelected>>", self.get_selected_combo_item)
        self.cbFilters.pack(side=TOP, anchor=W, fill=X, expand=YES)
        
        self.combo_label_frame.pack(side=TOP, anchor=W, fill=X, expand=0)
        
        left_widgets.pack(side=LEFT, fill=BOTH, anchor=W, expand=1)

        #buttons
        #-----------------------------------------------------------------------
        buttons_label_frame = self.engine.get_buttons_label_frame(self)

        self.btnSearch = self.engine.get_button(buttons_label_frame, "Refresh")
        self.btnSearch.bind("<Button-1>", self.on_open)

        self.btnAdd = self.engine.get_button(buttons_label_frame, "New")
        self.btnAdd.bind("<Button-1>", self.on_add)
        
        self.btnSamples = self.engine.get_button(buttons_label_frame, "Edit")
        self.btnSamples.bind("<Button-1>", self.on_edit)
        
        self.btClose = self.engine.get_button(buttons_label_frame, "Close")
        self.btClose.bind("<Button-1>", self.on_exit)

        self.coiche = self.engine.get_radio_buttons(buttons_label_frame,'Combo data',self.ops,self.filter_id,self.set_combo_values)

        buttons_label_frame.pack(side=RIGHT, fill=Y, expand=0)

    def update_status_bar(self):
        
        while True:
            s = "Astral date: "
            t = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            msg = s+t
            self.status_bar_text.set(msg)        
          
    def on_open(self, evt=None):

        _thread.start_new_thread(self.update_status_bar,())

        self.selected_product = None
        sql = "SELECT * FROM products ORDER BY product DESC"
        self.set_tree_values(sql,())
        self.cbFilters.set('')
        self.set_combo_values()

    def on_add(self, evt):

        obj = frames.product.Dialog(self,self.engine)
        obj.transient(self)
        obj.on_open()
                   
    def on_categories(self):

        obj = frames.categories.Dialog(self,self.engine)
        obj.transient(self)
        obj.on_open()
      
    def on_suppliers(self):

        obj = frames.suppliers.Dialog(self,self.engine)
        obj.transient(self)
        obj.on_open()

    def on_edit(self, evt):

        if self.selected_product is not None:
            obj = frames.product.Dialog(self,self.engine)
            obj.transient(self)
            obj.on_open(self.selected_product)
        else:
            msg = "Please select an item."
            messagebox.showwarning(self.engine.title,msg)

    def on_double_click(self, evt):

        self.on_edit(self)
 
    def get_selected_product(self, evt):
        
        pk = int(self.lstProducts.item(self.lstProducts.focus())['text'])
        self.selected_product = self.engine.get_selected('products','product_id', pk)

    def get_selected_combo_item(self, evt):
        
        index = self.cbFilters.current()
        selected_id = self.dict_combo_values[index]

        if self.filter_id.get() !=1:
            sql = "SELECT * FROM products WHERE supplier_id =? ORDER BY product DESC"
        else:
            sql = "SELECT * FROM products WHERE category_id =? ORDER BY product DESC"
            
        args = (selected_id,)
        self.set_tree_values(sql, args)
        
    def set_tree_values(self, sql, args):

        for i in self.lstProducts.get_children():
            self.lstProducts.delete(i)

        rs  = self.engine.read(True, sql, args)

        if rs:
            self.tree_products['text'] = 'Products %s'%len(rs)
            for i in rs:
                self.lstProducts.insert('', 0, text=i[0],values=(i[1],i[4],i[6],i[5]))
        else:self.tree_products['text'] = 'Products 0'
           

    def set_combo_values(self):

        index = 0
        self.dict_combo_values={}
        l = []

        if self.filter_id.get() !=1:
            self.combo_label_frame['text'] = 'Categories'
            sql = "SELECT category_id, category\
                   FROM categories\
                   WHERE enable =1\
                   ORDER BY category"
        else:
            self.combo_label_frame['text'] = 'Suppliers'
            sql = "SELECT supplier_id, company\
                   FROM suppliers\
                   WHERE enable =1\
                   ORDER BY company"
            
        rs = self.engine.read(True, sql, ())
            
        for i in rs:
            self.dict_combo_values[index]=i[0]
            index+=1
            l.append(i[1])

        self.cbFilters.set('')
        self.cbFilters['values']=l

    def on_about(self,):
        messagebox.showinfo(self.engine.title, self.engine.about)   
        
    def on_exit(self, evt=None):
        if messagebox.askokcancel(self.engine.title, "Do you want to quit?"):
            self.master.destroy()

def main():
    engine = Engine()
    root = Tk()
    root.option_readfile('option_db')
    root.style = ttk.Style()
    #('winnative', 'clam', 'alt', 'default', 'classic', 'vista', 'xpnative')
    root.style.theme_use("clam")
    #set icon
    imgicon = PhotoImage(file=os.path.join('icons', 'warehouse.png'))
    root.tk.call('wm', 'iconphoto', root._w, '-default', imgicon)
    app = App(engine)
    app.on_open()
    root.mainloop()
  
if __name__ == '__main__':
    main()
