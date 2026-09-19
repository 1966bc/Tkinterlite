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

    def __init__(self, path):
        self.path = path

    def __str__(self):
        return "class: {0}\npath: {1}".format(self.__class__.__name__, self.path)

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
