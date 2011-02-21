import sgmllib,traceback
from web_utils import *
from str_utils import *

class Tlink():
    def __init__(self, url,title):
        self.url=url
        self.title=title

class Tbl_alexa(sgmllib.SGMLParser):
    def __init__(self, url):
        sgmllib.SGMLParser.__init__(self)
        self.url=url
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
            request="http://www.alexa.com/site/linksin;"+str(step)+"/"+self.url
            self.html=get_page(request)
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
            self.links.append(Tlink(self.link_url,self.link_title))
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

    def get_links(self):
        return self.links

    def get_total(self):
        return self.total

