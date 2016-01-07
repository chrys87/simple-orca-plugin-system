#!/bin/bash

# Plugin Manager for Orca
# By Storm Dragon: https://stormdragon.tk
# Released under the terms of the unlicense: http://unlicense.org

# Add sites to check to the pluginSites array.
pluginSites=(
    'https://stormdragon.tk/orca-plugins/index.php'
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
answer="$(zenity --list --title "Simple Orca Plugin Manager" --text "Select an action:" --radiolist --column "" --column "" TRUE "Configure Plugins" FALSE "Install New Plugins")"
if [[ $__actionVariable ]]; then
eval $__actionVariable="'${answer,,}'"
else
echo "${answer,,}"
fi
}

configure_plugins()
{
local ifs="$IFS"
IFS=$'\n'
local pluginList="$(ls -1 ${xdgPath}/plugins-available/*-*.*)"
if [ -n "$pluginList" ]; then
pluginList="${pluginList}"$'\n'
fi
pluginList="${pluginList}$(ls -1 /usr/share/SOPS/plugins/plugins-available/*-*.*)"
local pluginName=""
declare -A local pluginPath
local checkList=""
local i=""
for i in $pluginList ; do
pluginName="$((basename "$i") | cut -d '-' -f1 | sed 's/startnotify\|blockcall\|stopnotify//')"
pluginPath[$pluginName]="$i"
if ! ls -1 "${xdgPath}/plugins-enabled/${pluginPath[$pluginName]##*/}" &> /dev/null ; then
checkList="${checkList}FALSE"$'\n'"${pluginName}"$'\n'"Disabled"$'\n'
else
checkList="${checkList}FALSE"$'\n'"${pluginName}"$'\n'"Enabled"$'\n'
fi
done
items="$(zenity --list --title "Simple Orca Plugin Manager" --text "Configure plugins::" --checklist --column "" --column "" --column "" $checkList | tr '|' $'\n')"
for i in $items ; do
if ! ls -1 "${xdgPath}/plugins-enabled/${pluginPath[$i]##*/}" &> /dev/null ; then
ln -s "${pluginPath[$i]}" "${xdgPath}/plugins-enabled/"
else
unlink "${xdgPath}/plugins-enabled/${pluginPath[$i]##*/}"
fi
done
IFS="$ifs"
if [ -n "$items" ]; then
echo "Plugins updated! Restarting Orca..."
orca -r &
fi
}

install_new_plugins()
{
die "Not emplimented yet"
}

get_xdg_path
get_action action
if [ -n "$action" ]; then
${action// /_}
fi
exit 0
