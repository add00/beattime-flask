# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from flask import abort
from flask.ext.login import current_user

from profiles import FORBIDDEN_USERNAMES
from profiles.models import Profile


def get_user(view_args):
    """
    Return user basing on request.
    """
    username = view_args.get('username')
    if username in FORBIDDEN_USERNAMES:
        abort(404)
    elif username:
        user = Profile.query.filter_by(username=username).first()
        if not user:
            abort(404)
        return user
    return current_user
