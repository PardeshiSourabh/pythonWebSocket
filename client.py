import socket
import json
from simulate import simulate
import time

c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
c.connect((socket.gethostname(), 5050))
simulations = 0

while simulations < 5000:
    msg = json.dumps(simulate('BTC')).encode('utf-8')
    msg_len = len(msg)
    c.send(msg + b' ' * (4096 - msg_len))

    simulations += 1
    time.sleep(1)


