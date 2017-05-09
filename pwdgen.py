# -*- coding:utf8 -*-
from flask import Flask, request, make_response
import hashlib,time
import xml.etree.ElementTree as ET
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def wechat_auth():
    if request.method == 'GET':
        token = 'cclove'
        signature = request.args.get('signature', '')
        timestamp = request.args.get('timestamp', '')
        nonce = request.args.get('nonce', '')
        echostr = request.args.get('echostr', '')
        s = [timestamp, nonce, token]
        s.sort()
        s = ''.join(s)
        print hashlib.sha1(s).hexdigest(),signature
        if (hashlib.sha1(s).hexdigest() == signature):
            print signature
            return make_response(echostr)
    else:
        rec = request.stream.read()
        xml_rec = ET.fromstring(rec)
        tou = xml_rec.find('ToUserName').text
        fromu = xml_rec.find('FromUserName').text
        content = xml_rec.find('Content').text
        xml_rep = "<xml><ToUserName><![CDATA[%s]]></ToUserName><FromUserName><![CDATA[%s]]></FromUserName><CreateTime>%s</CreateTime><MsgType><![CDATA[text]]></MsgType><Content><![CDATA[%s]]></Content><FuncFlag>0</FuncFlag></xml>"
        response = make_response(xml_rep % (fromu, tou, str(int(time.time())), content))
        response.content_type = 'application/xml'
        return response