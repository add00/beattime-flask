# -*- coding: utf-8 -*-
from __future__ import unicode_literals

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
