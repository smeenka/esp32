# ------------------------------------------------------------
#        Developping with MicroPython in an async way
#
# ------------------------------------------------------------
#                      === configuration  ===
# ------------------------------------------------------------
print("== Loading module config")

import ujson as json
import sys

settings = {}
dirty = False


if sys.platform == "linux": 
    filen =  "settings.json"
else:
    filen =  "/settings.json"


 
try:
    print ("Opening config file ",filen)
    with open(filen, "r") as f:
        text = f.read()
        settings = json.loads(text)

except Exception as e:
    print ("config file %s does not exist. Empty config created!"% filen )
    settings =  { }

def get(k, default = 0):
    if not k in settings:
        global dirty
        settings[k] = default
        dirty = True
    return settings[k]

def put(k,v):
    global dirty
    settings[k] = v
    dirty = True


def save():
    global dirty
    if dirty:
        try:
            with open(filen, "w") as f:
                text = json.dumps(settings)
                f.write(text)
                dirty = False
        except Exception as e:
            print ("Error while writing")
            raise e

count = get("bootcount",0)
#put("bootcount",count + 1)
