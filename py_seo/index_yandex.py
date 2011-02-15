import urllib2, httplib,sgmllib,socket,traceback
from urlparse import urlparse
from web_utils import *
from file_utils import *
from str_utils import *

def Tlink(url,title):
    link=dict()
    link['url']=url
    link['title']=title
    return link

class Tindex_yandex(sgmllib.SGMLParser):
    def __init__(self, url):
        sgmllib.SGMLParser.__init__(self)
        self.url=url
        self.links=[]
        self.pages=0
        self.total=0
        self.is_next=True
        self.text = None
        self.is_total=False
        self.is_another=False
        self.is_cell=False
        self.link_url=None
        self.link_title=None

    def parse(self,html):
        self.feed(html)
        self.close()

    def get(self):
        step=0
        while self.is_next==True:
            self.is_next=False
            request="http://webmaster.yandex.ru/check.xml?hostname="+self.url+"&page_num="+str(step)
            self.html=get_page(request)
            self.parse(self.html)
            if step==0:
                self.total=self.pages
            step+=1
        return True

     def handle_starttag(self, tag, method, attrs):
        self.text = ''
        method.__call__(attrs)

    def handle_data(self, data):
        if self.text!=None:
              self.text+=data

    def start_tr(self, attrs):
        for key,value in attrs:
            if key=="class":
                if value=="another":
                    self.is_another=True

    def end_tr(self):
        if self.is_another==True:
            self.links.append(Tlink(self.link_url,self.link_title))
            self.is_another=False

    def start_td(self, attrs):
        if self.is_another==True:
            for key,value in attrs:
                if key=="class":
                    if value=="cell":
                        self.is_cell=True

    def end_td(self):
        if self.is_cell==True:
            self.is_cell=False

    def start_a(self, attrs):
        pass

    def end_a(self):
        if self.is_cell==True:
            self.link_url=self.text.strip()

    def start_div(self, attrs):
        for key,value in attrs:
            if key=="class":
                if value=="header g-line":
                    self.is_total=True

    def end_div(self):
        if self.is_cell==True:
            self.link_title=self.text.strip()
        if self.is_total==True:
            content=self.text.strip()
            if content.find(':')>0:
                self.pages=int(content[content.find(':')+1:])
            self.is_total=False

    def get_links(self):
        return self.links

    def get_total(self):
        return self.total


