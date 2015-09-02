from datetime import datetime

from sqlalchemy import UniqueConstraint
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy_utils import generic_relationship
from sqlalchemy_utils.types.choice import ChoiceType

from beattime.config import db
from beattime.fields import Column
from beattime.mixins import PKMixin
from boards import CSS_CLASS, TASK_STATUS


class CommonInfoMixin(PKMixin):
    __abstract__ = True

    creation_date = Column(db.DateTime(), default=datetime.now)
    modification_date = Column(db.DateTime(), onupdate=datetime.now)

    @declared_attr
    def author(cls):
        return Column(db.Integer, db.ForeignKey('profiles.id'))


class Comment(CommonInfoMixin):
    """
    There is a possibility to comment Stickers or Boards. This model store
    all comments.
    """
    __tablename__ = 'comments'

    text = Column(db.Text())
    object_id = Column(db.Integer)
    object_type = Column(db.Unicode(255))
    object = generic_relationship(object_type, object_id)

    def __repr__(self):
        return '<Comment {} | {}>'.format(self.author, self.creation_date)


class Label(PKMixin):
    """
    Represents status of task for particular `Sticker` object.
    """
    __tablename__ = 'labels'

    color = Column(db.String(7))
    css_class = ChoiceType(CSS_CLASS)
    status = ChoiceType(TASK_STATUS)

    stickers = db.relationship('Sticker', backref='label')

    def __repr__(self):
        return '<Label {} | {}>'.format(self.status, self.color)


class Desk(CommonInfoMixin):
    """
    Boards container model.
    """
    __tablename__ = 'desks'

    # @desc: OneToOne relation.
    owner_id = Column(db.Integer, db.ForeignKey('profiles.id'))
    desk_slug = Column(db.String(5), unique=True)

    boards = db.relationship('Board', backref='desk')

    def __repr__(self):
        return '<Desk {}>'.format(self.desk_slug)


class Board(CommonInfoMixin):
    """
    Stickers container model.
    """
    __tablename__ = 'boards'
    __table_args__ = (
        UniqueConstraint('desk_id', 'sequence', name='_desk_sequence_uc'),
    )

    desk_id = Column(db.Integer, db.ForeignKey('desks.id'))
    title = Column(db.String(100))
    sequence = Column(db.Integer)
    prefix = Column(db.String(5), unique=True)
    sticker_sequence = Column(db.Integer, default=1)

    sprints = db.relationship('Sprint', backref='board')
    stickers = db.relationship('Sticker', backref='board')

    def __repr__(self):
        return '<Board {} | {}>'.format(self.title, self.desk_id)


class Sprint(CommonInfoMixin):
    """
    Sprint for creating next phases of learning.
    """
    __tablename__ = 'sprints'
    __table_args__ = (
        UniqueConstraint('board_id', 'number', name='_board_number_uc'),
    )

    board_id = Column(db.Integer, db.ForeignKey('boards.id'))
    number = Column(db.DECIMAL(precision=2))
    start_date = Column(db.DateTime())
    end_date = Column(db.DateTime())

    stickers = db.relationship('Sticker', backref='sprint')

    def __repr__(self):
        return '<Sprint {} {}>'.format(self.number, self.board_id)


class Sticker(CommonInfoMixin):
    """
    Sticker with task description.
    """
    __tablename__ = 'stickers'
    __table_args__ = (
        UniqueConstraint('board_id', 'sequence', name='_board_sequence_uc'),
    )

    board_id = Column(db.Integer, db.ForeignKey('boards.id'))
    caption = Column(db.String(100))
    # @desc: long text field.
    description = Column(db.Text())
    label_id = Column(db.Integer, db.ForeignKey('labels.id'))
    sequence = Column(db.Integer)
    # @desc: choices field.
    sprint_id = Column(
        db.Integer, db.ForeignKey('sprints.id'), nullable=True
    )

    def __repr__(self):
        return '<Sticker {} | {} | {} | {}>'.format(
            self.board_id, self.sequence, self.caption, self.label_id
        )
