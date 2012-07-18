# -*- coding: utf-8 -*-
from django.contrib import admin

from apps.slider.models import Photo
from sorl.thumbnail.admin import AdminImageMixin
from apps.utils.widgets import AdminImageCrop
from django import forms

class PhotoAdminForm(forms.ModelForm):
    image = forms.ImageField(
    	widget=AdminImageCrop(attrs={'path': 'slider/photo'}), 
    	label=u'Изображение'
    )
    model = Photo

class PhotoAdmin(AdminImageMixin, admin.ModelAdmin):
    list_display = ('id','admin_photo_preview','order','show',)
    list_display_links = ('id','admin_photo_preview',)
    list_editable = ('order','show',)
    list_filter = ('show',)
    form = PhotoAdminForm
    
admin.site.register(Photo, PhotoAdmin)