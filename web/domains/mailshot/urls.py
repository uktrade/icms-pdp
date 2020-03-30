#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.urls import path

from . import views

urlpatterns = [
    path('', views.MailshotListView.as_view(), name='mailshot-list'),
]