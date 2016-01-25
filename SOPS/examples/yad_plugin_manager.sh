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
    yad --error --title "Simple Orca Plugin Manager" --text "$1" | fold -s
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
answer="$(yad --list --title "Simple Orca Plugin Manager" --text "Select an action:" --column "Select an Action" "Configure Plugins" "Install New Plugins" "Close Simple Orca Plugin Manager")"
if [ $? -ne 0 ]; then
# Cancel or something other than an action was chosen, so close.
exit 0
fi
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
local items="$(yad --list --title "Simple Orca Plugin Manager" --text "Configure plugins:" --checklist --button "Toggle Selected Plugins:0" --button "Cancel:1" --separator $'\n' --column "" --column "Plugin" --column "Status" $checkList)"
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
local items="$(yad --list --title "Simple Orca Plugin Manager" --text "Install plugins:" --checklist --button "Install:0" --button "Cancel:1" --column "" --column "Plugin" $checkList)"
items="${items//TRUE|/}"
items="${items//|/}"
if [ -z "$items" ]; then
exit 0
fi
local keyList=""
local alphaNumericList="$(echo {a..z} {0..9} | sed -e 's/\([a-z]\)/FALSE \1/g' -e 's/FALSE a/TRUE a/')" #Keys
local modifierList="FALSE alt FALSE control FALSE control+alt FALSE shift" #Modifier
specList="FALSE startnotify FALSE stopnotify FALSE error FALSE blockcall" #commands

# yad notebooks write to a file:
local output="$(mktemp)"
for i in $items ; do
yad --plug=420 --tabnum=1 --text="Modifiers" --list --title "Simple Orca Plugin Manager" --text "Select modifier keys for $i:" --radiolist --separator __+__ --column "" --column "Keys" $modifierList >> "$output" &
yad --plug=420 --tabnum=2 --text="Keybinding" --list --title "Simple Orca Plugin Manager" --text "Select keyboard shortcut for $i:" --radiolist --separator __+__ --column "" --column "Keys" $alphaNumericList >> "$output" &
yad --plug=420 --tabnum=3 --text="Special" --list --title "Simple Orca Plugin Manager" --text "Select special options for $i:" --checklist --separator __+__ --column "" --column "Parameters" $specList >> "$output" &
yad --plug=420 --tabnum=4 --text="Parameters" --form --title "Simple Orca Plugin Manager" --selectable-labels --field "Parameters for $i::lbl" --field "Exec:chk" --field "parameters:eb" >> "$output" &
yad --notebook --key=420 --tab="Modifiers" --tab="Keybinding" --tab="Special" --tab="Parameters"
fileName="$(cat "$output" | tr -d $'\n')"
fileName="${fileName//control\+alt/control__+__alt}"
fileName="${fileName//TRUE__+__/}"
fileName="${fileName//FALSE|/}"
fileName="${fileName//TRUE|/exec__+__}"
fileName="${fileName//|/}"
fileName="${fileName/%__+__/}"
# fileName="$(yad --list --title "Simple Orca Plugin Manager" --text "Select keyboard shortcut for $i:" --checklist --separator __+__ --column "" --column "Keys" $checkList)"
if [ -z "$fileName" ]; then
exit 0
fi
# Get rid of the temperary file
rm "$output"
fileName="${i%.*}__-__${fileName}.${i##*.}"
echo "Installing ${i##*/}"
echo "fileName is $fileName"
exit 0
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
action="${action:0:-1}"
${action// /_}
fi
done
exit 0
