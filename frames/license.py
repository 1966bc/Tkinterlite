# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# project:  tkinterlite
# authors:  1966bc
# mailto:   [giuseppecostanzi@gmail.com]
# modify:   hiems MMXX
# -----------------------------------------------------------------------------
import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText


class UI(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(name="license")

        self.parent = parent
        self.init_ui()
        self.nametowidget(".").engine.center_me(self)

    def init_ui(self):

        
        f0 = ttk.Frame(self,
                       style="App.TFrame",
                       relief=tk.GROOVE,
                       borderwidth=1,
                       padding=8)

        self.txLicense = ScrolledText(f0,
                         wrap=tk.WORD,
                         bg="light yellow",
                         relief=tk.GROOVE,
                         font='TkFixedFont',)
        self.txLicense.pack(fill=tk.BOTH, expand=1)
        
        f0.pack(fill=tk.BOTH, padx=5, pady=5, expand=1)
        
    def on_open(self):

        msg = self.nametowidget(".").engine.get_license()
        
        if msg:
            self.txLicense.insert("1.0", msg)

        self.title(self.nametowidget(".").title())
