import math

def round_4(num):
	temp = round(num, 4)
	if temp>num:
		temp = temp - 0.0001
	else:
		pass
	return temp
