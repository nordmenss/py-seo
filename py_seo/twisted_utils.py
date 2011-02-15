from config import *
from twisted.internet.protocol import Protocol
import psycopg2
import psycopg2.extras
import socket,traceback,json

def get_socket(host,port,text):
	try:
		import socket
		s = socket.socket()
		s.connect((host,port))
		s.send(text)
		result=""
		while 1:
			data= s.recv(1024)
			result+=data
			if not data: break
			s.close()
		return result
	except:
		return False

def get_cursor():
	conn = psycopg2.connect(connection_params())
	return conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

def get_access_ip():
	try:
		cur = get_cursor()
		cur.execute("select ip FROM access_ip")
		rows = cur.fetchall()
		arr=[]
	    	for row in rows:
        		ip=row['ip']
        		arr.append(ip)
    		cur.close()
		arr.append("127.0.0.1")
		return arr
	except:
		print "I am unable to connect to the database"
		sys.exit(1)

access_ip=get_access_ip()

class Tserver(Protocol):
	def __init__(self):
		self.ip=1488
		self.conn=None
		self.cursor=None
		self.tempfile=""
		self.params=dict()

	def init_db(self):
		self.conn = psycopg2.connect(connection_params())
		self.cursor=self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
		self.conn.set_client_encoding('UTF8')

	def execute(self,sql):
		self.cursor.execute(sql,params)

	def get_sql(self,sql,params=()):
		self.cursor.mogrify(sql,params)

	def get_object(self):
		return self.cursor.fetchone()

	def close_db(self):
		try:
			if self.conn!=None:
				self.conn.commit()
				self.cursor.close()
				self.conn.close()
				self.conn=None
		except:
			traceback.print_exc(file=sys.stdout)

	def makeConnection(self,transport):
		Protocol.makeConnection(self, transport)
		self.ip=transport.getPeer().host
		if self.ip in access_ip:
			self.init_db()
		else:
			print "ip access false"
			transport.loseConnection()

	def connectionLost(self,reason):
		if self.conn!=None:
			self.close_db()
		Protocol.connectionLost(self,reason)

	def error2json(self,desc):
		return json.dumps({'result':0,"desc":desc})
