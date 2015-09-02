from datetime import datetime

from flask import current_app
from flask.ext.login import UserMixin, AnonymousUserMixin
from itsdangerous import TimedJSONWebSignatureSerializer
from werkzeug.security import generate_password_hash, check_password_hash

from beattime.config import db, auth_manager
from beattime.fields import Column
from beattime.mixins import PKMixin


friends = db.Table(
    'friends',
    db.Column(
        'left_profile_id', db.Integer, db.ForeignKey('profiles.id'),
        primary_key=True
    ),
    db.Column(
        'right_profile_id', db.Integer, db.ForeignKey('profiles.id'),
        primary_key=True
    )
)


class AnonymousUser(AnonymousUserMixin):
    """
    Anonymous User's model.
    """
    pass

auth_manager.anonymous_user = AnonymousUser


@auth_manager.user_loader
def load_user(user_id):
    return Profile.query.get(int(user_id))


class Profile(UserMixin, PKMixin):
    """
    Users' model.
    """
    __tablename__ = 'profiles'

    username = db.Column(db.String(64), unique=True, index=True)
    email = db.Column(db.String(64), unique=True, index=True)
    passwd = db.Column(db.String(128))

    avatar = Column(db.String(256))
    display_name = Column(db.String(128))
    # @desc: self and a ManyToMany relation.
    friends = db.relationship(
        'Profile',
        secondary=friends,
        primaryjoin=('Profile.id==friends.c.left_profile_id'),
        secondaryjoin=('Profile.id==friends.c.right_profile_id'),
        backref='left_friends'
    )
    motivation_quote = Column(db.String(256), nullable=True)
    # user = models.OneToOneField(User, verbose_name=_('user'))

    comments = db.relationship('Comment', backref='profile')
    desk = db.relationship(
        'Desk', uselist=False, backref='profile', foreign_keys='Desk.owner_id'
    )
    boards = db.relationship('Board', backref='profile')
    sprints = db.relationship('Sprint', backref='profile')
    stickers = db.relationship('Sticker', backref='profile')

    activities = db.relationship('Activities', backref='profile')

    def __repr__(self):
        return '<Profile {}>'.format(self.display_name)

    @property
    def password(self):
        """
        Don't allow to see user's password.
        """
        raise AttributeError('You cannot see a password!')

    @password.setter
    def password(self, password):
        """
        Set user's password.
        """
        self.passwd = generate_password_hash(password)

    def verify_password(self, password):
        """
        Check if given password complies to user's one.
        """
        return check_password_hash(self.passwd, password)

    def generate_reset_token(self):
        """
        Generate unique token.
        """
        token = TimedJSONWebSignatureSerializer(
            current_app.config['SECRET_KEY'],
            current_app.config['TOKEN_EXPIRATION'],
        )
        return token.dumps({'reset': self.id})

    def reset_password(self, in_token, new_password):
        """
        Reset password.
        """
        token = TimedJSONWebSignatureSerializer(
            current_app.config['SECRET_KEY']
        )
        try:
            data = token.loads(in_token)
        except:
            return False
        if data.get('reset') != self.id:
            return False
        self.password = new_password
        db.session.add(self)
        return True


class ActivityType(PKMixin):
    """
    Each activity ('Activities' record) has its own type. This model
    is intended to store these kind of data.
    """
    __tablename__ = 'activity_types'

    description = Column(db.String(256), nullable=True)
    name = Column(db.String(100))

    activities = db.relationship('Activities', backref='activity_type')

    def __repr__(self):
        return '<ActivityType {}>'.format(self.name)


class Activities(PKMixin):
    """
    Model to store users' activities of different types (defined in
    `ActivityType`).
    """
    __tablename__ = 'activities'

    what = Column(db.Integer, db.ForeignKey('activity_types.id'))
    when = Column(db.DateTime(), default=datetime.now)
    who = Column(db.Integer, db.ForeignKey('profiles.id'))

    def __repr__(self):
        return '<Activities {} | {} | {}>'.format(
            self.who, self.what, self.when
        )
