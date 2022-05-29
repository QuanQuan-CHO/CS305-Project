from flask import Flask, Response, Request
import sys
from gevent import pywsgi
import time
import re
from util import strip_comments

app = Flask(__name__)
app.debug = True
servers = []
current_pos = 0


@app.route('/')
def find_port():
    global current_pos
    ret = servers[current_pos]
    current_pos += 1
    if current_pos == servers.__len__():
        current_pos = 0
    return str(ret)


if __name__ == '__main__':
    with open(sys.argv[1]) as file:
        for line in strip_comments(file):
            servers.append(int(line))
    server = pywsgi.WSGIServer(('0.0.0.0', int(sys.argv[2])), app)
    server.serve_forever()
