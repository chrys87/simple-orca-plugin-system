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

get_keyboard_shortcut()
{
local alphaNumericList="$(echo {a..z} {0..9} | sed -e 's/\([a-z0-9]\)/FALSE \1/g')" #Keys
local pluginFileName
local p
local keyList=""
local modifierList="FALSE alt FALSE alt+shift FALSE control FALSE control+alt FALSE shift" #Modifier
local __shortcutKey="$1"
local specList="FALSE startnotify FALSE stopnotify FALSE error FALSE blockcall" #commands
shift
# yad notebooks write to a file:
local output="$(mktemp)"
for p in $@ ; do
yad --plug=420 --selectable-labels --tabnum=1 --text="Modifiers for $p" --list --title "Simple Orca Plugin Manager" --text "Select modifier keys for $i:" --radiolist --separator __+__ --column "" --column "Keys" $modifierList >> "$output" &
yad --plug=420 --selectable-labels --tabnum=2 --text="Keybinding for $p" --list --title "Simple Orca Plugin Manager" --text "Select keyboard shortcut for $i:" --radiolist --separator __+__ --column "" --column "Keys" $alphaNumericList >> "$output" &
yad --plug=420 --selectable-labels --tabnum=3 --text="Special for $p" --list --title "Simple Orca Plugin Manager" --text "Select special options for $i:" --checklist --separator __+__ --column "" --column "Parameters" $specList >> "$output" &
yad --plug=420 --tabnum=4 --selectable-labels --text="Parameters for $p" --form --separator "!" --title "Simple Orca Plugin Manager" --selectable-labels --field "Parameters for $i::lbl" --field "Exec:chk" --field "parameters:eb" >> "$output" &
yad --notebook --key=420 --tab="Modifiers for $p" --tab="Keybinding for $p" --tab="Special for $p" --tab="Parameters for $p"
# Read yad generated file into filenName variable, replacing single letter/number with key_letter/number and remove new lines
pluginFileName="$(cat "$output" | sed -e 's/^TRUE__+__\([a-z0-9]\)__+__$/key_\1__+__/' | tr -d $'\n')"
# Proper format for alt+shift and control+alt modifier.
pluginFileName="${pluginFileName//alt\+shift/alt__+__shift}"
pluginFileName="${pluginFileName//control\+alt/control__+__alt}"
# Remove TRUE__+__
pluginFileName="${pluginFileName//TRUE__+__/}"
# Remove FALSE and extra !s
pluginFileName="${pluginFileName//!FALSE!!/}"
pluginFileName="${pluginFileName//!FALSE/}"
# !TRUE or !TRUE!! is the exec flag.
pluginFileName="${pluginFileName//!TRUE!!/exec__+__}"
pluginFileName="${pluginFileName//!TRUE/exec__+__}"
# Remove ! from the end of the file name sttring
pluginFileName="${pluginFileName%!}"
# What ever !s are left are parameters.
pluginFileName="${pluginFileName//!/parameters_}"
# There are several item separators in this, so remove any left over |s
pluginFileName="${pluginFileName//|/}"
# Remove any __+__ separators from the end of the file name.
pluginFileName="${pluginFileName/%__+__/}"
if [ -z "$pluginFileName" ]; then
exit 0
fi
# Get rid of the temperary file
rm "$output"
pluginFileName="${p%.*}__-__${pluginFileName}.${p##*.}"
eval $__shortcutKey="'$pluginFileName'"
done
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
local items
items="$(yad --list --title "Simple Orca Plugin Manager" --text "Configure plugins:" --button "Toggle Selected Plugins:0" --button "Change Keyboard Shortcut:2" --button "Cancel:1" --checklist --separator $'\n' --column "" --column "Plugin" --column "Status" $checkList)"
if [ $? -eq 1 ]; then
close_simple_orca_plugin_manager
fi
if [ $? -eq 0 ]; then
for i in $items ; do
if ! ls -1 "${xdgPath}/plugins-enabled/${pluginPath[$i]##*/}" &> /dev/null ; then
ln -s "${pluginPath[$i]}" "${xdgPath}/plugins-enabled/"
else
unlink "${xdgPath}/plugins-enabled/${pluginPath[$i]##*/}"
fi
done
fi

if [ $? -eq 2 ]; then
for i in $items ; do
if ls -1 "${xdgPath}/plugins-enabled/${pluginPath[$i]##*/}" &> /dev/null ; then
unlink "${xdgPath}/plugins-enabled/${pluginPath[$i]##*/}"
fi
get_keyboard_shortcut fileName $i
mv "${xdgPath}/plugins-available/$i" "${xdgPath}/plugins-available/$fileName" || die "Could not make new shortcut."
done
fi
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
local fileName
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

for i in $items ; do
get_keyboard_shortcut fileName $i
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
action="${action:0:-1}"
${action// /_}
fi
done
exit 0
