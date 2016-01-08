# -*- coding: utf-8 -*-
# chrys
# version 0.1

import glob
import os
import subprocess
import random
import string
import _thread
from subprocess import Popen, PIPE

import orca.orca

#settings
scriptrepo = os.path.expanduser('~')+"/.config/SOPS/plugins-enabled/"

#globals
functions = []
inputEventHandlers = []
loaded = False
myKeyBindings = orca.keybindings.KeyBindings()

def outputMessage(Message):
    if (orca.settings.enableSpeech):
        orca.speech.speak(Message)
    if (orca.settings.enableBraille):
        orca.braille.displayMessage(Message)

def SetupShortcutAndHandle(fun, settings):
    inputEventHandlers.append(orca.input_event.InputEventHandler(fun, settings['scriptname'], settings))
    # just the orca modifier
    if not settings['shiftkey'] and not settings['ctrlkey'] and not settings['altkey']:
        myKeyBindings.add(orca.keybindings.KeyBinding(settings['key'], orca.keybindings.defaultModifierMask, orca.keybindings.ORCA_MODIFIER_MASK, inputEventHandlers[len(inputEventHandlers) - 1]))
    # orca + alt
    if not settings['shiftkey'] and not settings['ctrlkey'] and settings['altkey']:
        myKeyBindings.add(orca.keybindings.KeyBinding(settings['key'], orca.keybindings.defaultModifierMask, orca.keybindings.ORCA_ALT_MODIFIER_MASK, inputEventHandlers[len(inputEventHandlers) - 1]))
    # orca + CTRL
    if not settings['shiftkey'] and settings['ctrlkey'] and not settings['altkey']:
        myKeyBindings.add(orca.keybindings.KeyBinding(settings['key'], orca.keybindings.defaultModifierMask, orca.keybindings.ORCA_CTRL_MODIFIER_MASK, inputEventHandlers[len(inputEventHandlers) - 1]))
    # orca + alt + CTRL
    if not settings['shiftkey'] and settings['ctrlkey'] and settings['altkey']:
        myKeyBindings.add(orca.keybindings.KeyBinding(settings['key'], orca.keybindings.defaultModifierMask, orca.keybindings.ORCA_CTRL_ALT_MODIFIER_MASK, inputEventHandlers[len(inputEventHandlers) - 1]))
    # orca + shift
    if settings['shiftkey'] and not settings['ctrlkey'] and not settings['altkey']:
        myKeyBindings.add(orca.keybindings.KeyBinding(settings['key'], orca.keybindings.defaultModifierMask, orca.keybindings.ORCA_SHIFT_MODIFIER_MASK, inputEventHandlers[len(inputEventHandlers) - 1]))
    functions.append(fun)
    orca.settings.keyBindingsMap["default"] = myKeyBindings

def id_generator(size=7, chars=string.ascii_letters):
    return ''.join(random.choice(chars) for _ in range(size))

def initSettings():
    settings={
    'filepath':'',
    'scriptname':'',
    'functionname':'',
    'key':'',
    'shiftkey':False,
    'ctrlkey':False,
    'altkey':False,
    'startnotify':False,
    'stopnotify':False,
    'blockcall':False,
    'showstderr':False,
    }
    return settings

def parseFileName(filepath, settings):
    try:
        filename = os.path.basename(filepath) #filename
        filename = os.path.splitext(filename)[0].lower() #remove extension if we have one
        #remove scriptname seperated by -
        filenamehelper = filename.split('-')
        filename = filenamehelper[len(filenamehelper) - 1 ]
        settings['file'] = filepath
        settings['scriptname'] = 'NoNameAvailable'
        if len(filenamehelper) == 2:
            settings['scriptname'] = filenamehelper[0]
        #now get shortcuts seperated by +
        filenamehelper = filename.split('+')
        settings['key'] = filenamehelper[len(filenamehelper) - 1]
        settings['shiftkey'] = 'shift' in filenamehelper
        settings['ctrlkey'] = 'control' in filenamehelper
        settings['altkey'] = 'alt' in filenamehelper
        settings['startnotify'] = 'startnotify' in filenamehelper
        settings['stopnotify'] = 'stopnotify' in filenamehelper
        settings['blockcall'] = 'blockcall' in filenamehelper
        settings['showstderr'] = 'showstderr' in filenamehelper
        if len(settings['key']) != 1: #for now no special keys, but more valid data
        # for the return I realy should use a dict
            settings = initSettings()
            settings['key'] = 'ERROR'
            return settings
#            return '', 'ERROR', False, False, False, False, False, False, False 
        return settings
#        return scriptname, key, shiftkey, ctrlkey, altkey, startnotify, stopnotify, blockcall, showstderr
    except:
        settings = initSettings()
        settings['key'] = 'ERROR'
        return settings
        #return '', 'ERROR', False, False, False, False, False, False, False

def buildScriptFunctions(settings):
    currscript = "\'\"" + settings['file'] + "\"\'"
    fun_body = "def " + settings['functionname'] + "(script, inputEvent=None):\n"
    scriptname = settings['scriptname']
    if settings['blockcall']:
       scriptname = "blocking " + scriptname
    if settings['startnotify']:
        fun_body +="  outputMessage('start " + scriptname + "')\n"    
    fun_body +="  p = Popen(" + currscript + ", stdout=PIPE, stderr=PIPE, shell=True)\n"
    fun_body +="  stdout, stderr = p.communicate()\n"
    fun_body +="  message = ''\n"
    fun_body +="  if stdout:\n"
    fun_body +="    message += str(stdout, \"utf-8\")\n"
    fun_body +="  if " + str(settings['showstderr']) +" and stderr:\n"
    fun_body +="    message += ' error: ' + str(stderr, \"utf-8\")\n"
    fun_body +="  outputMessage( message)\n"
    if settings['stopnotify']:
        fun_body +="  outputMessage('finish " + scriptname + "')\n"
    fun_body +="  return True\n\n"
    fun_body +="def " + settings['functionname'] + "T(script, inputEvent=None):\n"
    fun_body +="  _thread.start_new_thread("+ settings['functionname'] + ",(script, inputEvent))\n\n"
    return fun_body

if not loaded:
    scriptlist = glob.glob(scriptrepo+'*')
    for currscript in scriptlist:
        settings = initSettings()
        settings = parseFileName(currscript, settings)
        if not settings['key'] in ['','ERROR']:
            settings['functionname'] = ''
            while settings['functionname'] == '' or settings['functionname'] + 'T' in globals() or settings['functionname'] in globals():
                settings['functionname'] = id_generator()
            exec(buildScriptFunctions(settings))
            if settings['blockcall']:
                fun = globals()[settings['functionname']]
            else:
                fun = globals()[settings['functionname']+"T"]
            SetupShortcutAndHandle(fun, settings)
    loaded = True

