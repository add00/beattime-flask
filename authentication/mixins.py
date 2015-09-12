# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from flask import current_app, render_template, redirect, url_for
from flask.ext.login import login_required, current_user


class LoginRequiredMixin(object):
    """
    Mixin class to handle login required.
    """
    decorators = [login_required]


class FormMixin(object):
    """
    Mixin class forms specific.
    """
    form_class = None
    methods = ['GET', 'POST']
    exclude_fields = None

    def get_form(self):
        """
        Return form.
        """
        form = self.form_class() if self.form_class else None
        if form and self.exclude_fields:
            for field_name in self.exclude_fields:
                del form[field_name]
        return form

    def get(self):
        """
        Provide view's form to the template.
        """
        form = self.get_form()
        return render_template('auth.html', form=form)


class PasswordResetFormMixin(FormMixin):
    """
    Mixin class to check if user is anonymous.
    """

    def get(self, token=None):
        if not current_user.is_anonymous():
            return redirect(url_for(current_app.config['DEFAULT_PAGE']))
        return super(PasswordResetFormMixin, self).get()
