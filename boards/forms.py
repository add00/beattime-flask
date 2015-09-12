# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from flask.ext.wtf import Form
from wtforms import StringField, SelectField
from wtforms.fields.html5 import DateField
from wtforms.widgets import TextArea
from wtforms.validators import Required, Length

from boards.models import Sprint


class BoardForm(Form):
    """
    Form for Board model.
    """
    title = StringField(
        'Title', validators=[Required(), Length(1, 100)]
    )
    prefix = StringField('Prefix', validators=[Required(), Length(1, 5)])


class CommentForm(Form):
    """
    Form for Comment model.
    """
    text = StringField('text', widget=TextArea(), validators=[Required()])


class SprintForm(Form):
    """
    Form for Sprint model.
    """
    number = StringField('Number', validators=[Required()])
    start_date = DateField('Start Date', validators=[Required()])
    end_date = DateField('End Date', validators=[Required()])


def enabled_categories():
    return Sprint.query.all()


class StickerForm(Form):
    """
    Form for Sticker model.
    """
    sprint_id = SelectField('Sprint')
    caption = StringField('Caption', validators=[Required()])
    description = StringField(
        'Description', widget=TextArea(), validators=[Required()]
    )

    def validate_sprint(form, field):
        """
        Pass sprint validation because it always has correct values since it
        dynamically prepopulated.
        """
        return True
