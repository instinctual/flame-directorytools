# Flame DirectoryTools
Original by Bob Maple (bobm-matchbox [at] idolum.com)

Instinctual version by GaryO.

This script is licensed under the Creative Commons Attribution-ShareAlike [CC BY-SA](https://creativecommons.org/licenses/by-sa/4.0/)


## What

DirectoryTools is a Python script for **Autodesk Flame 2020 and above** that
adds a context menu to the MediaHub letting you TAR directories
from within the Flame file browser.  This version is modified by Instinctual to submit the TAR process to a Backburner queue for processing by Backburner Servers.


## Installing

In Flame 2020 these hook scripts are more flexible and no longer need to be
manually merged into the main hooks file.

To install, simply copy DirectoryTools.py to /opt/Autodesk/shared/python for
access by everyone:

`cp DirectoryTools.py /opt/Autodesk/shared/python/`

then either restart Flame or use the Flame hotkey **Shift-Control-H-P** to
reload all Python hooks.


## Using

From within MediaHub, select a directory or directories and right-click to
bring up the context menu. You should see a new item called **Directory Tools**
at or near the bottom of the menu, and can choose to TAR the
selected directories. If multiple directories are selected, each one will be
tarred or zipped separately in their own archive.

### Notes on TAR files
After the .tar file is created, a companion file called .tar.list is created
showing the contents of the archive.
