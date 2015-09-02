# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, SubmitField
from wtforms.fields.html5 import EmailField
from wtforms.validators import Required, Length, Email, EqualTo

from beattime.validators import USERNAME_REGEX

PASSWORD_ERROR_MSG = 'The two password fields didn\'t match.'


class LoginForm(Form):
    """
    Form for login purposes.
    """

    username = StringField(
        'Username', validators=[Required(), USERNAME_REGEX, Length(1, 64)]
    )
    password = PasswordField('Password', validators=[Required()])
    submit = SubmitField('Login')


class RegistrationForm(Form):
    """
    Form for registration purposes.
    """
    username = StringField(
        'Username', validators=[Required(), USERNAME_REGEX, Length(1, 64)]
    )
    display_name = StringField('Display name')
    email = EmailField(
        'Email', validators=[Required(), Length(1, 64), Email()]
    )
    password = PasswordField('Password', validators=[Required()])
    password_confirm = PasswordField(
        'Confirm password', validators=[
            Required(), EqualTo('password', message=PASSWORD_ERROR_MSG)
        ]
    )
    avatar = StringField('Avatar')
    motivation_quote = StringField('Motivation quote')
    submit = SubmitField('Register')


class ChangePasswordForm(Form):
    """
    Form for change password purposes.
    """
    old_password = PasswordField('Old password', validators=[Required()])
    new_password = PasswordField('New password', validators=[
        Required()])
    new_password_confirm = PasswordField(
        'New password confirmation', validators=[Required()]
    )
    submit = SubmitField('Update Password')


class PasswordResetForm(Form):
    """
    Form for reset password purposes.
    """
    email = EmailField(
        'Email', validators=[Required(), Length(1, 64), Email()]
    )

    submit = SubmitField('Reset Password')


class PasswordResetDoneForm(Form):
    """
    Form for password reset confirmation purposes.
    """
    email = EmailField(
        'Email', validators=[Required(), Length(1, 64), Email()]
    )
    password = PasswordField('New Password', validators=[
        Required()])
    password_confirm = PasswordField(
        'Confirm password', validators=[
            Required(), EqualTo('password', message=PASSWORD_ERROR_MSG)
        ]
    )
    submit = SubmitField('Reset Password')
