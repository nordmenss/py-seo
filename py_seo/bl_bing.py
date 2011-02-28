from py_seo.json_bing import *

class Tbl_bing():
    def __init__(self,fqdn):
        self.json=Tjson_bing("'"+fqdn+"'%20-site:"+fqdn)

    def get(self):
        return self.json.get()

    def links(self):
        return self.json.links()

    def total(self):
        return self.json.total()

