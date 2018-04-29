import coinone_API as cryptotrade
import source_func
import file_writer as fileio
import mail_func as mail

import time
import datetime
import sys

def sell_crypto(payload, price, cur_crypto_avail):
	#send sell order to server
	payload["price"] = price
	payload["qty"] = source_func.round_4(cur_crypto_avail)
	sell = cryptotrade.sell_api(payload)
	fileio.write_log((str(datetime.datetime.now()) + " sell order placed, error: %(err)s, coinname: %(coin)s, price: %(price)d, quantity: %(qty)f, total: %(total)d\n" % { 'err':sell["errorCode"], 'coin':payload["currency"], 'price':payload["price"], 'qty':payload["qty"], 'total':payload["price"] * payload["qty"]}), 'main_log')
	while True:
		time.sleep(1)
		temp = cryptotrade.limit_order_api(payload["currency"])
		if temp["limitOrders"] == []:
			fileio.write_log((str(datetime.datetime.now()) + ' sell order completed, sell finished\n'), 'main_log')
			break

	
def buy_crypto(payload, price, buy_crypto_price):
	#send buy order to server
	payload["price"] = price
	payload["qty"] = buy_crypto_price
	buy = cryptotrade.buy_api(payload)
	fileio.write_log((str(datetime.datetime.now()) + " buy order placed, error: %(err)s, coinname: %(coin)s, price: %(price)d, quantity: %(qty)f, total: %(total)d\n" % { 'err':buy["errorCode"], 'coin':payload["currency"], 'price':payload["price"], 'qty':payload["qty"], 'total':payload["price"] * payload["qty"]}), 'main_log')	
	while True:
		time.sleep(1)
		temp = cryptotrade.limit_order_api(payload["currency"])
		if temp["limitOrders"] == []:
			fileio.write_log((str(datetime.datetime.now()) + ' buy order completed, buy finished\n'), 'main_log')
			break


def trade(PAYLOAD, krw_money):
	
	order_info_pre = cryptotrade.orderbook_api(PAYLOAD["currency"])
	crypto_krw_pre = float(order_info_pre["ask"][1]["price"])
	krw_crypto_pre = float(order_info_pre["bid"][1]["price"])
		
	#process buy
	buy_crypto_price = source_func.round_4(krw_money/crypto_krw_pre)
	buy_crypto(PAYLOAD, crypto_krw_pre, buy_crypto_price)
	
	#process sell
	balance = cryptotrade.balance_api()
	cur_crypto_avail = float(balance[PAYLOAD["currency"]]["avail"])
	cur_crypto_total = float(balance[PAYLOAD["currency"]]["balance"])
	cur_crypto_avail = float(balance[PAYLOAD["currency"]]["avail"])
	cur_crypto_total = float(balance[PAYLOAD["currency"]]["balance"])
	
	count = 0
	while True:
		time.sleep(1)
		count = count + 1
		order_info = cryptotrade.orderbook_api(PAYLOAD["currency"])
		krw_crypto = float(order_info["bid"][1]["price"])
		crypto_krw = float(order_info["bid"][1]["price"])
		crypto_krw_value = krw_crypto * cur_crypto_avail
		
		if crypto_krw_value > krw_money * 1.0045:
			fileio.write_log(str(datetime.datetime.now()) + " reached 1.0045!\n", 'calculate_log')
			time.sleep(1)
			cur_1 = order_info
			while True:
				time.sleep(180)
				cur_2 = cryptotrade.orderbook_api(PAYLOAD["currency"])
				cur_1_crypto_krw_value = float(cur_1["bid"][1]["price"]) * cur_crypto_avail
				cur_2_crypto_krw_value = float(cur_2["bid"][1]["price"]) * cur_crypto_avail
				
				if ((cur_1_crypto_krw_value - cur_2_crypto_krw_value) / cur_1_crypto_krw_value) *100 > 0.1: 
					sell_crypto(PAYLOAD, float(cur_2["bid"][1]["price"]), cur_crypto_avail)
					break
			
				cur_1 = cur_2
			break
		#elif crypto_krw_value < krw_money * 0.7:
		#	mail.danger_fall()
		#	fileio.write_danger()
		#	sys.exit()
		#	break	
			
			
def break_trade(PAYLOAD, krw_money, balance):

	cur_crypto_avail = float(balance[PAYLOAD["currency"]]["avail"])
	cur_crypto_total = float(balance[PAYLOAD["currency"]]["balance"])
	cur_crypto_avail = float(balance[PAYLOAD["currency"]]["avail"])
	cur_crypto_total = float(balance[PAYLOAD["currency"]]["balance"])
	count = 0
	while True:
		time.sleep(1)
		count = count + 1
		order_info = cryptotrade.orderbook_api(PAYLOAD["currency"])
		krw_crypto = float(order_info["bid"][1]["price"])
		crypto_krw = float(order_info["bid"][1]["price"])
		crypto_krw_value = krw_crypto * cur_crypto_avail
		
		if crypto_krw_value > krw_money * 1.0045:
			fileio.write_log(str(datetime.datetime.now()) + " reached 1.0045!\n", 'calculate_log')
			time.sleep(1)
			cur_1 = order_info
			while True:
				time.sleep(180)
				cur_2 = cryptotrade.orderbook_api(PAYLOAD["currency"])
				cur_1_crypto_krw_value = float(cur_1["bid"][1]["price"]) * cur_crypto_avail
				cur_2_crypto_krw_value = float(cur_2["bid"][1]["price"]) * cur_crypto_avail
				
				if ((cur_1_crypto_krw_value - cur_2_crypto_krw_value) / cur_1_crypto_krw_value) * 100 > 0.1:
					sell_crypto(PAYLOAD, float(cur_2["bid"][1]["price"]), cur_crypto_avail)
					break
			
				cur_1 = cur_2
			break
		#elif crypto_krw_value < krw_money * 0.7:
		#	mail.danger_fall()
		#	fileio.write_danger()
		#	sys.exit()
		#	break
