# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os

from flask import Blueprint
from flask import Flask

from authentication import bp_authentication
from authentication.views import *
from authentication.urls import *
from beattime.config import config, db, auth_manager, email, bootstrap
from boards import (
    bp_api,
    bp_board, bp_board_user,
    bp_profile, bp_profile_user,
    bp_sprint, bp_sprint_user,
    bp_sticker, bp_sticker_user,
)
from boards.views import *
from boards.urls import *

beattime = Blueprint(
    'beattime', __name__, static_url_path='/static/beattime',
    static_folder=os.path.join('static', 'beattime')
)


def create_app(name):
    app = Flask(__name__)
    app.config.from_object(config[name])

    db.init_app(app)
    auth_manager.init_app(app)
    bootstrap.init_app(app)
    email.init_app(app)

    app.register_blueprint(bp_authentication)
    app.register_blueprint(bp_api, url_prefix='/api')
    app.register_blueprint(bp_board, url_prefix='/board')
    app.register_blueprint(bp_board_user, url_prefix='/user/<username>/board')
    app.register_blueprint(bp_sprint, url_prefix='/board/<sequence>/sprint')
    app.register_blueprint(
        bp_sprint_user, url_prefix='/user/<username>/board/<sequence>/sprint'
    )
    app.register_blueprint(bp_profile)
    app.register_blueprint(bp_profile_user, url_prefix='/user/<username>')
    app.register_blueprint(bp_sticker, url_prefix='/sticker')
    app.register_blueprint(
        bp_sticker_user, url_prefix='/user/<username>/sticker'
    )

    return app
