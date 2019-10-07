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
from orca.orca import getSettingsManager
from orca.speech import speak, decreaseSpeechPitch, increaseSpeechPitch, increaseSpeechRate, decreaseSpeechRate, increaseSpeechVolume, decreaseSpeechVolume
import re
#
# properties
# nvda-style-speech-control-down__-__key_Down
# sopsproperty:error
# sopsproperty:loadmodule

TMP_FILE = "/tmp/OrcaChange" # file used to store the current functioRAT
LANGUAGE_file = "/etc/languages" # language files
LANG_PREF = 'f123-language-' #prefix to new profiles

class NvdaStyleSpeechControlDown:
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

    def _getControl(self):
        try:
            f = open(TMP_FILE, "r")
            key = f.read()
            f.close()
            key = key.rstrip('\r\n')
        except FileNotFoundError:
            key = 'volume'
    
        return key

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
        increment = 1 if ac == 'u' else -1
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
            msg = language
            speak(msg)

    def down(self):
        self._functions[self._control]('d')

f = NvdaStyleSpeechControlDown()
f.down()
