# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from wtforms.validators import Regexp

USERNAME_REGEX = Regexp(
    '^[A-Za-z][A-Za-z0-9_.]*$', 0,
    'Usernames must have only letters, numbers, dots or underscores'
)
