#!/usr/bin/python3
#-----------------------------------------------------------------------------
# project:  tkinterlite
# authors:  1966bc
# mailto:   [giuseppecostanzi@gmail.com]
# modify:   hiems MMXXI
#------------------------------------------------------------------------------
import os
import sys
import inspect
import subprocess
import datetime

from dbms import DBMS
from tools import Tools
from clock import Clock



class Engine(DBMS, Tools, Clock):
    def __init__(self,):
        super().__init__()

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

    def on_log(self, container, function, exc_value, exc_type, module):

        now = datetime.datetime.now()
        log_text = "{0}\n{1}\n{2}\n{3}\n{4}\n\n".format(now, function, exc_value, exc_type, module)
        log_file = open("log.txt", "a")
        log_file.write(log_text)
        log_file.close()

    def get_dimensions(self):

        try:
            d = {}
            with open("dimensions", "r") as filestream:
                for line in filestream:
                    currentline = line.split(",")
                    d[currentline[0]] = currentline[1]

            return d

        except FileNotFoundError:
            self.on_log(self,
                        inspect.stack()[0][3],
                        sys.exc_info()[1],
                        sys.exc_info()[0],
                        sys.modules[__name__])

    def get_license(self):
        """get license"""
        try:
            path = self.get_file("LICENSE")
            f = open(path, "r")
            v = f.read()
            f.close()
            return v
        except FileNotFoundError:
            self.on_log(inspect.stack()[0][3],
                        sys.exc_info()[1],
                        sys.exc_info()[0],
                        sys.modules[__name__])

    def get_icon(self, which):

        try:
            path = self.get_file(which)
            f = open(path, "r")
            v = f.readline()
            f.close()
            return v

        except FileNotFoundError:
            self.on_log(self,
                        inspect.stack()[0][3],
                        sys.exc_info()[1],
                        sys.exc_info()[0],
                        sys.modules[__name__])

    def get_log_file(self):

        try:
            path = self.get_file("log.txt")
            self.open_file(path)
        except FileNotFoundError:
            self.on_log(self,
                        inspect.stack()[0][3],
                        sys.exc_info()[1],
                        sys.exc_info()[0],
                        sys.modules[__name__])

    def get_theme(self):

        try:
            path = self.get_file("theme")
            f = open(path, "r")
            theme = f.readline()
            f.close()
            return theme
        except FileNotFoundError:
            self.on_log(self,
                        inspect.stack()[0][3],
                        sys.exc_info()[1],
                        sys.exc_info()[0],
                        sys.modules[__name__])              

    def busy(self, caller):
        caller.config(cursor="watch")
        caller.update()

    def not_busy(self, caller):
        caller.config(cursor="")
        caller.update()            


def main():
    #testing some stuff
    foo = Engine()
    print(foo)
    print(foo.set_connection())
    input('end')

if __name__ == "__main__":
    main()
