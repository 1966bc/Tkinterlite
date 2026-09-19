# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# project:  Tkinterlite
# authors:  Giuseppe Costanzi (1966bc)
# licence:  GPL-3.0-or-later, see LICENSE
# -----------------------------------------------------------------------------
"""The Singleton pattern, one window per name, written by hand.

A textbook Singleton is a class that allows a single instance of itself. What
an application needs is one open window per name: one list of categories, one
About, one dialog at a time for a product. So this is a register of the open
windows, by name - a pattern also called Multiton.

Two rules:

    show(name, build)     a list, About, License: if it is already open,
                          bring it to the front; build it only if it is not.
    replace(name, build)  a dialog, which is about one row: the one open is
                          closed through its own on_cancel, which tidies up
                          after itself, and a new one is built.

build is a function that makes the window, not a window: when the answer is
"it is already open", nothing is built at all.

Python offers another way to write a Singleton: override __new__, which runs
before __init__, and return the instance already made. It works and it is
worth knowing, but Python then calls __init__ again on the old instance, and
every subclass must remember to skip it. A register does the same in plain
sight.
"""


class Windows:
    """The windows open now, by name."""

    def __init__(self, log):
        #: The log, for the trace (--trace).
        self.log = log
        #: The dictionary of instances: name -> the window open under that name.
        self.dict_instances = {}

    def __str__(self):
        return "class: {0}\nopen: {1}".format(self.__class__.__name__,
                                              ", ".join(self.dict_instances))

    def show(self, name, build):
        """The window called name: the one open, brought to the front, or a new one."""
        window = self.dict_instances.get(name)

        if window is None:
            window = self.add(name, build)
        else:
            window.lift()
            window.focus_set()
            self.log.trace("{0}: already open, brought to the front".format(name))

        return window

    def replace(self, name, build):
        """A new window called name, after closing the one open under that name."""
        window = self.dict_instances.get(name)

        if window is not None:
            self.log.trace("{0}: closing the one open".format(name))
            window.on_cancel()

        return self.add(name, build)

    def add(self, name, build):
        """Build the window, remember it, open it; forget it when it is destroyed.

        <Destroy> arrives however the window is closed - a button, the title
        bar's X, the application ending - so the register cannot be left
        holding a window that is gone.
        """
        window = build()
        self.dict_instances[name] = window
        window.bind("<Destroy>", lambda evt: self.forget(name, window, evt), add="+")
        window.on_open()
        self.log.trace("{0}: built; dict_instances = {1}".format(name, list(self.dict_instances)))

        return window

    def forget(self, name, window, evt):
        """Take a destroyed window out of the register.

        A Toplevel receives <Destroy> for every widget inside it as well:
        only its own counts. And only while it is still the window registered
        under that name, not one that has already been replaced.
        """
        if str(evt.widget) == str(window) and self.dict_instances.get(name) is window:
            del self.dict_instances[name]
            self.log.trace("{0}: forgotten; dict_instances = {1}".format(name,
                                                                        list(self.dict_instances)))
