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
# nvda-style-speech-control-left__-__control__+__key_Left
# sopsproperty:error
# sopsproperty:loadmodule

TMP_FILE = "/tmp/OrcaChange" # file used to store the current function
_speechControls = [ 'volume', 'rate', 'pitch', 'language']
LANGUAGE_file = "/etc/languages" # language files
LANG_PREF = 'f123-language-' #prefix to new profiles

_speechControl = None
_plugin_function = None
_speechFunctions = None
_settingsManager = getSettingsManager()

def _getControl():
    try:
        f = open(TMP_FILE, "r")
        key = f.read()
        f.close()
        key = key.rstrip('\r\n')
    except FileNotFoundError:
        key = 'volume'

    return key

def _saveControl(control):
    f=open(TMP_FILE, 'w')
    f.write(control)
    f.close()
    _speechControl = control

def _getProfiles():
    return _settingsManager.availableProfiles()

def _getCurrentLanguages():
    return[[ 'default', 'default' ]] +  [ x for x in _getProfiles() if x[1].startswith(LANG_PREF) ]

def _getNewLanguages():
    try:
        f = open('/etc/languages', "r")
        l = f.read()
        f.close()
    except FileNotFoundError:
        l = ""

    return re.sub(r'( *languages *= *\( *)|( *\))|( {2:})|(\r|\n)', '', l).split(' ')

def _getProfile():
    return _settingsManager.getProfile()

def _getControl():
    try:
        f = open(TMP_FILE, "r")
        key = f.read()
        f.close()
        key = key.rstrip('\r\n')
    except FileNotFoundError:
        key = 'volume'

    return key

def _setFamily(voices, language):
    lang, variant = (language.split('_')+ [''])[0:2]
    family = {
        'name': language,
        'lang': lang,
        'variant': variant,
        'dialect': ''
    }
    for voice in voices:
        voices[voice]['family'] = family

def _createNewProfile(language):
    profileName = LANG_PREF + language
    general = _settingsManager.getGeneralSettings('default').copy()
    general['profile'] = [ language, profileName ]
    _setFamily(general['voices'], language)
    _settingsManager._backend.saveProfileSettings(profileName, general, {}, {})

def _createLanguageProfiles():
    languages = _getCurrentLanguages()
    pnames = [ x[1] for x in languages ]
    xlanguages = _getNewLanguages()
    newLanguages = [ x for x in xlanguages if not (LANG_PREF+x) in pnames ]
    for language in newLanguages:
        _createNewProfile(language)

def _change_rate(ac):
    if ac == 'u':
        increaseSpeechRate()
    else:
        decreaseSpeechRate()

def _change_volume(ac):
    if ac == 'u':
        increaseSpeechVolume()
    else:
        decreaseSpeechVolume()

def _change_pitch(ac):
    if ac == 'u':
        increaseSpeechPitch()
    else:
        decreaseSpeechPitch()

def _change_language(ac):
    _createLanguageProfiles()
    increment = 1 if ac == 'u' else -1
    languages = _getCurrentLanguages()
    profile = _getProfile()
    new = [ x[1] for x in languages ].index(profile) + increment
    if new < 0:
        new = len(languages) - 1
    elif new >= len(languages):
        new = 0
    newProfile = languages[new][1]
    language = None
    if profile != newProfile:
        _settingsManager.setProfile(newProfile)
    language = languages[new][0]
    if language:
        msg = language
        speak(msg)

def _changeControl(ac):
    increment = 1 if ac == 'r' else -1
    control = _speechControl
    index = (_speechControls.index(control) if control in _speechControls else -1) + increment
    if index < 0:
        index = len(_speechControls)  - 1
    elif index >= len(_speechControls):
        index = 0
    control = _speechControls[index]
    _saveControl(control)
    msg = control
    speak(msg)

def _init():
    global _speechControl
    global _speechFunctions
    global _plugin_function
    _plugin_function = __name__.split("_", 1)[-1]
    _speechControl = _getControl()
    _speechFunctions = {
        'language': _change_language,
        'rate': _change_rate,
        'volume': _change_volume,
        'pitch': _change_pitch
    }

def nvda_style_speech_control_left():
    _changeControl('l')

def nvda_style_speech_control_right():
    _changeControl('r')

def nvda_style_speech_control_up():
    _speechFunctions[_speechControl]('u')

def nvda_style_speech_control_down():
    _speechFunctions[_speechControl]('d')

###
_init()

_plugin_functions = {
    "nvda_style_speech_control_left": nvda_style_speech_control_left,
    "nvda_style_speech_control_right": nvda_style_speech_control_right,
    "nvda_style_speech_control_down": nvda_style_speech_control_down,
    "nvda_style_speech_control_up": nvda_style_speech_control_up
}

_plugin_functions[_plugin_function]()
