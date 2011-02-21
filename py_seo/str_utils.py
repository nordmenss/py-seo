from urlparse import urlparse
import urllib,datetime,traceback,time,dateutil.parser

def is_finded(text,substring):
	return text.find(substring,0)>=0

def trim(str_value):
	return str_value.strip()

def is_trim(str_value):
	return (str_value==trim(str_value))

def is_lower(str_value):
	return (str_value==str_value.lower())

def is_english(str_value):
	arr=['-','-']
	for c in map(chr, range(97, 123)):
		arr.append(c)
	for c in map(chr, range(65, 91)):
		arr.append(c)
	for c in str_value:
		if c not in arr:
			return False
	return True

def decode_gzip(content):
	from StringIO import StringIO
	import gzip
	buf = StringIO(content)
	f = gzip.GzipFile(fileobj=buf)
	data = f.read()
	return data

def ltrim(str_value):
    while str_value[0]==' ':
        str_value=str_value[1:]
    return str_value

def str_replace(old,new,str):
	new_str=str
	return new_str.replace(old,new);

def is_finded(str,substr):
	return str.find(substr,0)>=0

def bool2str(bool):
	if bool==True:
		return 'true'
	else:
		return 'false'

def get_value(content,key):
	pos1=content.find(key)+len(key)
	pos2=content.find("\n",pos1)
	return content[pos1:pos2]

def implode(separator,list):
	if len(list)>0:
		return separator.join(list)
	else:
		return ""

def explode(separator,string):
	return string.split(separator)

def str_get_lines(value):
	return explode("\n",value)

def get_url(url):
	try:
		page=urllib.urlopen(url)
		return page.read()
	except:
		return ''

def get_scheme(href):
	parse_object = urlparse(href)
	return parse_object.scheme

def get_host(href):
	parse_object = urlparse(href)
	return parse_object.netloc

def get_path(href):
	parse_object = urlparse(href)
	path=parse_object.path
	if len(path)>0:
		if path[0]!='/':
			path='/'+path
	else:
		path='/'
	return path


def parse_date(str_value):
	try:
		d=dateutil.parser.parse(str_value)
		return datetime.date(d.year,d.month,d.day)
	except:
		return get_date()

def is_valid_date(date_str):
	try:
		valid_date = time.strptime(date,'%Y-%m-%d')
		return True
	except ValueError:
		return False

def is_valid_pr_reponse(response):
	return  len(response) in (0,11,12)

def format_pr(response):
	if response=='':
		return 'NULL'
	else:
		list=response.split(":")
		return int(trim(list[2]))

def is_valid_bool(value):
	return (value=="true") or (value=="false")

