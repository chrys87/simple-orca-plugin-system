#!/bin/sh
#output the ESSID and signal level
#needs iw (for iwconfig)
echo "Signal "
iwconfig $(iwgetid | cut -d\  -f 1) | grep "Signal level=" | cut -d\  -f 15 | sed 's/level=//g' | sed 's/\/100//g'
echo " %"
echo "Name"
iwconfig $(iwgetid | cut -d\  -f 1) | grep ESSID | cut -d\" -f2
