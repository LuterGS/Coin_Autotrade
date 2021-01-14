import json
import requests
import time
import signal
import datetime

from multiprocessing import Process, Manager
import threading

import constant
from coinone_api import CoinoneAPI
from db import DB
import else_func
from else_func import timelog


class Coinone(CoinoneAPI, DB):

    def __init__(self):
        CoinoneAPI.__init__(self)
        DB.__init__(self)
        # super().__init__()

    def get_trusted_coin(self, select_count=constant.TRADE_COIN_NUM):
        ticker = self.get_tickers()
        # timelog("ticker :", ticker)
        ticker.pop('result')
        ticker.pop('errorCode')
        ticker.pop('timestamp')
        amount_vals = {}
        for data in ticker:
            amount_vals[data] = \
                ((float(ticker[data]['high']) + float(ticker[data]['low'])) / 2) * float(ticker[data]["volume"])
            # print(str(datetime.datetime.now()), data)
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
        if is_sell:  # 매도일 때, 매수 최고가로 팔기 위해 해당 가격을 돌려준다.
            return float(orderbook['bid'][0]['price'])  # 매수최고가
        else:
            return float(orderbook['ask'][0]['price'])  # 매도최저가

    def _get_coin_list(self, cur_coin_list, not_buy_list: list):
        coins = self.get_trusted_coin(constant.TRADE_COIN_NUM * 3)
        timelog("cur_coin_list : ", cur_coin_list, "\tnot_buy_list : ", not_buy_list)
        buy_list = {}
        counter = 0
        for coin in coins:
            coin_orderbook = self.get_orderbook(coin)
            if else_func.get_falling(coin_orderbook) or not_buy_list.count(coin) > 0 or cur_coin_list.count(coin) > 0:
                pass
            else:
                buy_list[coin] = self._get_coin_val(coin_orderbook, is_sell=False)
                counter += 1

            if counter == constant.TRADE_COIN_NUM - len(cur_coin_list):
                break

        if len(buy_list) < constant.TRADE_COIN_NUM - len(cur_coin_list):
            timelog("거래량이 높은 코인들조차 하락세입니다. 3시간동안 거래를 중지합니다.")
            time.sleep(constant.TIME_MARKET_COOLDOWN)
            return self._get_coin_list(cur_coin_list, not_buy_list)  # 재귀 이용
        else:
            return buy_list

    # 얘가 process로 돌아가게 됨
    def _check_and_buy(self, coin_name: str, coin_price: float):
        # 일단, main에서 이 코인을 새로 구매하지 않도록 먼저 DB에 넣음
        self.db_buy_coin(coin_name)

        # 구매 확인
        qty = round(constant.TRADE_ONECOIN_VAL / coin_price, 4)
        # print(coin_name, coin_price, qty)
        buy_result = self.buy_coin(coin_name, coin_price, qty)
        if buy_result is False: exit(0)
        buy_id = buy_result['orderId']
        buy_time = time.time()
        buy_price = round(coin_price * qty, 2)
        while True:
            # 주문이 완료되면 DB에 정상적으로 주문이 완료되었다고 입력 후 종료
            if self.trace_order(buy_id, coin_name)['status'] == 'filled':
                self.db_buy_confirm_coin(coin_name, coin_price, qty, buy_price)
                break

            # 만약 거래가 이루이지지 않으면 거래 취소 후 종료
            if time.time() - buy_time > 300:
                cancel_order = self.cancel_order(buy_id, coin_name, coin_price, qty, True)
                self.db_buy_erase_coin(coin_name)
                exit(0)

        # 구매금 확인 및 수량 업데이트
        # TODO: 코인을 쪼개서 구매했을 때 어떻게 처리할 것인가?
        complete_order = self.check_complete_order(coin_name)
        qty = 0.0
        heuristics_counter = 0
        for data in complete_order['completeOrders']:
            if data['orderId'] == buy_id:
                qty += int((float(data['qty']) - float(data['fee'])) * 10000) / 10000
                coin_price = float(data['price'])
            if heuristics_counter == 4:
                break
            heuristics_counter += 1

        timelog(coin_name + "\tbuy complete, qty : ", qty, "\tprice : ", coin_price)

        # 판매금액 재확인
        zero_count = else_func.get_zero(coin_price)
        if zero_count == 0:
            profit_price = round(coin_price * (1. + (constant.PROFIT_PERCENT / 100.0)), 1)
            loss_price = round(coin_price * (1. - (constant.LOSS_PERCENT / 100.0)), 1)
        else:
            profit_price = round((coin_price * (1. + (constant.PROFIT_PERCENT / 100.))) / (10 ** zero_count), 0) * (
                        10 ** zero_count)
            loss_price = round((coin_price * (1. - (constant.LOSS_PERCENT / 100.))) / (10 ** zero_count), 0) * (
                        10 ** zero_count)

        # print(coin_name + "\tbuy amount check, update val : ", profit_price, loss_price)

        # 가격 체크후 손익분기에 도달하면 판매하되, 판매가 딜레이되면 주문을 취소하고 다시 측정하는 방법을 계속 시도
        while True:
            # 가격 체크 후 적정 이득/손실에 도착하면 판매
            while True:
                cur_coin_val = self._get_coin_val(self.get_orderbook(coin_name))
                if cur_coin_val >= profit_price:
                    sell_result = self.sell_coin(coin_name, profit_price, qty)
                    if sell_result is False:
                        qty = qty - 0.0001
                        sell_result = self.sell_coin(coin_name, profit_price, qty)
                    sell_id = sell_result['orderId']
                    sell_time = time.time()
                    is_loss = False
                    break
                elif cur_coin_val < loss_price:
                    sell_result = self.sell_coin(coin_name, loss_price, qty)
                    if sell_result is False:
                        qty = qty - 0.0001
                        sell_result = self.sell_coin(coin_name, loss_price, qty)
                    sell_id = sell_result['orderId']
                    sell_time = time.time()
                    is_loss = True
                    break

            # print(coin_name + "\trequest sell complete, sleep for 5 seconds for confirm")
            # time.sleep(5)

            # 판매 주문이 올라가지 않았으면 주문 취소 후 재시도
            while True:
                if self.trace_order(sell_id, coin_name)['status'] == 'filled':
                    # print(check_order)

                    complete_order = self.check_complete_order(coin_name)
                    sell_price = 0
                    heuristics_counter = 0
                    for data in complete_order['completeOrders']:
                        if data['orderId'] == sell_id:
                            sell_price += round((float(data['qty']) + float(data['fee'])) * float(data['price']), 2)
                            heuristics_counter += 1
                        if heuristics_counter == 4:
                            break

                    self.db_sell_coin(coin_name, loss_price, profit_price, sell_price, qty, is_loss)

                    end = True
                    break

                if time.time() - sell_time > 100:
                    if is_loss:
                        cancel_order = self.cancel_order(sell_id, coin_name, loss_price, qty, True)
                    else:
                        cancel_order = self.cancel_order(sell_id, coin_name, profit_price, qty, True)
                    end = False

            if end:
                timelog("order cycle of " + coin_name + " is complete" + " profit : ", str(not is_loss))
                break

    def trade(self):
        cur_coin_list = self.get_cur_buy_list()
        buy_list = self._get_coin_list(cur_coin_list)
        timelog("cur_coin_list : ", cur_coin_list)
        timelog("buy_list : ", buy_list)
        for coin in buy_list:
            buy_result = self.buy_coin(coin, buy_list[coin], constant.TRADE_ONECOIN_VAL / buy_list[coin])
            timelog(coin, buy_list[coin])

    def db_listener(self):
        timelog('Listener is listening Redis...')
        for data in self._event_checker.listen():
            # print(data)
            if data['data'] == b'lrem':  # lrem이 이루어질 때만 시도함.
                cur_coin_list = self.get_cur_buy_list()
                not_buy_list = self.get_not_buy_list()
                buy_expect_list = self._get_coin_list(cur_coin_list, not_buy_list)
                timelog("buy_expect_list : ", buy_expect_list)
                for coin in buy_expect_list:
                    # print(coin)
                    thread = threading.Thread(target=self._check_and_buy, args=(
                    coin, buy_expect_list[coin]), name=coin)
                    # process = Process(target=self._check_and_buy, args=(coin, buy_expect_list[coin], self.private_checktime, self.public_checktime), name=coin)
                    thread.start()  # 얘는 그냥 실행만 시키고 끝나야하는데...
                # print("end of lpop onecycle")       #


if __name__ == "__main__":
    test = Coinone()
    test.db_listener()
    # t = Process(target=test.trade_newver, args=())
    # t.start()
    # time.sleep(5)
    # test.heavy_load()
