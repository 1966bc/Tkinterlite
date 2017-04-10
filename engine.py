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
import socket
import subprocess
import datetime
import tkinter as tk

from dbms import DBMS

class Engine(DBMS):
    def __init__(self):
        super(Engine, self).__init__()
        
        self.title = "Tkinterlite"
        
    def __str__(self):
        return "class: %s" % (self.__class__.__name__, )
 
    def get_log_ip(self):
        return socket.gethostbyname(socket.getfqdn())
    
    def get_log_time(self):
        return datetime.datetime.now()
    
    def get_date(self,):
        return datetime.datetime.now()

    def get_hour(self,):
        return "%s"% datetime.datetime.now().strftime("%H:%M:%S")
        
             
    def get_instance(self,obj):
        """accept an object, frame, and add it to a dictionary"""
        #print (obj.__class__.__name__)
        
        self.dict_instances[obj]= obj.__class__.__name__
        self.show_instances()

    def del_instance(self,name):
        #print (name)
        del self.dict_instances[name]
        self.show_instances()

    def match_instance(self,obj):
        """is an object istance alive?"""
        if obj in self.dict_instances:
            return True
        else:
            return False

    def show_instances(self,debug= None):
        if debug is not None:
            for k,v in self.dict_instances.iteritems():
                print (k)
            print ('-'*30)

    def open_file(self,path):

        if os.path.exists(path):
            if os.name == 'posix':
                subprocess.call(["xdg-open", path])
            else:
                os.startfile(path)
        else:
            msg = "%s\n%s" %(path,self.file_not_fount)
            
    def explode_dict(self, obj):
        #for debug...
        for k, v in obj.iteritems():
                print (k,v,type(v))

   
def main():


    print ("MRO:", [x.__name__ for x in Engine.__mro__])
   
   
    foo = Engine()

    print (foo)

    print (foo.get_connection())

    print (foo.app_title)
    
    input('end')
       
if __name__ == "__main__":
    main()
