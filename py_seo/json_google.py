import json,sys,traceback,urllib,urllib2
from web_utils import *
from str_utils import *

def data(url,title,desc):
    return [url,title,desc]

class Tjson_google():
    def __init__(self,source,q):
        self.q=q
        self.source=source
        self.arr=[]
        self.total=0

    def get(self):
        is_next=True
        step=0
        ok=False
        while is_next==True:
            try:
                request="https://ajax.googleapis.com/ajax/services/search/web?v=1.0&q="+self.q+"&start="+str(step)+"&key="+const.google_api+"&rsz=8"
                response=get_page(request)
                params=json.loads(response)
                if params['responseStatus']==200:
                    ok=True
                    responseData=params['responseData']
                    results=responseData['results']
                    if len(results)>0:
                        if step==0:
                            cursor=responseData['cursor']
                            self.total=int(cursor['estimatedResultCount'])
                        for result in results:
                            data=data(result['unescapedUrl'],result['title'],result['content'])
                            self.arr.append(data)
                    step+=8
                    is_next=((step<self.total) and (step<60))
                else:
                    is_next=False
            except:
                is_next=False
                traceback.print_exc(file=sys.stdout)
        return ok

    def get_count(self):
        try:
            request="https://ajax.googleapis.com/ajax/services/search/"+self.source+"?v=1.0&q="+q+"&key="+const.google_api+"&rsz=1"
            response=get_page(request)
            params=json.loads(response)
            if params['responseStatus']==200:
                responseData=params['responseData']
                results=responseData['results']
                if len(results)>0:
                    cursor=responseData['cursor']
                    self.total=int(cursor['estimatedResultCount'])
            return True
        except:
            traceback.print_exc(file=sys.stdout)
            return False

    def links(self):
        return self.arr

    def total(self):
        return self.total

