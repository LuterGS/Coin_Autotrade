import redis
import time
from multiprocessing import Process

import constant


class DB:

    def __init__(self):
        get_db_val = constant.GET_DB_VALUE()
        self._username = "LuterGS"
        self._ip = get_db_val["ip"]
        self._port = int(get_db_val["port"])
        self._password = get_db_val["password"]
        self._db = redis.StrictRedis(host=self._ip, port=self._port, db=0, password=None)

        # queue initer
        self._check_main()

        # event notifier
        self._event_checker = self._db.pubsub()
        self._event_checker.psubscribe("__keyspace@0__:cur_buy_list")

        # print(self._db.get("LuterGS"))
    def _event_checker2(self):
        for data in self._event_checker.listen():
            print(data)

    def _check_main(self):
        if self._db.lrange("not_buy_list", 0, -1) is None:
            self._db.lpush("not_buy_list", "btc")
            self._db.lpop("not_buy_list")
        if self._db.lrange("cur_buy_list", 0, -1) is None:
            self._db.lpush("cur_buy_list", "1")
            self._db.lpop("cur_buy_list")

    def db_buy_coin(self, coin: str):
        self._db.lpush("cur_buy_list", coin)

    def db_sell_coin(self, coin: str, is_loss: bool):
        self._db.lrem("cur_buy_list", 1, coin)
        if is_loss:
            self.db_loss_coin(coin)

    def db_loss_coin(self, coin: str):
        db_value = self._db.get(coin)
        if db_value is None:
            self._db.set(coin, 1)
        if db_value == b'0':
            self._db.set(coin, 1)
        if db_value == b'1':
            self._db.rpush("not_buy_list", coin)
            print(coin + " falling twice. cooldown...")
            time.sleep(constant.TIME_COOLDOWN)
            self._db.lrem("not_buy_list", 1, coin)
            self._db.set(coin, 0)

    def get_not_buy_list(self):
        db_value = self._db.lrange("not_buy_list", 0, -1)
        db_value = [value.decode() for value in db_value]
        print(db_value)
        return db_value

    def get_cur_buy_list(self):
        db_value = self._db.lrange("cur_buy_list", 0, -1)
        db_value = [value.decode() for value in db_value]
        print(db_value)
        return db_value


if __name__ == "__main__":
    test = DB()
    test._event_checker2()
