import json
import requests
import time
import signal

from multiprocessing import Process, Manager

import constant
from coinone_api import CoinoneAPI
from db import DB
import else_func


class Coinone(CoinoneAPI, DB):

    def __init__(self):
        CoinoneAPI.__init__(self)
        DB.__init__(self)
        # super().__init__()

    def get_trusted_coin(self, select_count=constant.TRADE_COIN_NUM):
        ticker = self.get_tickers()
        ticker.pop('result')
        ticker.pop('errorCode')
        ticker.pop('timestamp')
        amount_vals = {}
        for data in ticker:
            amount_vals[data] = \
                ((float(ticker[data]['high']) + float(ticker[data]['low'])) / 2) * float(ticker[data]["volume"])
            # print(data)
        amount_vals = sorted(amount_vals.items(), key=lambda item: item[1])
        amount_vals.reverse()
        amount_vals = dict(amount_vals[:select_count])
        amount_vals = list(amount_vals.keys())
        return amount_vals

    def _get_coin_val(self, orderbook, is_sell=True):
        """
        코인의 현재가를 return. 조금의 손실을 감수하고 바로 사기 위해, sell은
        :param is_sell:
        :return:
        """
        if is_sell:     # 매도일 때, 매수 최고가로 팔기 위해 해당 가격을 돌려준다.
            return float(orderbook['bid'][0]['price'])      # 매수최고가
        else:
            return float(orderbook['ask'][0]['price'])      # 매도최저가

    def _get_coin_list(self, cur_coin_list, not_buy_list: list):
        coins = self.get_trusted_coin(constant.TRADE_COIN_NUM * 2)
        print(coins)
        buy_list = {}
        counter = 0
        for coin in coins:
            coin_orderbook = self.get_orderbook(coin)
            if else_func.get_falling(coin_orderbook) or not_buy_list.count(coin) > 0:
                pass
            else:
                buy_list[coin] = self._get_coin_val(coin_orderbook, is_sell=False)
                counter += 1

            if counter == constant.TRADE_COIN_NUM:
                break

        if len(buy_list) < constant.TRADE_COIN_NUM:
            print("거래량이 높은 코인들조차 하락세입니다. 3시간동안 거래를 중지합니다.")
            time.sleep(10800)
            return self._get_coin_list(cur_coin_list)       # 재귀 이용
        else:
            return buy_list

    # 얘가 process로 돌아가게 됨
    def _check_and_buy(self, coin_name: str, coin_price: float):
        # 일단, main에서 이 코인을 새로 구매하지 않도록 먼저 DB에 넣음
        self.db_buy_coin(coin_name)

        # 구매 확인
        qty = round(constant.TRADE_ONECOIN_VAL / coin_price, 4)
        print(coin_name, coin_price, qty)
        buy_result = self.buy_coin(coin_name, coin_price, qty)
        if buy_result is False: exit(0)
        buy_id = buy_result['orderId']
        buy_time = time.time()
        while True:
            # 주문이 완료되면 주문 체크를 종료
            if len(self.check_order(coin_name)['limitOrders']) == 0:
                break

            # 만약 거래가 이루이지지 않으면 거래 취소 후 종료
            if time.time() - buy_time > 300:
                cancel_order = self.cancel_order(buy_result['orderId'], coin_name, coin_price, constant.TRADE_ONECOIN_VAL / coin_price)
                self.db_sell_coin(coin_name, False)
                exit(0)

        print("buy complete")

        # 구매금 확인 및 수량 업데이트
        complete_order = self.check_complete_order(coin_name)
        for data in complete_order['completeOrders']:
            if data['orderId'] == buy_id:
                qty = round(qty - float(data['fee']), 4)
                break
        profit_price = coin_price * (1. + (constant.PROFIT_PERCENT / 100.))
        loss_price = coin_price * (1. - (constant.LOSS_PERCENT / 100.))

        print("buy amount check, update val : ", qty, profit_price, loss_price)

        # 가격 체크후 손익분기에 도달하면 판매하되, 판매가 딜레이되면 주문을 취소하고 다시 측정하는 방법을 계속 시도
        while True:
            # 가격 체크 후 적정 이득/손실에 도착하면 판매
            while True:
                cur_coin_val = self._get_coin_val(self.get_orderbook(coin_name))
                if cur_coin_val >= profit_price:
                    sell_result = self.sell_coin(coin_name, profit_price, qty)
                    sell_id = sell_result['orderId']
                    sell_time = time.time()
                    is_loss = False
                    break
                elif cur_coin_val < loss_price:
                    sell_result = self.sell_coin(coin_name, loss_price, qty)
                    sell_id = sell_result['orderId']
                    sell_time = time.time()
                    is_loss = True
                    break

            print("request sell complete")

            # 판매 주문이 올라가지 않았으면 주문 취소 후 재시도
            while True:
                if len(self.check_order(coin_name)['limitOrders']) == 0:
                    self.db_sell_coin(coin_name, is_loss)
                    end = True
                    break

                if time.time() - sell_time > 100:
                    if is_loss:
                        cancel_order = self.cancel_order(sell_id, coin_name, loss_price, qty, is_sell=True)
                    else:
                        cancel_order = self.cancel_order(sell_id, coin_name, profit_price, qty, is_sell=True)
                    end = False

            if end:
                print("order cycle of " + coin_name + " is complete")
                break


    def trade(self):
        cur_coin_list = self.get_cur_buy_list()
        buy_list = self._get_coin_list(cur_coin_list)
        print("cur_coin_list : ", cur_coin_list)
        print("buy_list : ", buy_list)
        for coin in buy_list:
            buy_result = self.buy_coin(coin, buy_list[coin], constant.TRADE_ONECOIN_VAL / buy_list[coin])
            print(coin, buy_list[coin])



    def db_listener(self):
        print('Listener is listening Redis...')
        for data in self._event_checker.listen():
            if data['data'] == b'lpop':     # pop이 이루어질 때만 시도함.
                cur_coin_list = self.get_cur_buy_list()
                not_buy_list = self.get_not_buy_list()
                buy_expect_list = self._get_coin_list(cur_coin_list, not_buy_list)
                print(buy_expect_list)
                for coin in buy_expect_list:
                    print(coin)
                    process = Process(target=self._check_and_buy, args=(coin, buy_expect_list[coin]))
                    process.start()

if __name__ == "__main__":
    test = Coinone()
    test.db_listener()
    # t = Process(target=test.trade_newver, args=())
    # t.start()
    # time.sleep(5)
    # test.heavy_load()
