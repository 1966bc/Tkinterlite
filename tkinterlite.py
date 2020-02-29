#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import profile
import pstats
import frames.main as main

if len(sys.argv) > 1:
    profile.run('main.main()', 'profile_results')
    p = pstats.Stats('profile_results')
    p.sort_stats('cumulative').print_stats(10)
else:
    main.main()







