from itertools import product
import numpy as np

exchanges = ['binance', 'bitfinex', 'poloniex', 'kraken', 'bitmex', 'bitstamp', 'bitflyer', 'gemini', 'bittrex']
cryptos = {"BTC": [19122.00, 0.03474776796281548], "BCH": [296.35, 0.05596170339474446],
           "XRP": [0.633506, 0.04871884801238718], "LTC": [88.21, 0.03937180989491866],
           "LINK": [13.65, 0.06785578477344636], "ETH": [594.95, 0.06785578477344636],
           "EOS": [3.07, 0.07005437804082514], "DASH": [116.32, 0.07005437804082514],
           "XLM": [0.187249, 0.043658021474321206], "ADA": [0.16825, 0.043658021474321206],
           "DOT": [5.43654, 0.043658021474321206], "BNB": [31.18, 0.043658021474321206],
           "TRX": [0.0325, 0.043658021474321206], "XMR": [132.20, 0.030263488321165294],
           "XTZ": [2.39, 0.030263488321165294], "NEO": [18.035, 0.030263488321165294]}


def simulate(curr):
    """
        Generates a random json packet simulation for a crypto
    """

    result = []

    for crypto, exchange in list(product([curr], exchanges)):
        buy = cryptos[crypto][0] * (1 + np.random.normal(0, cryptos[crypto][1]))
        sell = cryptos[crypto][0] * (1 + np.random.normal(0, cryptos[crypto][1]))
        packet = {
            "id": crypto,
            "exchange": exchange,
            "buy_price": buy,
            "sell_price": sell
        }

        result.append(packet)

    return result
