import urllib2, httplib,sgmllib,socket,traceback
from urlparse import urlparse
from web_utils import *
from file_utils import *
from str_utils import *
from domain_class import *

class Tsite_page(sgmllib.SGMLParser):
    def __init__(self, domain,verbose=0):
        sgmllib.SGMLParser.__init__(self, verbose)
        self.domain=domain
        self.real_domain_url=domain
        self.text = None
        self.html = None
        self.url = None
        self.response=None
        self.headers_info=[]
        self.headers=dict()
        self.meta=[]
        self.redirects_count=0
        self.frontpage_links=[]
        self.google_adsense_key=None
        self.google_analytics_key=None
        self.robots_txt=None
        self.title=''
        self.metadesc=''
        self.metakeys=''
        self.encoding=None
        self.charset=None
        self.link_ordering=0
        self.link=dict()

    def init(self):
        self.redirects_count=0
        self.meta=[]
        self.frontpage_links=[]
        self.google_adsense_key=None
        self.google_analytics_key=None
        self.title=''
        self.metadesc=''
        self.metakeys=''
        self.link_ordering=0
        self.link=dict()

    def add_link(self):
        if self.link_ordering<35000:
            self.link_ordering+=1
            self.frontpage_links.append(self.link)
            self.link=dict()

    def parse(self,html):
        self.feed(html)
        self.close()

    def add_headers_info(self):
        header_info=headers_info()
        header_info['url']=self.url
        header_info['status']=self.response.status
        header_info['reason']=self.response.reason
        header_info['http_version']=self.response.version
        header_info['headers']=list(self.response.getheaders())
        self.headers_info.append(header_info)

    def get(self, timeout_value=10):
        try:
            self.url=self.domain
            conn = httplib.HTTPConnection(self.domain,timeout=timeout_value)
            conn.request("GET", "/")
            self.response = conn.getresponse()
            while self.response.status in (301,302,):#REDIRECT
                location=self.response.getheader('location', '')
                new_url=get_host(location)
                self.real_domain_url=new_url
                path=get_path(location)
                conn = httplib.HTTPConnection(new_url)
                conn.request("GET", path)
                self.url=new_url+path
                self.add_headers_info()
                self.response = conn.getresponse()
                self.redirects_count+=1
                if self.redirects_count==5:
                    break;
            self.add_headers_info()
            if self.response.status==200:
                self.headers=self.response.getheaders()
                self.parse_headers()
                html=self.response.read()
                if self.encoding!=None:
                    html=decode_gzip(html)
                if self.charset==None:
                    self.html=html
                    self.parse(self.html)
                    self.parse_meta()
                    self.init()
                    self.html=html
                else:
                    self.html=html
                if self.charset!=None:
                    if self.charset.lower() not in ["utf-8","utf8"]:
                        if self.charset!=None:
                            self.html=self.html.decode(self.charset,"replace").encode('UTF8')
                    else:
                        self.html=self.html.decode('utf-8',"replace")
                self.parse(self.html)
            conn.close()
            status=self.response.status
            if status==200:
                self.check_robots_txt()
            return (status==200)
        except:
            traceback.print_exc(file=sys.stdout)
            return False

    def check_robots_txt(self):
        try:
            conn = httplib.HTTPConnection(self.real_domain_url,timeout=4)
            conn.request("GET", "/")
            self.response = conn.getresponse()
            self.robots_txt=(self.response.status==200)
            conn.close()
        except:
            pass
            print "robots.txt error"


    def parse_headers(self):
        for k,v in self.headers:
            if k.lower()=="content-type":
                if is_finded(v,"charset=")==True:
                    parts=v.split(';')
                    if len(parts)==2:
                        charset=trim(parts[1])
                        parts=charset.split('=')
                        if len(parts)==2:
                            self.charset=trim(parts[1])
            if k.lower()=="content-encoding":
                self.encoding=v

    def parse_meta(self):
        for k,v in self.meta:
            if k.lower()=="content-type":
                if is_finded(v,"charset=")==True:
                    parts=v.split(';')
                    if len(parts)==2:
                        charset=trim(parts[1])
                        parts=charset.split('=')
                        if len(parts)==2:
                            self.charset=trim(parts[1])

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

    def start_meta(self, attrs):
        try:
            key=attrs[0][1]
            value=attrs[1][1]
            self.meta.append((key,value))
            if key=="description":
                self.metadesc=value
            if key=="keywords":
                self.metakeys=value
        except:
            pass

    def end_meta(self):
        pass

    def start_title(self,attrs):
        pass

    def end_title(self):
        self.title=self.text.strip()

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

    def handle_data(self, data):
        if self.text!=None:
              self.text+=data

    def report_unbalanced(self,tag):
        pass

    def handle_starttag(self, tag, method, attrs):
        self.text = ''
        method.__call__(attrs)

    def get_html(self):
        return self.html

    def is_robots_txt(self):
        return self.robots_txt

    def get_title(self):
        return self.title

    def get_metadesc(self):
        return self.metadesc

    def get_metakeys(self):
        return self.metakeys

    def get_metatags(self):
        return self.meta

    def get_frontpage_links(self):
        return self.frontpage_links

    def get_google_adsense_key(self):
        return self.google_adsense_key

    def get_google_analytics_key(self):
        return self.google_analytics_key

    def get_headers_info(self):
        return self.headers_info

