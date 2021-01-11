"""
코인원 API를 함수 형식으로 요청할 수 있도록 여기서 제작

요청제한 : 분당 300회 (초당 5회), 이 규칙을 어길 시 10분동안 밴당함

"""

import base64
import hashlib
import hmac
import json
import time
import httplib2
import requests
import time

from multiprocessing import Process, Manager

import constant


def public_timechecker(func):
    """
    코인원의 Public API는 분당 300회, 초당 5회이다. 따라서, 최소 0.2초의 텀을 두고 거래하도록 하는 데코레이터 메소드이다.
    이 데코레이터를 쓰면, 최근 Public API 요청 시간과 비교해 0.2초를 기다린다.
    :param func: class CoinoneAPI 내의 메소드
    """
    def wrapper(*args):
        cur_time = time.time()
        timediff = cur_time - args[0].public_checktime.get()
        if timediff < 2.3:
            time.sleep(timediff)
            args[0].public_checktime.set(time.time())
        args[0].public_checktime.set(cur_time)#  = cur_time
        # print(args[0].public_checktime)
        # print(type(args[0].public_checktime))
        return func(*args)
    return wrapper


def private_timechecker(func):
    """
    코인원의 Private API는 초당 10회이다. 따라서, 최소 0.1초의 텀을 두고 거래하도록 하는 데코레이터 메소드이다.
    이 데코레이터를 쓰면, 최근 Private API 요청 시간과 비교해 0.1초를 기다린다.
    :param func: class CoinoneAPI 내의 메소드
    """
    def wrapper(*args):
        cur_time = time.time()
        timediff = cur_time - args[0].private_checktime.get()
        if timediff < 1.5:
            time.sleep(timediff)
            args[0].private_checktime.set(time.time())
        args[0].private_checktime.set(cur_time)
        return func(*args)
    return wrapper


def success_check(func):
    def wrapper(*args):
        result = func(*args)
        if result["errorCode"] != "0":
            print(result)
            return False
        else:
            return result
    return wrapper


def _is_success(self, raw_json):
    # print(raw_json)
    if raw_json["errorCode"] != "0":
        # print(coin, raw_json)
        return False
    else:
        return raw_json


class CoinoneAPI:

    LOGIN = 'https://api.coinone.co.kr/v2/account/balance'
    ORDERBOOK = 'https://api.coinone.co.kr/orderbook'
    TICKER = 'https://api.coinone.co.kr/ticker'
    BUY = 'https://api.coinone.co.kr/v2/order/limit_buy'
    SELL = 'https://api.coinone.co.kr/v2/order/limit_sell'
    LIMIT_ORDER = 'https://api.coinone.co.kr/v2/order/limit_orders'
    COMPLETE_ORDER = 'https://api.coinone.co.kr/v2/order/complete_orders'
    CANCEL_ORDER = 'https://api.coinone.co.kr/v2/order/cancel'

    def __init__(self):
        # 시크릿 키와, 액세스 토큰을 받아온다.
        self._ACCESS_TOKEN, self._SECRET_KEY = self._get_key()

        # timechecker
        self.manager = Manager()
        self.public_checktime = self.manager.Value('L', time.time())
        self.private_checktime = self.manager.Value('L', time.time())
        # self.public_checktime.
        # self.public_checktime = time.time()
        # self.private_checktime = time.time()

    def _get_key(self):
        """
        constant에서 설정한 키 파일을 읽어들여와 Access Token과 Secret Key를 Return한다.
        :return: Access Token, Secret Key
        """
        key = []
        with open(constant.KEY_FILE_LOC, "r", encoding='utf8') as keyfile:
            for line in keyfile:
                line = line.replace("\n", "").split("=")
                key.append(line[1])

        return key[0], key[1].encode()

    def _get_encoded_payload(self, payload):
        payload['nonce'] = int(time.time() * 1000)

        dumped_json = json.dumps(payload)
        # print("dumped", dumped_json)
        encoded_json = base64.b64encode(bytes(dumped_json, 'utf-8'))
        return encoded_json

    def _get_signature(self, encoded_payload):
        signature = hmac.new(self._SECRET_KEY, encoded_payload, hashlib.sha512)
        return signature.hexdigest()

    def _get_response(self, url, payload):
        encoded_payload = self._get_encoded_payload(payload)

        headers = {
            'Content-type': 'application/json',
            'X-COINONE-PAYLOAD': encoded_payload,
            'X-COINONE-SIGNATURE': self._get_signature(encoded_payload),
        }

        http = httplib2.Http()
        response, content = http.request(url, 'POST', body=encoded_payload, headers=headers)

        # print(url, payload)
        # print(encoded_payload)
        # print(response, content)

        return json.loads(content.decode())

    @private_timechecker
    @success_check
    def get_balance(self):
        payload = {'access_token': self._ACCESS_TOKEN}
        return self._get_response(self.LOGIN, payload)

    @public_timechecker
    @success_check
    def get_orderbook(self, coin):
        return requests.get(self.ORDERBOOK, params={'currency': coin}).json()

    @public_timechecker
    @success_check
    def get_tickers(self):
        return requests.get(self.TICKER, params={'currency': 'all'}).json()

    @private_timechecker
    @success_check
    def buy_coin(self, currency: str, price: float, qty: float):
        # print(currency, price, qty)
        payload = {
            'access_token': self._ACCESS_TOKEN,
            'currency': currency,
            'price': str(price),
            'qty': qty
        }
        return self._get_response(self.BUY, payload)


    @private_timechecker
    @success_check
    def sell_coin(self, currency: str, price: float, qty: float):
        payload = {
            'access_token': self._ACCESS_TOKEN,
            'currency': currency,
            'price': str(price),
            'qty': qty
        }
        return self._get_response(self.SELL, payload)


    @private_timechecker
    @success_check
    def cancel_order(self, order_id, currency, price, qty, is_sell=True):
        payload = {
            'access_token': self._ACCESS_TOKEN,
            'order_id': order_id,
            'price': price,
            'qty': qty,
            'is_ask': 1 if is_sell is True else 0,
            'currency': currency
        }
        return self._get_response(self.CANCEL_ORDER, payload)


    @private_timechecker
    @success_check
    def check_order(self, coin):
        payload = {
            'access_token': self._ACCESS_TOKEN,
            'currency': coin
        }
        return self._get_response(self.LIMIT_ORDER, payload)


    @private_timechecker
    @success_check
    def check_complete_order(self, coin):
        payload = {
            'access_token': self._ACCESS_TOKEN,
            'currency': coin
        }
        return self._get_response(self.COMPLETE_ORDER, payload)


if __name__ == "__main__":
    test = CoinoneAPI()

    result = test.buy_coin("isdt", 0.50, 1000)
    result_id = result['orderId']
    print(result)
    res2 = test.check_order("isdt")
    print(res2)
    print(len(res2['limitOrders']), res2['limitOrders'])
    cancel = test.cancel_order(result_id, 'isdt', 0.50, 1000, False)
    print(cancel)
    res2 = test.check_order("isdt")
    print(res2)
    print(len(res2['limitOrders']), res2['limitOrders'])
