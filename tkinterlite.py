#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# project:  Tkinterlite
# authors:  Giuseppe Costanzi (1966bc)
# licence:  GPL-3.0-or-later, see LICENSE
# -----------------------------------------------------------------------------
"""Start Tkinterlite.

    python3 tkinterlite.py

To see where the time goes, the standard library's profiler runs it as it is,
without a line of code here:

    python3 -m cProfile -s cumulative tkinterlite.py
"""

import os
from tkinter import messagebox

from log import Log
from ui.app import App

#: The folder of this file: the log lives here, beside the program.
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))


def main():

    # The log comes first, so that even a failure to start is written down.
    log = Log(os.path.join(PROJECT_DIR, "tkinterlite.log"))

    # Before the main loop there is no report_callback_exception yet:
    # a failure here is written to the log, shown, and raised again.
    try:
        app = App("Tkinterlite", log)
    except Exception as exc:
        log.exception("start failed: {0}".format(exc))
        messagebox.showerror("Tkinterlite", "{0}\n\nDetails in {1}".format(exc, log.path))
        raise

    app.mainloop()


if __name__ == "__main__":
    main()
