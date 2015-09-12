# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os

from flask import Blueprint

BP_KWARGS = {
    'template_folder': 'templates',
    'static_url_path': '/static/boards',
    'static_folder': os.path.join('static', 'boards')
}
bp_api = Blueprint('bp_api', __name__, **BP_KWARGS)
bp_board = Blueprint('bp_board', __name__, **BP_KWARGS)
bp_board_user = Blueprint('bp_board_user', __name__, **BP_KWARGS)
bp_profile = Blueprint('bp_profile', __name__, **BP_KWARGS)
bp_profile_user = Blueprint('bp_profile_user', __name__, **BP_KWARGS)
bp_sprint = Blueprint('bp_sprint', __name__, **BP_KWARGS)
bp_sprint_user = Blueprint('bp_sprint_user', __name__, **BP_KWARGS)
bp_sticker = Blueprint('bp_sticker', __name__, **BP_KWARGS)
bp_sticker_user = Blueprint('bp_sticker_user', __name__, **BP_KWARGS)

OPEN = 'OPEN'
IN_PROGRESS = 'PROGRESS'
IN_REVIEW = 'REVIEW'
DONE = 'DONE'
BLOCKED = 'BLOCKED'
TASK_STATUS = (
    (OPEN, OPEN),
    (IN_PROGRESS, IN_PROGRESS),
    (IN_REVIEW, IN_REVIEW),
    (DONE, DONE),
    (BLOCKED, BLOCKED),
)

DETAIL = 'DETAIL'
DELETE = 'DELETE'
CREATE = 'CREATE'
LIST = 'LIST'
UPDATE = 'UPDATE'
ACTION = (
    (DETAIL, DETAIL),
    (DELETE, DELETE),
    (CREATE, CREATE),
    (LIST, LIST),
    (UPDATE, UPDATE),
)

CSS_CLASS = (
    (OPEN, 'bg-todo'),
    (IN_PROGRESS, 'bg-inprogress'),
    (IN_REVIEW, 'bg-inreview'),
    (DONE, 'bg-done'),
    (BLOCKED, 'bg-blocked')
)
