# ------------------------------------------------------------
#        Developping with MicroPython in an async way
#
# ------------------------------------------------------------
#                      === library  tests  ===
# ------------------------------------------------------------
print("==== /sd/test/lib/test_poll.py")
import machine
import utime as time
import uselect as select
import usocket as socket
import network

import logging
log = logging.getlogger("test")

poll = select.poll()   # create instance of poll class


class Client:
    def __init__(self,socket):
        log.info("Creating client for socket %s ",socket)
        socket.setblocking(False)
        self.socket = socket
        poll.register(socket)

    # return false if the connection is closed and this client must be destroyed    
    def listen(self,conn):
        if (conn == self.socket):
            line = conn.readline()
            if line == None or len(line) == 0:
                log.info ("%s socket closed",conn )
                poll.unregister(conn)
                return False
            else:
                log.info ("%s data: %s ",conn,line )
        else:
            log.info ("%s not my piece of cake",conn )
        return True                
        
    

class Server:
    def __init__(self,port):
        self.clients = [] 
        self.port = port
        log.info("Listening nonblocking to port %s (http)",port)

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(socket.getaddrinfo("0.0.0.0", 8080)[0][4])
        self.sock.setblocking(False)
        self.sock.listen(5)
        poll.register(self.sock)


    def listen(self):
        clientIp = ""
        readylist= poll.poll(0)
        if (len(readylist) > 0):
            print (readylist)

        for tuples in readylist:
            file = tuples[0]

            if file and file == self.sock:
                conn, clientaddr = file.accept()
                clientIp = str(clientaddr)
                log.info ("Got a connection from %s" , clientIp)
                client = Client (conn)
                self.clients.append(client)

            else:
                for client in self.clients: 
                    if not client.listen(file):
                        self.clients.remove(client)

log.info ("Waiting 30 seconds for a connection from %s " , 8080)
now = time.ticks_ms()
until = now + 30000

server = Server(8080)

while now < until:
    server.listen()
    time.sleep_ms(10) # to prevent blocking on unix                    
    now = time.ticks_ms()
