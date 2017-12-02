# ------------------------------------------------------------
#        Developping with MicroPython in an async way
#
# ------------------------------------------------------------
#                === application: neopixel klok  ===
# ------------------------------------------------------------
print("== module neoklok.py")
import logging
log  = logging.getlogger("neok")
log.setLevel(logging.DEBUG)
import config
import ujson  as json
from machine import RTC as rtc
import time

class Neoklok:

    def __init__(self):
        log.info("Constructor  Neoklok");

        self.zomertijdTabel = { # year: (march summertime, october wintertime)
            2016:(27, 30 ),
            2017:(26 ,29 ),
            2018:(25 ,28 ),
            2019:(31 ,27 ),
            2020:(29 ,25 ),
            2021:(28 ,31 ), 
            2022:(27 ,30 ),
            2023:(26 ,29 ),
            2024:(31 ,27 ),
            2025:(30 ,26 ),
            2026:(29 ,25 ),
            2027:(28 ,31 ),
            2028:(26 ,29 ),
            2029:(25 ,28 ),
            2030:(31 ,27 ),
            2031:(30 ,26 ),
            2032:(28 ,31 ),
            2033:(27 ,30 ),
            2034:(26 ,29 ),
            2035:(25 ,28 ),
            2036:(30 ,26 ),
            2037:(29 ,25 ),
            2038:(28 ,31 ),
            2039:(27 ,30 ),
            2040:(25 ,28 ),
            2041:(31 ,27 ),
            2042:(30 ,26 ),
            2043:(29 ,25 ),
            2044:(27 ,30 ),
            2045:(26 ,29 ),
            2046:(25 ,28 ),
            2047:(31 ,27 ),
            2048:(29 ,25 ),
            2049:(28 ,31 ),
            2050:(27 ,30 )
            }

    def sync(self,now):
        log.info("Syncing. " + self.toString() )
       
    def checkSummerWinter(self):
        now = time.localtime()
        offset = 1
        year  = now[0]
        month = now[1]
        day   = now[2]
        try:
            tup = self.zomertijdTabel[year]
            if 3 <  month < 10:
                offset = 2

            elif month == 3 and day >= tup[0]:
                offset = 2    
            elif month == 10 and day < tup[1]:
                offset = 2    
        except:
            pass        
        
        timeOffset = config.get('timeoffset',1) 

        if offset != timeOffset:
            if offset == 2:
                log.info("Changing to summertime")
            else:    
                log.info("Changing to wintertime")
            config.put("timeoffset",offset)


    def loadJsonTime(self,jsonString):
        obj = json.loads(jsonString)
        hour = obj.hour
        minute = obj.minute
        second = obj.second
        now = (2017,1,1,hour,minute,second,0,1)
        rtc.datetime(now)

    def getJsonTime(self):
        """Return a json string reperesenting the time """
        now = time.localtime()
        lhour = now[3] + config.get("timeoffset",1)
        return '{"hour":%s,"minute":%s,"second":%s}\n' % (lhour,now[4],now[5])

    def toString(self):
        now = time.localtime()
        lhour = now[3] + config.get("timeoffset",1)
        return "%2sh:%2sm:%2ss" % (lhour,now[4],now[5])


klok = Neoklok()
        
