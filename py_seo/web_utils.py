import socket
import urllib.request

def get_url(url,_timeout=10):
    return urllib.request.urlopen(url,timeout=_timeout).read()

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
