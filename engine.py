#!/usr/bin/python3
#-----------------------------------------------------------------------------
# project:  tkinterlite
# authors:  1966bc
# mailto:   [giuseppe.costanzi@gmail.com]
# modify:   10/04/2017
# version:  0.1                                                                
#-----------------------------------------------------------------------------
import os
import sys
import shelve

from dbms import DBMS
from widgets import Widgets

class Engine(DBMS, Widgets):
    def __init__(self):
        super(Engine, self).__init__()

        
        self.title = "Tkinterlite"

        self.version = self.get_version()

        platform = "Debian Release 9 (stretch) 64-bit"
        s = "%s ver %s\nwritten by\n1966bc\nMilk galaxy\nSolar System\nThird planet(Earth) Italy(Rome)\ngiuseppecostanzi@gmail.com\n%s"
        msg = (s % (self.title,self.version,platform))

        self.about = msg

        self.no_selected = "Attention!\nNo record selected!"
        self.mandatory = "Attention!\nField %s is mandatory!"
        self.delete = "Delete data?"
        self.ask_to_save = "Save data?"
        self.abort = "Operation aborted!"
        
        
    def __str__(self):
        return "class: %s" % (self.__class__.__name__, )


       
    def explode_dict(self, obj):
        #for debug...
        for k, v in obj.iteritems():
                print (k,v,type(v))

    def get_version(self):
        
        try:
            f = open('version', 'r')
            s = f.readline()
            f.close()
            return s
        except:
            print(inspect.stack()[0][3])
            print (sys.exc_info()[0])
            print (sys.exc_info()[1])
            print (sys.exc_info()[2])

    def get_dimensions(self):

        try:
            d = {}
            with open("dimensions", "r") as filestream:
                for line in filestream:
                    currentline = line.split(",")
                    d[currentline[0]] = currentline[1]
                      
            return d
        except:
            print(inspect.stack()[0][3])
            print (sys.exc_info()[0])
            print (sys.exc_info()[1])
            print (sys.exc_info()[2])                

   
def main():

    #testing some stuff

    print ("MRO:", [x.__name__ for x in Engine.__mro__])
   
    foo = Engine()

    print (foo)

    print (foo.get_connection())

    print (foo.title)

    x = foo.get_parameters()

    print (x)
    
    input('end')
       
if __name__ == "__main__":
    main()
