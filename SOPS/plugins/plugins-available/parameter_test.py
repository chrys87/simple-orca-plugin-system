#!/bin/python
# -*- coding: utf-8 -*-
# print parameters

import sys
import getopt
opts, extraparams = getopt.getopt(sys.argv[1:],"p:") 
print ("parameters")
for o,p in opts:
    print(o + " ")
    print(p)
print(extraparams)
