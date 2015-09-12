# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from flask import redirect, request, url_for
from flask.ext.login import current_user
from flask.views import View
from sqlalchemy.exc import IntegrityError

from authentication.forms import RegistrationForm
from beattime.config import db
from beattime.utils import handle_avatar, is_allowed_file_format
from boards import CREATE, DETAIL, LIST, OPEN, UPDATE
from boards.forms import StickerForm
from boards.mixins import (
    BoardMixin, CommentMixin, ProfileMixin, SprintMixin, StickerMixin
)
from boards.models import (
    Board, Comment, Desk, Label, Sprint, Sticker,
    BOARD_TYPE, SPRINT_TYPE, STICKER_TYPE,
)
from profiles.models import Profile


class ProfileDetail(ProfileMixin, View):
    action = DETAIL
    context_objects_name = 'boards'

    def get_objects(self):
        """
        Return only boards from desk of user from url.
        """
        if self.user.desk_owner:
            return self.user.desk_owner.board_set.all()


class ProfileUpdate(ProfileMixin, View):
    action = UPDATE
    form_class = RegistrationForm
    form_fields = [
        'display_name', 'friends', 'motivation_quote', 'avatar'
    ]

    def form_valid(self, form):
        """
        Update profile on form's data.
        """
        profile = self.get_object()

        _file = request.files['avatar']
        if _file and is_allowed_file_format(_file.filename):
            filename = handle_avatar(_file, profile)
            profile.avatar = filename

        profile.display_name = form.display_name.data
        profile.friends = db.session.query(Profile).filter(
            Profile.id.in_(form.friends.data)
        ).all()
        profile.motivation_quote = form.motivation_quote.data

        db.session.add(profile)

    def get_form(self):
        """
        Remove password specific fields.
        """
        form = super(ProfileUpdate, self).get_form()
        del form['password']
        del form['password_confirm']

        form.friends.choices = []
        if request.method == 'GET':
            form.friends.data = []

        for profile in Profile.query.all():
            if profile.id != self.user.id:
                form.friends.choices.append(
                    (int(profile.id), profile.display_name)
                )
                if profile in self.user.friends and request.method == 'GET':
                    form.friends.data.append(profile.id)

        return form


class FriendsList(ProfileMixin, View):
    action = LIST
    context_objects_name = 'friends'
    methods = ['GET']
    template_name = 'friends.html'

    def get_objects(self):
        """
        Return list of friends of given user.
        """
        return self.user.friends


class BoardDetail(BoardMixin, View):
    action = DETAIL
    context_objects_name = 'stickers'
    objects_model = Sticker

    def get_objects(self):
        """
        Return query of stickers that belong to desk of user sending a request.
        """
        board = self.get_object()
        return Sticker.query.filter_by(board_id=board.id, sprint_id=None).all()

    def context_data(self):
        context = super(BoardDetail, self).context_data()
        board_id = self.get_object().id
        context['sprints'] = Sprint.query.filter_by(board_id=board_id).all()
        return context


class BoardCreate(BoardMixin, View):
    action = CREATE

    def get_success_url(self):
        """
        After creation or update, back to a profile page.
        """
        username = request.view_args.get('username')
        if username:
            return url_for('bp_profile_user.profile-detail', username=username)
        return url_for('bp_profile.profile-detail')

    def form_valid(self, form):
        """
        Handle board form data.
        """
        board = Board(
            author=current_user.id,
            desk_id=self.user.desk_owner.id,
            title=form.title.data,
            sequence=Board.get_next_sequence(self.user),
            prefix=form.prefix.data,
            sticker_sequence=1
        )
        db.session.add(board)


class BoardComments(CommentMixin, BoardMixin, View):
    action = LIST
    paginate_by = 2
    paginated_objects_name = 'comments'

    def get_paginated_objects(self):
        """
        Provide board's comments.
        """
        obj = self.get_object()
        return Comment.query.filter_by(
            object_type=BOARD_TYPE, object_id=obj.id
        ).order_by(Comment.creation_date.desc())


class SprintDetail(SprintMixin, View):
    action = DETAIL


class SprintCreate(SprintMixin, View):
    action = CREATE

    def get_success_url(self):
        """
        After creation or update, back to a board page.
        """
        username = request.view_args.get('username')
        sequence = request.view_args.get('sequence')
        if username:
            return url_for(
                'bp_board_user.board-detail',
                sequence=sequence, username=username
            )
        return url_for('bp_board.board-detail', sequence=sequence)

    def get_object(self):
        """
        Return board.
        """
        desk_id = Desk.query.filter_by(owner_id=self.user.id).scalar().id
        return Board.query.filter_by(
            desk_id=desk_id,
            sequence=request.view_args.get('sequence')
        ).scalar()

    def form_valid(self, form):
        """
        Handle sprint form data.
        """
        board = self.get_object()
        sprint = Sprint(
            author=current_user.id,
            board_id=board.id,
            number=form.number.data,
            start_date=form.start_date.data,
            end_date=form.end_date.data
        )
        db.session.add(sprint)


class SprintComments(CommentMixin, SprintMixin, View):
    action = LIST
    paginate_by = 2
    paginated_objects_name = 'comments'

    def get_paginated_objects(self):
        """
        Provide board's comments.
        """
        obj = self.get_object()
        return Comment.query.filter_by(
            object_type=SPRINT_TYPE, object_id=obj.id
        ).order_by(Comment.creation_date.desc())


class StickerDetail(CommentMixin, StickerMixin, View):
    action = DETAIL
    paginate_by = 2
    paginated_objects_name = 'comments'

    def get_paginated_objects(self):
        """
        Provide stikcer's comments.
        """
        obj = self.get_object()
        return Comment.query.filter_by(
            object_type=STICKER_TYPE, object_id=obj.id
        ).order_by(Comment.creation_date.desc())


class StickerCreate(StickerMixin, View):
    action = CREATE

    def get_success_url(self):
        """
        Return success url after sticker creation.
        """
        number = request.view_args.get('number')
        sequence = request.view_args.get('sequence')
        username = request.view_args.get('username')

        if number:
            if username:
                return url_for(
                    'bp_sprint_user.sprint-detail',
                    number=number, sequence=sequence, username=username
                )
            return url_for(
                'bp_sprint.sprint-detail',
                number=number, sequence=sequence
            )
        if username:
            return url_for(
                'bp_board_user.board-detail',
                sequence=sequence, username=username
            )

        return url_for('bp_board.board-detail', sequence=sequence)

    def get_object(self):
        """
        Return board or sprint.
        """

        desk_id = Desk.query.filter_by(owner_id=self.user.id).scalar().id
        board = Board.query.filter_by(
            desk_id=desk_id,
            sequence=request.view_args.get('sequence')
        ).scalar()

        if request.view_args.get('number'):
            return Sprint.query.filter_by(
                board_id=board.id,
                number=request.view_args.get('number')
            ).scalar(), SPRINT_TYPE
        return board, BOARD_TYPE

    def get_form(self):
        """
        Prepopulate form.
        """
        obj, obj_type = self.get_object()

        board_id = obj.id if obj_type == BOARD_TYPE else obj.board_id
        form = super(StickerMixin, self).get_form()
        if request.view_args.get('number'):
            del form['sprint_id']
        else:
            form.sprint_id.choices = [
                (sprint.id, 'SPRINT #{}'.format(sprint.number))
                for sprint in Sprint.query.filter_by(board_id=board_id).all()
            ]
            form.sprint_id.choices.insert(0, (None, 'Backlog'))

        return form

    def validate_form(self, form):
        """
        Handle sticker form data.
        """
        obj, obj_type = self.get_object()
        board = (
            obj if obj_type == BOARD_TYPE else
            Board.query.filter_by(id=obj.board_id).scalar()
        )
        number = request.view_args.get('number')
        sprint_id = (
            form.sprint_id.data if not number else Sprint.query.filter_by(
                number=number, board_id=board.id
            ).scalar().id
        )
        sequence = board.sticker_sequence
        label_id = Label.query.filter_by(status=OPEN).scalar().id
        sticker = Sticker(
            author=current_user.id,
            board_id=board.id,
            caption=form.caption.data,
            description=form.description.data,
            label_id=label_id,
            sequence=sequence,
            sprint_id=sprint_id if not sprint_id == 'None' else None
        )
        db.session.add(sticker)
        try:
            db.session.commit()
            board.sticker_sequence = int(sequence) + 1
            db.session.add(board)
        except IntegrityError:
            db.session.rollback()
        return redirect(self.get_success_url())


class StickerUpdate(StickerMixin, View):
    action = UPDATE
    form_class = StickerForm
    form_name = 'sticker_form'

    def get_form(self):
        """
        Prepopulate form.
        """
        if request.method == 'POST':
            return self.form_class()

        sticker = self.get_object()
        sprint_set = (
            Board.query.filter_by(id=sticker.board_id).scalar().sprint_set
        )
        form = super(StickerMixin, self).get_form()
        form.sprint_id.choices = [
            (sprint.id, 'SPRINT #{}'.format(sprint.number))
            for sprint in sprint_set
        ]
        form.sprint_id.choices.insert(0, (None, 'Backlog'))
        form.sprint_id.default = sticker.sprint_id
        form.process()
        form.description.data = sticker.description
        form.caption.data = sticker.caption

        return form

    def get_success_url(self):
        """
        Back to a sticker page.
        """
        prefix = request.view_args.get('prefix')
        desk_id = Desk.query.filter_by(owner_id=self.user.id).scalar().id
        sequence = Board.query.filter_by(
            prefix=prefix, desk_id=desk_id
        ).scalar().sequence
        username = request.view_args.get('username')
        if username:
            return url_for(
                'bp_board.board-detail',
                username=username, sequence=sequence
            )
        return url_for(
            'bp_board.board-detail', sequence=sequence
        )

    def validate_form(self, form):
        """
        Update sticker on form's data.
        """
        sprint_data = form.sprint_id.data
        form.sprint_id = None if sprint_data == 'None' else int(sprint_data)
        sticker = self.get_object()
        form.populate_obj(sticker)
        db.session.add(sticker)

        return redirect(self.get_success_url())
