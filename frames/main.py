
import os
import threading
import queue
import datetime
import time
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

from engine import Engine
import frames.product
import frames.categories
import frames.suppliers


__author__ = "1966bc aka giuseppe costanzi"
__copyright__ = "Copyleft"
__credits__ = ["hal9000",]
__license__ = "GNU GPL Version 3, 29 June 2007"
__version__ = "42"
__maintainer__ = "1966bc"
__email__ = "giuseppecostanzi@gmail.com"
__date__ = "2018-12-23"
__status__ = "Production"


class ClockThread(threading.Thread):

    def __init__(self, queue,):
        threading.Thread.__init__(self)

        self.queue = queue
        self.check = True
        self.engine = Engine()

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
           

class App(tk.Frame):
    def __init__(self, engine):
        super().__init__()

        self.engine = engine
        self.queue = queue.Queue()
        self.clock = None
        #attention please, master is an attribute of self ergo root=Tk()
        self.master.protocol("WM_DELETE_WINDOW",self.on_exit)
        self.objs = []
        self.ops = ('Cateogries','Suppliers')
        self.status_bar_text = tk.StringVar()
        self.filter_id = tk.IntVar()

        self.cols = (["#0",'id','w',False,0,0],
                      ["#1",'Product','w',True,100,100],
                      ["#2",'Description','w',True,100,100],
                      ["#3",'Stock','w',True,20,20],
                      ["#4",'Price','w',True,20,20],)

    
        self.set_style()
        self.set_icon()
        self.set_title()
        self.center_ui()
        self.init_menu()
        self.init_toolbar()
        self.init_ui()
        self.init_status_bar()

    def set_style(self):
        self.master.style = ttk.Style()
        #('winnative', 'clam', 'alt', 'default', 'classic', 'vista', 'xpnative')
        self.master.style.theme_use("clam")
        self.master.style.configure('.', background=self.engine.get_rgb(240,240,237))

    def set_icon(self):
        imgicon = tk.PhotoImage(file=os.path.join('icons','warehouse.png'))
        self.master.call('wm', 'iconphoto', self.master._w, '-default', imgicon)

    def set_title(self):
        s = "{0} {1}".format(self.engine.title, __version__)
        self.master.title(s)
           
        
    def init_menu(self):

        m_main = tk.Menu(self, bd=1)
               
        m_file = tk.Menu(m_main, tearoff=0, bd=1)
        s_menu = tk.Menu(m_file)
                
        m_about = tk.Menu(m_main, tearoff=0, bd=1)
        
        m_main.add_cascade(label="File", underline=0, menu=m_file)
        m_main.add_cascade(label="?", underline=0, menu=m_about)

        m_file.add_cascade(label='Tools', menu=s_menu, underline=0)

        items = (("Cateogries", self.on_categories),
                 ("Suppliers", self.on_suppliers),)

        for i in items:
            s_menu.add_command(label=i[0], underline=0, command=i[1])

        m_file.add_separator()
 
        m_file.add_command(label="Exit", underline=0, command=self.on_exit)

        m_about.add_command(label="About", underline=0, command=self.on_about)

        self.master.config(menu=m_main)      

    def init_toolbar(self):

        toolbar = tk.Frame(self, bd=1, relief=tk.RAISED)

        img_exit = tk.PhotoImage(file=os.path.join('icons', 'exit.png'))
        img_info = tk.PhotoImage(file=os.path.join('icons', 'info.png'))

        exitButton = tk.Button(toolbar,width=20, image=img_exit, relief=tk.FLAT, command=self.on_exit)
        infoButton = tk.Button(toolbar,width=20, image=img_info, relief=tk.FLAT, command=self.on_about)
        
        exitButton.image = img_exit
        infoButton.image = img_info

        exitButton.pack(side=tk.LEFT, padx=2, pady=2)
        infoButton.pack(side=tk.LEFT, padx=2, pady=2)

        toolbar.pack(side=tk.TOP, fill=tk.X)

    def center_ui(self):

        ws = self.master.winfo_screenwidth()
        hs = self.master.winfo_screenheight()
        # calculate position x, y
        d = self.engine.get_dimensions()
        w = int(d['w'])
        h = int(d['h'])
        x = (ws/2) - (w/2)    
        y = (hs/2) - (h/2)
        self.master.geometry('%dx%d+%d+%d' % (w, h, x, y))     
        

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

        self.lblProdutcs = ttk.LabelFrame(w,text='Products',)
        self.lstProducts = self.engine.get_tree(self.lblProdutcs, self.cols,)
        self.lstProducts.bind("<<TreeviewSelect>>", self.get_selected_product)
        self.lstProducts.bind("<Double-1>", self.on_double_click)
        self.lblProdutcs.pack(fill=tk.BOTH, expand=1)
        #-----------------------------------------------------------------------

        #categories
        #-----------------------------------------------------------------------
        self.lblCombo = ttk.LabelFrame(w,)
        
        self.cbCombo =  ttk.Combobox(self.lblCombo)
        self.cbCombo.bind("<<ComboboxSelected>>", self.get_selected_combo_item)
        self.cbCombo.pack(side=tk.TOP, anchor=tk.W, fill=tk.X, expand=1)
        
        self.lblCombo.pack(side=tk.TOP, anchor=tk.W, fill=tk.X,pady=5, expand=0)
        
        w.pack(side=tk.LEFT, fill=tk.BOTH, anchor=tk.W, expand=1)

        #buttons and radio
        #-----------------------------------------------------------------------
        f = self.engine.get_frame(self, 8)

        bts = (('Reset', self.on_open),
               ('New', self.on_add),
               ('Edit', self.on_edit),
               ('Close', self.on_exit))

        for btn in bts:
            self.engine.get_button(f, btn[0] ).bind("<Button-1>", btn[1])

        self.engine.get_radio_buttons(f,
                                      'Combo data',
                                      self.ops,
                                      self.filter_id,
                                      self.set_combo_values).pack()

        f.pack(side=tk.RIGHT, fill=tk.Y, expand=0)
   
          
    def on_open(self, evt=None):

        self.selected_product = None
        sql = "SELECT * FROM products ORDER BY product ASC"
        self.set_tree_values(sql,())
        self.cbCombo.set('')
        self.set_combo_values()

     
        self.clock = ClockThread(self.queue)
        self.clock.start()
        self.periodic_call()


    def on_add(self, evt):

        obj = frames.product.Dialog(self,self.engine)
        obj.transient(self)
        obj.on_open()
                   
    def on_categories(self):

        obj = frames.categories.Dialog(self,self.engine)
        obj.on_open()
      
    def on_suppliers(self):

        obj = frames.suppliers.Dialog(self,self.engine)
        obj.on_open()

    def on_edit(self, evt):
        

        if self.lstProducts.focus():

            item_iid = self.lstProducts.selection()
            obj = frames.product.Dialog(self, self.engine, item_iid)
            obj.on_open(self.selected_product,)
            
        else:
            msg = "Please select an item."
            messagebox.showwarning(self.engine.title,msg)

    def on_double_click(self, evt):

        self.on_edit(self)
 
    def get_selected_product(self, evt):

        if self.lstProducts.focus():
            pk = int(self.lstProducts.item(self.lstProducts.focus())['text'])
            self.selected_product = self.engine.get_selected('products', 'product_id', pk)
         
    def get_selected_combo_item(self, evt):
        
        index = self.cbCombo.current()
        selected_id = self.dict_combo_values[index]

        if self.filter_id.get() !=1:
            sql = "SELECT * FROM products WHERE supplier_id =? ORDER BY product"
        else:
            sql = "SELECT * FROM products WHERE category_id =? ORDER BY product"
            
        args = (selected_id,)
        self.set_tree_values(sql, args)
        
    def set_tree_values(self, sql, args):

        self.lstProducts.tag_configure('is_enable', background='light gray')
        self.lstProducts.tag_configure('is_zero', background=self.engine.get_rgb(255,160,122))

        for i in self.lstProducts.get_children():
            self.lstProducts.delete(i)

        rs  = self.engine.read(True, sql, args)

        if rs:
            self.lblProdutcs['text'] = 'Products %s'%len(rs)
            for i in rs:
                if i[7] !=0:
                    if i[6]<1:
                        self.lstProducts.insert('', tk.END, iid=i[0], text=i[0],values=(i[1],i[4],i[6],i[5]), tags = ('is_zero',))
                    else:
                        self.lstProducts.insert('', tk.END, iid=i[0], text=i[0],values=(i[1],i[4],i[6],i[5]))
                        
                else:
                    self.lstProducts.insert('', tk.END, iid=i[0], text=i[0],values=(i[1],i[4],i[6],i[5]), tags = ('is_enable',))
        else:self.lblProdutcs['text'] = 'Products 0'
           

    def set_combo_values(self):

        index = 0
        self.dict_combo_values={}
        l = []

        if self.filter_id.get() !=1:
            self.lblCombo['text'] = 'Categories'
            sql = "SELECT category_id, category\
                   FROM categories\
                   WHERE enable =1\
                   ORDER BY category"
        else:
            self.lblCombo['text'] = 'Suppliers'
            sql = "SELECT supplier_id, company\
                   FROM suppliers\
                   WHERE enable =1\
                   ORDER BY company"
            
        rs = self.engine.read(True, sql, ())
            
        for i in rs:
            self.dict_combo_values[index]=i[0]
            index+=1
            l.append(i[1])

        self.cbCombo.set('')
        self.cbCombo['values']=l

    def on_about(self,):
        messagebox.showinfo(self.engine.title, self.engine.about)   
        
    def on_exit(self, evt=None):
        if messagebox.askokcancel(self.engine.title, "Do you want to quit?"):
            if(threading.active_count()!=1):
                if self.clock is not None:
                    self.clock.stop()
                self.master.destroy()

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
                msg = "%s"%(x)
                self.status_bar_text.set(msg)
            except queue.Empty:
                pass                  

def main():
    app = App(Engine())
    app.on_open()
    app.mainloop()
  
if __name__ == '__main__':
    main()
