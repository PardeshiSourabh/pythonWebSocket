import pandas as pd
import datetime
import socket
import threading
import pickle


margin_exchanges = ["binance", "bitflyer", "bitfinex", "kraken", "poloniex", "bitmex"]
records = pd.DataFrame(columns=['timestamp', 'curr_base', 'buy_exc', 'sell_exc',
                                'buy_price_b1', 'sell_price_a2', 'a1', 'b2',
                                'profit_usdt', 'pct_return', 't', 'buy_vol24h_base',
                                'sell_vol24h_base', 'profitable'])


def get_record(curr, quotes):
    # Filter out the quote information from our selected list of exchanges (per Crypto)
    bid_asks = {x['exchange']: [x['buy_price'], x['sell_price']] for x in quotes}
    # Buy lowest, Sell highest
    buy_from, sell_to = min(bid_asks, key=bid_asks.get), max(bid_asks, key=bid_asks.get)
    # Bx, Ax: Bid from exchange x, Ask for exchange x
    b1, a1, b2, a2 = bid_asks[buy_from][0], bid_asks[buy_from][1], bid_asks[sell_to][0], bid_asks[sell_to][1]

    # If spread is mutually exclusive
    if b2 > a1 and sell_to in margin_exchanges:
        # Transaction cost overhead
        t = 0.001 * (a1 + b2)
        # Profit including deducted transaction costs
        profit = b2 - a1 - t
        now = datetime.datetime.now()
        # Since we have all scalars, we use the df.from_records() method, to statically add
        # these values to global DataFrame.
        # Tod add to HashMap<TimeObject, Float, ..., Boolean> add everything statically using the appropriate variables.
        rec = pd.DataFrame.from_records([{'timestamp': now, 'curr_base': curr, 'buy_exc': buy_from,
                                          'sell_exc': sell_to, 'buy_price_b1': b1, 'sell_price_a2': a2,
                                          'a1': a1, 'b2': b2, 't': t,
                                          'profit_usdt': profit, 'pct_return': ((b2 - a1 - t) / a1) * 100,
                                          'buy_vol24h_base': bid_asks[buy_from][2],
                                          'sell_vol24h_base': bid_asks[sell_to][2],
                                          'profitable': True if profit > 0 else False}])
        return rec
    else:
        return pd.DataFrame.from_records([{'profitable': False}])


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((socket.gethostname(), 5050))


def handle_client(clientsocket, address):
    print(f"[NEW] {address} connected.")
    connected = True
    while connected:
        msg = clientsocket.recv(4096)
        data = pickle.load(msg)
        # Simulate exchange price report back here and send it back to the server


def start():
    s.listen()
    while True:
        clientsocket, address = s.accept()
        print(f"Connection from {address} established.")
        thread = threading.Thread(target=handle_client, args=(clientsocket, address))
        thread.start()
        print(f"[ACTIVE CONNECTIONS]: {threading.activeCount() - 1}")


print("STARTING EXCHANGE SERVER")
start()

