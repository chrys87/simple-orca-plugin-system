#!/bin/bash
#for this you need xprop
#it outputs the current workspace no
xprop -root _NET_CURRENT_DESKTOP | tail -c 3
