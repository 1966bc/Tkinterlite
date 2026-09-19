# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# project:  Tkinterlite
# authors:  Giuseppe Costanzi (1966bc)
# licence:  GPL-3.0-or-later, see LICENSE
# -----------------------------------------------------------------------------
"""The application log, written by hand.

The standard library has `logging`, which does this and much more: levels,
handlers, formats. This class does only what Tkinterlite needs, so that a
reader can see what a logger does underneath: take the time, find out who is
calling, append one entry to a file, and move the file aside when it is full.

It also keeps the trace: with `python3 tkinterlite.py --trace`, trace() prints
on the terminal, line by line, what the program is doing and what its
variables hold, while the window is in use.
"""

import datetime
import inspect
import os
import traceback


class Log:
    """One file, one entry per event: when, how serious, where, what."""

    #: Past this size, in bytes, the file is rotated before the next entry.
    MAX_SIZE = 1024 * 1024

    #: How many full files are kept: .1 is the most recent, .3 the oldest.
    BACKUPS = 3

    def __init__(self, path, tracing=False):
        self.path = path
        #: True when the program was started with --trace.
        self.tracing = tracing

    def __str__(self):
        return "class: {0}\npath: {1}".format(self.__class__.__name__, self.path)

    def is_empty(self):
        """True when nothing has been written yet: the file is born with the first entry."""
        return not os.path.exists(self.path) or os.path.getsize(self.path) == 0

    def trace(self, message):
        """Print what the program is doing, when it was started with --trace.

        Printed on the terminal and not written to the file: the trace is for
        watching the program work, beside its window. Each line says when,
        who - the class and method that called trace() - and what.

        It prints the data too - a row, the values of a form, the arguments
        of a statement - so it is for sample data like Northwind, never for a
        database that holds real people.

        inspect.currentframe() is the frame running this method; f_back is
        the one that called it, and its local 'self' is the object at work.
        """
        if self.tracing:
            caller = inspect.currentframe().f_back
            owner = caller.f_locals.get("self")
            where = caller.f_code.co_name
            if owner is not None:
                where = "{0}.{1}.{2}".format(owner.__class__.__module__,
                                             owner.__class__.__name__,
                                             where)
            now = datetime.datetime.now().strftime("%H:%M:%S")
            print("{0} {1:<34} {2}".format(now, where, message), flush=True)

    def error(self, message):
        """Something went wrong: when, where and what."""
        self.write("ERROR", message, "")

    def exception(self, message):
        """The same, from inside an except block, with the traceback.

        traceback.format_exc() reads the exception being handled at this
        moment, so this has to be called while it is being handled.
        """
        self.write("ERROR", message, traceback.format_exc())

    def write(self, level, message, trace):
        """Append one entry to the file.

        inspect.stack() is the chain of calls that led here: [0] is this
        method, [1] is error() or exception(), [2] is whoever called them.
        """
        where = inspect.stack()[2].function
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = "{0} {1} {2}: {3}\n{4}".format(now, level, where, message, trace)

        self.rotate()
        with open(self.path, "a", encoding="utf-8") as f:
            f.write(entry)

    def rotate(self):
        """Move the file aside when it is full, and keep BACKUPS of them.

        What logging.handlers.RotatingFileHandler does: .2 becomes .3, .1
        becomes .2, the file becomes .1, and the next entry starts a new
        file. os.replace overwrites its target, so the oldest copy goes.
        """
        if os.path.exists(self.path) and os.path.getsize(self.path) >= self.MAX_SIZE:
            for number in range(self.BACKUPS - 1, 0, -1):
                older = "{0}.{1}".format(self.path, number)
                if os.path.exists(older):
                    os.replace(older, "{0}.{1}".format(self.path, number + 1))
            os.replace(self.path, "{0}.1".format(self.path))
