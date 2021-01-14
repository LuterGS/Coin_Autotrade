import redis
import time
import datetime
from multiprocessing import Process

import constant
from else_func import timelog, datetime_to_str


class DB:

    def __init__(self):
        get_db_val = constant.GET_DB_VALUE()
        self._username = "coin_LuterGS"
        self._ip = get_db_val["ip"]
        self._port = int(get_db_val["port"])
        self._password = get_db_val["password"]
        self._db = redis.StrictRedis(host=self._ip, port=self._port, db=1, password=self._password)

        # key name init
        self._cur_buy_list = "coin_cur_buy_list"
        self._not_buy_list = "coin_not_buy_list"

        # event notifier
        self._event_checker = self._db.pubsub()
        self._event_checker.psubscribe("__keyspace@1__:" + self._cur_buy_list)

        # define buy, sell
        self._buy_dict = {
            "type": "buy",
            "coin": "coin",
            "price": "price",
            "qty": "qty",
            "total_price": "total_price"
        }
        self._sell_dict = {
            "type": "sell",
            "coin": "coin",
            "price": "price",
            "qty": "qty",
            "total_price": "total_price",
            "is_profit": "True"
        }


    def _event_checker2(self):
        for data in self._event_checker.listen():
            print(data)

    def _is_safe_coin(self, coin_list: str, coin: str):
        check = self._db.hget(coin_list, coin)
        if check is None or check == b'0':      # 이 코인은 한번도 손실을 입지 않은 경우
            return True
        elif check == b'1':                     # 이미 한번의 손실을 입은 경우
            return False

    def db_buy_coin(self, coin: str):
        self._db.rpush(self._cur_buy_list, coin)

    def db_buy_erase_coin(self, coin: str):
        self._db.lrem(self._cur_buy_list, 1, coin)

    def db_buy_confirm_coin(self, coin: str, price, qty, buy_price):
        cur_time = datetime_to_str(datetime.datetime.now())
        self._db.rpush(self._username, cur_time)        # coin_LuterGS에 넣음
        self._buy_dict["coin"] = coin
        self._buy_dict["price"] = price
        self._buy_dict["qty"] = qty
        self._buy_dict["total_price"] = buy_price
        self._db.hmset(self._username + "_" + cur_time, self._buy_dict)

    def db_sell_coin(self, coin: str, loss_price, profit_price, qty, sell_price, is_loss: bool):
        cur_time = datetime_to_str(datetime.datetime.now())
        self._db.rpush(self._username, cur_time)
        self._sell_dict["coin"] = coin
        self._sell_dict["price"] = loss_price if is_loss else profit_price
        self._sell_dict["qty"] = qty
        self._sell_dict["total_price"] = sell_price
        self._sell_dict["is_profit"] = str(not is_loss)
        self._db.hmset(self._username + "_" + cur_time, self._sell_dict)

        self._db.lrem(self._cur_buy_list, 1, coin)
        if is_loss:
            self._db_loss_coin(coin)

    def _db_loss_coin(self, coin: str):
        if self._is_safe_coin(self._not_buy_list, coin):
            self._db.hset(self._not_buy_list, coin, "1")
        else:
            self._db.hset(self._not_buy_list, coin, "2")
            timelog(coin + " is falling twice, will not buy for " + str(constant.TIME_COOLDOWN) + " seconds")
            time.sleep(constant.TIME_COOLDOWN)
            self._db.hset(self._not_buy_list, coin, "0")

    def get_not_buy_list(self):             # self._not_buy_list 중 값이 0~1인 것들만 return
        raw_dict = self._db.hgetall(self._not_buy_list)
        retr_list = []
        for data in raw_dict:
            if raw_dict[data] == b'2':
                retr_list.append(data.decode())
        return retr_list

    def get_cur_buy_list(self):
        db_value = self._db.lrange(self._cur_buy_list, 0, -1)
        db_value = [value.decode() for value in db_value]
        return db_value


if __name__ == "__main__":
    test = DB()

    print(test.get_not_buy_list())
