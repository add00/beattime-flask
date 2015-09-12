# -*- coding: utf-8 -*-
from __future__ import unicode_literals


class MultipleObjects(Exception):
    """
    Exception raised when single object is expected to be returned.
    """
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return repr(self.msg)
