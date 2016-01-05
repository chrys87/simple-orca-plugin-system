#!/bin/bash
# this presents the weather
# change the city to yours (see manual)
#for this you need weather-utils
if [ -e /usr/bin/weather ]; then
    weather nuernberg | tail -n  +5
fi
if [ -e /usr/bin/weather-report ]; then
    weather-report nuernberg | tail -n  +5
fi
