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

import profile
import pstats
import sys

import ui.main

if len(sys.argv) > 1:
    profile.run("ui.main.main()", "profile_results")
    pstats.Stats("profile_results").sort_stats("cumulative").print_stats(10)
else:
    ui.main.main()
