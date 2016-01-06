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

def SetupShortcutAndHandle(fun, scriptname, key, shiftkey, ctrlkey, altkey):
    if not fun:
        return
    if (key ==	 '') or (key ==	 'ERROR'):
        return
    inputEventHandlers.append(orca.input_event.InputEventHandler(fun, scriptname))   
    # just the orca modifier
    if not shiftkey and not ctrlkey and not altkey:
        myKeyBindings.add(orca.keybindings.KeyBinding(key, orca.keybindings.defaultModifierMask, orca.keybindings.ORCA_MODIFIER_MASK, inputEventHandlers[len(inputEventHandlers) - 1]))
    # orca + alt
    if not shiftkey and not ctrlkey and altkey:
        myKeyBindings.add(orca.keybindings.KeyBinding(key, orca.keybindings.defaultModifierMask, orca.keybindings.ORCA_ALT_MODIFIER_MASK, inputEventHandlers[len(inputEventHandlers) - 1]))
    # orca + CTRL
    if not shiftkey and ctrlkey and not altkey:
        myKeyBindings.add(orca.keybindings.KeyBinding(key, orca.keybindings.defaultModifierMask, orca.keybindings.ORCA_CTRL_MODIFIER_MASK, inputEventHandlers[len(inputEventHandlers) - 1]))
    # orca + alt + CTRL
    if not shiftkey and ctrlkey and altkey:
        myKeyBindings.add(orca.keybindings.KeyBinding(key, orca.keybindings.defaultModifierMask, orca.keybindings.ORCA_CTRL_ALT_MODIFIER_MASK, inputEventHandlers[len(inputEventHandlers) - 1]))
    # orca + shift
    if shiftkey and not ctrlkey and not altkey:
        myKeyBindings.add(orca.keybindings.KeyBinding(key, orca.keybindings.defaultModifierMask, orca.keybindings.ORCA_SHIFT_MODIFIER_MASK, inputEventHandlers[len(inputEventHandlers) - 1]))
    functions.append(fun)
    orca.settings.keyBindingsMap["default"] = myKeyBindings

def id_generator(size=7, chars=string.ascii_letters):
    return ''.join(random.choice(chars) for _ in range(size))

def parseFileName(filepath):
    try:
        filename = os.path.basename(filepath) #filename
        filename = os.path.splitext(filename)[0] #remove extension if we have one
        #remove scriptname seperated by -
        filenamehelper = filename.split('-')
        filename = filenamehelper[len(filenamehelper) - 1 ]
        scriptname = 'NoNameAvailable'
        if len(filenamehelper) == 2:
            scriptname = filenamehelper[0]
        #now get shortcuts seperated by +
        filenamehelper = filename.split('+')
        key = filenamehelper[len(filenamehelper) - 1]
        shiftkey = 'shift' in filenamehelper
        ctrlkey = 'control' in filenamehelper
        altkey = 'alt' in filenamehelper
        startnotify = 'startnotify' in filenamehelper
        stopnotify = 'stopnotify' in filenamehelper
        blockcall = 'blockcall' in filenamehelper
        showstderr = 'showstderr' in filenamehelper
        if len(key) != 1: #for now no special keys, but more valid data
        # for the return I realy should use a dict
            return '', 'ERROR', False, False, False, False, False, False, False 
        return scriptname, key, shiftkey, ctrlkey, altkey, startnotify, stopnotify, blockcall, showstderr
    except:
        return '', 'ERROR', False, False, False, False, False, False, False

def buildScriptFunctions(fun_name, currscript, scriptname, startnotify, stopnotify, blockcall, showstderr):
    currscript = "\'\"" + currscript + "\"\'"
    fun_body = "def " + fun_name + "(script, inputEvent=None):\n"
    if blockcall:
       scriptname = "blocking " + scriptname 
    if startnotify:
        fun_body +="  outputMessage('start " + scriptname + "')\n"    
    fun_body +="  p = Popen(" + currscript + ", stdout=PIPE, stderr=PIPE, shell=True)\n"
    fun_body +="  stdout, stderr = p.communicate()\n"
    fun_body +="  message = ''\n"
    fun_body +="  if stdout:\n"
    fun_body +="    message += str(stdout, \"utf-8\")\n"
    fun_body +="  if showstderr and stderr:\n"
    fun_body +="    message += ' error: ' + str(stderr, \"utf-8\")\n"
    fun_body +="  outputMessage( message)\n"
    if stopnotify:
        fun_body +="  outputMessage('finish " + scriptname + "')\n"
    fun_body +="  return True\n\n"
    fun_body +="def " + fun_name + "T(script, inputEvent=None):\n"
    fun_body +="  _thread.start_new_thread("+fun_name + ",(script, inputEvent,))\n\n"
    return fun_body

if not loaded:
    scriptlist = glob.glob(scriptrepo+'*')
    for currscript in scriptlist:
        scriptname, key, shiftkey, ctrlkey, altkey, startnotify, stopnotify, blockcall, showstderr = \
          parseFileName	(currscript)
        if key != 'ERROR':
            fun_name = ''
            while fun_name == '' or fun_name + 'T' in globals() or fun_name in globals():
                fun_name = id_generator()
            exec(buildScriptFunctions(fun_name, currscript, scriptname, startnotify, stopnotify, blockcall, showstderr))
            if blockcall:
                fun = globals()[fun_name]
            else:
                fun = globals()[fun_name+"T"]
            SetupShortcutAndHandle(fun, scriptname, key, shiftkey, ctrlkey, altkey)
    loaded = True

