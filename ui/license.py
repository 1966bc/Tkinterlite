# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# project:  Tkinterlite
# authors:  Giuseppe Costanzi (1966bc)
# licence:  GPL-3.0-or-later, see LICENSE
# -----------------------------------------------------------------------------
"""The licence, shown and not editable."""

import tkinter as tk
from tkinter import ttk


class UI(tk.Toplevel):
    """The text of LICENSE, read-only. It closes like any window, from its title bar."""

    #: Tk's "light yellow".
    PAPER = (255, 255, 224)

    def __init__(self, parent):
        super().__init__(name="license")

        self.parent = parent
        self.engine = parent.engine
        self.protocol("WM_DELETE_WINDOW", self.on_cancel)
        self.init_ui()
        self.engine.tools.center_me(self)

    def init_ui(self):

        frm_main = ttk.Frame(self, style="App.TFrame", padding=8)

        self.txt_license = self.engine.tools.get_text(frm_main)
        # Fixed width, because the licence is laid out in columns of plain text,
        # on the pale yellow of a sheet of paper, as it has always been here.
        self.txt_license.configure(font="TkFixedFont",
                                   background=self.engine.tools.get_rgb(*self.PAPER))

        frm_main.pack(fill=tk.BOTH, expand=1)

    def on_open(self):

        self.title("License")
        self.engine.tools.set_text(self.txt_license, self.engine.get_license())

    def on_cancel(self, evt=None):
        self.destroy()
