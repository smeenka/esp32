print ("== Loading asyncftp module ...")

import usocket as socket
import network
import uos as os 
import asyncio
import utime as time
import logging

import sys
log = logging.getlogger("aftp")

def send_list_data(path, dataclient, full):
    try: # whether path is a directory name
        for fname in sorted(os.listdir(path), key = str.lower):
            dataclient.send(make_description(path, fname, full))
    except: # path may be a file name or pattern
        pattern = path.split("/")[-1]
        path = path[:-(len(pattern) + 1)]
        if path == "":
            path = "/"
        for fname in sorted(os.listdir(path), key = str.lower):
            if fncmp(fname, pattern) == True:
                dataclient.send(make_description(path, fname, full))

def make_description(path, fname, full):
    if full:
        stat = os.stat(get_absolute_path(path,fname))
        file_permissions = "drwxr-xr-x" if (stat[0] & 0o170000 == 0o040000) else "-rw-r--r--"
        file_size = stat[6]
        description = "{}    1 owner group {:>10} Jan 1 2000 {}\r\n".format(
                file_permissions, file_size, fname)
    else:
        description = fname + "\r\n"
        print ("description:" , description)
    return description

def send_file_data(path, dataclient):
    with open(path, "r") as file:
        chunk = file.read(512)
        while len(chunk) > 0:
            dataclient.send(chunk)
            chunk = file.read(512)


def save_file_data(path, dataclient):
    with open(path, "w") as file:
        while True:
            chunk = dataclient.read(512)
            file.write(chunk)
            if len(chunk) < 512:
                print ("OK finished.....")
                break


def get_absolute_path(cwd, payload):
    # Just a few special cases "..", "." and ""
    # If payload start's with /, set cwd to /
    # and consider the remainder a relative path
    if payload.startswith('/'):
        cwd = "/"
    for token in payload.split("/"):
        if token == '..':
            if cwd != '/':
                cwd = '/'.join(cwd.split('/')[:-1])
                if cwd == '':
                    cwd = '/'
        elif token != '.' and token != '':
            if cwd == '/':
                cwd += token
            else:
                cwd = cwd + '/' + token
    return cwd

# compare fname against pattern. Pattern may contain
# wildcards ? and *.
def fncmp(fname, pattern):
    pi = 0
    si = 0
    while pi < len(pattern) and si < len(fname):
        if (fname[si] == pattern[pi]) or (pattern[pi] == '?'):
            si += 1
            pi += 1
        else:
            if pattern[pi] == '*': # recurse
                if (pi + 1) == len(pattern):
                    return True
                while si < len(fname):
                    if fncmp(fname[si:], pattern[pi+1:]) == True:
                        return True
                    else:
                        si += 1
                return False
            else:
                return False
    if pi == len(pattern.rstrip("*"))  and si == len(fname):
        return True
    else:
        return False

#main task of ftp server: accept connections on ftp port
def ftpserver(commPort = 21,dataP = 1024): 
    global dataSock
    global dataPort
    dataPort = dataP
    yield
    commAddr = None
    dataAddr = None
    commSock = None
    dataSock = None
    log.info("Starting ftp server on port %d data port %s", commPort,dataPort)
    if sys.platform == "linux":
        commAddr = socket.getaddrinfo("localhost",commPort)[0][-1]
        dataAddr = socket.getaddrinfo("localhost",dataPort)[0][-1]
    else:
        commAddr = ("",commPort)
        dataAddr = ("",dataPort)

    log.info ("Address info:%s",commAddr)
    # try to bind to address, kill os in case of faillure
    try:
        commSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        commSock.bind(commAddr)
        commSock.setblocking(False)
        commSock.listen(5)

        dataSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        dataSock.bind(dataAddr)
        if sys.platform == "linux":
            dataSock.setblocking(True) # timeout of 5 seconds
        else:    
            dataSock.settimeout(5) # timeout of 5 seconds
        dataSock.listen(5)


    except OSError as e:
        log.warn ("Accept socket error:%s",e) 
        if commSock:
            commSock.close()
        if dataSock:
            dataSock.close()
        raise e
    yield asyncio.StreamReader(commSock)

    log.info("Start listening")
    while True:
        try:
            s = yield asyncio.StreamWait()
            conn, clientaddr = commSock.accept()
            log.debug("Got a connection from %s " ,clientaddr)
            if conn:
                conn.setblocking(False)
                # handle request in a different task 
                asyncio.sched.task( commandHandle(conn) )

        except Exception as e:
            tup = e.args 
            messnr = 0
            if tup and len(tup) >0:
                messnr = tup[0]
            if messnr == 110 or messnr == 11: #EAGAIN: try again later
                print("y")
                pass
            else:    
                log.warn("Exception:%s %s ",e.__class__,tup)
                raise e

cwd = '.'
fromname = None
dataSock = None
dataPort = None

msg_250_OK = '250 OK\r\n'
addr = network.WLAN(network.STA_IF).ifconfig()[0]


# task which handles the incoming datastream on ftp socket
def commandHandle(conn):    
    log.debug("commandHandle")
    conn.send("220 Hello, this is the ESP32.\r\n")
    yield
    yield asyncio.StreamReader(conn)
    while True:
        try: 
            yield asyncio.StreamWait()
            line = conn.readline()

            if line:
                if len(line) <= 0:
                    print("Client disappeared")
                    conn.close();
                    conn = null;
                    break
                commandState(conn,line)                    
        except Exception as e:
            tup = e.args 
            messnr = 0
            if tup and len(tup) >0:
                messnr = tup[0]
            if messnr == 110 or messnr == 11: #EAGAIN: try again later
                pass
            else:    
                log.warn("Exception:%s %s ",e.__class__,tup)
                raise

def getDataClient():
    global dataSock
    dataclient, data_addr = dataSock.accept()
    if sys.platform != "linux":
        dataclient.settimeout(5) # timeout of 5 seconds
    return dataclient    


# function which parses one command line from the client
def commandState(conn,line):
    dataclient = None
    global cwd 
    global fromname
    global dataPort
    line = line.decode().strip()

    if len(line) <= 4:
        command = line.upper()
        payload = ""
        log.debug("Command=%s No payload",command)
    else:    
        words = line.split(" ")
        command = words[0].upper()
        payload = line[len(command):].lstrip()
        log.debug("Command=%s, Payload=%s",command, payload)

    path = get_absolute_path(cwd, payload)
    
    try:
        if command == "USER":
            conn.send("230 Logged in.\r\n")
        elif command == "SYST":
            conn.send("215 UNIX Type: L8\r\n")
        elif command == "NOOP":
            conn.send("200 OK\r\n")
        elif command == "FEAT":
            conn.send("211 no-features\r\n")
        elif command == "PWD":
            conn.send('257 "{}"\r\n'.format(cwd))
        elif command == "CWD":
            path = get_absolute_path(cwd, payload)
            files = os.listdir(path)
            cwd = path
            conn.send(msg_250_OK)
        elif command == "CDUP":
            cwd = get_absolute_path(cwd, "..")
            conn.send(msg_250_OK)
        elif command == "TYPE":
            # probably should switch between binary and not
            conn.send('200 Transfer mode set\r\n')
        elif command == "SIZE":
            size = os.stat(cwd)[6]
            conn.send('213 {}\r\n'.format(size))
        elif command == "QUIT":
            conn.send('221 Bye.\r\n')
            print ("Received QUIT, but staying alive!")
        elif command == "PASV":
            result = '227 Entering Passive Mode ({},{},{}).\r\n'.format(
                addr.replace('.',','), dataPort>>8, dataPort%256)
            conn.send(result)
            print ("Sending:",result)

        elif command == "LIST" or command == "NLST":
            if not payload.startswith("-"):
                place = path
            else:
                place = cwd
            dataclient = getDataClient()
            send_list_data(place, dataclient, command == "LIST" or payload == "-l")
            conn.send("150 Here comes the directory listing.\r\n")
            conn.send("226 Listed.\r\n")
        elif command == "RETR":
            dataclient = getDataClient()
            send_file_data(path, dataclient)
            conn.send("150 Opening data connection.\r\n")
            conn.send("226 Transfer complete.\r\n")
            
        elif command == "STOR":
            conn.send("150 Ok to send data.\r\n")
            dataclient = getDataClient()
            save_file_data(path, dataclient)
            conn.send("226 Transfer complete.\r\n")
        elif command == "DELE":
            try:
                os.stat(path)
                os.remove(path)
            except Exception as e:
                tup = e.args
                log.warn("Delete file fails if not existing: Exception: %s %s ",e.__class__,tup)   
            conn.send(msg_250_OK)
        elif command == "RMD":
            os.rmdir(path)
            conn.send(msg_250_OK)
        elif command == "MKD":
            os.mkdir(path)
            conn.send(msg_250_OK)
        elif command == "RNFR":
            fromname = path
            conn.send("350 Rename from\r\n")
        elif command == "RNTO":
            if temp:
                os.rename(fromname, path)
                fromname = None
                conn.send(msg_250_OK)
            else:
                raise Exception()
        elif command == "STAT":
            if payload == "":
                conn.send("211-Connected to ({})\r\n"
                           "    Data address ({})\r\n"
                           "211 TYPE: Binary STRU: File MODE: Stream\r\n".format(
                           remote_addr[0], addr))
            else:
                conn.send("213-Directory listing:\r\n")
                send_list_data(path, cl, True)
                conn.send("213 Done.\r\n")
        else:
            conn.send("502 Unsupported command.\r\n")
            log.warn("Unsupported command %s with payload %s",command, payload)

    except Exception as e:
        tup = e.args
        log.warn("Command %s failed: Exception: %s %s ",command, e.__class__,tup)   
        conn.send('550 Failed\r\n')

    if dataclient != None:
        dataclient.close()
        dataclient = None    
