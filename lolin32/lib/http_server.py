# ------------------------------------------------------------
#        Developping with MicroPython in an async way
#
# ------------------------------------------------------------
#                      === HTTP server ===
# ------------------------------------------------------------
import usocket as socket
import utime as time
import array
import sys
import asyncio 

import logging
log = logging.getlogger("http")

class HttpServer:
    def __init__(self, webroot ):
        log.info ("Constructor HttpServer") 
        # array of tupples ("route", callback)
        HttpServer.webroot = webroot
        self.resetRouteTable()
        self.socket = None

    def shutdown(self):
        self.socket.close()
        self.socket = None

    def onStart(self,path,callback):
        r = self.routes["begins"]
        r.append( (path, callback) )    

    def onEnd(self,path,callback):
        r = self.routes["ends"]
        r.append( (path, callback) )    

    def onExact(self,path,callback):
        r = self.routes["exact"]
        r.append( (path, callback) )    

    def onPost(self,path,callback):
        r = self.routes["post"]
        r.append( (path, callback) )    


    def resetRouteTable(self):    
        self.routes = {"ends":[],"begins":[] ,"exact":[] ,"post":[]}


    def bind(self,port):    
        log.info("bind server on port %d", port)
        if sys.platform == "linux":
            addr = socket.getaddrinfo("localhost",port)[0][-1]
        else:
            addr = ("",port)

        log.info ("Address info:%s",addr)
        # try to bind to address, kill os in case of faillure
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.bind(addr)
            s.setblocking(False)
            s.listen(5)
            self.socket = s
        except OSError as e:
            log.warn ("Accept socket error:%s",e) 
            s.close()
            s = None 
            raise e

    def listen(self,port = 80): 
        yield
        self.bind(port)
        yield asyncio.StreamReader(self.socket)

        log.info("Start listening")
        while True:
            try:
                yield asyncio.StreamWait()
                conn, clientaddr = self.socket.accept()
                #log.debug("Got a connection from %s " ,clientaddr)
                if conn:
                    conn.setblocking(False)
                    req = HttpRequest(conn,self.routes)
                    # handle request in a different task 
                    asyncio.sched.task( req.generator() )
            except Exception as e:
                tup = e.args 
                messnr = 0
                if tup and len(tup) >0:
                    messnr = tup[0]
                if messnr == 110 or messnr == 11: #EAGAIN: try again later
                    pass
                else:    
                    log.warn("Exception:%s %s ",e.__class__,tup)
                    raise e    


class HttpRequest:
    def __init__(self, conn, routes):
        self.conn = conn
        self.routes = routes  
        #log.debug("HttpRequest constructor")


    def generator(self):    
        yield
        self.task = yield asyncio.GetTaskRef()
        yield asyncio.StreamReader(self.conn)
        log.trace("Creating http task:%s",self.task.name)
        try: 
            routes = self.routes            
            # only for the first line block
            yield asyncio.StreamWait()
            conn = self.conn
            line = conn.readline()
            line = line.decode() 
            if line == None or len(line) == 0:
                return

            words = line.split()
            if len(words) < 3:
                log.debug ("Unable to parse line %s", line)
                return 
                
            method, fullpath, proto = words
            pathArray = fullpath.split("?", 1)
            params = {}
            if len(pathArray) > 1:
                p  = pathArray[1]
                pa = p.split("&")
                for p in pa:
                     log.debug("p: %s",p)
                     kv = p.split("=")
                     k = kv[0]
                     v = kv[1]
                     params[k] = v

            path = pathArray[0]    
            if path == "":
                path = "/"
            headers = {}
            # Assume that the rest of the header lines did arrive too
            # so the only wait here is due to the yield (less than a ms)
            line = conn.readline()
            while len(line) >2:
                #k, v = line.split(":", 1)
                log.trace("%s %s",self.task.name,line)
                line = conn.readline()
                yield

            body = array.array('B')


            self.path = path
            self.params = params
            self.headers = headers  
            
            if method == "POST":
                log.trace ("Getting post body")
                yield asyncio.StreamWait()
                body = conn.read(512)
                self.body = body.decode()

                log.debug ("Body:%s", body)

                for route  in routes["post"]:
                    path = route[0]
                    log.trace ("Testing post route %s",  path)
                    if self.path.startswith(path):
                        cb = route[1]
                        if cb:
                            yield from cb(self)
                        return
                yield from self.sendHeader(404)
                yield from self.sendContent("<h4>Sorry, no handler found for: %s!</h4>"%path) 
                return      


            for route  in routes["exact"]:
                path = route[0]
                log.trace ("Testing exact route %s" , path)
                if self.path == path:
                    cb = route[1]
                    if cb:
                        yield from cb(self)
                    return


            for route  in routes["ends"]:
                path = route[0]
                log.trace ("Testing ends route %s" , path)
                if self.path.endswith(path):
                    cb = route[1]
                    if cb:
                        yield from cb(self)
                    return


            for route  in routes["begins"]:
                path = route[0]
                log.trace ("Testing begins route %s" , path)
                if self.path.startswith(path):
                    cb = route[1]
                    if cb:
                        yield from cb(self)
                    return

            # request not handled, send 404        
            if self.conn:
                self.sendHeader(404)
                self.sendContent("<h4>Sorry, page not found: %s!</h4>"% path)        

        #except OSError as e:
        #    tup = e.args
        #    log.warn("handleRequest OSError: %s %s", e.__class__,tup)  

        finally:
            conn.close()     


    def sendOk(self):
        yield from self.sendHeader(200)

    def send(self,status, content_type,content):
        """ status is html status (200) etc, type is text/html, content is body """        
        yield from self.sendHeader(status,content_type )
        self.conn.send(content)


    def sendHeader(self,status, content_type = "text/html"):
        """status is html status (200) etc, type is text/html """        
        self.conn.send("HTTP/1.0 %d NA\r\n" % status)
        self.conn.send("Content-Type: %s\r\n" % content_type)
        self.conn.send("\r\n")
        yield

    def sendContent(self,content):
        self.conn.send(content)
        yield


    
    def sendFile(self, fname, content_type=None, templates = None):

        filename = HttpServer.webroot + fname
        log.debug("%s Sending file %s " , self.task.name, filename)
        if not content_type:
            content_type = self.get_mime_type(filename)
        self.sendHeader(200,content_type)
        f = None
        try:
            f =  open(filename, "rb") 
        except OSError as e:
            error = "<h4>Filename: %s. Error: %s</h4>" % (filename,e)
            log.warn("%s %s" , self.task.name, error)
            self.conn.send(error)       

        if f:    
            if templates: 
                yield from self.sendStreamTemplated(f,templates)
            else:    
                yield from self.sendStream(f)



    def sendStream(self, f):
        for buf in self.readBuf(f): # note that readBuf is a generator!
            yield from self.sendBuf(buf)

    def sendStreamTemplated(self, f,templates ):
        log.debug("sendStreamTemplated "  )
        total = 0

        # first use of generators!
        for line in self.readLine(f): # note that readLine is a generator
            char0 = line[0]
            if char0 == 64 or char0 == 35:  # character # or @
                line = line.decode()
                for k,v in templates.items():
                    if line.startswith(k):
                        templates[k] = None
                        try:
                            # first remove the template
                            template = line.replace(k,"")
                            if k[0] == '#':
                                line = template%v
                                log.debug("%s Template value:%s",self.task.name,v)
                                self.conn.send(line)       
                                yield
                            if k[0] == '@':
                                for tup in v:
                                    log.debug("%s Template tuple:%s",self.task.name,tup)
                                    listLine = template%tup
                                    self.conn.send(listLine)       
                                    yield
                        except Exception as e:
                            tup = e.args
                            log.warn("%s Exception:%s %s ",self.task.name,e.__class__,tup)
            else:
                # non templated lines
                self.conn.send(line)
                yield asyncio.Wait(1)
                            


    def sendBuf(self,buf):        
        total  = 0
        tosend = len(buf)
        while tosend > 0:    
            i = self.conn.send(buf)
            yield asyncio.Wait(5)
            tosend = tosend -i
            total = total + i
            buf = buf[i:]
            log.trace("Sending chunk. Total sent %d",  total )

    def readBuf(self,f): 
        """ Note:Generator!
            Reads a buffer from a file. Generator! 
            Returns a bytearray buffer of 512 bytes """
        while f:       
            buf = f.read(512)
            if buf and len(buf) > 0:
                log.trace("Yielding a buffer")
                yield buf    
            else:    
                log.debug ("%s File fully read", self.task.name)
                f.close()
                f = None

    def readLine(self,f): 
        """ Note:Generator!
            Reads a line of text from the file. Line is NOT transformed to text
            Returns a bytearray """
        while f:       
            line = f.readline()
            #log.info("yield line:%s ",line)
            if line:
                yield line
            else:
                log.debug ("%s File fully read", self.task.name)
                f.close() 
                f = None
   


            
    def get_mime_type(self,fname):
        if fname.endswith(".html"):
            return "text/html"
        if fname.endswith(".css"):
            return "text/css"
        return "text/plain"            


