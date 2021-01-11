import os


KEY_FILE_LOC = "key.txt"            # Access Key, Secret Key의 위치입니다.
# 저 파일은 다음과 같은 구조로 되어있습니다.
"""
Access_Token='발급받은 Access Token값'
Secret_Key='발급받은 Secret Key'
"""


TRADE_COIN_NUM = 2
TRADE_ONECOIN_VAL = 10000.0

PROFIT_PERCENT = 3.
LOSS_PERCENT = 1.

TIME_COOLDOWN = 3600

FALLING_RATIO = 2


# ====================== 이 아래는 건들지 말 것 =========================


_PATH = os.path.dirname(os.path.abspath(__file__)) + "/"


def GET_DB_VALUE():
    return_val = {}
    with open(_PATH + "DB_VALUE.txt", "r", encoding="utf8") as mqfile:
        for line in mqfile:
            line = line.replace("\n", "").split("=")
            return_val[line[0]] = line[1]
    return return_val