import requests
import base64
import time
import hmac
import hashlib
import pandas as pd
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

def call_kucookey(currency, currentpage, pagesize, credentials):
    url = 'https://api.kucoin.com'

    point = f'/api/v1/margin/lend/trade/settled?currency={currency}&currentPage={currentpage}&pageSize={pagesize}'
    call_type = 'GET'
    url = url + point

    now = int(time.time() * 1000)
    str_to_sign = str(now) + call_type + point
    signature = base64.b64encode(
        hmac.new(credentials[2].encode("utf-8"), str_to_sign.encode('utf-8'), hashlib.sha256).digest())
    passphrase = base64.b64encode(
        hmac.new(credentials[2].encode('utf-8'), credentials[1].encode('utf-8'), hashlib.sha256).digest())
    headers = {
        "KC-API-SIGN": signature,
        "KC-API-TIMESTAMP": str(now),
        "KC-API-KEY": credentials[0],
        "KC-API-PASSPHRASE": passphrase,
        "KC-API-KEY-VERSION": "2"
    }
    response = requests.request(call_type, url, headers=headers)
    if response.status_code == 403:
        print(
            f'HTTP response [{response.status_code}], {response.json()["msg"]}, if IP problem, use IP address associated with your API')
        exit(1)
    else:
        return response

def get_asset_list(credentials):
    api_key = credentials[0]
    api_passphrase = credentials[1]
    api_secret = credentials[2]
    url = 'https://api.kucoin.com'
    point = '/api/v1/accounts'
    call_type = 'GET'
    url = url + point

    now = int(time.time() * 1000)
    str_to_sign = str(now) + call_type + point
    signature = base64.b64encode(
        hmac.new(api_secret.encode("utf-8"), str_to_sign.encode('utf-8'), hashlib.sha256).digest())
    passphrase = base64.b64encode(
        hmac.new(api_secret.encode('utf-8'), api_passphrase.encode('utf-8'), hashlib.sha256).digest())
    headers = {
        "KC-API-SIGN": signature,
        "KC-API-TIMESTAMP": str(now),
        "KC-API-KEY": api_key,
        "KC-API-PASSPHRASE": passphrase,
        "KC-API-KEY-VERSION": "2"
    }
    response = requests.request(call_type, url, headers=headers)
    if response.status_code == 403:
        print(
            f'HTTP response [{response.status_code}], {response.json()["msg"]}, if IP problem, use IP address associated with your API')
        exit(1)
    temp = response.json()
    temp1 = pd.DataFrame(temp['data'])
    temp1.to_csv('accounts.csv')
    my_list = []

    for i in response.json()['data']:
        my_list.append(i['currency'])
    my_list = [*set(my_list)]
    return my_list


def get_last_price(coin, credentials):
    if coin == 'USDT':
        return 1
    api_key = credentials[0]
    api_passphrase = credentials[1]
    api_secret = credentials[2]
    url = 'https://api.kucoin.com'

    point = '/api/v1/market/orderbook/level1?symbol=' + coin + '-USDT'
    url = url + point
    call_type = 'GET'
    now = int(time.time() * 1000)
    str_to_sign = str(now) + call_type + point
    signature = base64.b64encode(
        hmac.new(api_secret.encode("utf-8"), str_to_sign.encode('utf-8'), hashlib.sha256).digest())
    passphrase = base64.b64encode(
        hmac.new(api_secret.encode('utf-8'), api_passphrase.encode('utf-8'), hashlib.sha256).digest())
    headers = {
        "KC-API-SIGN": signature,
        "KC-API-TIMESTAMP": str(now),
        "KC-API-KEY": api_key,
        "KC-API-PASSPHRASE": passphrase,
        "KC-API-KEY-VERSION": "2"
    }
    response = requests.request(call_type, url, headers=headers)

    temp = response.json()
    # print(response.json())
    if temp['data'] is None:
        return 0
    else:
        return temp['data']['bestBid']
