import userdata

import sys
import os

log_location = userdata.log_loc()

def write_log(string, file_name): 
	file_w = open(log_location + file_name + ".txt", 'a')
	file_w.write(string)
	file_w.close()
	
def write_danger():
	file_w = open(log_location + 'complete.txt', "a")
	file_w.write("Break because coin value is lower then 70% krw value. Need solution\n")
	file_w.close()
	
def write_money(money): #input as string format int- ex '10000'
	os.system('rm -rf ' + log_location + 'money.txt')
	file_w = open(log_location + 'money.txt', 'w')
	file_w.write(money)
	file_w.close()
	
def get_money():
	file_r = open(log_location + 'money.txt', 'r')
	money = int(file_r.readline())
	return money

def renew_log():
	
	filenum_loc = userdata.project_loc()
	file_r = open(filenum_loc + 'filenum.txt', 'r')
	filenum = int(file_r.readline())
	file_r.close()

	os.system("rm -rf " + filenum_loc + 'filenum.txt')	
	file_w = open(filenum_loc + 'filenum.txt', 'w')
	file_w.write(str(filenum + 1))
	file_w.close()

	os.system("mv " + filenum_loc + 'log ' + filenum_loc + 'log_old/log_v' + str(filenum))
	os.system("mkdir " + filenum_loc + 'log')
	os.system("mv " + filenum_loc + 'log_old/log_v' + str(filenum) + '/money.txt ' + filenum_loc + 'log/money.txt')


if __name__ == "__main__":
	renew_log()
	
	
