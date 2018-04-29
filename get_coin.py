import coinone_API as coin
import file_writer as fileio
import userdata

import json
import os
import sys
import random
import datetime

log_location = userdata.log_loc()

def out_json(num):

	ticker = coin.ticker_api()
	with open(log_location + 'ticker_' + str(num) + '.json', 'w') as json_file:
		json.dump(ticker, json_file, ensure_ascii=True)
		json_file.close
	fileio.write_log(str(datetime.datetime.now()) + " get ticker_" + str(num) + "\n", 'calculate_log')
	
def read_json(num):

	with open(log_location + 'ticker_' + str(num) + '.json', 'r') as json_file:
		data = json.load(json_file)
		
	return data
	

def del_json(num):

	os.system("rm -rf " + log_location + "ticker_" + str(num) + ".json")
	
def rename_json(num1, num2):
	
	del_json(num2)
	os.system("mv " + log_location + "ticker_" + str(num1) + ".json " + log_location + "ticker_" + str(num2) + ".json")
	
	
def get_plus(ticker1, ticker2):
	#get pluscoin

	list_plus = {
		"btc": ((float(ticker2["btc"]["last"]) - float(ticker1["btc"]["last"])) / float(ticker1["btc"]["last"])) * 100,
		"btg": ((float(ticker2["btg"]["last"]) - float(ticker1["btg"]["last"])) / float(ticker1["btg"]["last"])) * 100,
		"bch": ((float(ticker2["bch"]["last"]) - float(ticker1["bch"]["last"])) / float(ticker1["bch"]["last"])) * 100,
		"eth": ((float(ticker2["eth"]["last"]) - float(ticker1["eth"]["last"])) / float(ticker1["eth"]["last"])) * 100,
		"etc": ((float(ticker2["etc"]["last"]) - float(ticker1["etc"]["last"])) / float(ticker1["etc"]["last"])) * 100,
		"xrp": ((float(ticker2["xrp"]["last"]) - float(ticker1["xrp"]["last"])) / float(ticker1["xrp"]["last"])) * 100,
		"qtum": ((float(ticker2["qtum"]["last"]) - float(ticker1["qtum"]["last"])) / float(ticker1["qtum"]["last"])) * 100,
		"iota": ((float(ticker2["iota"]["last"]) - float(ticker1["iota"]["last"])) / float(ticker1["iota"]["last"])) * 100,
		"ltc": ((float(ticker2["ltc"]["last"]) - float(ticker1["ltc"]["last"])) / float(ticker1["ltc"]["last"])) * 100
	}
	
	list_plus_temp = {
		"btc": 1,
		"btg": 1,
		"bch": 1,
		"eth": 1,
		"etc": 1,
		"xrp": 1,
		"qtum": 1,
		"iota": 1,
		"ltc": 1,
	}
	
	if list_plus["btc"] < 0 or list_plus["btc"] > 8:
		del list_plus["btc"]
		list_plus_temp["btc"] = 0
	if list_plus["btg"] < 0 or list_plus["btg"] > 8:
		del list_plus["btg"]
		list_plus_temp["btg"] = 0
	if list_plus["bch"] < 0 or list_plus["bch"] > 8:
		del list_plus["bch"]
		list_plus_temp["bch"] = 0
	if list_plus["eth"] < 0 or list_plus["eth"] > 8:
		del list_plus["eth"]
		list_plus_temp["eth"] = 0
	if list_plus["etc"] < 0 or list_plus["etc"] > 8:
		del list_plus["etc"]
		list_plus_temp["etc"] = 0
	if list_plus["xrp"] < 0 or list_plus["xrp"] > 8:
		del list_plus["xrp"]
		list_plus_temp["xrp"] = 0
	if list_plus["qtum"] < 0 or list_plus["qtum"] > 8:
		del list_plus["qtum"]
		list_plus_temp["qtum"] = 0
	if list_plus["iota"] < 0 or list_plus["iota"] > 8:
		del list_plus["iota"]
		list_plus_temp["iota"] = 0
	if list_plus["ltc"] < 0 or list_plus["ltc"] > 8:
		del list_plus["ltc"]
		list_plus_temp["ltc"] = 0
	
	log = (str(datetime.datetime.now()) + str(list_plus_temp) + '\n')
	fileio.write_log(log, 'calculate_log')
	return list_plus_temp
	
	
def get_minus(ticker1, ticker2):
	#get minuscoin

	list_minus = {
		"btc": ((float(ticker2["btc"]["last"]) - float(ticker1["btc"]["last"])) / float(ticker1["btc"]["last"])) * 100,
		"btg": ((float(ticker2["btg"]["last"]) - float(ticker1["btg"]["last"])) / float(ticker1["btg"]["last"])) * 100,
		"bch": ((float(ticker2["bch"]["last"]) - float(ticker1["bch"]["last"])) / float(ticker1["bch"]["last"])) * 100,
		"eth": ((float(ticker2["eth"]["last"]) - float(ticker1["eth"]["last"])) / float(ticker1["eth"]["last"])) * 100,
		"etc": ((float(ticker2["etc"]["last"]) - float(ticker1["etc"]["last"])) / float(ticker1["etc"]["last"])) * 100,
		"xrp": ((float(ticker2["xrp"]["last"]) - float(ticker1["xrp"]["last"])) / float(ticker1["xrp"]["last"])) * 100,
		"qtum": ((float(ticker2["qtum"]["last"]) - float(ticker1["qtum"]["last"])) / float(ticker1["qtum"]["last"])) * 100,
		"iota": ((float(ticker2["iota"]["last"]) - float(ticker1["iota"]["last"])) / float(ticker1["iota"]["last"])) * 100,
		"ltc": ((float(ticker2["ltc"]["last"]) - float(ticker1["ltc"]["last"])) / float(ticker1["ltc"]["last"])) * 100
	}
	
	list_minus_temp = {
		"btc": 1,
		"btg": 1,
		"bch": 1,
		"eth": 1,
		"etc": 1,
		"xrp": 1,
		"qtum": 1,
		"iota": 1,
		"ltc": 1,
	}
		
	
	if list_minus["btc"] > -0.7:
		del list_minus["btc"]
		list_minus_temp["btc"] = 0
	if list_minus["btg"] > -0.7:
		del list_minus["btg"]
		list_minus_temp["btg"] = 0
	if list_minus["bch"] > -0.7:
		del list_minus["bch"]
		list_minus_temp["bch"] = 0
	if list_minus["eth"] > -0.7:
		del list_minus["eth"]
		list_minus_temp["eth"] = 0
	if list_minus["etc"] > -0.7:
		del list_minus["etc"]
		list_minus_temp["etc"] = 0
	if list_minus["xrp"] > -0.7:
		del list_minus["xrp"]
		list_minus_temp["xrp"] = 0
	if list_minus["qtum"] > -0.7:
		del list_minus["qtum"]
		list_minus_temp["qtum"] = 0
	if list_minus["iota"] > -0.7:
		del list_minus["iota"]
		list_minus_temp["iota"] = 0
	if list_minus["ltc"] > -0.7:
		del list_minus["ltc"]
		list_minus_temp["ltc"] = 0
	
	log = (str(datetime.datetime.now()) + str(list_minus_temp) + '\n')
	fileio.write_log(log, 'calculate_log')
	return list_minus_temp
	
def evaluate(term1, term2):
	
	temp3 = {
		"btc": term1["btc"] + term2["btc"],
		"btg": term1["btg"] + term2["btg"],
		"bch": term1["bch"] + term2["bch"],
		"eth": term1["eth"] + term2["eth"],
		"etc": term1["etc"] + term2["etc"],
		"xrp": term1["xrp"] + term2["xrp"],
		"qtum": term1["qtum"] + term2["qtum"],
		"iota": term1["iota"] + term2["iota"],
		"ltc": term1["ltc"] + term2["ltc"],
	}
	
	if temp3["btc"] != 2:
		del temp3["btc"]
	if temp3["btg"] != 2:
		del temp3["btg"]
	if temp3["bch"] != 2:
		del temp3["bch"]
	if temp3["eth"] != 2:
		del temp3["eth"]
	if temp3["etc"] != 2:
		del temp3["etc"]
	if temp3["xrp"] != 2:
		del temp3["xrp"]
	if temp3["qtum"] != 2:
		del temp3["qtum"]
	if temp3["iota"] != 2:
		del temp3["iota"]
	if temp3["ltc"] != 2:
		del temp3["ltc"]
		
	list_return = sorted(temp3, key=lambda k : temp3[k])
	log = (str(datetime.datetime.now()) + " " + str(list_return) + '\n')
	fileio.write_log(log, 'calculate_log')
	return list_return
		
		
	
	
def get_onecoin(coins):
	
	ticker = read_json(3)
	
	if len(coins) == 0:
		return 'NULL'
	else:
		numof_coin = len(coins)
		num = 0
		value_yesterday_per_today = { "start": 0}
		while(True):
			last = float(ticker[coins[(numof_coin-1) - num]]["last"])
			yesterday = (float(ticker[coins[(numof_coin-1) - num]]["yesterday_low"]) + float(ticker[coins[(numof_coin-1) - num]]["yesterday_high"])) / 2
		
			value_yesterday_per_today[coins[(numof_coin-1) - num]] = (last - yesterday) / yesterday * 100
			
			num = num + 1
			if num == numof_coin:
				break


		del value_yesterday_per_today["start"]	
		print coins
		print value_yesterday_per_today

		num = 0
		checker = value_yesterday_per_today[coins[(numof_coin-1) - num]]
		returner = coins[(numof_coin-1) - num]
		while(True):
			if value_yesterday_per_today[coins[(numof_coin-1) - num]] < checker:
				checker = value_yesterday_per_today[coins[(numof_coin-1) - num]]
				returner = coins[(numof_coin-1) - num]
				
			num = num + 1
			if num == numof_coin:
				break
		
		print returner
			
		log = (str(datetime.datetime.now()) + " catched coin is : " + str(returner) + '\n')
		fileio.write_log(log, 'calculate_log')
		fileio.write_log(log, 'main_log')
		return returner
		
		
def get_balance_avail_coin(balance, ticker, krw_money):		#get balance_avaliable coin

	list_all = [
		float(balance["btc"]["avail"]) * float(ticker["btc"]["last"]),
		float(balance["bch"]["avail"]) * float(ticker["bch"]["last"]),
		float(balance["eth"]["avail"]) * float(ticker["eth"]["last"]),
		float(balance["etc"]["avail"]) * float(ticker["etc"]["last"]),
		float(balance["xrp"]["avail"]) * float(ticker["xrp"]["last"]),
		float(balance["qtum"]["avail"]) * float(ticker["qtum"]["last"]),
		float(balance["iota"]["avail"]) * float(ticker["iota"]["last"]),
		float(balance["ltc"]["avail"]) * float(ticker["ltc"]["last"]),
		float(balance["btg"]["avail"]) * float(ticker["btg"]["last"]),
	]

	num = 0
	coin_num = -1 
	while num < 9 :
		if list_all[num] > krw_money * 0.75:
			coin_num = num
			
		else:
			pass
			
		num = num + 1
	
	if coin_num == -1:
		string = 'krw'
	elif coin_num == 0:
		string = "btc"
	elif coin_num == 1:
		string = "bch"
	elif coin_num == 2:
		string = "eth"
	elif coin_num == 3:
		string = "etc"
	elif coin_num == 4:
		string = "xrp"
	elif coin_num == 5:
		string = "qtum"
	elif coin_num == 6:
		string = "iota"
	elif coin_num == 7:
		string = "ltc"
	elif coin_num == 8:
		string = "btg"
		
	return string
		

if __name__ == "__main__":
	get_onecoin(["btc","btg","xrp","qtum"])
