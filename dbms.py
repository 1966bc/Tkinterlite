#!/usr/bin/python3
#-----------------------------------------------------------------------------
# project:  tkinterlite
# authors:  1966bc
# mailto:   [giuseppe.costanzi@gmail.com]
# modify:   29/02/2020
# version:  0.2
#-----------------------------------------------------------------------------
import sys
import inspect
import sqlite3 as lite

class DBMS:
    def __init__(self, *args, **kwargs):

        self.args = args
        self.kwargs = kwargs
        self.set_connection()


    def __str__(self):
        return "class: {0}\nMRO: {1}".format(self.__class__.__name__,
                                             [x.__name__ for x in DBMS.__mro__],)


    def set_connection(self):

        self.con = lite.connect("northwind.sl3",
                                detect_types=lite.PARSE_DECLTYPES|lite.PARSE_COLNAMES,
                                isolation_level='IMMEDIATE')
        self.con.text_factory = lite.OptimizedUnicode


    def read(self, fetch, sql, args=()):

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



    def get_fields(self, table):
        """return fields name of the args table ordered by field number

        @param name: table,
        @return: fields
        @rtype: tuple
        """
        try:

            columns = []
            fields = []

            sql = 'SELECT * FROM %s ' % table
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

        return "UPDATE %s SET %s =? WHERE %s =?"%(table, " =?, ".join(self.get_fields(table)), pk)

    def get_insert_sql(self, table, n):

        #n = len(args)

        return "INSERT INTO %s(%s)VALUES(%s)"%(table, ",".join(self.get_fields(table)), ",".join("?"*n))

    def get_selected(self, table, field, *args):
        """recive table name, pk and return a dictionary

        @param name: table,field,*args
        @return: dictionary
        @rtype: dictionary
        """

        d = {}
        sql = "SELECT * FROM %s WHERE %s =?" % (table, field)

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
