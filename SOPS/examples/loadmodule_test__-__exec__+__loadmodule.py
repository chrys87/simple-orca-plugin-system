#!/bin/python
# -*- coding: utf-8 -*-
# an example for import an advanced plugin
# loaded just once on starting orca (exec)
# change setting chname for !, let orca announce "bang" instead of !
import orca.orca # Imports the main screen reader
orca.chnames.chnames["!"] = "bang"

