#!/bin/bash
#for this you need xprop
#it outputs the current workspace no

if ! hash xprop &> /dev/null ; then
echo "This plugin requires the package xprop to function."
exit 1
fi
echo "Workspace $(($(xprop -root _NET_CURRENT_DESKTOP | tail -c 3) + 1))"
exit 0
