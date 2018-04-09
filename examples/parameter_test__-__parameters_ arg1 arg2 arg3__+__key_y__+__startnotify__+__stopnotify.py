#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#could used to print parameters passed by "parameters arg1 arg2 arg3"

import sys
import getopt
opts, extraparams = getopt.getopt(sys.argv[1:],"p:") 
print ("parameters")
for o,p in opts:
    print(o + " ")
    print(p)
print(extraparams)
