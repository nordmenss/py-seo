import os

class mem():
	def __init__(self):
		self.total_mem=None
		self.used_mem=None
		self.total_swap=None
		self.used_swap=None
		self.console_output=None
		self.run_freecolor()
		self.parse()

	def run_freecolor(self):
	    self.console_output=os.popen('freecolor -m -o').read()

	def parse(self):
		lines=self.console_output.split("\n")
		line_i=0
		for line in lines:
			print "line_i=",line_i
			if line_i>0:
				parts=line.split(" ")
				j=0
				for part in parts:
					if j<3:
						if part.strip()!='':
							print "part=",part
							if line_i==1:
								if j==1:
									self.total_mem=int(part)
								if j==2:
									self.used_mem=int(part)
							if line_i==2:
								if j==1:
									self.total_swap=int(part)
								if j==2:
									self.used_swap=int(part)
					j=+1
					print "j=",j
			line_i+=1


