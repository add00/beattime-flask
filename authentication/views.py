# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from flask import (
    current_app, flash, render_template, redirect, request, url_for
)
from flask.ext.login import (
    current_user, login_user, logout_user
)
from flask.views import MethodView

from authentication.forms import (
    LoginForm, RegistrationForm, ChangePasswordForm, PasswordResetForm,
    PasswordResetDoneForm
)
from authentication.mixins import (
    FormMixin, LoginRequiredMixin, PasswordResetFormMixin
)
from beattime.config import db
from beattime.email import send_email
from beattime.utils import is_allowed_file_format, handle_avatar
from boards.models import Desk
from profiles.models import Profile

LOGIN_PAGE = 'bp_authentication.login'


class LoginView(FormMixin, MethodView):
    """
    Login functionality view.
    """
    form_class = LoginForm

    def _on_success(self, user):
        """
        Log user when form validation passes.
        """
        login_user(user)

    def _on_error(self):
        """
        Show validation error.
        """
        flash(
            'Please enter a correct username and password. Note that both'
            'fields may be case-sensitive.'
        )

    def post(self):
        form = self.form_class()
        if form.validate_on_submit():
            username = form.username.data
            user = Profile.query.filter_by(username=username).first()
            if user and user.verify_password(form.password.data):
                self._on_success(user)
                return redirect(
                    request.args.get('next') or
                    url_for(current_app.config['DEFAULT_PAGE'])
                )
            self._on_error()
        return render_template('auth.html', form=form)


class LogoutView(LoginRequiredMixin, MethodView):
    """
    Logout functionality view.
    """

    def get(self):
        logout_user()
        return redirect(url_for(LOGIN_PAGE))


class RegistrationView(FormMixin, MethodView):
    """
    Registration functionality view.
    """
    form_class = RegistrationForm
    exclude_fields = ['friends']

    def _handle_avatar(self, user):
        """
        Append avatar if uploaded.
        """
        _file = request.files['avatar']
        if _file and is_allowed_file_format(_file.filename):
            filename = handle_avatar(_file, user)
            user.avatar = filename

    def _create_user(self, form):
        """
        Create user basing on form's data.
        """
        user = Profile(
            email=form.email.data,
            username=form.username.data,
            password=form.password.data,
            display_name=form.display_name.data,
            motivation_quote=form.motivation_quote.data,
        )
        db.session.add(user)
        self._handle_avatar(user)
        db.session.commit()
        desk = Desk(
            author=user.id, owner_id=user.id, desk_slug=user.username[:5]
        )
        db.session.add(desk)
        db.session.commit()

    def _validate_user(self, form):
        """
        Validates if user already exists.
        """
        is_valid = True
        if Profile.query.filter_by(username=form.username.data).scalar():
            form.username.errors.append('Username already taken')
            is_valid = False
        if Profile.query.filter_by(email=form.email.data).scalar():
            form.email.errors.append('Email already taken')
            is_valid = False

        return form, is_valid

    def post(self):
        """
        Handles POST.
        """
        form = self.get_form()
        if form.validate_on_submit():
            form, is_valid = self._validate_user(form)
            if is_valid:
                self._create_user(form)
                return redirect(url_for(LOGIN_PAGE))
        return render_template('auth.html', form=form)


class ChangePasswordView(LoginRequiredMixin, FormMixin, MethodView):
    """
    Change Password functionality view.
    """
    form_class = ChangePasswordForm

    def _verify_password(self, form):
        """
        Check if user has provided correct current password.
        """
        return current_user.verify_password(form.old_password.data)

    def _passwords_match(self, form):
        """
        Check if user has provided the same new password for two inputs.
        """
        return form.new_password.data == form.new_password_confirm.data

    def _append_errors(self, form, verify_password, passwords_match):
        """
        Append validation errors.
        """
        if not verify_password:
            form.old_password.errors.append(
                'Your old password was entered incorrectly. '
                'Please enter it again.'
            )
        if not passwords_match:
            form.new_password_confirm.errors.append(
                'The two password fields didn\'t match.'
            )

    def _valid_password(self, form):
        """
        Process password validation.
        """
        verify_password = self._verify_password(form)
        passwords_match = self._passwords_match(form)
        self._append_errors(form, verify_password, passwords_match)
        return verify_password and passwords_match

    def post(self):
        form = self.form_class()
        if form.validate_on_submit() and self._valid_password(form):
                current_user.password = form.new_password.data
                db.session.add(current_user)
                flash('Your password was changed.')
                return redirect(url_for(current_app.config['DEFAULT_PAGE']))
        return render_template("auth.html", form=form)


class PasswordResetView(PasswordResetFormMixin, MethodView):
    """
    Password Reset view.
    """
    form_class = PasswordResetForm

    def _handle_email(self, user):
        """
        Handle sending email with link to reset a password.
        """
        token = user.generate_reset_token()
        body = (
            'Hi {}! Click upon this link {} to reset your password.'.format(
                user, url_for(
                    'bp_authentication.reset',
                    token=token, _external=True
                )
            )
        )
        send_email('Reset Your Password', user, body)

    def post(self):
        if not current_user.is_anonymous():
            return redirect(url_for(current_app.config['DEFAULT_PAGE']))
        form = self.form_class()
        if form.validate_on_submit():
            user = Profile.query.filter_by(email=form.email.data).first()
            if user:
                self._handle_email(user)
            return redirect(url_for('bp_authentication.password-reset-done'))
        return render_template('auth.html', form=form)


class PasswordResetDoneView(PasswordResetFormMixin, MethodView):
    """
    View after the Password Reset.
    """
    methods = ['GET']


class ResetView(PasswordResetFormMixin, MethodView):
    """
    Password Reset view with token confirmation.
    """
    form_class = PasswordResetDoneForm

    def post(self, token):
        form = self.form_class()
        if form.validate_on_submit():
            user = Profile.query.filter_by(email=form.email.data).first()
            if user is None:
                return redirect(url_for('main.index'))
            if user.reset_password(token, form.password.data):
                flash('Your password has been updated.')
                return redirect(url_for('bp_authentication.reset-done'))
            return redirect(url_for(current_app.config['DEFAULT_PAGE']))
        return render_template('auth.html', form=form)


class ResetDoneView(PasswordResetFormMixin, MethodView):
    """
    View after the Password Reset has been confirmed via token.
    """
    methods = ['GET']
