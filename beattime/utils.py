# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
from datetime import datetime

from flask import current_app


def register_patterns(blueprint, rules):
    for view, url, name in rules:
        blueprint.add_url_rule(url, view_func=view.as_view(str(name)))


def is_allowed_file_format(filename):
    """
    Check whether file format is allowed.
    """
    return (
        '.' in filename and filename.rsplit('.', 1)[-1]
        in current_app.config['ALLOWED_EXTENSIONS']
    )


def handle_avatar(_file, profile):
    filename = '{}_{}.{}'.format(
        profile.username, datetime.now(),
        _file.filename.split('.', 1)[-1]
    )
    _file.save(
        os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
    )
    return filename
