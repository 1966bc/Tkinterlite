#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import profile
import pstats
import frames.main as main

main.main()
#to try performance.....
#profile.run('main.main()', 'profile_results')
#p = pstats.Stats('profile_results')
#p.sort_stats('cumulative').print_stats(20)






    
