import sys, urllib2, socket

def get_page(url,timeout=5):
    socket.setdefaulttimeout(timeout)
    return urllib2.urlopen(url).read()

def get_socket(host,port,text):
    try:
        s = socket.socket()
        s.connect((host,port))
        s.send(text)
        result=""
        while 1:
            data= s.recv(1024)
            result+=data
            if not data: break
        s.close()
        return result
    except:
        return False
