#!/bin/python
# -*- coding: utf-8 -*-
# just print the clipboard content. youst GTK3 GDK needed

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk
import os

def printClipboard():
    Message = ""
    FoundClipboardContent = False
    # Get Clipboard
    ClipboardObj = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)

    ClipboardText = ClipboardObj.wait_for_text()  
    ClipboardImage = ClipboardObj.wait_for_image()   

    if (ClipboardText != None):
        FoundClipboardContent = True
        if (ClipboardObj.wait_is_uris_available()):
            UriList = ClipboardText.split('\n')
            ObjectNo = 0			
            for Uri in UriList:
                ObjectNo += 1
                if (os.path.isdir(Uri)):
                    Message = Message + "Folder" #Folder
                if (os.path.isfile(Uri)):
                    Message = Message + "File" #File
                if (os.path.ismount(Uri)):
                    Message = Message + "Disk" #Mountpoint	 
                if (os.path.islink(Uri)):
                    Message = Message + "Link" #Link
                Message += " " + Uri[Uri.rfind('/') + 1:] + " "
            if (ObjectNo > 1):			
                Message = str(ObjectNo) + " Objects in clipboard " + Message # X Objects in Clipboard Object Object		
            else:
                Message = str(ObjectNo) + " Object in clipboard " + Message # 1 Object in Clipboard Object	
        else:		
            Message = "Text in clipboard " + ClipboardText # Text in Clipboard

    if (ClipboardImage != None):
        FoundClipboardContent = True
        Message = "The clipboard contains a image" # Image is in Clipboard

    if (not FoundClipboardContent):
        Message = "The clipboard is empty"
    print(Message)

printClipboard()
