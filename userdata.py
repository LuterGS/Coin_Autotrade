import datetime
import sys
import os

def sender():
	str = 'input your sender mail'
	return str

def getter():
	str = 'input your receive mail'
	return str

def ACCESS_TOKEN():
	str = 'input your coinone ACCESS_TOKEN'
	return str

def project_loc():
	os.system("pwd > location2.txt")
	loc = open("location2.txt", 'r')
	location = str(loc.readline())[0:-1] + '/'
	loc.close()

	return location


def log_loc():

	os.system("pwd > location.txt")
	loc = open("location.txt", 'r')
	location = (((str(loc.readline()))[0:-1]) + '/')
	loc.close()
	
	return_str = (location + "log/")
	return return_str
	
def SECRET_KEY():
	str = 'input your coinone SECRET_KEY'
	return str

if __name__ == "__main__":
	v1 = project_loc()
	print v1
	v2 = log_loc()
	print v2
