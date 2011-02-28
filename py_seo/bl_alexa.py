import traceback
from html.parser import HTMLParser
from py_seo.web_utils import *
from py_seo.str_utils import *

def data(fqdn,title):
    return [fqdn,title]

class Tbl_alexa(HTMLParser):
    def __init__(self, fqdn):
        HTMLParser.__init__(self)
        self.fqdn=fqdn
        self.links=[]
        self.total=0
        self.is_next=True
        self.text = None
        self.is_site_listing=False
        self.link_url=None
        self.link_title=None

    def parse(self,html):
        self.feed(html)
        self.close()

    def get(self):
        step=0
        while self.is_next==True:
            self.is_next=False
            request="http://www.alexa.com/site/linksin;"+str(step)+"/"+self.fqdn
            self.html=get_url(request)
            self.parse(self.html)
            step+=1
        return True

    def handle_starttag(self, tag, method, attrs):
        self.text = ''
        method.__call__(attrs)

    def handle_data(self, data):
        if self.text!=None:
              self.text+=data

    def start_div(self, attrs):
        for key,value in attrs:
            if value=="site-listing":
                self.is_site_listing=True

    def end_div(self):
        if self.is_site_listing==True:
            self.links.append(data(self.link_url,self.link_title))
            self.is_site_listing=False

    def start_a(self, attrs):
        if self.is_site_listing==True:
            for key,value in attrs:
                if key=="href":
                    self.link_url=str_replace("/siteinfo/","",value)
        else:
            for key,value in attrs:
                if key=="class":
                    if value=="next":
                        self.is_next=True

    def end_a(self):
        pass

    def start_strong(self, attrs):
        pass

    def end_strong(self):
        if self.is_site_listing==True:
            self.link_title=self.text.strip()

    def links(self):
        return self.links

    def total(self):
        return self.total

