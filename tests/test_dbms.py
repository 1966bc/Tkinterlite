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


class Store(DBMS):
    """DBMS as Engine uses it, with on_log keeping what it is told.

    In the application on_log comes from Engine and writes log.txt; here it
    only remembers, so a test can ask whether an error was logged.
    """

    def __init__(self):
        self.logged = []
        super().__init__(":memory:")
        self.con.executescript(SCHEMA)

    def on_log(self, *args):
        self.logged.append(args)


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

    def test_failed_read_is_logged_and_returns_none(self):
        # Today's behaviour, written down so that changing it is a decision:
        # step 7 of the plan makes a failed read raise instead.
        row = self.store.read(False, "SELECT * FROM customers")
        self.assertIsNone(row)
        self.assertEqual(len(self.store.logged), 1)


if __name__ == "__main__":
    unittest.main()
