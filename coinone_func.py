import json

import constant
import coinone_api



def get_balance():
    result = json.loads(coinone_api.get_response(coinone_api.LOGIN, {'access_token': coinone_api.ACCESS_TOKEN, }).decode())
    print(result)
    if result["errorCode"] != '0':
        print(result['result'])
        exit(1)
    print(result['ada'])

    trusted_coin = [coin.lower() for coin in constant.TRUST_COIN]
    trusted_result = {}
    for coin in trusted_coin:
        trusted_result[coin] = result[coin]
        trusted_result[coin]['avail'] = float(trusted_result[coin]['avail'])
        trusted_result[coin]['balance'] = float(trusted_result[coin]['balance'])
        trusted_result[coin]['jumooned'] = trusted_result[coin]['balance'] - trusted_result[coin]['avail']

    # trusted_result = {result[coin] for coin in trusted_coin}
    print(trusted_result)
    # trusted_result = [coin for coin in result]
    # print(trusted_coin)







if __name__ == "__main__":
    get_balance()
