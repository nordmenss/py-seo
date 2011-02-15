import sys,traceback
if not hasattr(sys, 'setdefaultencoding'):
   reload(sys)

if hasattr(sys, 'setdefaultencoding'):
   sys.setdefaultencoding("utf-8")
   del sys.setdefaultencoding
from str_utils import *
from web_utils import *
import json, xml.dom.minidom

class Talexa_page():
    def __init__(self, url):
        self.url=url
        self.xml=''
        self.is_exists=False

        self.email=None
        self.title=None
        self.owner=None
        self.phone=None
        self.is_dmoz=False
        self.dmoz_title=None
        self.speed=None
        self.linksin=None
        self.rank=None
        self.delta=None
        self.popularity=None
        self.first_date=None
        self.related_sites=[]

    def get(self):
        try:
            request="http://data.alexa.com/data?cli=10&dat=snbamz&url="+self.url
            self.xml=get_page(request)
            if len(trim(self.xml))>0:
                dom = xml.dom.minidom.parseString(get_page(request))
                dom.normalize()
                self.handleAlexa(dom)
                return True
            else:
                return False
        except:
            traceback.print_exc(file=sys.stdout)
            return False

    def handleAlexa(self,alexa):
        self.is_exists=(alexa.getElementsByTagName("POPULARITY")!=[])

        if self.is_exists==True:
            self.handlePHONE(alexa.getElementsByTagName("PHONE"))
            self.handleSPEED(alexa.getElementsByTagName("SPEED"))
            self.handleEMAIL(alexa.getElementsByTagName("EMAIL"))
            self.handleTITLE(alexa.getElementsByTagName("TITLE"))
            self.handleOWNER(alexa.getElementsByTagName("OWNER"))
            self.handleLINKSIN(alexa.getElementsByTagName("LINKSIN"))
            self.handlePOPULARITY(alexa.getElementsByTagName("POPULARITY"))
            self.handleREACH(alexa.getElementsByTagName("REACH"))
            self.handleRANK(alexa.getElementsByTagName("RANK"))
            self.handleCREATED(alexa.getElementsByTagName("CREATED"))
            self.handleCAT(alexa.getElementsByTagName("CAT"))
            self.handleRL(alexa.getElementsByTagName("RL"))

    def handlePHONE(self,phone):
        if phone!=[]:
            self.phone=remove_bad_chars(phone[0].attributes["NUMBER"].value)

    def handleSPEED(self,speed):
        if speed!=[]:
            self.speed=int(speed[0].attributes["TEXT"].value)

    def handleEMAIL(self,email):
        if email!=[]:
            self.email=remove_bad_chars(email[0].attributes["ADDR"].value)

    def handleTITLE(self,title):
        if title!=[]:
            self.title=remove_bad_chars(title[0].attributes["TEXT"].value)

    def handleOWNER(self,owner):
        if owner!=[]:
            self.owner=remove_bad_chars(owner[0].attributes["NAME"].value)

    def handleLINKSIN(self,linksin):
        if linksin!=[]:
            self.linksin=int(linksin[0].attributes["NUM"].value)

    def handlePOPULARITY(self,popularity):
        if popularity!=[]:
            self.popularity=int(popularity[0].attributes["TEXT"].value)

    def handleREACH(self,reach):
        if reach!=[]:
            self.rank=int(reach[0].attributes["RANK"].value)

    def handleRANK(self,rank):
        if rank!=[]:
            self.delta=int(rank[0].attributes["DELTA"].value)

    def handleCREATED(self,created):
        if created!=[]:
            year=trim(created[0].attributes["YEAR"].value)
            month=trim(created[0].attributes["MONTH"].value)
            day=trim(created[0].attributes["DAY"].value)
            if len(month)==1:
                month='0'+month
            if len(day)==1:
                day='0'+day
            self.first_date=remove_bad_chars(year+"-"+month+"-"+day)

    def handleCAT(self,cat):
        if cat!=[]:
            self.dmoz_title=unicode(cat[0].attributes["TITLE"].value)
            self.is_dmoz=True

    def handleRL(self,rls):
        if rls!=[]:
            for site in rls:
                url=site.attributes["HREF"].value
                self.related_sites.append(get_host(url))

    def is_exists(self):
        return

    def get_email(self):
        return self.email

    def get_title(self):
        return self.title

    def get_owner(self):
        return self.owner

    def get_phone(self):
        return self.phone

    def get_is_dmoz(self):
        return self.is_dmoz

    def get_dmoz_title(self):
        return self.dmoz_title

    def get_speed(self):
        return self.speed

    def get_email(self):
        return self.email

    def get_linksin(self):
        return self.linksin

    def get_rank(self):
        return self.rank

    def get_delta(self):
        return self.delta

    def get_popularity(self):
        return self.popularity

    def get_first_date(self):
        return self.first_date

    def get_related_sites(self):
        return self.related_sites

