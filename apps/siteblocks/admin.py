# -*- coding: utf-8 -*-
from django.contrib import admin
from django import forms
from apps.siteblocks.models import Settings, Contact
from apps.utils.widgets import RedactorMini
from sorl.thumbnail.admin import AdminImageMixin
from mptt.admin import MPTTModelAdmin
from apps.utils.widgets import Redactor

#--Виджеты jquery Редактора
class SettingsAdminForm(forms.ModelForm):
    class Meta:
        model = Settings

    def __init__(self, *args, **kwargs):
        super(SettingsAdminForm, self).__init__(*args, **kwargs)
        try:
            instance = kwargs['instance']
        except KeyError:
            instance = False
        if instance:
            if instance.type == u'input':
                self.fields['value'].widget = forms.TextInput()
            elif instance.type == u'textarea':
                self.fields['value'].widget = forms.Textarea()
            elif instance.type == u'redactor':
                self.fields['value'].widget = Redactor(attrs={'cols': 100, 'rows': 10},)

#--Виджеты jquery Редактора

class SettingsAdmin(admin.ModelAdmin):
    list_display = ('title','name','value',)
    form = SettingsAdminForm
admin.site.register(Settings, SettingsAdmin)

class ContactAdminForm(forms.ModelForm):
    class Meta:
        model = Contact

    class Media:
        js = (
            '/media/js/jquery.js',
            #'http://api-maps.yandex.ru/1.1/index.xml?key=AL-wrE8BAAAAxy9bEgMAl_YRsCtotTo0d6g3O96ykgenhdkAAAAAAAAAAACUSKq_f2kSJDTQEhTMfIyf19Y5Iw==&modules=pmap',
            'http://api-maps.yandex.ru/2.0/?load=package.full&mode=debug&lang=ru-RU',
            '/media/js/ymaps_form.js',
        )

class ContactAdmin(AdminImageMixin, admin.ModelAdmin):
    list_display = ('id','city','address','coord','order','is_published',)
    list_display_links = ('id','city','address',)
    list_editable = ('order','is_published',)
    list_filter = ('is_published',)
    form = ContactAdminForm
admin.site.register(Contact, ContactAdmin)

