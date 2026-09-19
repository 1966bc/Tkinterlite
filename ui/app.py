# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# project:  Tkinterlite
# authors:  Giuseppe Costanzi (1966bc)
# licence:  GPL-3.0-or-later, see LICENSE
# -----------------------------------------------------------------------------
"""The application: the root window, the engine, the clock.

The facts about the program live here too, once: its version and date, who
wrote it, under which licence. The About window shows them.
"""

import tkinter as tk
from tkinter import messagebox

from clock import Clock
from engine import Engine
from ui.main import Main

__author__ = "Giuseppe Costanzi (1966bc)"
__copyright__ = "Copyleft"
__credits__ = ["hal9000", ]
__license__ = "GNU GPL, version 3 or later"
__version__ = "42"
__maintainer__ = "1966bc"
__email__ = "giuseppecostanzi@gmail.com"
__date__ = "autumnus MMXXVI"
__status__ = "production"


class App(tk.Tk):
    """The application: the root window, the engine, the clock."""

    def __init__(self, title, log):
        super().__init__()

        self.engine = Engine(log)

        self.protocol("WM_DELETE_WINDOW", self.on_exit)
        self.title(title)
        self.engine.tools.set_style(self.engine.config.get("window", "theme"))
        self.set_icon()
        self.set_info()
        # The clock thread, started before the window that shows it (clock.py).
        self.clock = Clock()
        self.clock.start()

        main = Main(self)
        main.on_open()
        main.pack(fill=tk.BOTH, expand=1)
        self.engine.log.trace("ready; the engine holds log, config, db, tools, events, windows")

    def set_icon(self):
        # The icon in 16, 32 and 48 pixels: the window manager picks the
        # size each place needs, so it is never scaled up and blurred.
        icons = [tk.PhotoImage(data=data) for data in self.engine.get_icons("app")]
        self.iconphoto(True, *icons)

    def set_info(self):
        """The facts the About window shows, from the metadata at the top of this module."""
        self.info = {"name": self.title(),
                     "version": __version__,
                     "date": __date__,
                     "author": __author__,
                     "licence": __license__}

    def report_callback_exception(self, exc, val, tb):
        """Tkinter calls this for an exception raised in a callback.

        A button, a menu, an after(): every error coming out of the interface
        ends up here, the one place where it is handled. It is written to
        the log with its traceback and shown, so the application goes on and
        nothing fails in silence. Tkinter calls this from inside its own
        except block, which is what log.exception() needs.
        """
        self.engine.log.trace("{0}: {1}".format(exc.__name__, val))
        self.engine.log.exception("{0}: {1}".format(exc.__name__, val))
        messagebox.showerror(self.title(),
                             "{0}\n\nDetails in {1}".format(val, self.engine.log.path),
                             parent=self)

    def on_exit(self, evt=None):
        if messagebox.askokcancel(self.title(), "Do you want to quit?", parent=self):
            self.engine.db.con.close()
            self.clock.stop()
            self.engine.log.trace("database closed, clock stopped: goodbye")
            self.destroy()
