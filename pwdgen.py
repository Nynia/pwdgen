# -*- coding:utf8 -*-
from flask import Flask, request, make_response
import hashlib, time
import urllib
import urllib2
import json
import xml.etree.ElementTree as ET

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def wechat_auth():
    if request.method == 'GET':
        token = 'cclove'
        qurey = request.args
        signature = qurey.get('signature', '')
        timestamp = qurey.get('timestamp', '')
        nonce = qurey.get('nonce', '')
        echostr = qurey.get('echostr', '')
        s = [timestamp, nonce, token]
        s.sort()
        s = ''.join(s)
        if (hashlib.sha1(s).hexdigest() == signature):
            return make_response(echostr)
    else:
        rec = request.stream.read()
        xml_rec = ET.fromstring(rec)
        touser = xml_rec.find('ToUserName').text
        fromuser = xml_rec.find('FromUserName').text
        content = xml_rec.find('Content').text
        print [touser,fromuser,content]
        print sumof(fromuser+touser)
        password = gen_password(hashlib.sha1(content+touser).hexdigest(),sumof(fromuser))
        print password
        xml_rep = '''<xml>
            <ToUserName><![CDATA[%s]]></ToUserName>
            <FromUserName><![CDATA[%s]]></FromUserName>
            <CreateTime>%s</CreateTime>
            <MsgType><![CDATA[text]]></MsgType>
            <Content><![CDATA[%s]]></Content>
            <FuncFlag>0</FuncFlag>
            </xml>
        '''
        print password
        response = make_response(xml_rep % (fromuser, touser, str(int(time.time())), password))
        response.content_type = 'application/xml'
        return response


def get_access_token():
    url = 'https://api.weixin.qq.com/cgi-bin/token'
    payload = {
        'grant_type': 'client_credential',
        'appid': 'wx0c3b0b616cc6e6f7',
        'secret': 'b581d3bb9f90737ce1322da5bd79699b'
    }

    data = urllib.urlencode(payload)
    req = urllib2.Request(url, data)
    response = urllib2.urlopen(req)
    result = json.loads(response.read())
    return result.get('access_token')


def gen_password(str, openid):
    alpha = []
    for i in xrange(48, 58):
        alpha.append(chr(i))
    for i in xrange(65, 91):
        alpha.append((chr(i)))
    for i in xrange(97, 123):
        alpha.append((chr(i)))
    for i in ['!', '@', '#', '$', '^', '&', '*']:
        alpha.append(i)
    seq = ''.join(['{:0=8b}'.format(ord(i)) for i in str]).lstrip('0')
    i = 0
    result = ''
    j = i+1
    while j < len(seq):
        slice = seq[i:j]
        slice_int = int(slice, base=2)
        if slice_int >= alpha.index('a') and slice_int <= alpha.index('z'):
            result += alpha[slice_int]
            break
        j += 1
        if slice_int > alpha.index('z'):
            i = i+1
            j = i+1
    i = j
    j = i+1
    while j < len(seq):
        slice = seq[i:j]
        slice_int = int(slice, base=2)
        if slice_int >= alpha.index('0') and slice_int <= alpha.index('9'):
            result += alpha[slice_int]
            break
        j += 1
        if slice_int > alpha.index('z'):
            i = i+1
            j = i+1
    i = j
    j = i + 1
    while j < len(seq):
        slice = seq[i:j]
        slice_int = int(slice, base=2)
        if slice_int >= alpha.index('A') and slice_int <= alpha.index('Z'):
            result += alpha[slice_int]
            break
        j += 1
        if slice_int > alpha.index('z'):
            i = i+1
            j = i+1
    i = j
    j = i + 1
    while j < len(seq):
        slice = seq[i:j]
        slice_int = int(slice, base=2)
        if slice_int >= alpha.index('!') and slice_int <= alpha.index('*'):
            result += alpha[slice_int]
            break
        j += 1
        if slice_int > alpha.index('z'):
            i = i+1
            j = i+1
    i = j
    j = i + 1
    while j < len(seq):
        slice = seq[i:j]
        slice_int = int(slice, base=2)
        if slice_int >= alpha.index('0') and slice_int <= alpha.index('9'):
            result += alpha[slice_int]
            break
        j += 1
        if slice_int > alpha.index('z'):
            i = i+1
            j = i+1
    i = j
    j = i + 1
    while j < len(seq):
        slice = seq[i:j]
        slice_int = int(slice, base=2)
        if slice_int >= alpha.index('a') and slice_int <= alpha.index('z'):
            result += alpha[slice_int]
            break
        j += 1
        if slice_int > alpha.index('z'):
            i = i+1
            j = i+1
    permutation_list = []
    gen_permutation('123456', '', permutation_list)
    residual = openid % 64
    print result,residual
    return ''.join([result[int(i)-1] for i in permutation_list[residual]])

def gen_permutation(s1,s2,result):
    if len(s1) == 1:
        result.append(str(s1)+str(s2))
    else:
        for i in s1:
            tmp_list = list(s1[:])
            tmp_list.remove(i)
            gen_permutation(''.join(tmp_list),s2+i,result)

def sumof(str):
    result = 0
    for i in str:
        result += ord(i)
    return result
