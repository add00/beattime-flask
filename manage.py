#!/usr/bin/env python
import os

from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from beattime import create_app
from beattime.config import db
from boards.models import *
from profiles.models import *

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)

admin = Admin(app, name='microblog', template_mode='bootstrap3')
admin.add_view(ModelView(Label, db.session))
admin.add_view(ModelView(Profile, db.session))


if __name__ == '__main__':
    manager.run()
