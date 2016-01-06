install manually
1. place the parent folder "SOPS" (Simple Orca Plugin System) in /usr/share/
sudo cp -r SOPS /usr/share/
2. run as user:
cd /usr/share/SOPS
./install-for-current-user.sh # copy all the needed stuff to orca

install via packagemanager
1.1 Archlinux AUR - simpleorcapluginsystem-git
2. run as user:
cd /usr/share/SOPS
./install-for-current-user.sh # copy all the needed stuff to orca

administration
use ensop and dissop to enable and disable plugins, see docu.txt section 2.
by default not all plugins are activated

remove
remove package or
sudo rm -r /usr/share/SOPS # remove the mainfolder
rm -r ~/.local/share/orca/plugins # remove the enabled plugins in orca config
rm ~/.local/share/orca/SimplePluginLoader.py # remove loader from orca config
remove the following sectin from file ~/.local/share/orca/orca-customizations.py:
# Start SimpleOrcaPluginLoader DO NOT TOUCH!
import os
import importlib.util
spec = importlib.util.spec_from_file_location('SimplePluginLoader', os.path.expanduser('~')+'/.local/share/orca/SimplePluginLoader.py')
SimplePluginLoaderModule = importlib.util.module_from_spec(spec)
spec.loader.exec_module(SimplePluginLoaderModule)
# End SimpleOrcaPluginLoader DO NOT TOUCH!

