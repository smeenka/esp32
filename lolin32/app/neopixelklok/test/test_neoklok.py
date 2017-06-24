import sys
sys.path.append("../")

import neoklok
from  neoklok import klok
import utime as time

klok.hour = 3
klok.minute = 22

now = (0,0,0,3,30,0)
klok.sync(now)


while True:
    klok.nextSecond()
    print(klok.getJsonTime() )
    time.sleep(1)
    

    klok.nextSecond()
    print(klok.toString() )
    time.sleep(1)

    klok.nextSecond()
    print(klok.getJsonTime() )
    time.sleep(1)

    klok.nextSecond()
    print(klok.toString() )
    time.sleep(1)

    print("Expect to switch to winter")
    now = (2017,3,25,3,30,0)
    klok.checkSummerWinter(now)
    
    print("Expect to switch to summer")
    now = (2017,3,26,3,30,0)
    klok.checkSummerWinter(now)

    print("Expect to switch to winter")
    now = (2017,10,29,3,30,0)
    klok.checkSummerWinter(now)

    print("Expect to switch to summer")
    now = (2017,10,28,3,30,0)
    klok.checkSummerWinter(now)
 