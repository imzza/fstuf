# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import ugettext as _
import os
import datetime
import random

NAME = _(u'Nombre')


def upload_reformat_name(instance, filename, related_model=None):
    """
    Format the name of the file consisting of the date, random number and extension
    The directory name: app/model/pk/directory/
    """
    name, ext = os.path.splitext(filename)
    name = '%s_%s' % (datetime.datetime.now().strftime("%Y%m%d%H%M%S"), '{:05d}'.format(random.randint(0, 99999)))

    if related_model:
        directory = '%s/%s/%s/' % (instance._meta.app_label, str(instance.__class__.__name__).lower(), str(related_model.id))

    else:
        directory = ''
    return '%s%s%s' % (directory, name, ext.lower())


def upload_file_path(instance, filename):
    return upload_reformat_name(instance, filename, instance)


class FileTypeGroup(models.Model):
    name = models.CharField(verbose_name=NAME, max_length=25, null=True, blank=True, default=None)
    order = models.PositiveSmallIntegerField(verbose_name=_(u'Orden'), blank=True, default=1000, null=True)
    codename = models.CharField(max_length=10, null=True, blank=True, default=None, unique=True)

    def __str__(self):
        return '%s %s' % (self.codename, self.name)

    class Meta:
        verbose_name = _(u'Grupo de archivos')
        verbose_name_plural = _(u'Grupos de archivos')
        ordering = ['order', 'name']


class FileExtension(models.Model):
    MIME_TYPE_CHOICES = (
        ('application', _(u'Aplicación')),
        ('audio', _(u'Audio')),
        ('font', _(u'Fuente')),
        ('image', _(u'Imagen')),
        ('text', _(u'Texto')),
        ('video', _(u'Video')),
    )
    extension = models.CharField(verbose_name=_(u'Extensión'), max_length=10, blank=True, default=None, null=True,
                                 unique=True)
    description = models.CharField(verbose_name=_(u'Descripción'), max_length=200, blank=True, default=None, null=True)
    mime_type = models.CharField(verbose_name='MIME type', choices=MIME_TYPE_CHOICES, max_length=15, blank=True,
                                 default=None, null=True)
    mime_subtype = models.CharField(verbose_name='MIME subtype', max_length=80, blank=True, default=None, null=True)

    @property
    def mime_full(self):
        return '%s/%s' % (self.mime_type, self.mime_subtype)

    def __str__(self):
        return '%s' % self.extension

    class Meta:
        verbose_name = _(u'Extensión de archivo')
        verbose_name_plural = _(u'Extensiones de archivo')
        ordering = ['extension']


class FileType(models.Model):
    file_type_group = models.ManyToManyField(FileTypeGroup, verbose_name=_(u'Grupo de archivo'))
    file_extension = models.ManyToManyField(FileExtension, verbose_name=_(u'Extensión de archivo'))
    name = models.CharField(verbose_name=NAME, max_length=50, null=True, blank=True, default=None)
    max_size = models.PositiveIntegerField(verbose_name=_(u'Tamaño máximo (KB)'), null=True, blank=True, default=1024)
    num_files = models.PositiveSmallIntegerField(verbose_name=_(u'Núm. máx.'), null=True, blank=True, default=1)
    codename = models.CharField(max_length=20, unique=True)
    order = models.PositiveSmallIntegerField(verbose_name=_(u'Orden'), blank=True, default=1000, null=True)
    is_active = models.BooleanField(verbose_name=_(u'¿Activo?'), default=True)
    image_resize = models.BooleanField(verbose_name=_(u'¿Redimensionar?'), default=True)
    image_aspect_ratio = models.BooleanField(verbose_name=_(u'¿Mantener aspecto?'), default=True)
    image_width = models.PositiveIntegerField(verbose_name=_(u'Ancho de imágen'), default=1024)
    image_height = models.PositiveIntegerField(verbose_name=_(u'Alto de imágen'), default=768)
    image_quality = models.PositiveSmallIntegerField(verbose_name=_(u'Calidad de imagen'), default=70,
                                                     validators=[MaxValueValidator(100), MinValueValidator(25)])

    def __str__(self):
        return '%s' % self.name

    class Meta:
        verbose_name = _(u'Tipo de archivo')
        verbose_name_plural = _(u'Tipos de archivo')
        ordering = ['order']


class File(models.Model):
    """ File """
    file_type = models.ForeignKey(FileType, verbose_name=_('Tipo de archivo'), blank=True, default=None, null=True, on_delete=models.SET_NULL)
    file = models.FileField(upload_to=upload_file_path, blank=True, default=None, null=True)
    description = models.CharField(verbose_name=_('Descripción'), max_length=200, blank=True, default=None, null=True)
    is_visible = models.BooleanField(verbose_name=_('Es visible'), default=False, null=False)
    order = models.PositiveSmallIntegerField(verbose_name=_('Orden'), blank=True, default=None, null=True)
    # user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('Usuario'), blank=True, default=None, null=True, on_delete=models.SET_NULL)
    add_date = models.DateTimeField(verbose_name=_('Fecha de alta'), auto_now_add=True)