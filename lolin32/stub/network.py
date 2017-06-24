print("==== /stub/network.py: STUB for unix")


import logging
log = logging.getlogger("nstub")
log.setLevel(logging.DEBUG)

AP_IF       = 1
STA_IF      = 2
STAT_IDLE   = 0
STAT_CONNECTING     = 1  
STAT_WRONG_PASSWORD = 2
STAT_NO_AP_FOUND    = 3
STAT_CONNECT_FAIL   = 4
STAT_GOT_IP         = 5

class WLAN:
    def __init__(self,type):
        self.onoff = False
        self.ip = "0.0.0.0"
        self.ssid = "niet verbonden"

        log.info("Constructor WLAN ")
        if type == AP_IF:
           log.info("Type Access point")
        if type == STA_IF:
           log.info("Type station")

    def config(self , key = None,essid=None,password=None):
        log.info("config key: %s",key )
        if key == "ip":
            return self.ip
        if key == "essid":
            return self.ssid

    def active(self, onoff = False):
        log.info("Setting interface active: %s  ",onoff)
        self.onoff = onoff
        return onoff


    def connect(self,ssid,pw):
        log.info ("Connect to AP %s" , ssid )
        self.ssid = ssid
        self.ip = "192.168.2.33"
        

    def isconnected(self):
        log.info("isconnected: ")
        return self.ssid != "niet_verbonden"

    def ifconfig(self, tupleParm  =  None):
        log.info("ifconfig: %s",tupleParm )
        return (self.ip,self.ssid)    


    def status(self):
        if not self.onoff:
           return STAT_IDLE
        if self.isconnected():
            return STAT_GOT_IP
        else:
            return STAT_CONNECTING    


        return 1

    def scan(self):
        return  [(b"niet_verbonden",b"hidden",80,"4","5"),(b"bovenburen",b"hidden",80,"4","5"),(b"benedenburen",b"hidden",70,"4","5")]   



