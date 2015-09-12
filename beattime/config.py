# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os

from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.bootstrap import Bootstrap
from flask.ext.login import LoginManager
from flask.ext.mail import Mail

basedir = os.path.abspath(os.path.dirname(__file__))
db = SQLAlchemy()
bootstrap = Bootstrap()
auth_manager = LoginManager()
auth_manager.session_protection = 'strong'
auth_manager.login_view = 'bp_authentication.login'
email = Mail()


class Config:
    SECRET_KEY = 'YOU WONT GUESS'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    TOKEN_EXPIRATION = 3600
    MAIL_SENDER = 'test@test.com'
    DEFAULT_PAGE = 'bp_profile.profile-detail'
    UPLOAD_FOLDER = 'beattime/static/beattime/img/avatars'
    ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])


class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = (
        'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')
    )


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = (
        'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')
    )


config = {
    'dev': DevConfig,
    'test': TestConfig,
    'default': DevConfig
}
