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
pluginName="$((basename "${i%__-__*}") | sed 's/startnotify\|blockcall\|stopnotify//')"
pluginPath[$pluginName]="$i"
if ! ls -1 "${xdgPath}/plugins-enabled/${pluginPath[$pluginName]##*/}" &> /dev/null ; then
checkList="${checkList}FALSE"$'\n'"${pluginName}"$'\n'"Disabled"$'\n'
else
checkList="${checkList}FALSE"$'\n'"${pluginName}"$'\n'"Enabled"$'\n'
fi
done
local items="$(zenity --list --title "Simple Orca Plugin Manager" --text "Configure plugins:" --checklist --ok-label "Configure" --separator $'\n' --column "" --column "" --column "" $checkList)"
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
for i in $pluginSites ; do
plugins=($(echo -n "${i%/*}/";curl -s "$i" | grep -A 10000 '<!-- begin plugin list -->' | grep -B 10000 '<!-- end plugin list -->' | grep -v '<!--'))
done
for i in ${plugins[@]} ; do
checkList="${checkList}FALSE ${i##*/} "
pluginList[${i##*/}]="$i"
done
local items="$(zenity --list --title "Simple Orca Plugin Manager" --text "Install plugins:" --checklist --ok-label "Install" --column "" --column "" $checkList | tr '|' $'\n')"
if [ -z "$items" ]; then
exit 0
fi
local keyList=""
checkList="$(echo {a..z} {0..9} | sed 's/\([a-z]\)/FALSE \1/g')" #Keys
checkList="FALSE alt FALSE control FALSE shift $checkList" #Modifier
checkList="FALSE startnotify FALSE stopnotify FALSE showstderr FALSE parameters FALSE blockcall $checkList" #commands

for i in $items ; do
fileName="$(zenity --list --title "Simple Orca Plugin Manager" --text "Select keyboard shortcut for $i:" --checklist --separator __+__ --column "" --column "" $checkList)"
if [ -z "$fileName" ]; then
exit 0
fi
fileName="${i%.*}__-__${fileName}.${i##*.}"
echo "Installing ${i##*/}"
wget -O "${xdgPath}/plugins-available/$fileName" "${pluginList[$i]}" || die "Could not install plugin $i"
chmod +x "${xdgPath}/plugins-available/$fileName" || die "Could not set execute permissions for plugin $i"
ln -s "${xdgPath}/plugins-available/$fileName" "${xdgPath}/plugins-enabled/$fileName" || die "Could not link plugin $i"
echo "Plugin $i installed successfully."
done
if [ -n "$i" ]; then
echo "Restarting orca"
orca -r &
fi
}

get_xdg_path
get_action action
if [ -n "$action" ]; then
${action// /_}
fi
exit 0
