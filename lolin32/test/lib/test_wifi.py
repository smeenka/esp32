print("== Loading module test_wifi")
import wifi
import utime as time
import config
import machine  

led = machine.Pin(5, mode=machine.Pin.OUT)

def blink(n,on = 100,off=900):
    for i in range(n):
        led.value(0)
        time.sleep_ms(on)
        led.value(1)
        time.sleep_ms(off)


wifi.startap("test1234","1234")
print("Check access point exists with name test1234 and password 1234")
blink(5)
wifi.startap()
print("default config: ap should be alive")
blink(5,500,500)

ssid = "your ssid"
pw = config.get(ssid)
print("Trying to connect to " + ssid  + " password" + pw)
wifi.connect2ap(ssid)
while not wifi.wlan.isconnected():
    blink(1,50,500)
print ("wlan config......")
wifi.wlan.ifconfig()



