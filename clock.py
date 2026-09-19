# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# project:  Tkinterlite
# authors:  Giuseppe Costanzi (1966bc)
# licence:  GPL-3.0-or-later, see LICENSE
# -----------------------------------------------------------------------------
"""A clock on its own thread: how a thread and Tkinter work together.

Tkinter is single-threaded: only the thread that runs the main loop may touch
a widget. A second thread that calls label.config(...) itself works on one
machine, some of the time, and freezes or crashes on another - which is why
threads in Tkinter are argued about on every forum.

The pattern that works, in three parts:

    the thread makes data       Clock.run() puts a string on a queue
    the queue carries it        queue.Queue is safe between threads
    the main loop takes it      Main.check_clock() drains it, from after()

The thread never touches a widget; the main loop never waits for the thread.

For a clock this is more than is needed: after(1000, ...) alone would do. It is
here to show the pattern for work that does block - reading a slow device,
watching a folder - where the main loop must not stop and wait.
"""

import datetime
import queue
import threading


class Clock(threading.Thread):
    """Puts the time on a queue every second, on a thread of its own."""

    def __init__(self):
        # daemon: the thread ends with the program, even if stop() is forgotten.
        # A name, so that it can be told apart in threading.enumerate() or a traceback.
        super().__init__(name="clock", daemon=True)
        self.queue = queue.Queue()
        #: Set by stop(). An Event and not a boolean: wait() on it returns the
        #: moment it is set, so the thread does not sleep out its second first.
        self.stopping = threading.Event()

    def stop(self):
        """Ask the thread to end. Called from the main loop, on exit."""
        self.stopping.set()

    def run(self):
        """The thread's own code: one message now, then one a second until stopped.

        stopping.wait(1.0) is the sleep and the check in one: it returns False
        after a second, or True as soon as stop() is called.
        """
        self.put_time()
        while not self.stopping.wait(1.0):
            self.put_time()

    def put_time(self):
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.queue.put("Astral date: {0}".format(now))

    def drain(self):
        """Take every message off the queue, oldest first, without waiting.

        Called from the main loop, the only thread that takes from the queue:
        so a queue that is not empty here still has something for get_nowait().
        """
        messages = []
        while not self.queue.empty():
            messages.append(self.queue.get_nowait())
        return messages
