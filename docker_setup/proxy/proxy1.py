import re
import sys
import time
from xml.dom import minidom

import requests
from flask import Flask, Response, request, session, redirect, render_template, url_for
from gevent import pywsgi

app = Flask(__name__)
app.debug = True
default_port = None
throughput = 0
bit_rates = []
danmaku_list = []
comment_list = []
danmakus = ''
comments = ''

app.secret_key = 'fkdjsafjdkfdlkjfadskjfadskljdsfklj'
file = open('output.txt', 'w')


@app.route('/<name>')
def index(name):
    if 'username' not in session:
        return redirect(url_for('login'))
    if len(request.args) > 0:
        global danmakus, comments
        method = request.args.get('method')
        if method == 'get_danmaku':
            return danmakus
        elif method == 'get_comment':
            return comments
        username = request.args.get('username')
        content = request.args.get('content')
        if method == 'comment':
            time = request.args.get('time')
            comment_list.append(username + '-' + content + '-' + time)
            comments = '&'.join(comment_list)
        elif method == 'danmaku':
            danmaku_list.append(content)
            danmakus = '&'.join(danmaku_list)
        elif method == 'get_username':
            if 'username' in session:
                return session['username']
    return Response(requests.get('http://127.0.0.1:8080/%s' % name))


@app.route('/close')
def close_server():
    server.stop()
    sys.exit(0)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('index', name='index.html'))
    return render_template('login.html')


@app.route('/logout')
def logout():
    # remove the username from the session if it is there
    session.pop('username', None)
    return redirect(url_for('login'))


@app.route('/vod/<name>')
def flash(name=None):
    global throughput, file, bit_rates
    bit_rate = 0
    if name == 'big_buck_bunny.f4m':
        port = int(request_dns())
        text = requests.get('http://127.0.0.1:%d/vod/%s' % (port, name)).text
        bit_rates = get_bitrate(text)
        bit_rates.sort()
        bit_rates.reverse()
        name = '10.f4m'
    else:
        real_name = re.match('\d*(Seg.*)', name).group(1)
        for bitrate in bit_rates:
            if bitrate * 1.5 <= throughput:
                bit_rate = bitrate
                break
        name = str(bit_rate) + real_name
        print(name)

    port = int(request_dns())
    start = time.time()
    res = requests.get('http://127.0.0.1:%d/vod/%s' % (port, name))
    end = time.time()
    T_new = len(res.content) / (end - start) / 1000
    throughput = alpha * T_new + (1 - alpha) * throughput
    out = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ' ' + str(end - start) + ' ' + str(
        T_new) + ' ' + str(throughput) + ' ' + str(bit_rate) + ' ' + str(port) + ' ' + name
    file.write(out)
    file.flush()
    print(out)
    return Response(res)


def request_dns():
    global default_port
    if default_port != None:
        return default_port
    return int(requests.get('http://127.0.0.1:%d/' % dns_port).content)


def get_bitrate(xml_str):
    # DOMTree = minidom.parse("../www/vod/big_buck_bunny.f4m")
    DOMTree = minidom.parseString(xml_str)
    data = DOMTree.documentElement
    medias = data.getElementsByTagName('media')
    bitrates = []
    for m in medias:
        if m.hasAttribute("bitrate"):
            bitrates.append(int(m.getAttribute("bitrate")))
    return bitrates


if __name__ == '__main__':
    # bit_rates = get_bitrate()
    argc = sys.argv.__len__()
    assert argc == 5 or argc == 6
    if argc == 6:
        default_port = sys.argv[5]
    log_file = sys.argv[1]
    file = open(log_file, 'w')
    alpha = float(sys.argv[2])
    listen_port = int(sys.argv[3])
    dns_port = int(sys.argv[4])
    server = pywsgi.WSGIServer(('0.0.0.0', listen_port), app)
    server.serve_forever()
