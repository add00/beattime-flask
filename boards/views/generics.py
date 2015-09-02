# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from flask.views import View
from flask import render_template, request
from boards import bp_profile, DETAIL
from boards.models import Label
from beattime.mixins import ContextMixin


# @profile.route('/')
# def show_followed():
#     return render_template('base.html', data='asa')


class ProfileDetail(ContextMixin, View):
    action = DETAIL
    methods = ['GET', 'POST']

    def get_template_name(self):
        return 'profile.html'

    def render_template(self, context):
        return render_template(self.get_template_name(), **context)

    def get_objects(self):
        # import ipdb; ipdb.set_trace()
        return Label.query.all()

    def dispatch_request(self):
        # if request.method == 'GET':
        context = self.context_data()
        context.update({'objects': self.get_objects()})
        return self.render_template(context)


bp_profile.add_url_rule('/', view_func=ProfileDetail.as_view(str('profiledetail')))

# class ProfileDetail(ProfileMixin, ListView):
#     action = DETAIL

#     def get_context_data(self, **kwargs):
#         """
#         Provide profile data.
#         """
#         context = super(ProfileDetail, self).get_context_data(**kwargs)
#         context['boards'] = self.get_queryset()

#         return context

#     def get_queryset(self):
#         """
#         Return only boards from desk of user from url.
#         """
#         self.object = self.get_object()
#         return self.object.desk.board_set.all()
