#! /usr/bin/python
# nvda-style-speech-control-right__-__error__+__loadmodule__+__control__+__key_Right

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
from orca.orca import getSettingsManager
from orca.speech import speak, decreaseSpeechPitch, increaseSpeechPitch, increaseSpeechRate, decreaseSpeechRate, increaseSpeechVolume, decreaseSpeechVolume
import re

TMP_FILE = "/tmp/OrcaChange" # file used to store the current functioRAT
LANGUAGE_file = "/etc/languages" # language files
LANG_PREF = 'f123-language-' #prefix to new profiles
_controls = [ 'volume', 'rate', 'pitch', 'language']
class Functions:
    _settingsManager = getSettingsManager()
    _control = None
    _functions = None
    def __init__(self):
        self._control = self._getControl()
        self._functions = {
            'language': self._change_language,
            'rate': self._change_rate,
            'volume': self._change_volume,
            'pitch': self._change_pitch
        }
        
    def _getProfiles(self):
        return self._settingsManager.availableProfiles()

    def _getCurrentLanguages(self):
        return[[ 'default', 'default' ]] +  [ x for x in self._getProfiles() if x[1].startswith(LANG_PREF) ]

    def _getNewLanguages(self):
        try:
            f = open('/etc/languages', "r")
            l = f.read()
            f.close()
        except FileNotFoundError:
            l = ""
    
        return re.sub(r'( *languages *= *\( *)|( *\))|( {2:})|(\r|\n)', '', l).split(' ')

    def _getProfile(self):
        return self._settingsManager.getProfile()

    def getFunction(self, fn):
        return getattr(self, fn, None)

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

    def _createLanguageProfiles(self):
        languages = self._getCurrentLanguages()
        pnames = [ x[1] for x in languages ]
        xlanguages = self._getNewLanguages()
        newLanguages = [ x for x in xlanguages if not (LANG_PREF+x) in pnames ]
        for language in newLanguages:
            self._createNewProfile(language)

    def _setFamily(self, voices, language):
        lang, variant = (language.split('_')+ [''])[0:2]
        family = {
            'name': language,
            'lang': lang,
            'variant': variant,
            'dialect': ''
        }
        for voice in voices:
            voices[voice]['family'] = family

    def _createNewProfile(self, language):
        profileName = LANG_PREF + language
        general = self._settingsManager.getGeneralSettings('default').copy()
        general['profile'] = [ language, profileName ]
        self._setFamily(general['voices'], language)
        self._settingsManager._backend.saveProfileSettings(profileName, general, {}, {})

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

    def _change_rate(self, ac):
        if ac == 'u':
            increaseSpeechRate()
        else:
            decreaseSpeechRate()

    def _change_volume(self, ac):
        if ac == 'u':
            increaseSpeechVolume()
        else:
            decreaseSpeechVolume()
            
    def _change_pitch(self, ac):
        if ac == 'u':
            increaseSpeechPitch()
        else:
            decreaseSpeechPitch()

    def _change_language(self, ac):
        self._createLanguageProfiles()
        increment = 1 if ac == 'u' else 'd'
        languages = self._getCurrentLanguages()
        profile = self._getProfile()
        new = [ x[1] for x in languages ].index(profile) + increment
        if new < 0:
            new = len(languages) - 1
        elif new >= len(languages):
            new = 0
        newProfile = languages[new][1]
        language = None
        if profile != newProfile:
            self._settingsManager.setProfile(newProfile)
        language = languages[new][0]
        if language:
            msg = 'Changing language to %s' % language
            speak(msg)
            
    def up(self):
        self._functions[self._control]('u')
        
    def down(self):
        self._functions[self._control]('u')

    def left(self):
        self._changeControl('l')

    def right(self):
        self._changeControl('r')

f = Functions()
f.right()
