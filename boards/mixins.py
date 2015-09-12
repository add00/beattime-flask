# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from flask import request, url_for
from flask.ext.login import current_user
from sqlalchemy import and_

from authentication.mixins import LoginRequiredMixin
from beattime.config import db
from beattime.mixins import ViewMixin
from boards.forms import BoardForm, CommentForm, SprintForm, StickerForm
from boards.models import (
    Board, Comment, Desk, Sprint, Sticker,
    BOARD_TYPE, SPRINT_TYPE, STICKER_TYPE,
)


class CommentMixin(object):
    form_class = CommentForm

    # def get_object(self):
    #     """
    #     Return sticker or board, basing on request.
    #     """
    #     self.url_name = request.url_rule.endpoint
    #     if self.url_name == 'bp_profile.sticker-detail':
    #         return Sticker.query.filter_by(
    #             board__desk__owner__user=self.user,
    #             board__prefix=self.kwargs['prefix'],
    #             sequence=self.kwargs['sequence']
    #         ).scalar()
    #     elif self.url_name == 'bp_profile.board-comments':
    #         desk_id = Desk.query.filter_by(owner_id=self.user.id).scalar().id
    #         return Board.query.filter_by(
    #             desk_id=desk_id,
    #             sequence=request.view_args.get('sequence')
    #         ).scalar()
    #     elif self.url_name == 'bp_profile.sprint-comments':
    #         return Sprint.query.filter_by(
    #             number=self.kwargs['sprint_number'],
    #             board__desk__owner__user=self.user,
    #             board__sequence=self.kwargs['board_sequence']
    #         ).scalar()

    def get_success_url(self):
        """
        After creation, back to a previous page.
        """
        return url_for(request.url_rule.endpoint, **request.view_args)
        # if request.view_args.get('username'):
        #     return url_for('boards:{}-username'.format(self.url_name))
        # return url_for('boards:{}'.format(self.url_name))

    def form_valid(self, form):
        """
        Append default data while creating a comment, not provided in a form.
        """
        obj = self.get_object()
        comment = Comment(
            author=current_user.id,
            object_id=obj.id,
            object_type=obj.object_type,
            text=form.text.data
        )
        db.session.add(comment)
        db.session.commit()

        return super(CommentMixin, self).form_valid(form)


class ProfileMixin(LoginRequiredMixin, ViewMixin):
    methods = ['GET', 'POST']
    context_object_name = 'profile'
    template_name = 'profile.html'

    def get_object(self):
        """
        Return profile.
        """
        return self.user


class BoardMixin(LoginRequiredMixin, ViewMixin):
    methods = ['GET', 'POST']
    template_name = 'board.html'
    context_object_name = 'board'
    object_model = Board
    form_class = BoardForm

    def get_object(self):
        """
        Get board basing on url.
        """
        desk_id = Desk.query.filter_by(owner_id=self.user.id).scalar().id
        return Board.query.filter_by(
            desk_id=desk_id,
            sequence=request.view_args.get('sequence')
        ).scalar()


class SprintMixin(LoginRequiredMixin, ViewMixin):
    methods = ['GET', 'POST']
    template_name = 'sprint.html'
    context_object_name = 'sprint'
    object_model = Sprint
    form_class = SprintForm

    def get_object(self):
        """
        Get board basing on url.
        """
        desk_id = Desk.query.filter_by(owner_id=self.user.id).scalar().id
        board_id = Board.query.filter_by(
            desk_id=desk_id,
            sequence=request.view_args.get('sequence')
        ).scalar().id
        return Sprint.query.filter_by(
            board_id=board_id,
            number=request.view_args.get('number')
        ).scalar()


class StickerMixin(LoginRequiredMixin, ViewMixin):
    methods = ['GET', 'POST']
    template_name = 'sticker.html'
    context_object_name = 'sticker'
    object_model = Sticker

    def get_object(self):
        """
        Get board basing on url.
        """
        desk_id = Desk.query.filter_by(owner_id=self.user.id).scalar().id
        return Sticker.query.filter(and_(
            Board.desk_id == desk_id,
            Board.prefix == request.view_args.get('prefix'),
            Sticker.sequence == request.view_args.get('sequence'),
        )).scalar()



    #     desk_id = Desk.query.filter_by(owner_id=self.user.id).scalar().id
    #     board_id = Board.query.filter_by(
    #         desk_id=desk_id,
    #         sequence=request.view_args.get('sequence')
    #     ).scalar().id
    #     return Sprint.query.filter_by(
    #         board_id=board_id,
    #         number=request.view_args.get('number')
    #     ).scalar()

    # def get_object(self):
    #     """
    #     Return sticker for given number from requesting user's board.
    #     Sticker can be editted by its author or owner of desk.
    #     """
    #     if not self.user.is_authenticated():
    #         # Redirect to log in page.
    #         raise Http404('Access denied')

    #     return Sticker.objects.get(
    #         board__desk__owner__user=self.user,
    #         board__prefix=self.kwargs['prefix'],
    #         sequence=self.kwargs['sequence']
    #     )

