#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'Aurora Wu (wuxy91@gmail.com)'
__copyright__ = "Copyright (c) 2013- aurorawu.com"

import config
import json
import requests
from flask import Flask, jsonify, request as req
import hashlib
import tools

app = Flask(__name__)


@app.route("/")
def index():
    return "This is an index page!"


@app.route("/wx", methods=["GET"])
def validate_wx_dev_config():
    sign = req.args.get('signature')
    timestamp = req.args.get('timestamp')
    nonce = req.args.get('nonce')
    echostr = req.args.get('echostr')
    to_sort_list = [config.wx_my_token, timestamp, nonce]
    sha1 = hashlib.sha1()
    to_sort_list.sort()
    map(sha1.update, to_sort_list)
    hashcode = sha1.hexdigest()
    if sign == hashcode:
        return echostr
    else:
        return ''


@app.route("/wx", methods=["POST"])
def receive_wx_posted_xml():
    sign = req.args.get('signature')
    timestamp = req.args.get('timestamp')
    nonce = req.args.get('nonce')
    openid = req.args.get('openid')
    encrypt_type = req.args.get('encrypt_type')
    msg_signature = req.args.get('msg_signature')
    xml = req.get_data()
    print xml
    if encrypt_type == 'aes':
        xml = tools.decrypt_wx_xml_data(xml, msg_signature, timestamp, nonce)
    #return 'success'
    msg_model = tools.parse_xml(xml)
    if msg_model.msg_type == "text":
        reply = "your message is %s" % msg_model.content #Only support Text Message now!
    else:    
        reply = "your message type is not supported now!"
    ret_xml = tools.model2reply(msg_model, reply)
    # ret_xml = tools.model2xml(msg_model)
    print ret_xml
    if encrypt_type == 'aes':
        tools.encrypt_wx_xml_data(ret_xml, nonce)
    return ret_xml


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=config.port, debug=config.debug)
