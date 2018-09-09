#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
from flask import Flask, request, abort
from datetime import datetime
from email.header import Header
from email.mime.text import MIMEText
import smtplib
import json
import traceback


app = Flask(__name__)


def get_mail_msg(event_time):
    message = MIMEText(
        u'您的12306订票帮手提醒您在{0}时有余票！'.format(event_time),
        'plain', 'utf-8')
    message['From'] = Header(app.config['SMTP']['sender-name'], 'utf-8')
    message['To'] = Header(app.config['SMTP']['receiver-name'], 'utf-8')

    message['Subject'] = Header(u'12306订票帮手邮件提醒', 'utf-8')
    return message.as_string()


@app.route('/notify', methods=['GET'])
def notify():
    timestamp = request.args.get('timestamp', type=int)
    if not timestamp:
        return abort(400)
    else:
        event_time = datetime.fromtimestamp(timestamp)
        datetime.ctime

        try:
            smtpobj = smtplib.SMTP(app.config['SMTP']['host'], app.config['SMTP']['port'])
            smtpobj.login(app.config['SMTP']['user'], app.config['SMTP']['pass'])
            senderrs = smtpobj.sendmail(
                app.config['SMTP']['sender'],
                app.config['SMTP']['receiver'],
                get_mail_msg(event_time)
            )
        except smtplib.SMTPException as e:
            print(traceback.format_exc())

        return json.dumps({
            u'senderrs': senderrs
        })


@app.after_request
def after_request(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


if __name__ == '__main__':
    app.config['DEBUG'] = True
    app.config['SMTP'] = {
        'host': 'smtp.qq.com',
        'port': 25,
        'user': 'user',
        'pass': 'password',
        'sender': 'foo@bar.com',
        'sender-name': u'昆金犒',
        'receiver': 'foo@bar.com',
        'receiver-name': u'昆金犒'
    }
    app.run(host='localhost', port=35528)
