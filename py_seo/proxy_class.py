import sys
sys.path.append('/usr/development/includes')
import socket
import const

class Proxy():
    def __init__(self):
        self.proxy_id=0
        self.url=''

class ProxyHttp(Proxy):
    def __init__(self):
        pass

class ProxySocks(Proxy):
    def __init__(self):
        self.is_socks5=False


class ProxyList():
    def __init__(self):
        self.proxies=[]
        self.title=""
        self.text=""

    def get(self):
        try:
            text=json.dumps({'task':"select", 'task': self.title})
            result=get_socket(const.proxyd_host,settings.const.proxyd_port,text)
            if result!=False:
                self.text=result
            return True
        except:
            return False

class HttpList(ProxyList):
    def __init__(self):
        ProxyList.__init__(self)
        self.title="best_http"

    def get(self):
        try:
            if ProxyList.get()==True:
                lines=self.text.splitlines()
                for line in lines:
                    http=ProxyHttp()
                    list=self.text.split(',')
                    if len(list)==4:
                        http.proxy_id=list[0]
                        http.url=list[1]
                        self.proxies.append(http)
                return True
            return False
        except:
            return False

class SocksList(ProxyList):
    def __init__(self):
        ProxyList.__init__(self)
        self.title="best_socks"

    def get(self):
        try:
            if ProxyList.get()==True:
                lines=self.text.splitlines()
                for line in lines:
                    http=ProxySocks()
                    list=self.text.split(',')
                    if len(list)==4:
                        http.proxy_id=list[0]
                        http.url=list[1]
                        self.proxies.append(http)
                return True
            return False
        except:
            return False
