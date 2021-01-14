# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _

from sample.models import FileType, File


class FileForm(forms.ModelForm):
    file_type = forms.ModelChoiceField(
        widget=forms.Select(
            attrs={
                'class': 'form-control',
                'onchange': 'generate_upload_widget(this.value)'
            },
        ),
        empty_label=_('Seleccione...'),
        label=_(u'Tipo de archivo o documento'),
        queryset=FileType.objects.all(),
        required=False
    )
    file = forms.FileField(
        widget=forms.FileInput(
            attrs={
                'class': 'hidden',
            }
        ),
        label=False,
        required=False
    )

    # file_date = forms.DateField(
    #     widget=forms.DateInput(
    #         attrs={
    #             'class': 'form-control',
    #             'readonly': ''
    #         }
    #     ),
    #     label=_(u'Fecha del archivo'),
    #     required=False
    # )

    description = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'rows': 1,
                'style': 'resize: vertical;'
            }
        ),
        label=_(u'Descripción'),
        required=False,
        error_messages={
            'required': _(u'Debe escribir la descripción del daño'),
        },
    )

    def __init__(self, *args, **kwargs):
        super(FileForm, self).__init__(*args, **kwargs)

    class Meta:
        model = File
        fields = ['file_type', 'file', 'description']
