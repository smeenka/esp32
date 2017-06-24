print("== Loading module config")

import ujson as json
settings = {}
dirty = False
 
try:
    print ("Opening config file settings.json")
    with open("/settings.json", "r") as f:
        text = f.read()
        settings = json.loads(text)

except Exception as e:
    print ("config file does not exist. Empty config created!", e)
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
            with open("/settings.json", "w") as f:
                text = json.dumps(settings)
                f.write(text)
                dirty = False
        except Exception as e:
            print ("Error while writing")
            raise e

count = get("bootcount",0)
put("bootcount",count + 1)
