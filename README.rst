kucoin-lending-profit-report
============================
.. image:: https://img.shields.io/badge/python-3.6%2B-green
    :target: https://pypi.org/project/python-kucoin

Overview
--------

Generate a profit summary of all (or some) Kucoin asset lending activities, has option to dump all lending activities into a .CSV

Features
--------

-  Can specify only one asset to report on

-  Can dump all asset transactions into .CSV, for later scrutiny

-  Implementation of REST endpoints

Setup
-----

-  Generate a 'Trade' API in Kucoin

-  Store generated keys in your env under

   -  API_KEY,

   -  API_PASSPHRASE,

   -  API_SECRET

-  populate my_coins list with assets you want to report on, ie. my_coins = ['ETH', 'USDT']

-  alternatively leave my_coins empty ie. my_coins = [] to report on all assets

-  all reports (.CSV files) end up in cwd/pwd

-  IMPORTANT: slow_it_up_to_secs variable slows down the frequency of API calls, this is necessary, otherwise you will start getting 'Too many requests in a short period of time, please retry later'

Change Log
----------
+-------+-------------------------------------------------------------+
| 1.0.0 | -  Initial release                                          |
+-------+-------------------------------------------------------------+

