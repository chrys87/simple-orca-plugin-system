1.Howto write a plugin:

1.1 Filename:
description-<command>+control+alt+<key char>.sh
the description is optional, its used for key assign announcement
it dont have to be a shell script. python, perl and anything that produce an STD out also works here.

1.2 Modifiers / Keys /Commands
1.2.1 Moddifiers
you always have to press the orca key.
control= CTRL key
shift = shift key
alt = Alt key
the order of those three modifier keys doesnt matter and they are optional
but if they are exist only a few combinations (predefined by orca) is valid:
Valid modifier combinations:
alt (description-alt+w.sh)
control (description-control+w.sh)
shift (description-shift+w.sh)
control + alt (description-control+alt+w.sh)

1.2.2 Key
<Key char> is a singel character. its a musthave.
d.sh # uses orca + d as shortcut. the <char> has to be always the last character in 
the filename before the extension starts

1.2.3 Commands and Pluginsettings
with <command> you could controll the behaviour of the plugins. you could add more than one command. the order is optional. 
startnotify = announce "start <description>" before the script is executed. this useful as feedback for 
commands with longer progresstimes.
stopnotify = annouce "finish <description>". This is usefull as feedback for plugins with no output.
blockcall = dont start script in a thread, be careful, this locks orca until the script is finish
showstderr = not only show stdout but also stderr

1.3 Filecontent:
just normal shell, perl, python  scripts. orca will read the STD out (examples included)

2 Administration
2.1 Folders
plugins-available:
contains all existing scripts plus the administration scripts. its the script repository.
plugins-enabled:
contains the enabled (active) scripts. this folder will be read by orca.

2.2 Administration tools
the tools are located in the plugins-available folder 
./en <scriptname> #enables an script so its active
./dis <scriptname> #disable the script, its not used anymore
they just create links in plugins-enabled and make the scripts executable
to reload the plugins in orca, you have to restart orca
