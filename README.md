SOPS — Simple Orca Plugin System
===================================

SOPS provides a simple way to write custom plugins for screen  reader Orca. It
requires Orca to be installed.

Manual Installation
-------------------

-   If you want to install this software system-wide, copy this directory to
    /usr/share/SOPS:

        sudo cp -dpr . /usr/share/SOPS

    You are free to choose a different location, as soon as the directory is not
    moved after installation.

-   As user, run:

        sh /usr/share/SOPS/install-for-current-user.sh

    This installs the plugin locally and registers a few default plugins with
    Orca.

    Note: replace `/usr/share/SOPS` through the path you chose during the
    previous step.

install via package manager
---------------------------

-   On Debian and derivatives, it is enough to issue
    `sudo apt install orca-sops`.
-   For Arch Linux, the package simpleorcapluginsystem-git from the AUR can be
    installed.

After the installation, run:

    sh /usr/share/SOPS/install-for-current-user.sh # copy all the needed stuff to orca

Documentation And Usage
-----------------------

The documentation can be found in the doc folder or in the Arch wiki at
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


