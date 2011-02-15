import json,sys,traceback
from web_utils import *
from str_utils import *

def Tlink(url,title):
    link=dict()
    link['url']=url
    link['title']=title
    link['created']=None
    return link

class Tyahoo_base():
    def __init__(self,domain):
        self.domain=domain
        self.links=[]
        self.total=0
        self.response=''

    def request_count(self):
        return ''

    def get_count(self):
        try:
            response=get_page(self.request_count())
            params=json.loads(response)
            response=params['ysearchresponse']
            if int(response['responsecode'])==200:
                self.total=int(response['deephits'])
            return True
        except:
            traceback.print_exc(file=sys.stdout)
            return False

    def request_links(self):
        return ''

    def parse_lines(self):
        lines=self.response.splitlines(False)
        if is_finded(self.request_links(),"omit_inlinks")==True:
            start=1
        else:
            start=0
        i=0
        for line in lines:
            if i>start:
                values=line.split("\t")
                title=values[0]
                url=values[1]
                self.links.append(Tlink(url,title))
            i+=1

    def get(self):
        try:
            if self.get_count()==True:
                if self.total>0:
                    request=self.request_links()
                    self.response=get_url(request)
                    if self.response!="":
                        self.parse_lines()
                    else:
                        return False
                return True
            else:
                return False
        except:
            traceback.print_exc(file=sys.stdout)
            return False

    def get_links(self):
        return self.links

    def get_total(self):
        return self.total

class Tbl_yahoo(Tyahoo_base):
    def request_count(self):
        return "http://boss.yahooapis.com/ysearch/se_inlink/v1/"+self.domain+"?appid="+const.yahoo_api+"&format=json&omit_inlinks=domain&count=0"

    def request_links(self):
        return "http://siteexplorer.search.yahoo.com/export?p="+self.domain+"&bwm=i&bwmf=u&bwmo=d"

class Tindex_yahoo(Tyahoo_base):
    def request_count(self):
        return "http://boss.yahooapis.com/ysearch/se_pagedata/v1/"+self.domain+"?appid="+const.yahoo_api+"&format=json&count=0"

    def request_links(self):
        return "http://siteexplorer.search.yahoo.com/export?p="+self.domain+"&fr=sfp"
