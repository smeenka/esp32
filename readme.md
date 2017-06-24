
# ESP32 library and tools
***

* [Lolin32 board](lolin32/readme.md)
* [esplorer](esplorer/readme.md)

# 
***

# First time initialization

A fresh board, just flashed with micropython, but with a blank file system. 

How to get files on the board?

See [esplorer](esplorer/readme.md) for this.

# Onboard Development cycle
***

*  After reboot the board is connected to an AP
*  Within a try except block an unit test or an app is started
*  In case of an exception (or pressing <ctrl-c>) the ftpserver is started

* In Sublime Text3 use plugin ftpsync
* in the root of the lolin32 tree place file ftpsync.settings

* When saving a file in sublime, the file is automatically uploaded to the board.

* For massive file transfer one can use krusader. Works very nice.


# Unix Development cycle
***

For rapid development I use a linux host machine for development.

This can be done by using the build tool in sublime text editor:

To do this:

* build the linux variant of the micropython stack
* Add ~/bin to $PATH: add next line to .bashrc:

	export PATH=$PATH:~/bin

* Add the micropython executable to ~/bin 
* Create file  ~/.config/sublime-text3/Packages/User/micropython.sublime-build

with content:

	{
	    "cmd": ["/home/anton/bin/micropython", "$file"],
	    "file_regex": "^[ ]*File \"(...*?)\", line ([0-9]*)",
	    "selector": "py",
	    "env":{"MICROPYPATH":"/data1/workspace/micropython/esp32/lolin32/stub:/data1/workspace/micropython/esp32/lolin32lib"}
	}

Replace the path's with the actual paths as used by you.

The sub directory contains stubs for the hardware on the lolin32 board, which is not available on the linux host.




