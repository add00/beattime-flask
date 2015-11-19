#!/usr/bin/env python
import os

from flask import render_template
from flask.ext.admin.contrib import sqla
from flask.ext.migrate import Migrate, MigrateCommand
from flask.ext.script import Manager
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from wtforms.fields import SelectField

from beattime import create_app
from beattime.config import db
from boards.models import *
from profiles.models import *


app = create_app(os.getenv('FLASK_CONFIG') or 'default')
admin = Admin(app, name='beattime', template_mode='bootstrap3')
manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)


class CommentAdmin(sqla.ModelView):
    form_overrides = dict(object_type=SelectField)
    form_args = dict(
        object_type=dict(choices=OBJECT_TYPE)
    )


class LabelAdmin(sqla.ModelView):
    form_overrides = dict(css_class=SelectField, status=SelectField)
    form_args = dict(
        css_class=dict(choices=CSS_CLASS), status=dict(choices=TASK_STATUS)
    )

admin.add_view(LabelAdmin(Label, db.session))
admin.add_view(ModelView(Profile, db.session))
admin.add_view(ModelView(Desk, db.session))
admin.add_view(ModelView(Board, db.session))
admin.add_view(ModelView(Sprint, db.session))
admin.add_view(ModelView(Sticker, db.session))
admin.add_view(CommentAdmin(Comment, db.session))


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


@manager.command
def test():
    """
    Test command.
    """
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


if __name__ == '__main__':
    manager.run()
