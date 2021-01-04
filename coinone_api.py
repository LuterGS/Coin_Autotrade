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

import coinone_func
import constant

LOGIN = 'https://api.coinone.co.kr/v2/account/balance'


def get_key():
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


ACCESS_TOKEN, SECRET_KEY = get_key()


def get_encoded_payload(payload):
    payload['nonce'] = int(time.time() * 1000)

    dumped_json = json.dumps(payload)
    print("dumped", dumped_json)
    encoded_json = base64.b64encode(bytes(dumped_json, 'utf-8'))
    return encoded_json


def get_signature(encoded_payload):
    signature = hmac.new(SECRET_KEY, encoded_payload, hashlib.sha512)
    return signature.hexdigest()


def get_response(url, payload):

    encoded_payload = get_encoded_payload(payload)
    print(encoded_payload)

    headers = {
        'Content-type': 'application/json',
        'X-COINONE-PAYLOAD': encoded_payload,
        'X-COINONE-SIGNATURE': get_signature(encoded_payload),
    }

    http = httplib2.Http()
    response, content = http.request(url, 'POST', body=encoded_payload, headers=headers)

    return content


if __name__ == "__main__":
    print(get_response(action='v2/account/balance', payload={
        'access_token': ACCESS_TOKEN,
    }))
