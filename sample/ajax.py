# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.translation import ugettext as _
from django.http import HttpResponse
from django.shortcuts import render

from sample.forms import FileForm
from sample.models import File, FileType
import json
from django.views.decorators.csrf import csrf_exempt



def create_file(request):
    """ Add file """
    data = {'status': None, 'message': None}

    if request.method == 'POST' and request.FILES:

        file_form = FileForm(data=request.POST, files=request.FILES)
        file_form.save(commit=True)

        data['status'] = 200
        data['message'] = _(u'Archivo cargado correctamente')

    else:
        # Data to generate response when id invalid
        data['status'] = 405
        data['message'] = _(u'Método no permitido')

    return HttpResponse(json.dumps(data), content_type='application/json')


def get_file_filters(request):
    data = {'status': None, 'message': None}

    if request.is_ajax() and request.method == 'POST':
        file_type_id = request.POST.get('file_type') or None
        file_type = FileType.objects.get(pk=file_type_id, is_active=True)
        file = File.objects.filter(file_type=file_type.pk)

        data = json.dumps([{
            'pk': file_type.pk,
            'fields': {
                'codename': file_type.codename,
                'file_extension': list(file_type.file_extension.values_list('extension', flat=True)),
                'name': file_type.name,
                'max_size': file_type.max_size,
                'num_files': -1 if file.count() >= file_type.num_files else file_type.num_files,
                'image_resize':
                    {
                        'width': file_type.image_width,
                        'height': file_type.image_height,
                        'quality': file_type.image_quality
                }
            }
        }])
    else:
        # Data to generate response when id invalid
        data['status'] = 405
        data['message'] = _('Método no permitido')
        data = json.dumps(data)

    return HttpResponse(data, content_type='application/json')


def upload_file(request):
    return render(request, 'upload.html')


@csrf_exempt
def upload_file_chunks(request):
    uploaded_file = request.FILES['file']
    chunk = request.POST.get('chunk', '0')
    chunks = request.POST.get('chunks', '0')
    name = request.POST.get('name', '')
    if not name:
        name = uploaded_file.name

    temp_file = 'c:/temp/'+name

    print(temp_file)
    with open(temp_file, ('wb' if chunk == '0' else 'ab')) as f:
        for content in uploaded_file.chunks():
            f.write(content)

    if int(chunk) + 1 >= int(chunks):
        # form.save(temp_file, name)
        data = json.dumps({'sam': 'Done'})
        return HttpResponse(data, content_type='application/json')

    data = json.dumps({'sam': 'Sam'})
    return HttpResponse(data, content_type='application/json')
