SOPS — Simple Orca Plugin System
===================================

SOPS provides a simple way to write custom plugins for screen  reader Orca. It
requires Orca to be installed.

Manual Installation
-------------------


0.  If you want to install this software system-wide, copy this directory to
    /usr/share/SOPS:

        sudo cp -dpr . /usr/share/SOPS
2.  As user, run:

        sh /usr/share/install-for-current-user.sh

    This installs the plugin locally and registers a few default plugins with
    Orca.

install via package manager
---------------------------


*Archlinux AUR - simpleorcapluginsystem-git, run as user:*

sh /usr/share/SOPS/install-for-current-user.sh # copy all the needed stuff to orca

Wiki/ Documentation/ Usage/ Administration:
-------------------------------------------

For full documentation look into the ./docu.txt file or at
https://wiki.archlinux.org/index.php/Simple_Orca_Plugin_System

Uninstallation
--------------

-   if installed by your package manager, use this one
-   otherwise remove /usr/share/SOPS

        sudo rm -r /usr/share/SOPS # remove the mainfolder
-   remove user-local installation:

        rm -r ~/.config/SOPS # remove the userplugins and the configuration

    -   remove the following section from file `~/.local/share/orca/orca-customizations.py` :

    ```python
    # Start SimpleOrcaPluginLoader DO NOT TOUCH!
    import os
    import importlib.util
    spec = importlib.util.spec_from_file_location('SimplePluginLoader', os.path.expanduser('~')+'/.config/SOPS/SimplePluginLoader.py')
    SimplePluginLoaderModule = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(SimplePluginLoaderModule)
    # End SimpleOrcaPluginLoader DO NOT TOUCH!
    ```


