#!/bin/python
# an example for import an python module into orca
# name
#loadmodule_test__-__exec__+__loadmodule__+__y.py
#runs on start so chname is available
#and run on orca + y (speaks test) everytime
import orca.orca # Imports the main screen reader
orca.chnames.chnames["!"] = "bang"
orca.speech.speak("test")
