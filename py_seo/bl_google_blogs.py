 from bl_alexa import *
from bname_parser import *

class Tbname_bl_google_blogs(Tparser):
    def __init__(self,domain):
        Tparser.__init__(self,domain)
        self.xml=Tbl_google_blogs(self.domain.url)

    def get_sql(self):
        values=[]
        for link in self.xml.get_links():
            sql_value=self.get_sql("(%s,%s,%s,%s,%s,%s)",(link['url'],link['title'],link['description'],link['publisher'],link['creator'],link['posted'],))
            values.append(sql_value)
        sql="SELECT add_bls_google_blogs("+str(self.domain_id)+",ARRAY["+implode(",",values)+"]::text_text_text_text_text_date[],"+str(self.xml.get_total())+");"
        return sql


