import os
import pandas as pd
import random
import time
from datetime import datetime
from externalcall import call_kucookey, get_asset_list, get_last_price

#{'code': '200002', 'msg': 'Too many requests in a short period of time, please retry later'}

sum_dict = {}
# my_coins = ['ETH', 'USDT']
my_coins = []            #assets in this list will be th only ones that will be reported on
dump_lend_hist = True    #save all lending transations to a .CSV
slow_it_up_to_secs = 60  #needed to slowdown that KC calls, otherwise you'll start getting 'Too many requests in a short period of time, please retry later'

api_key = os.environ.get("API_KEY")
api_passphrase = os.environ.get("API_PASSPHRASE")
api_secret = os.environ.get("API_SECRET")
credentials = [api_key, api_passphrase, api_secret]
if not my_coins:
    my_coins = get_asset_list(credentials)

if not my_coins:
    print('nothing to process')
    exit(0)

for coin in my_coins:
    print(f'processing {coin}')
    response = call_kucookey(coin, 1, 1, credentials) #get number of rows to decide how many pages to ask for
    # print(response.json())
    temp = response.json()
    if temp['data']['totalNum'] == 0:
        print(f'no lending history for {coin}')
        continue
    initial_call = pd.DataFrame(temp['data'])
    total_nbr_of_rows = int(initial_call["totalNum"])

    total_nbr_of_pages = int(total_nbr_of_rows / 50) + 1

    final_set = pd.DataFrame()
    for i in range(1, total_nbr_of_pages + 1):
        print(f' getting page {i} of {total_nbr_of_pages}')
        response = call_kucookey(coin, i, 50, credentials)
        temp = response.json()
        # print(temp)
        temp1 = pd.DataFrame(temp['data'])
        final_set = final_set.append(temp1)
        time.sleep(random.randint(10, slow_it_up_to_secs))
    if dump_lend_hist:
        final_set.to_csv(f'{coin}_all_lend_transactions.csv')

    size = 0.0
    repaid = 0.0
    interest = 0.0

    earliest_date = 9968291874766
    latest_date = 0

    for index, row in final_set.iterrows():
        size += float(row['items']['size'])
        repaid += float(row['items']['repaid'])
        interest += float(row['items']['interest'])
        if row['items']['settledAt'] > latest_date:
            latest_date = row['items']['settledAt']
        if row['items']['settledAt'] < earliest_date:
            earliest_date = row['items']['settledAt']

    earliest_date = datetime.fromtimestamp(earliest_date / 1000).strftime("%d/%m/%Y %I:%M:%S")
    latest_date = datetime.fromtimestamp(latest_date / 1000).strftime("%d/%m/%Y %I:%M:%S")
    curr_USDT_price = get_last_price(coin, credentials)
    if curr_USDT_price == 0:
        profit_in_USDT = 'unable to get exchange rate'
    else:
        profit_in_USDT = float(curr_USDT_price) * float(interest)

    data = {
        "size": size,
        "repaid": repaid,
        "interest": interest,
        "from": earliest_date,
        "to": latest_date,
        "profit USDT": profit_in_USDT,
        "curr USDT price": curr_USDT_price
    }
    sum_dict[coin] = data
    temp_df = pd.DataFrame(sum_dict)
    temp_df = temp_df.T
    temp_df = temp_df[['size', 'repaid', 'interest', 'from', 'to', 'profit USDT', 'curr USDT price']]

    temp_df.to_csv('lending_summary.csv')


