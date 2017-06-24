import wifi
import utime as time

counter = 0

def main():
    wifi.ap.active(False)
    print("ap connected:" , wifi.ap.isconnected() )
    print ("Switching on AP")
    wifi.ap.active(True)
    print("ap connected:" , wifi.ap.isconnected() )
    print ("Pleas connect to AP")

    while not wifi.ap.isconnected():
        print ("Pleas connect to AP")
        time.sleep(10)

    print ("Switching on Station mode")
    wifi.wlan.active(True)
    time.sleep(1)
    print("wlan connected:" , wifi.wlan.isconnected())
    print("wlan status:" , wifi.wlan.status() )
    time.sleep(1)	
    print ("Scan for networks")
    networks = wifi.wlan.scan()
    for nw in networks:
        print ("%s %s %s %s %s" % nw)

 

    if wifi.wlan.isconnected():
        print("Already connected to AP. Rememberd settings!")
    else:    
        print ("Pleas connect to AP")

    settings = wifi.wlan.ifconfig() 
    print (settings)
    print ("ip:%s   subnet:%s  gateway%s  dns:%s"%settings) 

main()
