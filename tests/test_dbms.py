# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# project:  Tkinterlite
# authors:  Giuseppe Costanzi (1966bc)
# licence:  GPL-3.0-or-later, see LICENSE
# -----------------------------------------------------------------------------
"""Tests for dbms.py, on a database in memory: northwind.sl3 is never touched.

Run them from the project directory:

    python3 -m unittest discover -s tests -v
"""

import os
import sqlite3
import tempfile
import unittest

from dbms import DBMS

SCHEMA = """
CREATE TABLE suppliers (
    supplier_id INTEGER PRIMARY KEY,
    company TEXT,
    enable BOOLEAN DEFAULT '1'
);
CREATE TABLE lots (
    code TEXT,
    lot_id INTEGER PRIMARY KEY,
    expiry TEXT
);
INSERT INTO suppliers VALUES (1, 'Exotic Liquids', 1);
INSERT INTO suppliers VALUES (2, 'Tokyo Traders', 0);
"""


class MemoryLog:
    """A stand-in for Log that keeps its entries in a list instead of a file.

    DBMS only calls log.error(), so this is all a test needs: the entries can
    be read back without opening a file.
    """

    def __init__(self):
        self.entries = []

    def error(self, message):
        self.entries.append(message)


class Store(DBMS):
    """DBMS on a database in memory, with the test schema and a MemoryLog."""

    def __init__(self):
        super().__init__(":memory:", MemoryLog())
        self.con.executescript(SCHEMA)


class TestSchema(unittest.TestCase):
    """The structure of a table is asked of the schema, not guessed."""

    def setUp(self):
        self.store = Store()

    def tearDown(self):
        self.store.con.close()

    def test_primary_key(self):
        self.assertEqual(self.store.get_primary_key("suppliers"), "supplier_id")

    def test_primary_key_not_in_first_place(self):
        self.assertEqual(self.store.get_primary_key("lots"), "lot_id")

    def test_fields_leave_out_the_key(self):
        self.assertEqual(self.store.get_fields("suppliers"), ("company", "enable"))

    def test_fields_leave_out_the_key_wherever_it_is(self):
        self.assertEqual(self.store.get_fields("lots"), ("code", "expiry"))

    def test_unknown_table_is_refused(self):
        with self.assertRaises(ValueError):
            self.store.get_fields("customers")


class TestStatements(unittest.TestCase):
    """INSERT and UPDATE are built from the schema, values go by name."""

    def setUp(self):
        self.store = Store()

    def tearDown(self):
        self.store.con.close()

    def test_insert(self):
        sql, args = self.store.get_insert("suppliers",
                                          {"company": "Pavlova", "enable": 1})
        self.assertEqual(sql, "INSERT INTO suppliers (company, enable) VALUES (?, ?)")
        self.assertEqual(args, ["Pavlova", 1])

    def test_update_puts_the_key_last(self):
        sql, args = self.store.get_update("suppliers", 2,
                                          {"company": "Pavlova", "enable": 1})
        self.assertEqual(sql,
                         "UPDATE suppliers SET company = ?, enable = ? WHERE supplier_id = ?")
        self.assertEqual(args, ["Pavlova", 1, 2])

    def test_args_follow_the_schema_not_the_dictionary(self):
        sql, args = self.store.get_insert("suppliers",
                                          {"enable": 0, "company": "Pavlova"})
        self.assertEqual(args, ["Pavlova", 0])

    def test_missing_column_is_refused(self):
        with self.assertRaises(ValueError):
            self.store.get_insert("suppliers", {"company": "Pavlova"})

    def test_unknown_column_is_refused(self):
        with self.assertRaises(ValueError):
            self.store.get_insert("suppliers",
                                  {"company": "Pavlova", "enable": 1, "city": "Rome"})


class TestReadWrite(unittest.TestCase):
    """Rows go in with write and come back, by name, with read."""

    def setUp(self):
        self.store = Store()

    def tearDown(self):
        self.store.con.close()

    def test_read_by_name(self):
        row = self.store.read(False, "SELECT * FROM suppliers WHERE supplier_id = ?", (1,))
        self.assertEqual(row["company"], "Exotic Liquids")

    def test_read_all(self):
        rows = self.store.read(True, "SELECT * FROM suppliers ORDER BY supplier_id")
        self.assertEqual([row["company"] for row in rows],
                         ["Exotic Liquids", "Tokyo Traders"])

    def test_insert_then_read(self):
        sql, args = self.store.get_insert("suppliers",
                                          {"company": "Pavlova", "enable": 1})
        new_id = self.store.write(sql, args)
        row = self.store.get_selected("suppliers", "supplier_id", new_id)
        self.assertEqual(row, {"supplier_id": 3, "company": "Pavlova", "enable": 1})

    def test_update_then_read(self):
        sql, args = self.store.get_update("suppliers", 2,
                                          {"company": "Tokyo Traders", "enable": 1})
        self.store.write(sql, args)
        row = self.store.get_selected("suppliers", "supplier_id", 2)
        self.assertEqual(row["enable"], 1)

    def test_failed_read_raises_and_is_logged(self):
        # It used to be logged and returned as None, and the error surfaced
        # later, somewhere else. Now it raises where it happens.
        with self.assertRaises(sqlite3.Error):
            self.store.read(False, "SELECT * FROM customers")
        self.assertEqual(self.store.log.entries,
                         ["read failed: SELECT * FROM customers"])

    def test_failed_write_raises_is_logged_and_rolled_back(self):
        with self.assertRaises(sqlite3.Error):
            self.store.write("INSERT INTO suppliers (city) VALUES (?)", ("Rome",))
        self.assertEqual(len(self.store.log.entries), 1)
        rows = self.store.read(True, "SELECT * FROM suppliers")
        self.assertEqual(len(rows), 2)


class TestDump(unittest.TestCase):
    """The whole database as SQL, into a folder that may not exist yet."""

    def setUp(self):
        self.store = Store()
        self.folder = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.store.con.close()
        self.folder.cleanup()

    def test_dump_creates_the_folder_and_the_file(self):
        folder = os.path.join(self.folder.name, "dumps")
        path = self.store.dump(folder)
        self.assertEqual(os.path.dirname(path), folder)
        with open(path, "r", encoding="utf-8") as f:
            text = f.read()
        self.assertIn("CREATE TABLE suppliers", text)
        self.assertIn("Exotic Liquids", text)


if __name__ == "__main__":
    unittest.main()
