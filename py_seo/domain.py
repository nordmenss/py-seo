from str_utils import *
import datetime

def headers_info():
    info=dict()
    info['url']=None
    info['status']=None
    info['reason']=None
    info['http_version']=None
    info['headers']=[]
    return info

def Tlink_dated(url,title,time=None,description=None):
    link=dict()
    link['url']=url
    link['title']=title
    if description!=None:
        link['description']=description
    if time!=None:
        link['time']=time
    return link

class Tdomain():
    def __init__(self):
        self.domain_id=None
        self.url=""
        self.ip=None
        self.whois_domain=None
        self.whois_domain_updated=None
        self.whois_ip=None
        self.whois_ip_updated=None
        self.country_code=None
        self.latitude=None
        self.longitude=None
        self.site_title=None
        self.site_metadesc=None
        self.site_metakeys=None
        self.is_robots_txt=None
        self.created=""
        self.is_deleted=False
        self.whois_updated=None
        self.whois_created=None
        self.whois_expiration=None
        self.free_date=None
        self.pr=None
        self.pr_updated=""
        self.google_indexed=None
        self.google_bl=None

        self.alexa_updated=None
        self.alexa_rank=None
        self.alexa_delta=None
        self.alexa_popularity=None
        self.alexa_linksin=None
        self.alexa_email=None
        self.alexa_title=None
        self.alexa_owner=None
        self.alexa_phone=None
        self.alexa_speed=None
        self.alexa_updated=None
        self.alexa_is_dmoz=False
        self.alexa_dmoz_title=None
        self.alexa_first_date=None

        self.wa_first_date=None
        self.is_wa_updated=None
        self.nc_first_date=None
        self.is_nc_updated=False
        self.site_updated=None
        self.encoding=None
        self.page_size=None
        self.google_adsense_key=None
        self.google_analytics_key=None

        self.headers_info=[]
        self.metatags=[]
        self.frontpage_links=[]

        self.bl=[]

        self.bl_alexa_updated=None
        self.bl_bing=[]
        self.bl_bing_total=None
        self.bl_bing_updated=None
        self.bl_google=[]
        self.bl_google_total=None
        self.bl_google_updated=None
        self.bl_google_blogs=[]
        self.bl_google_blogs_total=None
        self.bl_google_blogs_updated=None
        self.bl_google_twitter=[]
        self.bl_google_twitter_total=None
        self.bl_google_twitter_updated=None
        self.bl_yahoo=[]
        self.bl_yahoo_total=None
        self.bl_yahoo_updated=None

        self.el_bing=[]
        self.el_bing_total=None
        self.el_bing_updated=None

        self.index_bing=[]
        self.index_bing_total=None
        self.index_bing_updated=None
        self.index_google=None
        self.index_google_total=None
        self.index_google_updated=None
        self.index_yahoo=[]
        self.index_yahoo_total=None
        self.index_yahoo_updated=None
        self.index_yandex=[]
        self.index_yandex_total=None
        self.index_yandex_updated=None

        self.images_bing_total=None
        self.images_bing_updated=None
        self.images_google_total=None
        self.images_google_updated=None

        self.has_subdomains=None
        self.has_related_sites=None
        self.subdomains=[]
        self.related_sites=[]
        self.alexa_related_updated=None
        self.google_related_updated=None

    def has_key(self,key):
        return hasattr(self,key)

    def get_dict(self):
        arr=dict()
        for key in self.__dict__.keys():
            if key.find("updated",0)<0:
                value=self.__dict__[key]
                if value is not None:
                    if  (value.__class__==datetime.date) or (value.__class__==datetime.datetime):
                        value=str(value)
                    ok=True
                    if value.__class__==list:
                        ok=(len(value)>0)
                    if value.__class__==list:
                        ok=(len(value)>0)
                    if value.__class__==dict:
                        ok=(len(value)>0)
                    if ok==True:
                        arr[key]=value
        return arr