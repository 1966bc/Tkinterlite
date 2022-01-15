#!/usr/bin/python3
#-----------------------------------------------------------------------------
# project:  tkinterlite
# authors:  1966bc
# mailto:   [giuseppecostanzi@gmail.com]
# modify:   hiems MMXXI
#------------------------------------------------------------------------------
""" This is the clock module of Tkinterlite."""
import threading
import queue
import datetime
import time


class Clock(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

        self.queue = queue.Queue()
        self.check = True

    def stop(self):
        self.check = False

    def run(self):

        """Feeds the tail."""

        while self.check:
            s = "Astral date: "
            t = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            msg = "{0} {1}".format(s, t)
            time.sleep(1)
            self.queue.put(msg)
    
    def check_queue(self, obj):

        """Returns a formatted string representing time."""

        while self.queue.qsize():
            try:
                x = self.queue.get(0)
                msg = "{0}".format(x)
                obj.set(msg)
            except queue.Empty:
                pass
