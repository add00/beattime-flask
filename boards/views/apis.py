# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from flask import request
from flask.views import View

from beattime.mixins import ViewMixin
from boards.utils import get_user


class StickerAPI(ViewMixin, View):

    def dispatch_request(self):
        """
        Return stickers for logged in user.
        """
        profile = get_user(request.args)
        stickers = {
            sticker.sequence: {
                'status': sticker.label.status.value,
                'caption': sticker.caption,
                'description': sticker.description,
            }
            for sticker in profile.sticker_set
        }
        return json.dumps(stickers)
