#!/bin/sh

# Make sure this isn't ran as root:
if [ "$(whoami)" = "root" ]; then
echo "This script does not need root privileges."
exit 1
fi

# is it already installed? so break
if [ -e "$HOME/.local/share/orca/orca-customizations.py" ]; then
    if grep -q "spec.loader.exec_module(SimplePluginLoaderModule)" "$HOME/.local/share/orca/orca-customizations.py"; then
        echo "Simple Orca Plugin System is already installed for this user"
        exit 1
    fi
fi

#create structure in home
xdgPath="${XDG_CONFIG_HOME:-$HOME/.config}"
mkdir -p "$xdgPath/SOPS/plugins-available"
mkdir -p "$xdgPath/SOPS/plugins-enabled"
ln -s "/usr/share/SOPS/SimplePluginLoader.py" $xdgPath/SOPS/

# include it in orca
echo "" >> "$HOME/.local/share/orca/orca-customizations.py"
echo "# Start SimpleOrcaPluginLoader DO NOT TOUCH!" >> "$HOME/.local/share/orca/orca-customizations.py"
echo "import importlib.util, os" >> "$HOME/.local/share/orca/orca-customizations.py"
echo "spec = importlib.util.spec_from_file_location('SimplePluginLoader', os.path.expanduser('~')+'/.config/SOPS/SimplePluginLoader.py')" >> "$HOME/.local/share/orca/orca-customizations.py"
echo "SimplePluginLoaderModule = importlib.util.module_from_spec(spec)" >> "$HOME/.local/share/orca/orca-customizations.py"
echo "spec.loader.exec_module(SimplePluginLoaderModule)" >> "$HOME/.local/share/orca/orca-customizations.py"
echo "# End SimpleOrcaPluginLoader DO NOT TOUCH!" >> "$HOME/.local/share/orca/orca-customizations.py"
echo "" >> "$HOME/.local/share/orca/orca-customizations.py"

#enable some scripts by default
cd "/usr/share/SOPS/plugins/plugins-available/"
../../tools/ensop workspacenumber.sh
../../tools/ensop clipboard.py
../../tools/ensop plugin_manager.sh

cd "$HOME/.config/SOPS/plugins-enabled"
mv workspacenumber.sh workspacenumber__-__key_x.sh
mv clipboard.py clipboard__-__key_c.py
mv plugin_manager.sh plugin_manager__-__supressoutput__+__control__+__key_p.sh
exit 0
