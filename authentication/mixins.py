# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from flask import render_template, redirect, url_for
from flask.ext.login import login_required, current_user

from authentication import DEFAULT_PAGE


class LoginRequiredMixin(object):
    """
    Mixin class to handle login required.
    """
    decorators = [login_required]


class FormMixin(object):
    """
    Mixin class forms specific.
    """
    form = None
    methods = ['GET', 'POST']

    def get(self):
        """
        Provide view's form to the template.
        """
        form = self.form() if self.form else None
        return render_template('auth.html', form=form)


class PasswordResetFormMixin(FormMixin):
    """
    Mixin class to check if user is anonymous.
    """

    def get(self, token=None):
        if not current_user.is_anonymous():
            return redirect(url_for(DEFAULT_PAGE))
        return super(PasswordResetFormMixin, self).get()
