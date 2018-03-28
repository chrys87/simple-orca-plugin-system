#!/bin/sh
set -e

SCRIPT_SRC=$(dirname $0)

# Make sure this isn't ran as root:
if [ "$(whoami)" = "root" ]; then
echo "This script does not need root privileges."
exit 1
fi

# is it already installed? so break
if [ -e "$CUSTOMIZATIONS" ]; then
    if grep -q "spec.loader.exec_module(SimplePluginLoaderModule)" "$CUSTOMIZATIONS"; then
        echo "Simple Orca Plugin System is already installed for this user"
        exit 1
    fi
fi

#create structure in home
xdgPath="${XDG_CONFIG_HOME:-$HOME/.config}"
mkdir -p "$xdgPath/SOPS/plugins-available"
mkdir -p "$xdgPath/SOPS/plugins-enabled"
cp "$SCRIPT_SRC/SimplePluginLoader.py" $xdgPath/SOPS/

# include it in orca
CUSTOMIZATIONS="$HOME/.local/share/orca/orca-customizations.py"
if ! [ -f `dirname "$CUSTOMIZATIONS"` ]; then
	mkdir -p `dirname "$CUSTOMIZATIONS"`
fi
echo >> "$CUSTOMIZATIONS"
echo "# Start SimpleOrcaPluginLoader DO NOT TOUCH!" >> "$CUSTOMIZATIONS"
echo "try:" >> "$CUSTOMIZATIONS"
echo "  import importlib.util, os" >> "$CUSTOMIZATIONS"
echo "  spec = importlib.util.spec_from_file_location('SimplePluginLoader', os.path.expanduser('~')+'/.config/SOPS/SimplePluginLoader.py')" >> "$CUSTOMIZATIONS"
echo "  SimplePluginLoaderModule = importlib.util.module_from_spec(spec)" >> "$CUSTOMIZATIONS"
echo "  spec.loader.exec_module(SimplePluginLoaderModule)" >> "$CUSTOMIZATIONS"
echo "except Exception as e:" >> "$CUSTOMIZATIONS"
echo "  print('Problem while loading SOPS:' + str(e))" >> "$CUSTOMIZATIONS"
echo "# End SimpleOrcaPluginLoader DO NOT TOUCH!" >> "$CUSTOMIZATIONS"
echo "" >> "$CUSTOMIZATIONS"

#enable some scripts by default
cd "$SCRIPT_SRC/plugins/plugins-available/"
../../tools/ensop workspacenumber.sh
../../tools/ensop clipboard.py
../../tools/ensop plugin_manager.sh

cd "$HOME/.config/SOPS/plugins-enabled"
mv workspacenumber.sh workspacenumber__-__key_x.sh
mv clipboard.py clipboard__-__key_c.py
mv plugin_manager.sh plugin_manager__-__supressoutput__+__control__+__key_p.sh
exit 0
