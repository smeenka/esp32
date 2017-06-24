# Lolin32

[Back to the main page](../readme.md)

Content:
* [Asyncio cooperative multitasking](asyncio.md)

The content of the lolin32 directory should be uploaded to a device.

This can be done for example with filemanager konquerer on ubuntu, and the lolin32 board running the ftpserver.

## main.py


Currently the esp32 stack does not add the /lib to the system 
path.

So this done in main.py:

	import sys
	sys.path.append("/lib")


Every application, not started from main.py should add /lib to the system path 


## Status of the library

All modules in the library are functional.

The http_server though is not fully funcional. Work to do is to better integrate the server with the asyncio operation system.

The server is functional but one gets sometimes often OS errors.
In the browser one has to press sometimes F5 to get the result.

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