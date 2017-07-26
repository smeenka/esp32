# Lolin32

[Back to the main page](../readme.md)

Content:
* [Asyncio cooperative multitasking](asyncio.md)
* [Robonova robot and hitec servos in HMI mode](robonova.md)

The content of the lolin32 directory should be uploaded to a device.

This can be done for example with filemanager krusader on ubuntu, and the lolin32 board running the ftpserver.

After uploading the stack the first thing to do is:

	import wifi
	wifi.connect2ap("your_ssid","verysecret")

In this way the ssid and password is stored in the config file.
Next boot the main.py will connect to the ap automagically.

If preferred one can manually edit the config.json file and modify the wlan_ip key:

	"wlan_ip":"192.168.xxx.xxx"	

## main.py


Currently the esp32 stack does not add the /lib to the system 
path.

So this done in main.py:

	import sys
	sys.path.append("/lib")


Every application, not started from main.py should add /lib to the system path 


## Status of the library

All modules in the library are functional.

asyncio:
* supports waiting on streams with select
* supports signaling
* supports waiting and time related functions

asyncftp:
* based on version in https://github.com/cpopp/MicroFTPServer
* ftpserver as an asyncio task: can run concurrent aside a web server
* supports only passive mode

http_server:
* fully async, embedded in asyncio
* supporting concurrently muliple streams, multiple clients
* supports POST (limited to 512 bytes, only tekst)
* supports templating, single line and multiple line 
* supports REST calls

logging:
* java log4j alike

uftpserver:
* version from https://github.com/cpopp/MicroFTPServer with small modifications
* synchronous ftp server
* supports only passive mode

config:
* easy configuration for apps and unit tests
* config file: settings.json
* only one place in the file system contains config information (not checked in into git!)

wifi:
* contains references to ap and wlan objects
* managing ssid and passwords with the help of config

neopixels:
* support for adding colors to existing color


# Unit test of the library: best way to begin!

Modify main.py such that:

	try:
	    print ("Starting application")
	    os.chdir("/test/lib")
	    import test
	except Exception as e:
	    print ("Exception:",e)
	except  KeyboardInterrupt:
	    print ("KeyboardInterrupt")

and modify in /test/lib/test.py such that the requested test is started.

Connect a neopixel string with at least 4 pixels to pin 13 for some tests.	    

