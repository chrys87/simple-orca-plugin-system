#! /usr/bin/python

#
# Copyright 2019, F123 Consulting, <information@f123.org>
# Copyright 2019, Michael Taboada, <michael@michaels.world>
# Copyright 2019, Informal Informática, <gestao@informal.com.br>
#
# This is free software; you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free
# Software Foundation; either version 3, or (at your option) any later
# version.
#
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this package; see the file COPYING.  If not, write to the Free
# Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA.
#
from orca.speech import speak
# properties
# nvda-style-speech-control-right__-__control__+__key_Right
# sopsproperty:error
# sopsproperty:loadmodule

TMP_FILE = "/tmp/OrcaChange" # file used to store the current functioRAT
_controls = [ 'volume', 'rate', 'pitch', 'language']

class NvdaStyleSpeechControlRight:
    _control = None

    def __init__(self):
        self._control = self._getControl()

    def _getControl(self):
        try:
            f = open(TMP_FILE, "r")
            key = f.read()
            f.close()
            key = key.rstrip('\r\n')
        except FileNotFoundError:
            key = 'volume'
    
        return key

    def _saveControl(self, control):
        f=open(TMP_FILE, 'w')
        f.write(control)
        f.close()
        self._control = control

    def _changeControl(self, ac):
        increment = 1 if ac == 'r' else -1
        control = self._control
        index = (_controls.index(control) if control in _controls else -1) + increment
        if index < 0:
            index = len(_controls)  - 1
        elif index >= len(_controls):
            index = 0
        control = _controls[index]
        self._saveControl(control)
        msg = control
        speak(msg)

    def right(self):
        self._changeControl('r')

f = NvdaStyleSpeechControlRight()
f.right()
