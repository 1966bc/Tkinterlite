# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# project:  Tkinterlite
# authors:  Giuseppe Costanzi (1966bc)
# licence:  GPL-3.0-or-later, see LICENSE
# -----------------------------------------------------------------------------
"""About Tkinterlite: what it is, who wrote it, what it runs on."""

import sys
import tkinter as tk
import webbrowser
from tkinter import ttk


class UI(tk.Toplevel):
    """A small window with the icon, the name, and a few facts."""

    #: Where the source lives. Opened with webbrowser, from the standard library.
    SOURCE = "https://github.com/1966bc/Tkinterlite"

    def __init__(self, parent, info):
        super().__init__(name="about")

        self.parent = parent
        self.engine = parent.engine
        #: The facts, from the metadata in ui/main.py: version, date, author...
        self.info = info
        self.transient(parent)
        self.resizable(0, 0)
        self.protocol("WM_DELETE_WINDOW", self.on_cancel)
        self.init_ui()
        self.engine.tools.center_me(self)

    def init_ui(self):

        frm_main = ttk.Frame(self, style="App.TFrame", padding=16)

        # The largest of the icon's sizes. Kept on self: a PhotoImage that only
        # a local variable points to is collected, and the label goes blank.
        self.icon = tk.PhotoImage(data=self.engine.get_icons("app")[-1])
        ttk.Label(frm_main, image=self.icon).grid(row=0, column=0, rowspan=2,
                                                  sticky=tk.N, padx=(0, 12))
        ttk.Label(frm_main, style="Title.TLabel",
                  text=self.info["name"]).grid(row=0, column=1, sticky=tk.W)
        ttk.Label(frm_main, style="App.TLabel",
                  text="Tkinter and SQLite, with the standard library only.").grid(row=1,
                                                                                  column=1,
                                                                                  sticky=tk.W)

        ttk.Separator(frm_main).grid(row=2, column=0, columnspan=2, sticky=tk.EW, pady=12)

        facts = (("Version:", "{0}, {1}".format(self.info["version"], self.info["date"])),
                 ("Author:", self.info["author"]),
                 ("Licence:", self.info["licence"]),
                 ("Python:", ".".join(map(str, sys.version_info[:3]))),
                 ("Tk:", self.tk.call("info", "patchlevel")))

        frm_facts = ttk.Frame(frm_main, style="App.TFrame")
        for row, (label, value) in enumerate(facts):
            ttk.Label(frm_facts, style="App.TLabel", text=label).grid(row=row, column=0,
                                                                     sticky=tk.W)
            ttk.Label(frm_facts, style="App.TLabel", text=value).grid(row=row, column=1,
                                                                     sticky=tk.W, padx=(8, 0))

        ttk.Label(frm_facts, style="App.TLabel", text="Source:").grid(row=len(facts), column=0,
                                                                      sticky=tk.W)
        link = ttk.Label(frm_facts, style="Link.TLabel", text=self.SOURCE, cursor="hand2")
        link.grid(row=len(facts), column=1, sticky=tk.W, padx=(8, 0))
        link.bind("<Button-1>", self.on_source)
        frm_facts.grid(row=3, column=0, columnspan=2, sticky=tk.W)

        buttons = self.engine.tools.get_button_column(frm_main,
                                                      (("Close", self.on_cancel),),
                                                      window=self)
        buttons.grid(row=4, column=0, columnspan=2, sticky=tk.E, pady=(12, 0))

        frm_main.pack(fill=tk.BOTH, expand=1)

    def on_open(self):

        self.title("About {0}".format(self.info["name"]))

    def on_source(self, evt=None):
        webbrowser.open(self.SOURCE)

    def on_cancel(self, evt=None):
        self.destroy()
