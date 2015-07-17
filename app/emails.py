#! /usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'Jack Bai'

from flask import current_app, render_template
from flask.ext.mail import Message
from . import mail
from threading import Thread


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(to, subject, template, **kw):
    app = current_app._get_current_object()
    msg = Message(app.config['MYBLOG_MAIL_SUBJECT_PREFIX'] + ' ' + subject, 
        sender=app.config['MYBLOG_MAIL_SENDER'], recipients=[to])
    msg.body = render_template(template + '.txt', **kw)
    msg.html = render_template(template + '.html', **kw)
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr
