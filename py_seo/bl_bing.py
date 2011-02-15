 from bl_alexa import *
from bname_parser import *

class Tbname_bl_bing(Tparser):
    def __init__(self,domain):
        Tparser.__init__(self,domain)
        self.json=Tjson_bing("'"+self.url+"'%20-site:"+self.url)

    def get_sql(self):
        values=[]
        for link in self.json.get_links():
            sql_value=self.get_sql("(%s,%s,%s,%s)",(link['url'],link['title'],link['description'],link['added'],))
            values.append(sql_value)
        sql="SELECT add_bls_bing("+str(self.domain_id)+",ARRAY["+implode(",",values)+"]::text_text_text_date[],"+str(self.json.get_total())+");"
        return sql


