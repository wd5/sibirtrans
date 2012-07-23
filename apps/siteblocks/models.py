# -*- coding: utf-8 -*-
import os
from django.utils.translation import ugettext_lazy as _
from django.db import models
from pytils.translit import translify
from apps.utils.utils import ImageField
from apps.utils.managers import PublishedManager

type_choices = (
    (u'input',u'input'),
    (u'textarea',u'textarea'),
    (u'redactor',u'redactor'),
)

class Settings(models.Model):
    title = models.CharField(
        verbose_name = u'Название',
        max_length = 150,
    )
    name = models.CharField( 
        verbose_name = u'Служебное имя',
        max_length = 250,
    )
    value = models.TextField(
        verbose_name = u'Значение'
    )
    type = models.CharField(
        max_length=20,
        verbose_name=u'Тип значения',
        choices=type_choices
    )
    class Meta:
        verbose_name =_(u'site_setting')
        verbose_name_plural =_(u'site_settings')

    def __unicode__(self):
        return u'%s' % self.name

class Contact(models.Model):
    city = models.CharField(verbose_name = u'город',max_length = 100)
    city_in = models.CharField(verbose_name = u'в',max_length = 100, help_text=u'например Москва, тогда в: Москве')
    address = models.CharField(verbose_name = u'адрес',max_length = 255)
    phone = models.CharField(verbose_name = u'номер телефона',max_length = 255)
    coord = models.CharField(max_length=100, verbose_name=u'Координаты')
    map = models.CharField(max_length=1, verbose_name=u'Карта', blank=True)
    order = models.IntegerField(u'порядок сортировки', help_text=u'Чем больше число, тем выше располагается элемент', default=10)
    is_published = models.BooleanField(verbose_name = u'Опубликовано', default=True)

    objects = PublishedManager()

    class Meta:
        ordering = ['-order']
        verbose_name =_(u'contact')
        verbose_name_plural =_(u'contacts')

    def __unicode__(self):
        return u'%s' % self.city