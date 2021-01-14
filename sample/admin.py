# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.translation import ugettext as _
from django.contrib import admin
from django.db.models import ManyToManyField
from django.forms import CheckboxSelectMultiple

from sample.models import FileExtension, FileType, FileTypeGroup


@admin.register(FileExtension)
class FileExtensionAdmin(admin.ModelAdmin):
    list_display = ('extension', 'description', 'mime_full')
    list_editable = ['description']
    list_filter = ['mime_type']
    search_fields = ['extension']


@admin.register(FileType)
class FileTypeAdmin(admin.ModelAdmin):

    def get_extensions(self, obj):
        return ", ".join([ext.extension for ext in obj.file_extension.all()])
    get_extensions.short_description = _('Extensiones admitidas')

    fieldsets = (
        (None, {
            'fields': ('name', 'codename', ('max_size', 'num_files'), ('order', 'is_active'))
        }),
        (_('Redimensionado de imagenes'), {
            'fields': ('image_resize', 'image_quality', ('image_width', 'image_height'))
        }),
        (_('Grupos y extensiones'), {
            'classes': ('collapse',),
            'fields': ('file_type_group', 'file_extension')
        }),
    )
    formfield_overrides = {
        ManyToManyField: {'widget': CheckboxSelectMultiple}
    }
    list_display = ('name', 'max_size', 'num_files', 'order', 'codename', 'get_extensions')
    list_editable = ['max_size', 'num_files', 'order', 'codename']
    list_filter = ['file_type_group', 'is_active']
    search_fields = ['name', 'codename']


@admin.register(FileTypeGroup)
class FileTypeGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'order', 'codename')
    list_editable = ['codename']