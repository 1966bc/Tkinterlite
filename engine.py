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

        self.version = 2

        platform = "Debian Release 9 (stretch) 64-bit"
        s = "%s ver %s\nwritten by\n1966bc\nMilk galaxy\nSolar System\nThird planet(Earth) Italy(Rome)\ngiuseppecostanzi@gmail.com\n%s"
        msg = (s % (self.title,self.version,platform))

        self.about = msg
        
        
    def __str__(self):
        return "class: %s" % (self.__class__.__name__, )


       
    def explode_dict(self, obj):
        #for debug...
        for k, v in obj.iteritems():
                print (k,v,type(v))

   
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
