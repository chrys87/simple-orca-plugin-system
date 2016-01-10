#!/bin/python
# -*- coding: utf-8 -*-
# translate the current clipboard with translate-shell
# parameters: <language> <Replace Clipboard [True,False]>
# needs GTK3 GDK and translate-shell http://tuxdiary.com/2015/01/21/translate-shell/

import gi, os, sys
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk

escape_dict={'\a':r'\a',
        '\b':r'\b',
        '\c':r'\c',
        '\f':r'\f',
        '\n':r' ',
        '\r':r'\r',
        '\t':r'\t',
        '\v':r'\v',
        '\'':r'\'',
        '\"':r'\"',
        '\0':r'\0',
        '\1':r'\1',
        '\2':r'\2',
        '\3':r'\3',
        '\4':r'\4',
        '\5':r'\5',
        '\6':r'\6',
        '\7':r'\7',
        '\8':r'\8',
        '\9':r'\9',
        "'" : r" ",
        '"' : r' '}

def raw_string(text):
    """Returns a raw string representation of text"""
    new_string=''
    for char in text:
        try: new_string+=escape_dict[char]
        except KeyError: new_string+=char
    return new_string

def setTextToClipboard(text):
    ClipboardObj = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
    ClipboardObj.set_text(text, -1)

def displayClipboardTranslation(language, toClipboard):
    Message = ""
    # Get Selection
    ClipboardObj = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)

    ClipboardText = ClipboardObj.wait_for_text()  

    if (ClipboardText != None):
        ClipboardText = raw_string(ClipboardText)		
        TranslationText = os.popen('translate-shell -b :'+ language +' "'+ ClipboardText +'"').read()
        TranslationText = TranslationText[:-1]
        if TranslationText in '/bin/sh: translate-shell: ':
            Message = "Please install translate-shell translate-shell" # install translate-shell
        else:
            TranslationText = ClipboardText = raw_string(TranslationText)		
            if toClipboard:
        	    setTextToClipboard(TranslationText)
        	    Message = "New clipboard " + TranslationText # Neue Zwischenabglage
            else:
                Message = "Übersetzt " + TranslationText # Übersetzt
    else:
        Message = "Clipboard is empty" #Zwischenablage ist leer

    # Say/braille something.
    print(Message)
	
displayClipboardTranslation(sys.argv[1],sys.argv[2] == 'True')
