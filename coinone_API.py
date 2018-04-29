import userdata

import base64
import json
import hashlib
import hmac
import httplib2
import time
import urllib2

ACCESS_TOKEN = userdata.ACCESS_TOKEN()
SECRET_KEY = userdata.SECRET_KEY()

BUY_URL = 'https://api.coinone.co.kr/v2/order/limit_buy/'
SELL_URL = 'https://api.coinone.co.kr/v2/order/limit_sell/'
BALANCE_URL = 'https://api.coinone.co.kr/v2/account/balance/'
ORDER_URL = 'https://api.coinone.co.kr/v2/order/limit_orders/'
URL_ORDERBOOK = 'https://api.coinone.co.kr/orderbook/?format=json&currency='
URL_TICKER = 'https://api.coinone.co.kr/ticker/?format=json&currency=all'

BALANCE_PAYLOAD = {
	"access_token": ACCESS_TOKEN,
}

def get_encoded_payload(payload):
	payload["nonce"] = int(time.time()*1000)
	
	dumped_json = json.dumps(payload)
	encoded_json = base64.b64encode(dumped_json)
	return encoded_json
	
def get_signature(encoded_payload, secret_key):
	signature = hmac.new(str(secret_key).upper(), str(encoded_payload), hashlib.sha512);
	return signature.hexdigest()
	
def sell_api(payload):
	encoded_payload = get_encoded_payload(payload)
	headers = {
		'Content-type': 'application/json',
		'X-COINONE-PAYLOAD': encoded_payload,
		'X-COINONE-SIGNATURE': get_signature(encoded_payload, SECRET_KEY)
	}
	http = httplib2.Http()
	response, content = http.request(SELL_URL, 'POST', headers=headers, body=encoded_payload)
	content = json.loads(content)
	return content 
	
def buy_api(payload):
	encoded_payload = get_encoded_payload(payload)
	headers = {
		'Content-type': 'application/json',
		'X-COINONE-PAYLOAD': encoded_payload,
		'X-COINONE-SIGNATURE': get_signature(encoded_payload, SECRET_KEY)
	}
	http = httplib2.Http()
	response, content = http.request(BUY_URL, 'POST', headers=headers, body=encoded_payload)
	content = json.loads(content)
	return content 
	
def balance_api():
	balance_payload = get_encoded_payload(BALANCE_PAYLOAD)
	headers = {
		'Content-type': 'application/json',
		'X-COINONE-PAYLOAD': balance_payload,
		'X-COINONE-SIGNATURE': get_signature(balance_payload, SECRET_KEY)
	}
	http = httplib2.Http()
	response, content = http.request(BALANCE_URL, 'POST', headers=headers, body=balance_payload)
	content = json.loads(content)
	return content
	
def limit_order_api(coin):
	ORDER_PAYLOAD = {
		"access_token": ACCESS_TOKEN,
		"currency": coin,
	}
	order_payload = get_encoded_payload(ORDER_PAYLOAD)
	headers = {
		'Content-type': 'application/json',
		'X-COINONE-PAYLOAD': order_payload,
		'X-COINONE-SIGNATURE': get_signature(order_payload, SECRET_KEY)
	}
	http = httplib2.Http()
	response, content = http.request(ORDER_URL, 'POST', headers=headers, body=order_payload)
	content = json.loads(content)
	return content
	
def ticker_api():
	order_raw = urllib2.urlopen(URL_TICKER)
	order_data = json.loads(order_raw.read())
	return order_data
	
def orderbook_api(type):
	
	order_raw = urllib2.urlopen(URL_ORDERBOOK + type)
	order_data = json.loads(order_raw.read())
	return order_data

		
		
