import coinone_API as cryptotrade
import get_coin
import buy_sell as trade
import mail_func as mail
import file_writer as fileio
import userdata

import sys
import os
import datetime
import time

log_location = userdata.log_loc()
ACCESS_TOKEN = userdata.ACCESS_TOKEN()

PAYLOAD = {
	"access_token": ACCESS_TOKEN,
	"price": 10000,
	"qty": 0.1,
	"currency": "NULL",
}

if __name__ == "__main__":

	#get money
	krw_money = fileio.get_money()
	print (krw_money, type(krw_money))
	
	#start system, log
	fileio.write_log((str(datetime.datetime.now()) + ' Starting trade, input money: %(money)d\n'%{'money':krw_money}), 'main_log')
	
	#get already available coin
	ticker = cryptotrade.ticker_api()
	balance_outro = cryptotrade.balance_api()
	balance_coininfo = get_coin.get_balance_avail_coin(balance_outro, ticker, krw_money)
	balance_krw = float(balance_outro["krw"]["avail"])

	

	#if altcoin is detected _ break trade
	if balance_coininfo != "krw":  
		PAYLOAD["currency"] = balance_coininfo
		fileio.write_log(str(datetime.datetime.now()) + ' avaliable coin: ' + balance_coininfo + ', target krw: ' + str(krw_money * 1.06) + '\n', 'main_log')
		trade.break_trade(PAYLOAD, krw_money, balance_outro)

	#Else if altcoin is none _ start trade
	elif balance_coininfo == "krw": 
	
		fileio.write_log(str(datetime.datetime.now()) + ' avaliable money: ' + str(balance_krw) + ', target krw: ' + str(krw_money * 1.06) + '\n', 'main_log') 
		
		#if earn-sendmail, if lose-reset krw
		if balance_krw > krw_money * 1.06:
			new_money = int((((int(balance_krw) - krw_money))*0.75) + krw_money)
			print type(new_money), new_money
			fileio.write_money(str(new_money))
#			mail.reaching_point(((float(new_money) - float(krw_money)) / float(krw_money)) * 100, 'Earn one time complete')
			krw_money = fileio.get_money()
			
		elif balance_krw < krw_money:
			krw_money = int(balance_krw * 0.97)
			fileio.write_money(str(krw_money))
		
		while True:

			get_coin.del_json(1)
			get_coin.del_json(2)
			get_coin.del_json(3)
			
			get_coin.out_json(1)
			ticker_1 = get_coin.read_json(1)
			time.sleep(900)
			get_coin.out_json(2)
			ticker_2 = get_coin.read_json(2)
			time.sleep(300)
			get_coin.out_json(3)
			ticker_3 = get_coin.read_json(3)
			
			coin_term1 = get_coin.get_minus(ticker_1, ticker_2)
			coin_term2 = get_coin.get_plus(ticker_2, ticker_3)
			correct_coins = get_coin.evaluate(coin_term1, coin_term2)

			if correct_coins != []:
				checker = cryptotrade.ticker_api()
				PAYLOAD["currency"] = get_coin.get_onecoin(correct_coins)
				trade.trade(PAYLOAD, krw_money)

				break
