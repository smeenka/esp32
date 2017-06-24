print("== Loading module wifi")
import network    
import logging
import utime as time
import config

log = logging.getlogger("wifi")

wlan  = network.WLAN(network.STA_IF)
ap    = network.WLAN(network.AP_IF)

def getIp(): 
    tup = wlan.ifconfig()
    return tup[0]

def off():
    wlan.active(False)
    ap.active(False)


def connect2ap(ssid= None,pw = None):
    """ If pw is None get the password from the config file 
        If pw is not None, write ssid,pw to the config file

        If ip is None in config file choose dhcp config
        else get ip. 
        If gw is None  it is assumed as 192.168.2.254, 
        If dns is None it is assumed as 192.168.2.254, 
        Deactivate the wlan, wait 1 second and activate with given ssid and pw
    """ 
    log.info("Connecting to ap %s",ssid)

    if not ssid:
        ssid = config.get("ssid","xxxx")
    else:
        config.put("ssid",ssid)    

    if not pw:
        pw = config.get(ssid,"geheim")
    else:
        config.put(ssid,pw)


    ip  = config.get("wlan_ip")     
    gw  = config.get("wlan_gw","192.168.2.254")     
    dns = config.get("wlan_dns","192.168.2.254")
    config.save()

    wlan.active(False)
    wlan.active(True)     
    if ip:
        wconf = ( ip,'255.255.255.0',gw,dns)
        wlan.ifconfig( wconf )
    wlan.connect(ssid,pw)
         


def startap(ssid = None,pw = None):
    if ssid:
        config.put("ap_ssid",ssid)
    ssid = config.get("ap_ssid","micropython2")
    
    if pw:
        config.put("ap_pw",pw)
    pw = config.get("ap_pw","12345678") 
    config.save()   

    log.info("Starting AP with ssid:%s",ssid)

    ap.active(False)
    time.sleep_ms(100)
    ap.active(True)     
    time.sleep_ms(100)
    ap.config(essid=ssid, channel=11,password=pw)










