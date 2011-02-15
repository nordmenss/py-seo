import os, sys
sys.path.append('/usr/development/domains/includes')
import const

def create_file(filename):
	open(filename, "w").close()

def get_file(filename):
	pf = file(filename, 'r')
	result = pf.read()
	pf.close()
	return result

def add2file(filename, content):
	output = open(filename, "a")
	output.write(content)
	output.close()

def write2file(filename, content):
	FILE = open(filename, "w")
	FILE.writelines(content)
	FILE.close()

def is_file_exists(filename):
	if len(filename)>0:
		return os.path.isfile(filename)
	else:
		return False

def is_dir_exists(dirname):
	if len(dirname)>0:
		return os.path.exists(dirname)
	else:
		return False

def mkdir(path):
    if not os.access(path, os.F_OK):
        os.mkdir(path)

def delete_file(filename):
	os.remove(filename)

def delete_file_if_exists(filename):
	if is_file_exists(filename)==True:
		delete_file(filename)

def get_lines(filename):
	result=[]
	for line in file(filename):
		result.append(line.strip())
	return result

def flag_file(filename):
	return const.flags_sqldir+'/'+os.path.basename(filename)

def set_flag(filename):
	create_file(flag_file(filename))

def write_sql(filename,sql):
	filename=const.sqldir+'/'+const.daemon_name+'_'+filename+'.sql'
	write2file(filename,sql)
	set_flag(filename)