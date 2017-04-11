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

class Engine(DBMS):
    def __init__(self):
        super(Engine, self).__init__()

        
        self.parameters = self.get_parameters()
        
        self.title = "Tkinterlite"

        self.about = "Tkinterlite\nDeveloped in Python 3.4.2 by:\n1966bc on Debian 8.7 jessie"
        
        
    def __str__(self):
        return "class: %s" % (self.__class__.__name__, )


    def get_parameters(self):
        """read parameters file
 
        @param name: none
        @return: dictionary 
        @rtype: dictionary
        """
        
        try:
            d = {}
            path = os.path.join(os.getcwd(),'parameters')
            db = shelve.open(path)
            for k, v in db.items():
                d[k] = (v)
            db.close()
            return d
        except:
            print (sys.exc_info()[0])
            print (sys.exc_info()[1])
            print (sys.exc_info()[2])
            

       
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
