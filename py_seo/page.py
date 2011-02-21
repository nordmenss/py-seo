import urllib2, httplib,sgmllib,socket,traceback
from urlparse import urlparse
from web_utils import *
from file_utils import *
from str_utils import *
from domain_class import *

class Tpage(Thttp_page):
    def __init__(self, domain,verbose=0):
        sgmllib.SGMLParser.__init__(self)
        self.url = None
        self.links=[]
        self.google_adsense_key=None
        self.google_analytics_key=None
        self.link=dict()
        self.sql=''

    def init(self):
        self.meta=[]
        self.links=[]
        self.google_adsense_key=None
        self.google_analytics_key=None
        self.link=dict()

    def add_link(self):
        if len(self.links)<35000:
            self.links.append(self.link)
            self.link=dict()

    def start_a(self, attrs):
        try:
            for key,value in attrs:
                if key=="href":
                    self.link['href']=value
                    if is_finded(value,"http://"):
                        if is_finded(get_host(value),self.domain)==False:
                            self.link['external']=True
                if key=="title":
                    if trim(value)!="":
                        self.link['title']=value
                if key=="rel":
                    if value=="nofollow":
                        self.link['nofollow']=True
        except:
            pass

    def end_a(self):
        try:
            if self.text.strip()!="":
                self.link['content']=self.text.strip()
            self.add_link()
        except:
            pass

    def parse_google_adsense_key(self,text):
        if is_finded(text,"_getTracker")==True:
            p=text.find("_getTracker")
            p1=text.find('"',p)+1
            p2=text.find('"',p1)
            self.google_adsense_key=text[p1:p2]

    def parse_google_analytics_key(self,text):
        if is_finded(text,"google_ad_client")==True:
            p=text.find("google_ad_client")
            p1=text.find('"',p)+1
            p2=text.find('"',p1)
            self.google_analytics_key=text[p1:p2]

    def start_script(self,attrs):
        pass

    def end_script(self):
        text=self.text.strip()
        self.parse_google_adsense_key(text)
        self.parse_google_analytics_key(text)

    def handle_comment(self,data):
        self.parse_google_adsense_key(data)
        self.parse_google_analytics_key(data)

    def get_links(self):
        return self.links

    def get_google_adsense_key(self):
        return self.google_adsense_key

    def get_google_analytics_key(self):
        return self.google_analytics_key
