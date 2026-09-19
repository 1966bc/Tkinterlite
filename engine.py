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
from clock import Clock



class Engine(DBMS, Tools, Clock):
    def __init__(self, log):
        # The database beside the program, wherever it is started from.
        super().__init__(self.get_file("northwind.sl3"), log)

        self.no_selected = "Attention!\nNo record selected!"
        self.ask_to_delete = "Delete data?"
        self.ask_to_save = "Save data?"
        self.abort = "Operation aborted!"

    def __str__(self):
        return "class: {0}\nMRO:{1}".format(self.__class__.__name__,
                       [x.__name__ for x in Engine.__mro__])

    def get_clock(self,):
        """Instance the clock."""
        return Clock()
        
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

    def get_dimensions(self):
        """The main window size, from the dimensions file: {"w": ..., "h": ...}."""
        d = {}
        with open(self.get_file("dimensions"), "r") as filestream:
            for line in filestream:
                currentline = line.split(",")
                d[currentline[0]] = currentline[1]

        return d

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

    def get_theme(self):
        """The ttk theme name, from the theme file."""
        with open(self.get_file("theme"), "r") as f:
            theme = f.readline().strip()

        return theme
