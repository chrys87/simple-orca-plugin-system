#!/bin/bash
#for this you need acpi
#it outputs battery information

if ! hash acpi &> /dev/null ; then
echo "This plugin requires the package acpi to function."
exit 1
fi
acpi
exit 0
