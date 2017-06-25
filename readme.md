
# ESP32 library and tools
***

* [Lolin32 board](lolin32/readme.md)
* [esplorer](esplorer/readme.md)

# A note about this repository
***

This repository contains 
* library's
* stubs
* unit tests for libs and asyncio
* application (neopixelklok) 


I used to work with the esp8266, but was not satisfied with the stability of the platform (file system corruption etc).

Currently I focus on the esp32 development, as this is a very promising platform. Hopefully the porting of micropython to the esp32 platform will proceed.

As development tools I use ubuntu 16.04, minicom and Sublime Text3 and krusader for ftp file transfer. Sorry no windows support!


# Onboard Development cycle as proposed here
***

1) install plugin ftpsync in Sublime Text3.

When configured correctly Sublime Text3 will upload the file to the board on each save.

The root of the target file system should contain the file ftpsync.settings. See file lolin32/ftpsync.settings

2) assumed here is that the target board has a copy of all files in lolin32/. 

After resetting of the target device, main.py will:

*  connect to an AP (wifi.connect2ap()) 
*  Within a try except block an unit test or an app is started
*  In case of an exception (or pressing <ctrl-c>) the ftpserver is started
* In Sublime Text3 use plugin ftpsync
* in the root of the lolin32 tree place file ftpsync.settings

* When saving a file in sublime, the file is automatically uploaded to the board.
* pressing *ctrl-D* or do a hard reset for the next cycle


# Linux Development cycle as proposed here:
***

For rapid development I use a linux host machine for development.
Ubuntu 16.04 to be precice. Sorry, but the instructions given  here are only for linux, not for Windows!

## Step 1: build the linux variant of the micropython stack
[readme:](https://github.com/micropython/micropython-esp32)

## Step 2: place the linux  executable micropython on your $PATH 

for example:

	cd 
	mkdir bin
	# add next line to .bashrc:
	export PATH=$PATH:~/bin
	# Add the micropython executable to ~/bin 

## Step 3: install the micropython build in Sublime Text3:


* Create file  ~/.config/sublime-text3/Packages/User/micropython.sublime-build

with content:

	{
	    "cmd": ["/home/anton/bin/micropython", "$file"],
	    "file_regex": "^[ ]*File \"(...*?)\", line ([0-9]*)",
	    "selector": "py",
	    "env":{"MICROPYPATH":"/data1/workspace/micropython/esp32/lolin32/stub:/data1/workspace/micropython/esp32/lolin32lib"}
	}

Replace the path's with the actual paths as used by you.

# Create stubs for all hardware on the ESP32 board

Already done: see lolin32/stubs!

Note that the sublime-build for micropython will add the stub first on the micropython PATH


# First time initialization
***

A fresh board, just flashed with micropython, but with a blank file system. 

How to get files on the board?

See [esplorer](esplorer/readme.md) for this.

As soon as the board is connected to the wlan, and the ftpserver is running: copy with krusader all files in lolin32/ to the target file system

# A note about minicom

In minicom disable the hardware handshake, otherwise *ctrl-C* or *ctrl-D* will not work:
* within minicom press ctrl-A z (minicom command summary)
* O (configuration)
* Serial port setup
* D (Hardware Flow Control: no)
* G (Software Flow Control: no)
* Save setup as dft in configuration

