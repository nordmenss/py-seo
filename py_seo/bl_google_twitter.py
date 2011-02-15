 from bl_alexa import *
from bname_parser import *

class Tbname_bl_google_twitter(Tparser):
    def __init__(self,domain):
        Tparser.__init__(self,domain)
        self.json=Tjson_google("web","site:twitter.com%20intext:"+self.domain.url)

    def get_sql(self):
       values=[]
        for link in self.json.get_links():
            sql_value=self.get_sql("(%s,%s,%s)",(link['url'],link['title'],link['description'],))
            values.append(sql_value)
        sql=self.sql.append("SELECT add_bls_google_twitter("+str(self.domain_id)+",ARRAY["+implode(",",values)+"]::text_text_text[],"+str(json_google.get_total())+");")
        return sql


