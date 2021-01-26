from requests import Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import time, datetime, json
import pandas as pd

url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/market-pairs/latest'

headers = {
    'Accepts': 'application/json',
    'Accept-Encoding': 'deflate, gzip',
    'X-CMC_PRO_API_KEY': 'c4b9fd33-b7b5-498f-8982-bffd7e051eb9'
}

exchanges = ['binance', 'bitfinex', 'poloniex', 'kraken', 'bitmex',
             'bitstamp', 'bitflyer', 'gemini', 'bittrex']
cryptos = ["BTC", "BCH", "XRP", "LTC", "LINK", "ETH", "EOS", "DASH", "XLM", "ADA", "DOT", "BNB", "TRX", "XMR",
           "XTZ", "NEO"]

session = Session()
session.headers.update(headers)
records = pd.DataFrame(columns=['timestamp', 'currency', 'buy_exc', 'sell_exc',
                                'buy_price_b1', 'sell_price_a2', 'a1', 'b2',
                                'profit_usdt', 'pct_return', 'buy_volume_24h_base',
                                'sell_volume_24h_base', 'profitable'])


def get_record(curr, quotes):
    bid_asks = {x['exchange']['name']: [x['quote']['exchange_reported']['price'], x['quote']['USD']['price'],
                                        x['quote']['exchange_reported']['volume_24h_base']] for x in quotes}

    buy_from, sell_to = min(bid_asks, key=bid_asks.get), max(bid_asks, key=bid_asks.get)
    b1, a1, b2, a2 = bid_asks[buy_from][0], bid_asks[buy_from][1], bid_asks[sell_to][0], bid_asks[sell_to][1]
    t = 0.001 * (a1 + b2)
    profit = b2 - a1 - t
    now = datetime.datetime.now()
    rec = pd.DataFrame.from_records([{'timestamp': now, 'currency': curr, 'buy_exc': buy_from,
                                      'sell_exc': sell_to, 'buy_price_b1': b1, 'sell_price_a2': a2,
                                      'a1': a1, 'b2': b2,
                                      'profit_usdt': profit, 'pct_return': ((b2 - a1 - t) / a1) * 100,
                                      'buy_volume_24h_base': bid_asks[buy_from][2],
                                      'sell_volume_24h_base': bid_asks[sell_to][2],
                                      'profitable': True if profit > 0 else False}])
    return rec


sims = 0

while sims < 700:

    for crypto in cryptos:

        parameters = {
            'symbol': crypto,
            'matched_symbol': 'USDT'
        }

        try:
            response = session.get(url, params=parameters)
            data = json.loads(response.text)
            filtered_quotes = list(filter(lambda x: x['exchange']['slug'] in exchanges,
                                          data['data']['market_pairs']))
            record = get_record(crypto, filtered_quotes)
            records = pd.concat([records, record])
            print(records.tail(14))
            sims += 1
            time.sleep(10)

        except (ConnectionError, Timeout, TooManyRedirects) as e:
            print(e)

'''
    Optimal Transaction Value: F(Depth(BA_Buy) and Depth(BA_Sell)) -> Balanced ? Min: 
    Coins to add: [WBTC, NEM] -> Not Supported by CoinMarketCap
    Try and Catch block for unsupported currencies
'''
