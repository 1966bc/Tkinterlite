#!/usr/bin/python3
#-----------------------------------------------------------------------------
# project:  tkinterlite
# authors:  1966bc
# mailto:   [giuseppecostanzi@gmail.com]
# modify:   hiems MMXX
#-----------------------------------------------------------------------------
import sys
import inspect
import datetime
import sqlite3 as lite

class DBMS:
    def __init__(self,):
        self.set_connection()
        #super().__init__()

    def __str__(self):
        return "class: {0}\nMRO: {1}".format(self.__class__.__name__,
                                             [x.__name__ for x in DBMS.__mro__],)

    def set_connection(self):

        self.con = lite.connect("northwind.sl3",
                                detect_types=lite.PARSE_DECLTYPES|lite.PARSE_COLNAMES,
                                isolation_level='IMMEDIATE')
        self.con.text_factory = lite.OptimizedUnicode


    def read(self, fetch, sql, args=()):

        """Remember that fetchall() return a list.\
           An empty list is returned when no rows are available.
           Testing if the list is empty with 'if rs' or 'if not rs'
           Otherwise fetchone() return a single sequence, or None
           when no more data is available.
           Testing as 'if rs is not None'.
        """

        try:
            cur = self.con.cursor()
            cur.execute(sql, args)

            if fetch == True:
                rs = cur.fetchall()
            else:
                rs = cur.fetchone()
            cur.close()
            return rs

        except:
            self.on_log(self,
                        inspect.stack()[0][3],
                        sys.exc_info()[1],
                        sys.exc_info()[0],
                        sys.modules[__name__])

    def write(self, sql, args=()):

        try:
            cur = self.con.cursor()
            cur.execute(sql, args)
            self.con.commit()
            return cur.lastrowid

        except:
            self.con.rollback()
            self.on_log(self,
                        inspect.stack()[0][3],
                        sys.exc_info()[1],
                        sys.exc_info()[0],
                        sys.modules[__name__])
            
        finally:
            try:
                cur.close()
            except:
                self.on_log(self,
                            inspect.stack()[0][3],
                            sys.exc_info()[1],
                            sys.exc_info()[0],
                            sys.modules[__name__])

    def dump(self,):

        dt = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        s = dt + ".sql"
        with open(s, 'w') as f:
            for line in self.con.iterdump():
                f.write('%s\n' % line)

    def get_fields(self, table):
        """return fields name of the args table ordered by field number

        @param name: table,
        @return: fields
        @rtype: tuple
        """
        try:

            columns = []
            fields = []
            sql = "SELECT * FROM {0}".format(table)
            cur = self.con.cursor()
            cur.execute(sql)

            for field in cur.description:
                columns.append(field[0])
            cur.close()

            for k, v in enumerate(columns):
                if k > 0:
                    fields.append(v)

            return tuple(fields)
        except:
            self.on_log(self,
                        inspect.stack()[0][3],
                        sys.exc_info()[1],
                        sys.exc_info()[0],
                        sys.modules[__name__])
        finally:
            try:
                cur.close()
            except:
                self.on_log(self,
                            inspect.stack()[0][3],
                            sys.exc_info()[1],
                            sys.exc_info()[0],
                            sys.modules[__name__])


    def get_update_sql(self, table, pk):
        """recive a table name and his pk to format an update sql statement

        @param name: table, pk
        @return: sql formatted stringstring
        @rtype: string
        """
        return "UPDATE {0} SET {1} =? WHERE {2} =?".format(table, " =?, ".join(self.get_fields(table)), pk)

    def get_insert_sql(self, table, n):
        """recive a table name and len of args, len(args),
           to format an insert sql statement

        @param name: table, n = len(args)
        @return: sql formatted stringstring
        @rtype: string
        """

        return "INSERT INTO {0}({1})VALUES({2})".format(table, ",".join(self.get_fields(table)), ",".join("?"*n))


    def get_selected(self, table, field, *args):
        """recive table name, pk and return a dictionary

        @param name: table,field,*args
        @return: dictionary
        @rtype: dictionary
        """

        d = {}
        sql = "SELECT * FROM {0} WHERE {1} = ?".format(table, field)

        for k, v in enumerate(self.read(False, sql, args)):
            d[k] = v

        return d


def main():

    foo = DBMS()
    print(foo)

    sql = "SELECT name FROM sqlite_master WHERE type = 'table'"
    rs = foo.read(True, sql)
    if rs:
        for i in enumerate(rs):
            print(i)

    input('end')

if __name__ == "__main__":
    main()
