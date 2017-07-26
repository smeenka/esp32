# ------------------------------------------------------------
#        Developping with MicroPython in an async way
#
# ------------------------------------------------------------
#                      === library  tests  ===
# ------------------------------------------------------------
# main.py -- put your code here!
print("Loading module test_lowpower ...")

import uos as os
import sys
import utime as time
import machine
import network
import wifi

led    = machine.Pin(5, mode=machine.Pin.OUT)
sense  = machine.Pin(33, mode=machine.Pin.IN)
#adcp   = machine.Pin(33, mode=machine.Pin.IN)
print("1")
adc    = machine.ADC(sense)
print("2")


now = time.ticks_ms()
until = now + 1000

"""
while 1:
	while now < until:
		now = time.ticks_ms()
	until += 1000
	v = 1024 * adc.read() /4096
	print("ADC:%d mv" % v)
"""

print("Switching on blue led")
led.value(0)
time.sleep(2)

print("Switching off blue led")
led.value(1)
time.sleep(2)



print("Switching off WLAN")
wlan = wifi.wlan
wlan.disconnect()
#time.sleep(5)

print("Switching off AP")
ap = wifi.ap
ap.disconnect()
time.sleep(5)

#print("Switching to 240 MHz")
#achine.freq(240)
#ime.sleep(5)


now = time.ticks_ms()
until = now + 1000

"""
while 1:
	while now < until:
		now = time.ticks_ms()
	until += 1000
	print("ADC:" , adc.read())
"""


now = time.ticks_ms()
count = 0
while count < 100:
    machine.idle() 


    count += 1
now1 = time.ticks_ms()
diff = now1- now
print("1000 loops in %s ms. Per loop %s ms" %( diff, diff/1000) )

print("Sleeping forever")
while True:
    machine.idle()
    if led.value() == 1:
    	led.value(0)
    else: 
    	led.value(1)	





