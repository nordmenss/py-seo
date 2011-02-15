import urllib2, httplib
from urlparse import urlparse

class Thttp_connection():
    def __init__(self, timeout_value=10):
        self.path=None
        self.conn = httplib.HTTPConnection(self.domain.url,timeout=timeout_value)
        self.page=Thttp_page(self.conn)

    def get_page(self,path):
        self.page.get(path)

    def close(self):
        self.conn.close()