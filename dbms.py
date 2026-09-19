# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# project:  Tkinterlite
# authors:  Giuseppe Costanzi (1966bc)
# licence:  GPL-3.0-or-later, see LICENSE
# -----------------------------------------------------------------------------
import datetime
import os
import sqlite3 as lite

class DBMS:
    def __init__(self, database, log):
        # Both are given by whoever creates the object: the application
        # passes the file beside the program and its Log, a test passes
        # ":memory:" and a log of its own.
        self.database = database
        self.log = log
        self.set_connection()

    def __str__(self):
        return "class: {0}\nMRO: {1}".format(self.__class__.__name__,
                                             [x.__name__ for x in DBMS.__mro__],)

    def set_connection(self):

        self.con = lite.connect(self.database,
                                detect_types=lite.PARSE_DECLTYPES|lite.PARSE_COLNAMES,
                                isolation_level='IMMEDIATE')
        # Every row can be read by column name, row["stock"], and not only
        # by position, row[6], which silently changes meaning the day a
        # column is added.
        self.con.row_factory = lite.Row


    def read(self, fetch, sql, args=()):

        """Remember that fetchall() return a list.\
           An empty list is returned when no rows are available.
           Testing if the list is empty with 'if rs' or 'if not rs'
           Otherwise fetchone() return a single sequence, or None
           when no more data is available.
           Testing as 'if rs is not None'.

           A failed query is written to the log, with the statement, and
           raised again: it never turns into an empty result.
        """

        cur = self.con.cursor()
        try:
            cur.execute(sql, args)
            if fetch == True:
                rs = cur.fetchall()
            else:
                rs = cur.fetchone()
        except lite.Error:
            self.log.error("read failed: {0}".format(sql))
            raise
        finally:
            cur.close()

        if fetch == True:
            self.log.trace("{0} {1} -> {2} rows".format(" ".join(sql.split()), args, len(rs)))
        else:
            self.log.trace("{0} {1} -> {2}".format(" ".join(sql.split()), args, self.get_dict(rs)))

        return rs

    def write(self, sql, args=()):
        """Run one statement and commit it; return the id of the new row.

        A failed statement is rolled back, written to the log with the
        statement, and raised again.
        """

        cur = self.con.cursor()
        try:
            cur.execute(sql, args)
            self.con.commit()
            row_id = cur.lastrowid
        except lite.Error:
            self.con.rollback()
            self.log.error("write failed, rolled back: {0}".format(sql))
            raise
        finally:
            cur.close()

        self.log.trace("{0} {1} -> lastrowid {2}".format(" ".join(sql.split()), args, row_id))

        return row_id

    def get_dict(self, row):
        """A row as a dictionary, for the trace; None stays None."""
        found = None
        if row is not None:
            found = dict(row)
        return found

    def dump(self, folder):
        """Write the whole database as SQL into folder; return the file's path.

        The file is named after the moment, YYYYMMDDHHMMSS.sql, so dumps
        sort by date and never overwrite each other. The folder is created
        the first time.
        """
        name = "{0}.sql".format(datetime.datetime.now().strftime("%Y%m%d%H%M%S"))
        path = os.path.join(folder, name)

        os.makedirs(folder, exist_ok=True)

        with open(path, "w", encoding="utf-8") as f:
            for line in self.con.iterdump():
                f.write("{0}\n".format(line))

        return path

    def get_table_info(self, table):
        """What a table is made of, asked of the schema.

        PRAGMA table_info says, for every column, its name and whether it is
        the primary key: nothing is guessed from the order of the columns.

        @param name: table
        @return: (name, is primary key) per column, in table order
        @rtype: list
        """
        rows = self.read(True, "PRAGMA table_info({0})".format(table))

        if not rows:
            raise ValueError("no table {0}".format(table))

        return [(row["name"], bool(row["pk"])) for row in rows]

    def get_primary_key(self, table):
        """The primary key column of a table, asked of the schema.

        @param name: table
        @return: column name
        @rtype: string
        """
        keys = [name for name, is_key in self.get_table_info(table) if is_key]

        if len(keys) != 1:
            raise ValueError("{0} has {1} primary key columns, not one".format(table,
                                                                               len(keys)))

        return keys[0]

    def get_fields(self, table):
        """Column names of a table, primary key excluded, in table order.

        The key is left out because the schema says it is the key, not
        because it happens to be the first column.

        @param name: table
        @return: fields
        @rtype: tuple
        """
        return tuple(name for name, is_key in self.get_table_info(table) if not is_key)

    def get_args(self, table, values):
        """The values of a row as a list, in the order the schema declares.

        values is a dictionary keyed by column name, so no window has to know
        the order of the columns. A missing column and an unknown one are
        both refused, naming the table.

        @param name: table, values
        @return: args
        @rtype: list
        """
        fields = self.get_fields(table)
        missing = [name for name in fields if name not in values]
        unknown = [name for name in values if name not in fields]

        if missing or unknown:
            raise ValueError("{0}: missing {1}, not a column {2}".format(table,
                                                                        missing,
                                                                        unknown))

        return [values[name] for name in fields]

    def get_insert(self, table, values):
        """An INSERT and its args, with the values given by column name.

        @param name: table, values
        @return: sql, args
        @rtype: tuple
        """
        fields = self.get_fields(table)
        sql = "INSERT INTO {0} ({1}) VALUES ({2})".format(table,
                                                         ", ".join(fields),
                                                         ", ".join("?" * len(fields)))

        return (sql, self.get_args(table, values))

    def get_update(self, table, key_value, values):
        """An UPDATE and its args, with the values given by column name.

        The primary key is asked of the schema and its value goes last.

        @param name: table, key_value, values
        @return: sql, args
        @rtype: tuple
        """
        assignments = ", ".join("{0} = ?".format(name) for name in self.get_fields(table))
        sql = "UPDATE {0} SET {1} WHERE {2} = ?".format(table,
                                                       assignments,
                                                       self.get_primary_key(table))
        args = self.get_args(table, values)
        args.append(key_value)

        return (sql, args)

    def get_selected(self, table, field, *args):
        """recive table name, pk and return a dictionary keyed by column name

        @param name: table,field,*args
        @return: dictionary
        @rtype: dictionary
        """

        sql = "SELECT * FROM {0} WHERE {1} = ?".format(table, field)

        return dict(self.read(False, sql, args))
