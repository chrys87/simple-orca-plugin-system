#!/bin/bash

# Plugin Manager for Orca
# By Storm Dragon: https://stormdragon.tk
# Released under the terms of the unlicense: http://unlicense.org

# Add sites to check to the pluginSites array.
pluginSites=(
    'https://stormdragon.tk/orca-plugins/'
    )
get_xdg_path()
{
xdgPath="${XDG_CONFIG_HOME:-$HOME/.config}"
xdgPath="${xdgPath}/SOPS"
if ! [ -d "$xdgPath" ]; then
mkdir -p "${xdgPath}/plugins-{available,enabled}"
fi
}

die()
{
    zenity --error --title "Simple Orca Plugin Manager" --text "$1" | fold -s
    if [[ "$2" =~ ^[0-9]+$ ]]; then
        if [ $2 -le 255 ]; then
            exit $2
        fi
    fi
        exit 1
}

get_action()
{
local __actionVariable="$1"
answer="$(zenity --list --title "Simple Orca Plugin Manager" --text "Select an action:" --radiolist --column "Select" --column "Action" TRUE "Enable/Disable Plugins" FALSE "Install New Plugins")"
if [[ $__actionVariable ]]; then
eval $__actionVariable="'$answer'"
else
echo "$answer"
fi
}

enable_disable_plugins()
{
local pluginList="$(ls ${xdgPath}/plugins-available/*-*.*)"
pluginList="${pluginList} $(ls /usr/share/SOPS/plugins/plugins-available/*-*.*)"
local pluginName=""
local checkList=""
local i=""
for i in $pluginList ; do
pluginName="$(echo "${i##*/}" | cut -d '-' -f1 | sed 's/startnotify\|blockcall\|stopnotify//')"
ls $xdgPath/plugins-enabled/*$pluginName* &> /dev/null
if [ $? -eq 2 ]; then
checkList="${checkList}FALSE ${pluginName} "
else
checkList="${checkList}TRUE ${pluginName} "
fi
done
answer="$(zenity --list --title "Simple Orca Plugin Manager" --text "Configure plugins::" --checklist --column "" --column "" $checkList | tr '|' $'\n')"
echo "$answer"
}

install_plugins()
{
die "Not emplimented yet"
}

get_xdg_path
get_action action
if [ "$action" = "Enable/Disable Plugins" ]; then
enable_disable_plugins
fi
if [ "$action" = "Install New Plugins" ]; then
install_plugins
fi
exit 0
