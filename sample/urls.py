# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from sample import views as sample_views
from sample import ajax as sample_ajax

urlpatterns = [
    url(r'^$', sample_views.home, name='home'),
    url(r'^sample/ajax/get-file_filters/$', sample_ajax.get_file_filters, name='ajax_common_get_file_filters'),
    url(r'^samples/ajax/upload/$', sample_ajax.create_file, name='ajax_create_file'),
    url(r'^samples/upload/$', sample_ajax.upload_file, name='upload_file'),
    url(r'^upload/$', sample_ajax.upload_file_chunks, name='upload_file_chunks'),
]