# -*- coding: utf-8 -*-
# chrys
# version 0.5

import glob
import os
import importlib.util
import random
import string
import _thread
from subprocess import Popen, PIPE

import orca.orca

#settings
pluginrepo = os.path.expanduser('~')+"/.config/SOPS/plugins-enabled/"

#globals
pluginList = []
loaded = False
myKeyBindings = orca.keybindings.KeyBindings()

def outputMessage(Message):
    if (orca.settings.enableSpeech):
        orca.speech.speak(Message)
    if (orca.settings.enableBraille):
        orca.braille.displayMessage(Message)

def SetupShortcutAndHandle( settings):
    settings['inputeventhandler'] = orca.input_event.InputEventHandler(settings['function'], settings['pluginname'])
    # just the orca modifier
    if not settings['shiftkey'] and not settings['ctrlkey'] and not settings['altkey']:
        myKeyBindings.add(orca.keybindings.KeyBinding(settings['key'], orca.keybindings.defaultModifierMask, orca.keybindings.ORCA_MODIFIER_MASK, settings['inputeventhandler']))
    # orca + alt
    if not settings['shiftkey'] and not settings['ctrlkey'] and settings['altkey']:
        myKeyBindings.add(orca.keybindings.KeyBinding(settings['key'], orca.keybindings.defaultModifierMask, orca.keybindings.ORCA_ALT_MODIFIER_MASK, settings['inputeventhandler']))
    # orca + CTRL
    if not settings['shiftkey'] and settings['ctrlkey'] and not settings['altkey']:
        myKeyBindings.add(orca.keybindings.KeyBinding(settings['key'], orca.keybindings.defaultModifierMask, orca.keybindings.ORCA_CTRL_MODIFIER_MASK, settings['inputeventhandler']))
    # orca + alt + CTRL
    if not settings['shiftkey'] and settings['ctrlkey'] and settings['altkey']:
        myKeyBindings.add(orca.keybindings.KeyBinding(settings['key'], orca.keybindings.defaultModifierMask, orca.keybindings.ORCA_CTRL_ALT_MODIFIER_MASK, settings['inputeventhandler']))
    # orca + shift
    if settings['shiftkey'] and not settings['ctrlkey'] and not settings['altkey']:
        myKeyBindings.add(orca.keybindings.KeyBinding(settings['key'], orca.keybindings.defaultModifierMask, orca.keybindings.ORCA_SHIFT_MODIFIER_MASK, settings['inputeventhandler']))
    # alt + shift
    if settings['shiftkey'] and not settings['ctrlkey'] and settings['altkey']:
        myKeyBindings.add(orca.keybindings.KeyBinding(settings['key'], orca.keybindings.defaultModifierMask, orca.keybindings.SHIFT_ALT_MODIFIER_MASK, settings['inputeventhandler']))

    orca.settings.keyBindingsMap["default"] = myKeyBindings

def id_generator(size=7, chars=string.ascii_letters):
    return ''.join(random.choice(chars) for _ in range(size))

def initSettings():
    settings={
    'filepath':'',
    'pluginname':'',
    'functionname':'',
    'key':'',
    'shiftkey':False,
    'ctrlkey':False,
    'altkey':False,
    'startnotify':False,
    'stopnotify':False,
    'blockcall':False,
    'error':False,
    'exec': False,
    'executeable':False,
    'parameters':'',
    'function':None,
    'inputeventhandler':None,
    'valid':False,
    'supressoutput':False
    }
    return settings

def getPluginSettings(filepath, settings):
    try:
        settings['file'] = filepath
        fileName, fileExtension = os.path.splitext(filepath)
        if (fileExtension and (fileExtension != '')): #if there is an extension
            settings['loadable'] = (fileExtension.lower() == '.py') # only python is loadable
        filename = os.path.basename(filepath) #filename
        filename = os.path.splitext(filename)[0] #remove extension if we have one
        #remove pluginname seperated by __-__
        filenamehelper = filename.split('__-__')
        filename = filenamehelper[len(filenamehelper) - 1 ]
        settings['permission'] = os.access(filepath, os.X_OK )
        settings['pluginname'] = 'NoNameAvailable'
        if len(filenamehelper) == 2:
            settings['pluginname'] = filenamehelper[0]
        #now get shortcuts seperated by __+__
        filenamehelper = filename.split('__+__')
        if len([y for y in filenamehelper if 'parameters_' in y.lower()]) == 1 and\
          len([y for y in filenamehelper if 'parameters_' in y.lower()][0]) > 11:
            settings['parameters'] = [y for y in filenamehelper if 'parameters_' in y.lower()][0][11:]
        if len([y for y in filenamehelper if 'key_' in y.lower()]) == 1 and\
          len([y for y in filenamehelper if 'key_' in y.lower()][0]) > 4 :
            settings['key'] = [y for y in filenamehelper if 'key_' in y.lower()][0][4:]
        if settings['key'] == '':
            settings['key'] = filenamehelper[len(filenamehelper) - 1].lower()
        settings['shiftkey'] = 'shift' in map(str.lower, filenamehelper)
        settings['ctrlkey'] = 'control' in map(str.lower, filenamehelper)
        settings['altkey'] = 'alt' in map(str.lower, filenamehelper)
        settings['startnotify'] = 'startnotify' in map(str.lower, filenamehelper)
        settings['stopnotify'] = 'stopnotify' in map(str.lower, filenamehelper)
        settings['blockcall'] = 'blockcall' in map(str.lower, filenamehelper)
        settings['error'] = 'error' in map(str.lower, filenamehelper)
        settings['supressoutput'] = 'supressoutput' in map(str.lower, filenamehelper)
        settings['exec'] = 'exec' in map(str.lower, filenamehelper)    
        settings['loadmodule'] = 'loadmodule' in map(str.lower, filenamehelper) 
        settings = readSettingsFromPlugin(settings)
        if not settings['loadmodule']:
            if not settings['permission']: #subprocessing only works with exec permission
                return initSettings()
        if settings['loadmodule'] and not settings['loadable']: #sorry.. its not loadable only .py is loadable
            return initSettings()
        if (len(settings['key']) < 1): #no shortcut
            if not settings['exec']: # and no exec -> the plugin make no sense because it isnt hooked anywhere
                return initSettings() #so not load it (sets valid = False)
            else:
                settings['key'] = '' #there is a strange key, but exec? ignore the key..
        settings['valid'] = True # we could load everything
        return settings
    except:
        return initSettings()

def readSettingsFromPlugin(settings):
    if not os.access(settings['file'], os.R_OK ):
        return settings
    fileName, fileExtension = os.path.splitext(settings['file'])
    if (fileExtension and (fileExtension != '')): #if there is an extension
        if (fileExtension.lower() != '.py') and \
          (fileExtension.lower() != '.sh'):
            return settings
    else:
        return settings

    with open(settings['file'], "r") as pluginFile:
        for line in pluginFile:
            settings['shiftkey'] = ('sopsproperty:shift' in line.lower().replace(" ", "")) or settings['shiftkey']
            settings['ctrlkey'] = ('sopsproperty:control' in line.lower().replace(" ", "")) or settings['ctrlkey']
            settings['altkey'] = ('sopsproperty:alt' in line.lower().replace(" ", "")) or settings['altkey']
            settings['startnotify'] = ('sopsproperty:startnotify' in line.lower().replace(" ", "")) or settings['startnotify']
            settings['stopnotify'] = ('sopsproperty:stopnotify' in line.lower().replace(" ", "")) or settings['stopnotify']
            settings['blockcall'] = ('sopsproperty:blockcall' in line.lower().replace(" ", "")) or settings['blockcall']
            settings['error'] = ('sopsproperty:error' in line.lower().replace(" ", "")) or settings['error']
            settings['supressoutput'] = ('sopsproperty:supressoutput' in line.lower().replace(" ", "")) or settings['supressoutput']
            settings['exec'] = ('sopsproperty:exec' in line.lower().replace(" ", "")) or settings['exec']
            settings['loadmodule'] = ('sopsproperty:loadmodule' in line.lower().replace(" ", "")) or settings['loadmodule']
    return settings

def buildPluginSubprocess(settings):
    currplugin = "\'\"" + settings['file'] + "\" " + settings['parameters'] + "\'"
    pluginname = settings['pluginname']
    if settings['blockcall']:
       pluginname = "blocking " + pluginname
    fun_body = "def " + settings['functionname'] + "(script=None, inputEvent=None):\n"
    if settings['startnotify']:
        fun_body +="  outputMessage('start " + pluginname + "')\n"    
    fun_body +="  p = Popen(" + currplugin + ", stdout=PIPE, stderr=PIPE, shell=True)\n"
    fun_body +="  stdout, stderr = p.communicate()\n"
    fun_body +="  message = ''\n"
    fun_body +="  if not " + str(settings['supressoutput']) + " and stdout:\n"
    fun_body +="    message += str(stdout, \"utf-8\")\n"
    fun_body +="  if " + str(settings['error']) + " and stderr:\n"
    fun_body +="    message += ' error: ' + str(stderr, \"utf-8\")\n"
    fun_body +="  outputMessage( message)\n"
    if settings['stopnotify']:
        fun_body +="  outputMessage('finish " + pluginname + "')\n"
    fun_body +="  return True\n\n"
    fun_body +="def " + settings['functionname'] + "T(script=None, inputEvent=None):\n"
    fun_body +="  _thread.start_new_thread("+ settings['functionname'] + ",(script, inputEvent))\n\n"
    return fun_body

def buildPluginExec(settings):
    pluginname = settings['pluginname']
    if settings['blockcall']:
       pluginname = "blocking " + pluginname
    fun_body = "def " + settings['functionname'] + "(script=None, inputEvent=None):\n"
    if settings['startnotify']:
        fun_body +="  outputMessage('start " + pluginname + "')\n"
    fun_body += "  try:\n"  
    fun_body += "    spec = importlib.util.spec_from_file_location(\"" + settings['functionname'] + "\",\""+ settings['file']+"\")\n"
    fun_body += "    "+settings['functionname'] + "Module = importlib.util.module_from_spec(spec)\n"
    fun_body += "    spec.loader.exec_module(" + settings['functionname'] + "Module)\n"
    fun_body += "  except:\n"
    fun_body += "    pass\n"
    if settings['error']:
        fun_body += "    outputMessage(\"Error while executing " + pluginname + "\")\n"
    if settings['stopnotify']:
        fun_body +="  outputMessage('finish " + pluginname + "')\n"
    fun_body += "  return True\n\n"
    fun_body +="def " + settings['functionname'] + "T(script=None, inputEvent=None):\n"
    fun_body +="  _thread.start_new_thread("+ settings['functionname'] + ",(script, inputEvent))\n\n"
    return fun_body

def getFunctionName(settings):
    settings['functionname'] = ''
    while settings['functionname'] == '' or settings['functionname'] + 'T' in globals() or settings['functionname'] in globals():
        settings['functionname'] = id_generator()
    return settings

if not loaded:
    pluginlist = glob.glob(pluginrepo+'*')
    for currplugin in pluginlist:
        settings = initSettings()
        settings = getPluginSettings(currplugin, settings)
        if not settings['valid']:
            continue
            
        settings = getFunctionName(settings)
        
        if settings['loadmodule']:
            exec(buildPluginExec(settings)) # load as python module
        else:
            exec(buildPluginSubprocess(settings)) # run as subprocess
            
        if settings['blockcall']:
            settings['function'] = globals()[settings['functionname']] # non threaded
        else:
            settings['function'] = globals()[settings['functionname']+"T"] # T = Threaded
 
          
        if settings['exec']: # exec on load if we want
            settings['function']()

        if not settings['key'] == '':
            SetupShortcutAndHandle(settings)
        pluginList.append(settings) # store in a list
    loaded = True

