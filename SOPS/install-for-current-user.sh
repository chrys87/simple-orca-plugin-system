#!/bin/sh

# is it already installed? so break
if [ -e "$HOME/.local/share/orca/orca-customizations.py" ]; then
    if grep -q "spec.loader.exec_module(SimplePluginLoaderModule)" "$HOME/.local/share/orca/orca-customizations.py"; then
        echo "Simple Orca Plugin System is already installed for this user"
        exit 1
    fi
fi

#user plugins
mkdir -p "$HOME/.config/SOPS/plugins-available"

# include it in orca
mkdir -p "$HOME/.config/SOPS/plugins-enabled"
ln -s "/usr/share/SOPS/SimplePluginLoader.py" $HOME/.config/SOPS/
echo "" >> "$HOME/.local/share/orca/orca-customizations.py"
echo "# Start SimpleOrcaPluginLoader DO NOT TOUCH!" >> "$HOME/.local/share/orca/orca-customizations.py"
echo "import os" >> "$HOME/.local/share/orca/orca-customizations.py"
echo "import importlib.util" >> "$HOME/.local/share/orca/orca-customizations.py"
echo "spec = importlib.util.spec_from_file_location('SimplePluginLoader', os.path.expanduser('~')+'/.config/SOPS/SimplePluginLoader.py')" >> "$HOME/.local/share/orca/orca-customizations.py"
echo "SimplePluginLoaderModule = importlib.util.module_from_spec(spec)" >> "$HOME/.local/share/orca/orca-customizations.py"
echo "spec.loader.exec_module(SimplePluginLoaderModule)" >> "$HOME/.local/share/orca/orca-customizations.py"
echo "# End SimpleOrcaPluginLoader DO NOT TOUCH!" >> "$HOME/.local/share/orca/orca-customizations.py"

#enable some scripts by default
cd "./plugins/plugins-available/"
./ensop "workspacenumber-x.sh"
./ensop "clipboard-c.py"
./ensop "battery-alt+r.py"
./ensop "weather-startnotify+control+alt+w.sh"
exit 0
