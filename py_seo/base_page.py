import urllib2, httplib,sgmllib,socket,traceback
from str_utils import *

class Tbase_page(sgmllib.SGMLParser):
    def __init__(self):
        sgmllib.SGMLParser.__init__(self,url)
        self.url=url
        self.conn=None
        self.text=None
        self.html=None
        self.response=None
        self.headers=None
        self.meta=[]
        self.status=None
        self.redirect_to=None

        self.encoding=None
        self.charset=None

        self.title=None
        self.metadesc=None
        self.metakeys=None

    def parse(self):
        self.feed(self.html)
        self.close()

    def prepare(self):
        self.text=None
        self.html=None
        self.response=None
        self.headers=None
        self.meta=[]
        self.status=None
        self.redirect_to=None

        self.encoding=None
        self.charset=None

        self.title=None
        self.metadesc=None
        self.metakeys=None

    def get(self):
        try:
            self.prepare()
            self.conn = httplib.HTTPConnection(get_host(self.url),timeout=10)
            self.conn.request("GET", get_path(self.url))
            self.response = conn.getresponse()
            self.status=self.response.status
            self.response = conn.getresponse()
            if self.response.status in (301,302,):#REDIRECT
                self.redirect_to=self.response.getheader('location', '')
            else:
                if self.response.status==200:
                    self.headers=self.response.getheaders()
                    self.html=self.response.read()
                    if self.encoding!=None:
                        html=decode_gzip(html)
                    if self.charset==None:
                        self.html=html
                        self.parse()
                        self.parse_meta()
                        self.prepare()
                        self.html=html
                    else:
                        self.html=html
                    if self.charset!=None:
                        if self.charset.lower() not in ["utf-8","utf8"]:
                            if self.charset!=None:
                                self.html=self.html.decode(self.charset,"replace").encode('UTF8')
                        else:
                            self.html=self.html.decode('utf-8',"replace")
                    self.parse()
            return True
        except:
            traceback.print_exc(file=sys.stdout)
            return False

    def parse_headers(self):
        for k,v in self.headers:
            if k.lower()=="content-type":
                if is_finded(v,"charset=")==True:
                    parts=v.split(';')
                    if len(parts)==2:
                        charset=parts[1].strip()
                        parts=charset.split('=')
                        if len(parts)==2:
                            self.charset=parts[1].strip()
            if k.lower()=="content-encoding":
                self.encoding=v

    def start_title(self,attrs):
        pass

    def end_title(self):
        self.title=self.text.strip()

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

    def is_redirect(self):
        return (self.redirect_to!=None)

    def get_redirect(self):
        return self.redirect_to

    def get_title(self):
        return self.title

    def get_metadesc(self):
        return self.metadesc

    def get_metakeys(self):
        return self.metakeys

    def get_metatags(self):
        return self.meta

