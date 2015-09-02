# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from threading import Thread
from flask import current_app
from flask.ext.mail import Message
from beattime.config import email


def send_async_email(app, message):
    """
    Send an email message.
    """
    with app.app_context():
        email.send(message)


def send_email(subject, user, body):
    """
    Prepare and provide an email to send.
    """
    app = current_app._get_current_object()
    if app.config['DEBUG']:
        print body
        return
    message = Message(
        recipients=[user.email], subject=subject, body=body,
        sender=app.config['MAIL_SENDER']
    )
    thread = Thread(target=send_async_email, args=[app, message])
    thread.start()
    return thread
