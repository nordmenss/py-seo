import traceback
from py_seo.str_utils import *
from py_seo.base_page import *

def link_data(href,anchor_text,nofollow,is_img):
    return [str(href),str(anchor_text),bool(nofollow),bool(is_img)]

class Tpage(Tbase_page):
    def __init__(self,url):
        sgmllib.SGMLParser.__init__(self,url)
        self.links=[]
        self.google_adsense_key=None
        self.google_analytics_key=None
        self.is_http_link=False
        self.href=None
        self.anchor_text=None
        self.nofollow=None
        self.is_img=None

    def add_link(self):
        if len(self.links)<35000:
            self.links.append(link_data(self.href,self.anchor_text,self.nofollow,self.is_img))

    def start_a(self, attrs):
        self.is_http_link=False
        self.href=None
        self.anchor_text=None
        self.nofollow=None
        self.is_img=None
        try:
            for key,value in attrs:
                if key=="href":
                    self.href=value
                    if get_scheme(value)=='http':
                        self.is_http_link=True
                        self.href=value
                if key=="rel":
                    if is_finded(value,"nofollow"):
                        self.nofollow=True
        except:
            pass

    def end_a(self):
        try:
            if self.is_http_link==True:
                if self.text.strip()!="":
                    self.anchor_text=self.text.strip()
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
