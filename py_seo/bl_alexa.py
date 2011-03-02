import traceback
from lxml.html import document_fromstring
from py_seo.web_utils import *
from py_seo.str_utils import *

def data(fqdn,title):
    return [fqdn,title]

class Tbl_alexa():
    def __init__(self, fqdn):
        self.page=None
        self.fqdn=fqdn
        self.arr=[]
        self.total=0
        self.is_next=True

    def get(self):
        step=0
        while self.is_next==True:
            request="http://www.alexa.com/site/linksin;"+str(step)+"/"+self.fqdn
            self.html=get_url(request)
            self.page=document_fromstring(self.html)
            for link in self.page.cssselect('a.title'):
                href=link.get('href')
                href=str_replace('/siteinfo/','',href)
                content=link.text_content()
                self.arr.append(data(href,content))
            self.is_next=(self.page.cssselect('a.next')!=[])
            step+=1
        return True

    def data(self):
        return self.arr

    def total(self):
        return self.total

