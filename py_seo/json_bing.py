import sys, urllib,urllib2,json,traceback
from web_utils import *
from str_utils import *

def Tlink(url,title,description,added):
    link=dict()
    link['url']=url
    link['title']=title
    link['description']=description
    link['added']=added
    return link

def key_or_null(params,key):
    if params.has_key(key)==True:
        return params[key]
    else:
        return None

class Tjson_bing():
    def __init__(self, q):
        self.q=q
        self.links=[]
        self.total=0
        self.limit=0

    def get(self):
        is_next=True
        step=0
        while is_next==True:
            try:
                request="http://api.bing.net/json.aspx?AppId="+const.bing_api+"&Version=2.0&Market=en-US&Query="+self.q+"&Sources=web&Web.Count=50&Web.Offset="+str(step)
                response=get_page(request)
                params=json.loads(response)
                web=params['SearchResponse']['Web']
                self.limit=web['Total']
                if self.limit>0:
                    results=web['Results']
                    if step==0:
                        self.total=web['Total']
                    for r in results:
                        self.link=Tlink(key_or_null(r,'Url'),key_or_null(r,'Title'),key_or_null(r,'Description'),str(parse_date(key_or_null(r,'DateTime'))))
                        self.links.append(self.link)
                    step+=50
                    is_next=(step<self.limit)
                else:
                    is_next=False
                    errors=params['Errors']
                    for error in errors:
                        message=error['Message']
                        print "Tindex_from_bing error",message
            except:
                is_next=False
                traceback.print_exc(file=sys.stdout)
        return True

    def get_links(self):
        return self.links

    def get_total(self):
        return self.total

