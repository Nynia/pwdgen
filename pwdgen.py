# -*- coding:utf8 -*-
from flask import Flask, request, make_response
import hashlib

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def wechat_auth():
    print 'hello world'
    if request.method == 'GET':
        token = 'cclove'
        signature = request.args.get('signature', '')
        timestamp = request.args.get('timestamp', '')
        nonce = request.args.get('nonce', '')
        echostr = request.args.get('echostr', '')
        s = [timestamp, nonce, token]
        s.sort()
        s = ''.join(s)
        print hashlib.sha1(s).hexdigest()
        if (hashlib.sha1(s).hexdigest() == signature):
            return make_response(echostr)