# -*- coding: utf-8 -*-
from django.contrib import admin
from django import forms
from apps.mainblock.models import Country,CountryImage,Hotel,HotelImage,Tour,TourImage,TourImageSlider,Order,AdvertasingOnMain, Service, Fact
from apps.utils.widgets import RedactorMini, Redactor, ColorPicker
from sorl.thumbnail.admin import AdminImageMixin
from mptt.admin import MPTTModelAdmin

class FactInline(admin.TabularInline):
    fields = ('value','title','order','is_published')
    model = Fact

class CountryAdminForm(forms.ModelForm):
    image_main_title_colorpicker = forms.CharField(widget=ColorPicker,label = u'Цвет подписи на главном изображении',)
    interesting_facts_colorpicker = forms.CharField(widget=ColorPicker,label = u'Цвет текста итересных фактов',)
    interesting_facts = forms.CharField(widget=Redactor(attrs={'cols': 170, 'rows': 20}),label = u'Интересные факты',)
    description = forms.CharField(widget=Redactor(attrs={'cols': 170, 'rows': 20}),label = u'Описание',)
    image_other_description = forms.CharField(widget=Redactor(attrs={'cols': 170, 'rows': 20}),label = u'Описание под дополнительным изображением',)

    class Meta:
        model = Country

class CountryImageInline(AdminImageMixin, admin.TabularInline):
    model = CountryImage

class CountryAdmin(AdminImageMixin, admin.ModelAdmin):
    list_display = ('id','title','is_popular','is_published',)
    list_display_links = ('id','title',)
    list_editable = ('is_popular','is_published',)
    search_fields = ('title','image_main_title', 'interesting_facts', 'map_title',
                     'map_subtitle', 'description', 'image_other_description',)
    list_filter = ('is_popular','is_published',)
    inlines = [FactInline, CountryImageInline]
    form = CountryAdminForm
    fieldsets = (
            (None, {
                'fields': ('title',)
            }),
            ('Главное изображение', {
                'classes': ('collapse',),
                'fields': ('image_main', 'image_main_title', 'image_main_title_colorpicker', 'interesting_facts_colorpicker',)
            }),
            ('Карта', {
                'classes': ('collapse',),
                'fields': ('map_image', 'map_title', 'map_subtitle',)
            }),
            (None, {
                'fields': ('description',)
            }),
            ('Дополнительное изображение', {
                'classes': ('collapse',),
                'fields': ('image_other','image_other_description',)
            }),
            (None, {
                'fields': ('is_popular','is_published',)
            }),
        )

admin.site.register(Country, CountryAdmin)

class ServiceAdmin(admin.ModelAdmin):
    list_display = ('id','title',)
    list_display_links = ('id','title',)
    search_fields = ('title',)

admin.site.register(Service, ServiceAdmin)

class HotelAdminForm(forms.ModelForm):
    image_main_title_colorpicker = forms.CharField(widget=ColorPicker,label = u'Цвет подписи на главном изображении',)
    interesting_facts_colorpicker = forms.CharField(widget=ColorPicker,label = u'Цвет текста итересных фактов',)
    interesting_facts = forms.CharField(widget=Redactor(attrs={'cols': 170, 'rows': 20}),label = u'Интересные факты',)
    description = forms.CharField(widget=Redactor(attrs={'cols': 170, 'rows': 20}),label = u'Описание',)
    conditions_text = forms.CharField(widget=Redactor(attrs={'cols': 170, 'rows': 20}),label = u'Условия проживания',)
    short_description = forms.CharField(widget=Redactor(attrs={'cols': 170, 'rows': 20}),label = u'Краткое описание',)

    class Meta:
        model = Hotel

class HotelImageInline(AdminImageMixin, admin.TabularInline):
    model = HotelImage

class HotelAdmin(AdminImageMixin, admin.ModelAdmin):
    list_display = ('id','title','country','order','is_published',)
    list_display_links = ('id','title','country',)
    list_editable = ('order','is_published',)
    search_fields = ('title','image_main_title', 'interesting_facts', 'map_title',
                     'map_subtitle', 'description',  'short_description', 'conditions_text',)
    list_filter = ('country','service','is_published',)
    filter_horizontal = ('service',)
    inlines = [FactInline, HotelImageInline,]
    form = HotelAdminForm
    fieldsets = (
            (None, {
                'fields': ('country','title',)
            }),
            ('Главное изображение', {
                'classes': ('collapse',),
                'fields': ('image_main', 'image_main_title', 'image_main_title_colorpicker', 'interesting_facts_colorpicker',)
            }),
            ('Карта', {
                'classes': ('collapse',),
                'fields': ('map_image', 'map_title', 'map_subtitle',)
            }),
            ('Описание и условия проживания', {
                'classes': ('collapse',),
                'fields': ('description','short_description','conditions_text')
            }),
            (None, {
                'fields': ('service','order','is_published',)
            }),
        )

admin.site.register(Hotel, HotelAdmin)

class TourImageInline(AdminImageMixin, admin.TabularInline):
    model = TourImage

class TourAdminForm(forms.ModelForm):
    description = forms.CharField(widget=Redactor(attrs={'cols': 170, 'rows': 20}),label = u'Описание',)

    class Meta:
        model = Tour

class TourAdmin(AdminImageMixin, admin.ModelAdmin):
    list_display = ('id','title','price','order','is_published',)
    list_display_links = ('id','title',)
    list_editable = ('price','order','is_published',)
    search_fields = ('title','price', 'stars', 'start_date_text', 'first_day_title',
                     'second_day_title', 'third_day_title', )
    list_filter = ('hotel','country','price','is_published','start_date',)
    filter_horizontal = ('hotel',)
    exclude = ('country',)
    form = TourAdminForm
    inlines = [TourImageInline,]
    fieldsets = (
                (None, {
                    'fields': ('title','description','price','stars','type',)
                }),
                ('Блок стартовой черты', {
                    'classes': ('collapse',),
                    'fields': ('start_date','start_date_text',)
                }),
                ('день 1', {
                    'classes': ('collapse',),
                    'fields': ('first_day_number','first_day_title','first_day_image',)
                }),
                ('день 2', {
                    'classes': ('collapse',),
                    'fields': ('second_day_number','second_day_title','second_day_image',)
                }),
                ('день 3', {
                    'classes': ('collapse',),
                    'fields': ('third_day_number','third_day_title','third_day_image',)
                }),
                (None, {
                    'fields': ('hotel','order','is_published',)
                }),
            )

admin.site.register(Tour, TourAdmin)

class TourImageSlideAdminForm(forms.ModelForm):
    image_main_title_colorpicker = forms.CharField(widget=ColorPicker,label = u'Цвет подписи на главном изображении',)
    interesting_facts_colorpicker = forms.CharField(widget=ColorPicker,label = u'Цвет текста итересных фактов',)
    interesting_facts = forms.CharField(widget=Redactor(attrs={'cols': 170, 'rows': 20}),label = u'Интересные факты',)

    class Meta:
        model = TourImageSlider

class TourImageSlideAdmin(AdminImageMixin, admin.ModelAdmin):
    list_display = ('id','tour','image_main_title','order','is_published',)
    list_display_links = ('id','tour','image_main_title',)
    list_editable = ('order','is_published',)
    search_fields = ('image_main_title', 'map_title', 'map_subtitle',)
    list_filter = ('tour','is_published',)
    inlines = [FactInline,]
    form = TourImageSlideAdminForm

admin.site.register(TourImageSlider, TourImageSlideAdmin)

class AdvertasingOnMainAdmin(AdminImageMixin, admin.ModelAdmin):
    list_display = ('id','admin_adv_preview','tour',)
    list_display_links = ('id','tour',)

admin.site.register(AdvertasingOnMain, AdvertasingOnMainAdmin)

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id','fullname','create_date','tour','hotel',)
    list_display_links = ('id','fullname','create_date','tour','hotel',)
    search_fields = ('fullname','contacts', 'note', )
    readonly_fields = ('fullname','contacts', 'note', 'tour','hotel','create_date',)
    list_filter = ('tour','hotel','create_date',)

admin.site.register(Order, OrderAdmin)
