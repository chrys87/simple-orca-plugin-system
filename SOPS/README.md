install manually
1. place the parent folder "SOPS" (Simple Orca Plugin System) in /usr/share/
sudo cp -r SOPS /usr/share/
2. run as user:
/usr/share/SOPS/install-for-current-user.sh # copy all the needed stuff to orca

install via packagemanager
1.1 Archlinux AUR - simpleorcapluginsystem-git
2. run as user:
/usr/share/SOPS/install-for-current-user.sh # copy all the needed stuff to orca

Wiki/ Documentation/ Usage/ Administration:
for full documentation look into the ./docu.txt file or at
https://wiki.archlinux.org/index.php/Simple_Orca_Plugin_System

remove
remove package or
sudo rm -r /usr/share/SOPS # remove the mainfolder
rm -r ~/.config/SOPS # remove the userplugins and the configuration
remove the following sectin from file ~/.local/share/orca/orca-customizations.py:
# Start SimpleOrcaPluginLoader DO NOT TOUCH!
import os
import importlib.util
spec = importlib.util.spec_from_file_location('SimplePluginLoader', os.path.expanduser('~')+'/.config/SOPS/SimplePluginLoader.py')
SimplePluginLoaderModule = importlib.util.module_from_spec(spec)
spec.loader.exec_module(SimplePluginLoaderModule)
# End SimpleOrcaPluginLoader DO NOT TOUCH!


