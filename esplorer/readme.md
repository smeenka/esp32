# Esplorer
***
[Back to the main page](../readme.md)



Esplorer (https://esp8266.ru/esplorer/) is a very nice tool.

## Chicken egg situation 

A blank board, or a corrupted board. Just flashed, but no contend in the file system.

How to get contact with the board, how to get files on the file system.

## About the Esplorer tool

The esplorer tool is downloaded from https://esp8266.ru/esplorer/ 

The tool has one main flaw: the upload to a board does not work.

Why: its too fast, the lolin32 board cannot cope with the speed of the upload.

Settings are available in the esplorer tool to set a waittime. But esplorer will always jump to the default setting (no waittime).

## Variant in this directory

So I build my own variant of the tool, based on checkout:

	72385c47df65e8c10727d730f17132cda3551fb8 
	Merge pull request #56 from oddstr13/ pr-autodetect-issue-41-fix Fixes 4refr0nt/ESPlorer#41

The esplorer variant in this directory does add a fixed waittime for upload of 5 ms.

Use  button *Send to ESP*. This button will load the file in memory in the lolin32.

Do not use button *Save to ESP*. Saving a file is not functional as the waittime of 5 ms way to fast.

How to use:

* copy the file esplorer.sh and ESPlorer.jar to ~/bin
* assumes is that ~/bin is in your $PATH
* start with esplorer.sh

## Snippet: connect to an AP

	ssid="<your ssid>"
	password="geheim"

	import machine
	import network
	wlan = network.WLAN(network.STA_IF)
	wlan.active(False)

	# for wipy2 board only
	antenna = machine.Pin(16, machine.Pin.OUT, value=0)

	if not wlan.isconnected():
	   print('connecting to:', ssid)
	   wlan.active(True)
	   wlan.ifconfig(  ('192.168.2.80', '255.255.255.0', '192.168.2.254', '192.168.2.254') )
	   wlan.connect(ssid, password)
	   while not wlan.isconnected():
	       pass
	print('network config:', wlan.ifconfig())

## Snippet: ftpserver

	import uftpserver
	uftpserver.ftpserver()

Assumed here is that the uftpserver module is a frozen module in the firmware.

If your firmware does not contain a frozen uftpserver module, place the while content of the file as a snippet (see lolin32/lib/uftpserver)






