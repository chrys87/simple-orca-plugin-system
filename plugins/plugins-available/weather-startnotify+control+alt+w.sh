#!/bin/bash
# this presents the weather
# change the city to yours (see manual)
#for this you need weather-utils
# this is the default of the software
if [ -e /usr/bin/weather ]; then
    weather nuernberg | tail -n  +5
fi

#sadly in arch it is renamed caused by an fileconflict so we have to check
if [ -e /usr/bin/weather-report ]; then
    weather-report nuernberg | tail -n  +5
fi
