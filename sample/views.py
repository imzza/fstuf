# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.translation import ugettext as _
from django.shortcuts import render

# Create your views here.
from sample.forms import FileForm
from sample.models import File


def home(request):
    files = File.objects.all()
    form = FileForm()
    return render(request, 'home.html', {'files': files, 'form': form})


