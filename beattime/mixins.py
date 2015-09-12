# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from flask import current_app, request, redirect, render_template, url_for
from wtforms.widgets import HiddenInput

from beattime.exceptions import MultipleObjects
from boards.utils import get_user


class CommonInfoMixin(object):
    """
    Append common data to view instance.
    """

    def __init__(self):
        self.user = get_user(request.view_args)


class PaginationMixin(object):
    paginate_by = None
    paginated_objects_name = 'paginated_objects'

    def get_paginated_objects(self):
        """
        Provide query to paginate.
        """

    def pagination(self):
        """
        Provide paginated objects to context.
        """
        objects = self.get_paginated_objects()
        if objects:
            page = request.args.get('page', 1, type=int)

            pagination = objects.paginate(
                page, per_page=self.paginate_by, error_out=False
            )

            prev_page = page - 1 if pagination.has_prev else None
            next_page = page + 1 if pagination.has_next else None

            return {
                self.paginated_objects_name: pagination.items,
                'prev_page': prev_page,
                'next_page': next_page,
                'pages_num': range(1, pagination.pages + 1),
                'page_num': page

            }


class ContextMixin(CommonInfoMixin, PaginationMixin):
    """
    Mixin class to pass kwargs and other extra data to context.
    """
    action = None
    context_object_name = 'object'
    context_objects_name = 'objects'
    form_class = None
    form_name = 'form'
    form_fields = '__all__'
    success_url = None
    model = None
    object_model = None
    objects_model = None

    def _get_short_urls_allowed(self):
        """
        Return if `username` argument can be omitted while rendering urls.
        """
        return request.view_args.get('username') is None

    def _has_view_attrs(self, model):
        """
        Check if it's possible to filter model by view args.
        """
        return all([hasattr(model, attr) for attr in request.view_args.keys()])

    def get_object(self):
        """
        Provide object basing on model and view args.
        """
        model = self.object_model or self.model
        if model and self._has_view_attrs(model):
            obj = model.query.filter_by(**request.view_args)
            if obj.count() > 1:
                raise MultipleObjects(
                    'Many objects returned for the specified criteria.'
                )
            return obj.scalar()

    def get_objects(self):
        """
        Provide objects list basing on model and view args.
        """
        model = self.objects_model or self.model
        if model and self._has_view_attrs(model):
            return model.query.filter_by(**request.view_args).all()

    def _prepare_form(self, form):
        """
        Trim form's fields basing on `form_fields` parameter.
        """
        if not self.form_fields == '__all__':
            disable_fields = set(form.data.keys()) - set(self.form_fields)
            for field_name in disable_fields:
                form[field_name].widget = HiddenInput()
                form[field_name].label.text = ''

        return form

    def _prepopulate_form(self, form, obj):
        """
        Prepopulate form with data from object for update purposes.
        Method is ran only on GET request method.
        """
        for field_name in form.data.keys():
            value = getattr(obj, field_name, '')
            form[field_name].data = value
        return form

    def get_form(self):
        """
        Provide form.
        """
        if hasattr(self, 'form'):
            return self.form
        if self.form_class:
            obj = self.get_object()
            if obj:
                form = self._prepare_form(self.form_class(obj=obj))
                if request.method == 'POST':
                    return form
                return self._prepopulate_form(form, obj)
            return self.form_class()

    def form_valid(self, form):
        """
        Action on valid form
        """

    def validate_form(self, form):
        """
        Validate form.
        """
        if form.validate_on_submit():
            self.form_valid(form)
            success_url = self.get_success_url()
            if success_url:
                return redirect(success_url)
            return redirect(
                url_for(current_app.config['DEFAULT_PAGE']) or '/'
            )
        if hasattr(self, 'context'):
            return self.render_template(self.context)
        return self.render_template(self.context_data())

    def get_success_url(self):
        """
        Provide success url.
        """
        if self.success_url:
            return self.success_url

    def context_data(self):
        """
        Return common context data.
        """
        context = request.view_args
        context.update({
            'action': self.action,
            'user': self.user,
            'short_urls_allowed': self._get_short_urls_allowed(),
            self.context_object_name: self.get_object(),
            self.context_objects_name: self.get_objects(),
            self.form_name: self.get_form()
        })
        if self.paginate_by:
            context.update(self.pagination())

        return context


class ViewMixin(ContextMixin):
    """
    Common features of generic views.
    """
    template_name = None

    def render_template(self, context):
        """
        Template renderer.
        """
        return render_template(self.template_name, **context)

    def dispatch_request(self, *args, **kwargs):
        """
        Handle request, getting context data and proccessing form.
        """
        self.context = self.context_data()
        if request.method == 'POST' and self.context[self.form_name]:
            return self.validate_form(self.context[self.form_name])
        return self.render_template(self.context)
