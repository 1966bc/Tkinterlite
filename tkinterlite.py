#!/usr/bin/python3
#-----------------------------------------------------------------------------
# project:  tkinterlite
# authors:  1966bc
# mailto:   [giuseppe.costanzi@gmail.com]
# modify:   10/04/2017
# version:  0.1                                                                
#-----------------------------------------------------------------------------

from tkinter import *
from tkinter import ttk
from tkinter import messagebox

from engine import Engine
import product
import categories
import suppliers
import parameters

class App(Frame):
    def __init__(self, master=None):
        super().__init__(master)

        self.engine = Engine()
        self.master.title(self.engine.title)
        self.master = master
        
        self.init_menu()
        self.init_status_bar()
        self.init_window()
        
    def init_menu(self):

        mnuMain = Menu(self.master, bd = 1)
        
        mFile = Menu(mnuMain, tearoff=0, bd = 1)
        mTools = Menu(mnuMain, tearoff=0, bd = 1)
        mAbout = Menu(mnuMain, tearoff=0, bd = 1)
        
        mnuMain.add_cascade(label="File", menu=mFile)
        mnuMain.add_cascade(label="Tools", menu=mTools)
        mnuMain.add_cascade(label="Info", menu=mAbout)
        
        mFile.add_command(label="Parameters", command=self.on_parameters)
        mFile.add_command(label="Exit", command=self.on_exit)
        mTools.add_command(label="Categories", command=self.on_categories)
        mTools.add_command(label="Suppliers", command=self.on_suppliers)
        mAbout.add_command(label="About", command=self.on_about)
             
        self.master.config(menu=mnuMain)

    def init_status_bar(self):

        self.status = Label(self.master, text = 'Ready', bd=1, relief=SUNKEN, anchor=W)
        self.status.pack(side=BOTTOM, fill=X)

    # FIXME This function work, format widggets correctly, only if buttons Frame are first object create....why?
    def init_window(self):

        """create widgets"""

        self.pack(fill=BOTH, expand=1)

        #buttons
        #-----------------------------------------------------------------------
        self.buttons = Frame(self, padx=10, pady=10)
        self.btnRefresh = Button(self.buttons, text="Refresh", command=self.on_open)
        self.btnRefresh.pack(fill=X, anchor=W, pady=10)
        
        self.btnNew = Button(self.buttons, text="New", command=self.on_add_product)
        self.btnNew.pack(fill=X, anchor=W, pady=10)

        self.btnEdit = Button(self.buttons, text="Edit", command=self.on_edit)
        self.btnEdit.pack(fill=X, anchor=W, pady=10)

        self.btClose = Button(self.buttons, text="Close", command=self.on_exit)
        self.btClose.pack(fill = X,anchor=W, pady=10)
        
        self.buttons.pack(side=RIGHT, fill=BOTH)
        #-----------------------------------------------------------------------

        #products
        #-----------------------------------------------------------------------
        self.products = Frame(self,)
        
        self.lfProducts = LabelFrame(self.products,text='Products')
        self.lfProducts.pack(side=TOP, fill=BOTH, expand =1)
        
        self.lstProducts = ttk.Treeview(self.lfProducts,
                                        columns=('ID','Product', 'Description', 'Stock','Price'),
                                        selectmode='browse',
                                        padding = 5,
                                        show='headings',
                                        displaycolumns=('#all',))
        #bind TreeviewSelect
        self.lstProducts.bind("<<TreeviewSelect>>", self.get_selected_product)
        self.lstProducts.bind("<Double-1>", self.on_double_click)
        
        self.lstProducts.heading('#0', text='ID',)
        self.lstProducts.heading('#1', text='Product',)
        self.lstProducts.heading('#2', text='Description')
        self.lstProducts.heading('#3', text='Stock')
        self.lstProducts.heading('#4', text='Price')
        self.lstProducts.column('#0', stretch=NO,width=0)
        self.lstProducts.column('#1', stretch=YES,width=300)
        self.lstProducts.column('#2', stretch=YES)
        self.lstProducts.column('#3', stretch=YES,width=50)
        self.lstProducts.column('#4', stretch=YES,width=50)
        #add Scrollbar to ttk.Treeview
        treeScroll = Scrollbar(self.lfProducts)
        treeScroll.configure(command=self.lstProducts.yview)
        self.lstProducts.configure(yscrollcommand=treeScroll.set)
        
        self.lstProducts.pack(side=LEFT,fill=BOTH, expand=1)
        treeScroll.pack(side=LEFT,fill=Y,expand=0)

        self.products.pack(side=TOP, fill=BOTH, expand=1)
        #-----------------------------------------------------------------------

        #categories
        #-----------------------------------------------------------------------
        self.categories = Frame(self,)
        self.lfCategories = LabelFrame(self.categories,text='Categories')
        self.lfCategories.pack(side=TOP, fill=X)
    
        self.cbCategories =  ttk.Combobox(self.lfCategories)
        self.cbCategories.bind("<<ComboboxSelected>>", self.get_selected_category)
        
        self.cbCategories.pack(side=BOTTOM, fill=X)
        self.categories.pack(side=BOTTOM, fill=BOTH)

        
    def on_open(self):

        self.selected_product = None
        sql = "SELECT * FROM products ORDER BY product DESC"
        self.set_tree_values(sql,())
        self.set_combo_values()

    def on_add_product(self):

        obj = product.Dialog(self,self.engine)
        obj.on_open()
        obj.wait_visibility()
        obj.grab_set()
        self.master.wait_window(obj)

    def on_parameters(self,):

        obj = parameters.Dialog(self,self.engine)
        obj.on_open()
        obj.wait_visibility()
        obj.grab_set()
        self.master.wait_window(obj)
        
    def on_categories(self):

        obj = categories.Dialog(self,self.engine)
        obj.on_open()
      
    def on_suppliers(self):

        obj = suppliers.Dialog(self,self.engine)
        obj.on_open()

    def on_edit(self,):

        if self.selected_product is not None:
            obj = product.Dialog(self,self.engine)
            obj.on_open(self.selected_product)
            obj.wait_visibility()
            obj.grab_set()
            self.master.wait_window(obj)
        else:
            msg = "Please select an item."
            messagebox.showwarning(self.engine.title,msg)

    def on_double_click(self,event):

        self.on_edit()
 
    def get_selected_product(self, event):
        
        pk = int(self.lstProducts.item(self.lstProducts.focus())['text'])
        self.selected_product = self.engine.get_selected('products','product_id', pk)

    def get_selected_category(self, event):
        
        index = self.cbCategories.current()
        category_id = self.dict_categories[index]
        sql = "SELECT * FROM products WHERE category_id =? ORDER BY product DESC"
        args = (category_id,)
        self.set_tree_values(sql, args)
        
    def set_tree_values(self,sql,args):

        for i in self.lstProducts.get_children():
            self.lstProducts.delete(i)

        index = 0
        self.dict_products={}            

        rs  = self.engine.read(True, sql, args)
        
        for i in rs:
            self.lstProducts.insert('', 0, text=i[0],values=(i[1],i[4],i[6],i[5]))
            self.dict_products[index]=i[0]
            index+=1

    def set_combo_values(self):

        index = 0
        self.dict_categories={}
        l = []

        sql = "SELECT category_id, category FROM categories ORDER BY category"
        rs = self.engine.read(True, sql, ())
            
        for i in rs:
            self.dict_categories[index]=i[0]
            index+=1
            l.append(i[1])

        self.cbCategories['values']=l

    def on_about(self,):
        messagebox.showinfo(self.engine.title, self.engine.about)   
        
    def on_exit(self):
        if messagebox.askokcancel(self.engine.title, "Do you want to quit?"):
            self.master.destroy()

def main():
    root = Tk()
    width = root.winfo_screenwidth()
    height = root.winfo_screenheight()
    #full screen
    #root.geometry(str(width) + "x" + str(height))
    app = App(master=root)
    app.on_open()
    app.master.protocol("WM_DELETE_WINDOW",app.on_exit)
    app.mainloop()
  
if __name__ == '__main__':
    main()
