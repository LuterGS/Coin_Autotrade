import os


KEY_FILE_LOC = "key.txt"            # Access Key, Secret Key의 위치입니다.
# 저 파일은 다음과 같은 구조로 되어있습니다.
"""
Access_Token='발급받은 Access Token값'
Secret_Key='발급받은 Secret Key'
"""

DB_FILE_LOC = "DB_VALUE.txt"
# 저 파일은 다음과 같은 구조로 되어있습니다.
"""
ip=127.0.0.1
port=1234
password=foo_bar
"""


TRADE_COIN_NUM = 3          # 거래할 코인 수
TRADE_ONECOIN_VAL = 10000.0     # 각 코인의 구매량. 끝에 .0 붙여서 float형으로 해야 함

PROFIT_PERCENT = 3.         # 이득 퍼센트. 해당 퍼센트를 넘게 이득보면 매도
LOSS_PERCENT = 1.           # 손실 퍼센트. 해당 퍼센트를 넘게 손해보면 매도

TIME_COOLDOWN = 3600        # 같은 코인을 두 번 손해봤을 때, 한 시간동안 해당 코인은 구매하지 않음

FALLING_RATIO = 2           # 거래 코인 판별시, 매도물량 총합 대 매수물량 총합이 해당 비율을 넘어가면 해당 코인은 거래하지 않음


# ====================== 이 아래는 건들지 말 것 =========================


_PATH = os.path.dirname(os.path.abspath(__file__)) + "/"


def GET_DB_VALUE():
    return_val = {}
    with open(_PATH + "DB_VALUE.txt", "r", encoding="utf8") as mqfile:
        for line in mqfile:
            line = line.replace("\n", "").split("=")
            return_val[line[0]] = line[1]
    return return_val