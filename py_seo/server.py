import os

class memory():
	def __init__(self):
		self.memory_total_mb=None
		self.memory_used_mb=None
		self.swap_total_mb=None
		self.swap_used_mb=None
		self.console_output=None
		self.run_freecolor()
		self.parse()

	def run_freecolor(self):
	    self.console_output=os.popen('freecolor -m -o').read()

	def parse(self):
		lines=self.console_output.split("\n")
		line_i=0
		for line in lines:
			if line_i>0:
				parts=line.split(" ")
				j=0
				for part in parts:
					if j<3:
						if part.strip()!='':
							if line_i==1:
								if j==1:
									self.memory_total_mb=int(part)
								if j==2:
									self.memory_used_mb=int(part)
							if line_i==2:
								if j==1:
									self.swap_total_mb=int(part)
								if j==2:
									self.swap_used_mb=int(part)
							j+=1
			line_i+=1


