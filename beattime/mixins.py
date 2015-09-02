# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from beattime.config import db


class PKMixin(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)


class ContextMixin(object):
    """
    Mixin class to pass kwargs and other extra data to context.
    """
    action = None

    def context_data(self):
        """
        Return common context data.
        """
        context = {'action': self.action}
        return context
