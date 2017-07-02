# ------------------------------------------------------------
#        Developping with MicroPython in an async way
#
# ------------------------------------------------------------
#                      === unix stubs  ===
# ------------------------------------------------------------
print("==== /stub/machine.py: STUB for unix")

import logging
import ubinascii
log = logging.getlogger("esp")



def neopixel_write(pin, buf, dummy :True):
	buffer = ""
	log.debug(ubinascii.hexlify(buf[:30], " "))
