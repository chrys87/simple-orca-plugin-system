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
mkdir -p "${xdgPath}/plugins-available"
mkdir -p "${xdgPath}/plugins-enabled"
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
answer="$(zenity --list --title "Simple Orca Plugin Manager" --text "Select an action:" --column "Select an Action" "Configure Plugins" "Install New Plugins" "Close Simple Orca Plugin Manager")"
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
pluginName="$((basename "${i%__-__*}") | sed 's/startnotify\|blockcall\|stopnotify//')"
pluginPath[$pluginName]="$i"
if ! ls -1 "${xdgPath}/plugins-enabled/${pluginPath[$pluginName]##*/}" &> /dev/null ; then
checkList="${checkList}FALSE"$'\n'"${pluginName}"$'\n'"Disabled"$'\n'
else
checkList="${checkList}FALSE"$'\n'"${pluginName}"$'\n'"Enabled"$'\n'
fi
done
local items="$(zenity --list --title "Simple Orca Plugin Manager" --text "Configure plugins:" --checklist --ok-label "Toggle Selected Plugins" --separator $'\n' --column "" --column "Plugin" --column "Status" $checkList)"
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
echo "Checking for plugins, please wait..."
local i=""
local checkList
declare -A local pluginList=""
local plugins
for i in ${pluginSites[@]} ; do
plugins=($(curl -s "$i" | grep -A 10000 '<!-- begin plugin list -->' | grep -B 10000 '<!-- end plugin list -->' | grep -v '<!--'))
for l in ${plugins[@]} ; do
checkList="${checkList}FALSE ${l##*/} "
pluginList[$l]="${i%/*}/$l"
done
done
local items="$(zenity --list --title "Simple Orca Plugin Manager" --text "Install plugins:" --checklist --ok-label "Install" --column "" --column "Plugin" $checkList | tr '|' $'\n')"
if [ -z "$items" ]; then
exit 0
fi
local keyList=""
checkList="$(echo {a..z} {0..9} | sed 's/\([a-z]\)/FALSE \1/g')" #Keys
checkList="FALSE alt FALSE control FALSE shift $checkList" #Modifier
checkList="FALSE startnotify FALSE stopnotify FALSE showstderr FALSE parameters FALSE blockcall $checkList" #commands

for i in $items ; do
fileName="$(zenity --list --title "Simple Orca Plugin Manager" --text "Select keyboard shortcut for $i:" --checklist --separator __+__ --column "" --column "Keys" $checkList)"
if [ -z "$fileName" ]; then
exit 0
fi
fileName="${i%.*}__-__${fileName}.${i##*.}"
echo "Installing ${i##*/}"
wget -O "${xdgPath}/plugins-available/$fileName" "${pluginList[$i]}" || die "Could not download plugin $i from ${pluginList[$i]}"
chmod +x "${xdgPath}/plugins-available/$fileName" || die "Could not set execute permissions for plugin $i"
ln -s "${xdgPath}/plugins-available/$fileName" "${xdgPath}/plugins-enabled/$fileName" || die "Could not link plugin $i"
echo "Plugin $i installed successfully."
done
if [ -n "$i" ]; then
echo "Restarting orca"
orca -r &
fi
}

close_simple_orca_plugin_manager()
{
exit 0
}

get_xdg_path
while : ; do
get_action action
if [ -n "$action" ]; then
${action// /_}
fi
done
exit 0
