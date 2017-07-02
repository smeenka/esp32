# ------------------------------------------------------------
#        Developping with MicroPython in an async way
#
# ------------------------------------------------------------
#                      === unix stubs  ===
# ------------------------------------------------------------
print("==== /stub/machine.py: STUB for unix")

import logging
import utime as time

log = logging.getlogger("mach")
log.info("Machine stub for Linux build")


# Created by Anton Smeenk
#Note that this is the stub for Linux, to be able to test software for the esp8266 on linux

class Pin:
    IN = 1
    OUT = 2

    def __init__(self,pinnr,mode):
    	if mode == 1: 
    			modename = "IN" 
    	else: 
    		modename = "OUT"
    	self.pinnr = pinnr	
        log.info ("Constructor pin %s mode:%s",pinnr,modename) 

    def value(self, val=None):
        return 1    


class PWM:
    def __init__(self,pin,freq = None,duty = None):
        log.info ("Constructor PWM on pin %s ",pin.pinnr) 
        self.fr = 0
        self.du = 50

    def freq(self,f = None):
    	if f:
    		log.debug("Setting freq to %s",f)
    		self.fr = f
    	return self.fr	    
    
    def duty(self,d = None):
    	if d:
    		log.debug("Setting duty to %s",d)
    		self.du = d
    	return self.du	   


def idle():
	log.trace("Switch power to idle")
	time.sleep_ms(1)

def deepsleep():
	log.debug("Switch power to deepsleep")
