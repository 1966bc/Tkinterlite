#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# project:  Tkinterlite
# authors:  Giuseppe Costanzi (1966bc)
# licence:  GPL-3.0-or-later, see LICENSE
# -----------------------------------------------------------------------------
"""Start Tkinterlite.

    python3 tkinterlite.py        start the application
    python3 tkinterlite.py x      any argument: run it under the profiler, and
                                  print the ten calls that took longest
"""

import os
import profile
import pstats
import sys
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
    if len(sys.argv) > 1:
        profile.run("main()", "profile_results")
        pstats.Stats("profile_results").sort_stats("cumulative").print_stats(10)
    else:
        main()
