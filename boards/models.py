from datetime import datetime

from sqlalchemy import and_
from sqlalchemy import func, UniqueConstraint
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy_utils import generic_relationship
from sqlalchemy_utils.types.choice import ChoiceType

from beattime.config import db
from beattime.fields import Column
from boards import (
    CSS_CLASS, TASK_STATUS, OPEN, IN_PROGRESS, IN_REVIEW, DONE, BLOCKED
)
from profiles.models import Profile

BOARD_TYPE = 'Board'
SPRINT_TYPE = 'Sprint'
STICKER_TYPE = 'Sticker'
OBJECT_TYPE = (
    (BOARD_TYPE, BOARD_TYPE),
    (SPRINT_TYPE, SPRINT_TYPE),
    (STICKER_TYPE, STICKER_TYPE),
)


class PKMixin(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)


class CommonInfoMixin(PKMixin):
    __abstract__ = True

    creation_date = Column(db.DateTime(), default=datetime.now)
    modification_date = Column(
        db.DateTime(), default=datetime.now, onupdate=datetime.now
    )

    @declared_attr
    def author(cls):
        return Column(db.Integer, db.ForeignKey('profiles.id'))


class Comment(CommonInfoMixin):
    """
    There is a possibility to comment Stickers or Boards. This model store
    all comments.
    """
    __tablename__ = 'comments'

    text = db.Column(db.Text())
    object_id = Column(db.Integer)
    object_type = db.Column(ChoiceType(OBJECT_TYPE))

    @property
    def object(self):
        """
        Return commented object.
        """
        MODEL = {
            BOARD_TYPE: Board,
            SPRINT_TYPE: Sprint,
            STICKER_TYPE: Sticker
        }
        return MODEL[self.object_type].filter_by(
            object_id=self.object_id
        ).scalar()

    def __repr__(self):
        return '<Comment {} | {}>'.format(self.author, self.creation_date)


class Label(PKMixin):
    """
    Represents status of task for particular `Sticker` object.
    """
    __tablename__ = 'labels'

    color = Column(db.String(7))
    css_class = db.Column(ChoiceType(CSS_CLASS))
    status = db.Column(ChoiceType(TASK_STATUS))

    sticker_set = db.relationship('Sticker', backref='label')

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

    board_set = db.relationship('Board', backref='desk', lazy='dynamic')

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

    sprint_set = db.relationship('Sprint', backref='board')
    sticker_set = db.relationship('Sticker', backref='board')

    def __repr__(self):
        return '<Board {} | {}>'.format(self.title, self.desk_id)

    @property
    def object_type(self):
        return BOARD_TYPE

    @staticmethod
    def get_next_sequence(profile):
        """
        Return next board sequence
        """
        last_sequence = (
            db.session.query(func.max(Board.sequence)).filter_by(
                desk=profile.desk_owner
            ).scalar()
        ) or 0
        return last_sequence + 1


class Sprint(CommonInfoMixin):
    """
    Sprint for creating next phases of learning.
    """
    __tablename__ = 'sprints'
    __table_args__ = (
        UniqueConstraint('board_id', 'number', name='_board_number_uc'),
    )

    board_id = Column(db.Integer, db.ForeignKey('boards.id'))
    number = Column(db.String(100))
    start_date = Column(db.DateTime())
    end_date = Column(db.DateTime())

    sticker_set = db.relationship('Sticker', backref='sprint')

    @property
    def object_type(self):
        return SPRINT_TYPE

    @property
    def open(self):
        """
        Returns open sprint's stickers.
        """
        label_id = Label.query.filter_by(status=OPEN).scalar().id
        return Sticker.query.filter_by(
            label_id=label_id, sprint_id=self.id
        ).all()

    @property
    def in_progress(self):
        """
        Returns in progress sprint's stickers.
        """
        label_id = Label.query.filter_by(status=IN_PROGRESS).scalar().id
        return Sticker.query.filter_by(
            label_id=label_id, sprint_id=self.id
        ).all()

    @property
    def in_review(self):
        """
        Returns in review sprint's stickers.
        """
        label_id = Label.query.filter_by(status=IN_REVIEW).scalar().id
        return Sticker.query.filter_by(
            label_id=label_id, sprint_id=self.id
        ).all()

    @property
    def done(self):
        """
        Returns done sprint's stickers.
        """
        label_id = Label.query.filter_by(status=DONE).scalar().id
        return Sticker.query.filter_by(
            label_id=label_id, sprint_id=self.id
        ).all()

    @property
    def blocked(self):
        """
        Returns blocked sprint's stickers.
        """
        label_id = Label.query.filter_by(status=BLOCKED).scalar().id
        return Sticker.query.filter_by(
            label_id=label_id, sprint_id=self.id
        ).all()

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

    @property
    def object_type(self):
        return STICKER_TYPE

    @property
    def author_display_name(self):
        """
        Return author of sticker.
        """
        return Profile.query.filter_by(id=self.author).scalar().display_name

    @property
    def board_sequence(self):
        """
        Return board sequence.
        """
        return Board.query.filter_by(id=self.board_id).scalar().sequence

    @property
    def prefix(self):
        """
        Return sticker's board prefix.
        """
        return Board.query.filter_by(id=self.board_id).scalar().prefix

    def __repr__(self):
        return '<Sticker {} | {} | {} | {}>'.format(
            self.board_id, self.sequence, self.caption, self.label_id
        )
