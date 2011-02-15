 from bl_alexa import *
from bname_parser import *

class Tbname_bl_yahoo(Tparser):
    def __init__(self,domain):
        Tparser.__init__(self,domain)
        self.html=Tbl_yahoo(self.url)

    def get_sql(self):
        values=[]
        for link in self.html.get_links():
            sql_value=self.get_sql("(%s,%s)",(link['url'],link['title']))
            values.append(sql_value)
        sql="SELECT add_bls_yahoo("+str(self.domain_id)+",ARRAY["+implode(",",values)+"]::text_text[],"+str(self.html.get_total())+");"
        return sql


