#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# an example for import an advanced plugin
# loaded just once on starting orca (exec)
# change setting chname for !, let orca announce "bang" instead of !

#the following could be done to specify SOPS propertys in the file
#sopsproperty:loadmodule
import orca.orca # Imports the main screen reader
orca.chnames.chnames["!"] = "bang"

