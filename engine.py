#!/usr/bin/python3
#-----------------------------------------------------------------------------
# project:  tkinterlite
# authors:  1966bc
# mailto:   [giuseppecostanzi@gmail.com]
# modify:   hiems MMXXI
#------------------------------------------------------------------------------
import os
import sys
import subprocess

from dbms import DBMS
from tools import Tools
from config import Config
from events import Events


class Engine:
    """The one object every window reaches: it owns the parts, it is none of them.

    Composition, not inheritance: Engine is not a database, it has one. Each
    part is an attribute, so a call says who does the work -
    engine.db.read(...), engine.tools.center_me(...) - and each part can be
    built and tested on its own.
    """

    def __init__(self, log):
        self.log = log
        # The settings, read by the Config class from tkinterlite.ini.
        self.config = Config(self.get_file("tkinterlite.ini"))
        # The database beside the program, wherever it is started from.
        self.db = DBMS(self.get_file("northwind.sl3"), log)
        # Styles and widget helpers.
        self.tools = Tools()
        # Who changed what, told to the windows that show it: the Observer.
        self.events = Events()

        self.no_selected = "Attention!\nNo record selected!"
        self.ask_to_delete = "Delete data?"
        self.ask_to_save = "Save data?"
        self.abort = "Operation aborted!"

    def __str__(self):
        return "class: {0}\nparts: log, config, db, tools, events".format(self.__class__.__name__)

    def get_python_version(self,):
        return "Python version:\n{0}".format(".".join(map(str, sys.version_info[:3])))

    def get_file(self, file):
        """# return full path of the directory where program resides."""

        return os.path.join(os.path.dirname(__file__), file)

    def open_file(self, path):
        """open file on linux and windows"""
        if os.path.exists(path):
            if os.name == 'posix':
                subprocess.call(["xdg-open", path])
            else:
                os.startfile(path)

    def get_license(self):
        """get license"""
        with open(self.get_file("LICENSE"), "r") as f:
            v = f.read()

        return v

    def get_icon(self, which):
        """An icon: its file holds one base64 PNG."""
        with open(self.get_file(which), "r") as f:
            v = f.readline()

        return v

    def get_icons(self, which):
        """Every size of an icon: its file holds one base64 PNG per line."""
        with open(self.get_file(which), "r") as f:
            icons = f.read().split()

        return icons

    def open_log(self):
        """Open the log file with the program the system uses for text."""
        self.open_file(self.log.path)
