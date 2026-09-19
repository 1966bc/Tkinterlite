# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# project:  Tkinterlite
# authors:  Giuseppe Costanzi (1966bc)
# licence:  GPL-3.0-or-later, see LICENSE
# -----------------------------------------------------------------------------
"""Tests for log.py, on a file in a temporary directory."""

import os
import tempfile
import unittest

from log import Log


class TestLog(unittest.TestCase):
    """Each entry says when, how serious, where and what."""

    def setUp(self):
        self.folder = tempfile.TemporaryDirectory()
        self.log = Log(os.path.join(self.folder.name, "tkinterlite.log"))

    def tearDown(self):
        self.folder.cleanup()

    def get_text(self):
        with open(self.log.path, "r", encoding="utf-8") as f:
            text = f.read()
        return text

    def test_error_says_level_where_and_what(self):
        self.log.error("something went wrong")
        text = self.get_text()
        self.assertIn("ERROR", text)
        self.assertIn("test_error_says_level_where_and_what", text)
        self.assertIn("something went wrong", text)

    def test_exception_adds_the_traceback(self):
        try:
            int("abc")
        except ValueError:
            self.log.exception("not a number")
        text = self.get_text()
        self.assertIn("not a number", text)
        self.assertIn("Traceback (most recent call last)", text)
        self.assertIn("ValueError", text)

    def test_empty_until_the_first_entry(self):
        self.assertTrue(self.log.is_empty())
        self.log.error("first")
        self.assertFalse(self.log.is_empty())

    def test_entries_are_appended(self):
        self.log.error("first")
        self.log.error("second")
        text = self.get_text()
        self.assertLess(text.index("first"), text.index("second"))


class TestRotation(unittest.TestCase):
    """A full file is moved aside, and only BACKUPS of them are kept."""

    def setUp(self):
        self.folder = tempfile.TemporaryDirectory()
        self.log = Log(os.path.join(self.folder.name, "tkinterlite.log"))
        # A few bytes instead of a megabyte, on this instance only: every
        # entry is longer than this, so every entry after the first rotates.
        self.log.MAX_SIZE = 10

    def tearDown(self):
        self.folder.cleanup()

    def exists(self, suffix):
        return os.path.exists(self.log.path + suffix)

    def test_small_file_is_not_rotated(self):
        self.log.MAX_SIZE = 1024
        self.log.error("first")
        self.log.error("second")
        self.assertFalse(self.exists(".1"))

    def test_full_file_moves_to_one(self):
        self.log.error("first")
        self.log.error("second")
        with open(self.log.path + ".1", "r", encoding="utf-8") as f:
            self.assertIn("first", f.read())
        with open(self.log.path, "r", encoding="utf-8") as f:
            self.assertNotIn("first", f.read())

    def test_only_backups_are_kept(self):
        for number in range(10):
            self.log.error("entry {0}".format(number))
        self.assertTrue(self.exists(".1"))
        self.assertTrue(self.exists(".2"))
        self.assertTrue(self.exists(".3"))
        self.assertFalse(self.exists(".4"))
        with open(self.log.path + ".3", "r", encoding="utf-8") as f:
            self.assertIn("entry 6", f.read())


if __name__ == "__main__":
    unittest.main()
