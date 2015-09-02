from beattime.config import db

from functools import partial


Column = partial(db.Column, nullable=False)
