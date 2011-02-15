import os

class mem():
	def __init__(self):
		self.total_mem=None
		self.used_mem=None
		self.total_swap=None
		self.used_swap=None
		self.console_output=None
		self.run_freecolor()

	def run_freecolor(self):
	    self.console_output=os.popen('freecolor -m -o').read()

	def parse(self):
		lines=self.console_output.split("\n")
		for line_i in range(2,3):
			parts=lines[line_i].split(" ")
			j=0
			for part in parts:
				if j<3:
					if part.strip()!='':
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

