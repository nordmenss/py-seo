from urlparse import urlparse

class Tfrontpage(Thttp_connection):
    def __init__(self,domain,timeout=10):
        Thttp_connection.__init__(self,10)
        self.domain=domain
        self.real_domain_url=domain
        self.robots_txt=None
        self.sql=''

    def parse(self):
        try:
            self.get_page("/")
            while self.page.is_redirect()==True:
                self.redirects_count+=1
                redirect=self.page.get_redirect()
                host=get_host(redirect)
                if host!=self.domain.url:#redirect to other domain
                    break
                else:
                    path=get_path(location)
                    self.get_page(path)
        except:
            traceback.print_exc(file=sys.stdout)
            return False

    def check_robots_txt(self):
        try:
            conn = httplib.HTTPConnection(self.real_domain_url,timeout=4)
            conn.request("GET", "/")
            self.response = conn.getresponse()
            self.robots_txt=(self.response.status==200)
            conn.close()
        except:
            traceback.print_exc(file=sys.stdout)

    def is_robots_txt(self):
        return self.robots_txt

http_connection.close()