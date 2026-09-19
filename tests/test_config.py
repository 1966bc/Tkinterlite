# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# project:  Tkinterlite
# authors:  Giuseppe Costanzi (1966bc)
# licence:  GPL-3.0-or-later, see LICENSE
# -----------------------------------------------------------------------------
"""Tests for config.py, on .ini files written in a temporary directory."""

import os
import tempfile
import unittest

from config import Config

GOOD = """; a comment
# another comment

[window]
theme = clam
width = 800
height = -1

[database]
url = file:northwind.sl3?mode=ro
"""


class TestConfig(unittest.TestCase):
    """A good file is read; a bad one is refused, naming the line."""

    def setUp(self):
        self.folder = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.folder.cleanup()

    def get_config(self, text):
        path = os.path.join(self.folder.name, "test.ini")
        with open(path, "w", encoding="utf-8") as f:
            f.write(text)
        return Config(path)

    def assert_refused(self, text, words):
        with self.assertRaises(ValueError) as caught:
            self.get_config(text)
        self.assertIn(words, str(caught.exception))

    def test_sections_and_keys(self):
        config = self.get_config(GOOD)
        self.assertEqual(sorted(config.sections), ["database", "window"])
        self.assertEqual(config.get("window", "theme"), "clam")

    def test_whole_numbers(self):
        config = self.get_config(GOOD)
        self.assertEqual(config.get_int("window", "width"), 800)
        self.assertEqual(config.get_int("window", "height"), -1)

    def test_value_may_contain_equals(self):
        config = self.get_config(GOOD)
        self.assertEqual(config.get("database", "url"), "file:northwind.sl3?mode=ro")

    def test_line_outside_any_section(self):
        self.assert_refused("theme = clam\n", "line 1: outside any section")

    def test_line_without_equals(self):
        self.assert_refused("[window]\n\nwidht 800\n", 'line 3: no "=" in "widht 800"')

    def test_key_twice(self):
        self.assert_refused("[window]\nwidth = 1\nwidth = 2\n", "line 3: width twice in [window]")

    def test_section_twice(self):
        self.assert_refused("[window]\n[window]\n", "line 2: section [window] twice")

    def test_missing_key(self):
        config = self.get_config(GOOD)
        with self.assertRaises(ValueError):
            config.get("window", "colour")

    def test_missing_section(self):
        config = self.get_config(GOOD)
        with self.assertRaises(ValueError):
            config.get("printer", "name")

    def test_not_a_whole_number(self):
        config = self.get_config(GOOD)
        with self.assertRaises(ValueError):
            config.get_int("window", "theme")


if __name__ == "__main__":
    unittest.main()
