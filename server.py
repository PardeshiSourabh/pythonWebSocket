import socket
import threading
import json
from get_spread import get_spread

'''
    Packet format: {
    'id': 'BTC',
    'exchange': bitfinex,
    'buy_price': '16054.56',
    'sell_price': '16092.72',
    }
'''

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((socket.gethostname(), 5050))


def handle_client(clientsocket, address):
    print(f"[NEW] {address} connected.")
    connected = True
    while connected:
        msg = clientsocket.recv(4096)
        data = json.loads(msg)
        print(get_spread('BTC', data))


def start():
    s.listen()
    while True:
        clientsocket, address = s.accept()
        print(f"Connection from {address} established.")
        thread = threading.Thread(target=handle_client, args=(clientsocket, address))
        thread.start()
        print(f"[ACTIVE CONNECTIONS]: {threading.activeCount() - 1}")


print("[STARTING SERVER ...]")
start()

