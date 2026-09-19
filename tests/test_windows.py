# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# project:  Tkinterlite
# authors:  Giuseppe Costanzi (1966bc)
# licence:  GPL-3.0-or-later, see LICENSE
# -----------------------------------------------------------------------------
"""Tests for windows.py: one window per name, without Tk.

Windows only asks a window to bind, lift, take the focus, open and close, so
a small stand-in that does those things and writes them down is enough.
"""

import unittest

from windows import Windows


class QuietLog:
    """Stands in for Log: the trace is off, so trace() says nothing."""

    def trace(self, message):
        pass


class Event:
    """What Tk hands to a <Destroy> binding: the widget being destroyed."""

    def __init__(self, widget):
        self.widget = widget


class FakeWindow:
    """Stands in for a Toplevel, and remembers what was done to it."""

    def __init__(self, path):
        self.path = path
        self.done = []
        self.on_destroy = None

    def __str__(self):
        return self.path

    def bind(self, sequence, func, add=None):
        self.on_destroy = func

    def lift(self):
        self.done.append("lift")

    def focus_set(self):
        self.done.append("focus")

    def on_open(self):
        self.done.append("open")

    def on_cancel(self):
        self.done.append("cancel")
        self.destroy()

    def destroy(self):
        self.on_destroy(Event(self))


class TestWindows(unittest.TestCase):

    def setUp(self):
        self.windows = Windows(QuietLog())
        self.built = []

    def build(self):
        window = FakeWindow(".categories")
        self.built.append(window)
        return window

    def test_show_builds_once(self):
        first = self.windows.show("categories", self.build)
        second = self.windows.show("categories", self.build)
        self.assertIs(first, second)
        self.assertEqual(len(self.built), 1)
        self.assertEqual(first.done, ["open", "lift", "focus"])

    def test_show_builds_again_after_it_is_closed(self):
        first = self.windows.show("categories", self.build)
        first.destroy()
        second = self.windows.show("categories", self.build)
        self.assertIsNot(first, second)
        self.assertEqual(len(self.built), 2)

    def test_replace_closes_the_old_one_first(self):
        first = self.windows.replace("category", self.build)
        second = self.windows.replace("category", self.build)
        self.assertIsNot(first, second)
        self.assertEqual(first.done, ["open", "cancel"])
        self.assertIs(self.windows.dict_instances["category"], second)

    def test_a_widget_inside_does_not_close_the_window(self):
        window = self.windows.show("categories", self.build)
        window.on_destroy(Event(".categories.!frame.!listbox"))
        self.assertIs(self.windows.dict_instances["categories"], window)

    def test_an_old_window_does_not_forget_the_new_one(self):
        first = self.windows.show("categories", self.build)
        second = FakeWindow(".categories")
        self.windows.dict_instances["categories"] = second
        first.destroy()
        self.assertIs(self.windows.dict_instances["categories"], second)


if __name__ == "__main__":
    unittest.main()
