import re
import sys
import time

import requests
from flask import Flask, Response
from gevent import pywsgi

app = Flask(__name__)
app.debug = True
default_port = None
throughput = 0
bit_rates = [1000, 500, 100, 10]

@app.route('/<name>')
def index(name = None):
    if name == None:
        return 'Hello World'
    return Response(requests.get('http://127.0.0.1:8080/%s' % name))

@app.route('/vod/<name>')
def flash(name = None):
    global throughput
    bit_rate = 0
    if name == 'big_buck_bunny.f4m':
        name = '10.f4m'
    else:
        real_name = re.match('\d*(Seg.*)', name).group(1)
        for bit_rate in bit_rates:
            if bit_rate * 1.5 <= throughput:
                break
        name = str(bit_rate) + real_name
        print(name)
    
    port = int(request_dns())
    start = time.time()
    res = requests.get('http://127.0.0.1:%d/vod/%s' % (port, name))
    end = time.time()
    current_T = res.content.__len__() / (end - start)
    throughput = alpha * throughput + (1 - alpha) * current_T
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),  ' ', end - start, " ", current_T, " ", throughput, " ",
        bit_rate, " ", port, " ", name)
    return Response(res)

def request_dns():
    global default_port
    if default_port != None:
        return default_port
    return int(requests.get('http://127.0.0.1:%d/' % dns_port).content)

if __name__ == '__main__':
    argc = sys.argv.__len__()
    assert argc == 5 or argc == 6
    if argc == 6:
        default_port = sys.argv[5]
    log_file = sys.argv[1]
    alpha = float(sys.argv[2])
    listen_port = int(sys.argv[3])
    dns_port = int(sys.argv[4])
    server = pywsgi.WSGIServer(('0.0.0.0', listen_port), app)
    server.serve_forever()
