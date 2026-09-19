# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# project:  Tkinterlite
# authors:  Giuseppe Costanzi (1966bc)
# licence:  GPL-3.0-or-later, see LICENSE
# -----------------------------------------------------------------------------
import tkinter as tk
from tkinter import ttk


class UI(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(name="license")

        self.parent = parent
        self.engine = parent.engine
        self.init_ui()
        self.engine.tools.center_me(self)

    def init_ui(self):

        
        f0 = ttk.Frame(self,
                       style="App.TFrame",
                       relief=tk.GROOVE,
                       borderwidth=1,
                       padding=8)

        self.txLicense = self.engine.tools.get_text(f0)
        # Fixed width: the licence is laid out in columns of plain text.
        self.txLicense.configure(font="TkFixedFont")
        
        f0.pack(fill=tk.BOTH, padx=5, pady=5, expand=1)
        
    def on_open(self):

        self.engine.tools.set_text(self.txLicense, self.engine.get_license())

        self.title(self.nametowidget(".").title())
