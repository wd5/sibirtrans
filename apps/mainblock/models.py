# -*- coding: utf-8 -*-
import os, datetime
from django.utils.translation import ugettext_lazy as _
from django.db import models
from pytils.translit import translify
from apps.utils.utils import ImageField
from apps.utils.managers import PublishedManager
from sorl.thumbnail import get_thumbnail
from django.db.models.signals import post_save


def file_path_countryImage(instance, filename):
    return os.path.join('images','countryImage',  translify(filename).replace(' ', '_') )

def file_path_countryFlags(instance, filename):
    return os.path.join('images','countryFlags',  translify(filename).replace(' ', '_') )

class Country(models.Model):
    title = models.CharField(verbose_name = u'название', max_length = 100)
    second_title = models.CharField(verbose_name = u'название страны в ссылках', max_length = 100, help_text='Например для ссылки "Все туры по ..."')
    icon = ImageField(verbose_name=u'иконка флага', upload_to=file_path_countryFlags)
    image_main = ImageField(verbose_name=u'главное изображение', upload_to=file_path_countryImage)
    image_main_title = models.CharField(verbose_name = u'подпись на главном изображении', max_length = 100, blank=True)
    image_main_title_colorpicker = models.CharField(verbose_name = u'цвет подписи на главном изображении', max_length = 7, blank=True)
    interesting_facts_colorpicker = models.CharField(verbose_name = u'цвет текста итересных фактов', max_length = 7, blank=True)
    map_image = ImageField(verbose_name=u'изображение карты', upload_to=file_path_countryImage)
    map_title = models.CharField(verbose_name = u'заголовок карты', max_length = 50)
    map_subtitle = models.CharField(verbose_name = u'подзаголовок карты', max_length = 50, blank=True)
    #map_text_colorpicker = models.CharField(verbose_name = u'цвет подписи к карте', max_length = 7, blank=True)
    description = models.TextField(verbose_name = u'описание',)
    image_other = ImageField(verbose_name=u'дополнительное изображение', upload_to=file_path_countryImage, blank=True)
    image_other_description = models.TextField(verbose_name = u'описание под дополнительным изображением', blank=True)
    is_popular = models.BooleanField(verbose_name = u'популярное направление', default=False)
    is_published = models.BooleanField(verbose_name = u'Опубликовано', default=True)

    objects = PublishedManager()

    class Meta:
        ordering = ['title']
        verbose_name =_(u'country')
        verbose_name_plural =_(u'countries')

    def __unicode__(self):
        return u'%s' % self.title

    def get_additional_images(self):
        return self.countryimage_set.all()

    def get_facts(self):
        return self.fact_country.all()

    def get_tours(self):
        return self.tour_set.published()

    def get_pop_tours(self):
        return self.tour_set.published().filter(is_popular=True)

    def get_absolute_url(self):
        return u'/countries/%s/' % self.id

    def get_map_cropimg_url(self):
        file, ext = os.path.splitext(self.map_image.url)
        url = file + "_crop.png"
        return url

def pre_crop_map(sender, instance, created, **kwargs):
    from apps.utils.utils import crop_map_image_util
    from django.conf import settings
    file, ext = os.path.splitext(instance.map_image.url)
    url = file + "_crop.png"
    output_size = [300, 300]
    path = "%s%s" % (settings.ROOT_PATH, url)
    if os.path.isfile(path):
        pass
    else:
        try:
            crop_map_image_util(
                post=False,
                original_img=instance.map_image,
                output_size=output_size
            )
        except:
            pass

post_save.connect(pre_crop_map, sender=Country)

class CountryImage(models.Model):
    country = models.ForeignKey(Country, verbose_name=u'страна')
    image = ImageField(verbose_name=u'Картинка', upload_to=file_path_countryImage)
    order = models.IntegerField(verbose_name=u'Порядок сортировки',default=10)

    class Meta:
        ordering = ['-order',]
        verbose_name =_(u'country_photo')
        verbose_name_plural =_(u'country_photos')

    def __unicode__(self):
        return u'изображение для страны %s' %self.country.title

def file_path_serviceImage(instance, filename):
    return os.path.join('images','serviceImage',  translify(filename).replace(' ', '_') )

class Service(models.Model):
    image = ImageField(verbose_name=u'изображение', upload_to=file_path_serviceImage)
    title = models.CharField(verbose_name = u'название', max_length = 50)

    class Meta:
        ordering = ['id']
        verbose_name =_(u'service')
        verbose_name_plural =_(u'services')

    def __unicode__(self):
        return u'%s' % self.title

def file_path_hotelImage(instance, filename):
    return os.path.join('images','hotelImage',  translify(filename).replace(' ', '_') )

class Hotel(models.Model):
    country = models.ForeignKey(Country, verbose_name=u'страна')
    title = models.CharField(verbose_name = u'название', max_length = 100)
    price = models.CharField(verbose_name=u'цена', max_length = 100, blank=True)
    image_main = ImageField(verbose_name=u'главное изображение', upload_to=file_path_hotelImage)
    image_main_title = models.CharField(verbose_name = u'подпись на главном изображении', max_length = 100, blank=True)
    image_main_title_colorpicker = models.CharField(verbose_name = u'цвет подписи на главном изображении', max_length = 7, blank=True)
    interesting_facts_colorpicker = models.CharField(verbose_name = u'цвет текста интересных фактов', max_length = 7, blank=True)
    map_image = ImageField(verbose_name=u'изображение карты', upload_to=file_path_hotelImage)
    map_title = models.CharField(verbose_name = u'заголовок карты', max_length = 50)
    map_subtitle = models.CharField(verbose_name = u'подзаголовок карты', max_length = 50, blank=True)
    #map_text_colorpicker = models.CharField(verbose_name = u'цвет подписи к карте', max_length = 7, blank=True)
    description = models.TextField(verbose_name = u'описание',)
    short_description = models.TextField(verbose_name = u'краткое описание',)
    conditions_text = models.TextField(verbose_name = u'условия проживания',)
    service = models.ManyToManyField(Service, verbose_name=u'сервис', blank=True, null=True)

    order = models.IntegerField(verbose_name=u'Порядок сортировки',default=10)
    is_published = models.BooleanField(verbose_name = u'Опубликовано', default=True)

    objects = PublishedManager()

    class Meta:
        ordering = ['-order']
        verbose_name =_(u'hotel')
        verbose_name_plural =_(u'hotels')

    def __unicode__(self):
        return u'%s' % self.title

    def get_additional_images(self):
        return self.hotelimage_set.all()

    def get_orders(self):
        return self.order_set_hotel.all()

    def get_absolute_url(self):
        return u'/hotels/%s/' % self.id

    def get_facts(self):
        return self.fact_hotel.all()

    def get_services(self):
        return self.service.all()

    def get_map_cropimg_url(self):
        file, ext = os.path.splitext(self.map_image.url)
        url = file + "_crop.png"
        return url

post_save.connect(pre_crop_map, sender=Hotel)

class HotelImage(models.Model):
    hotel = models.ForeignKey(Hotel, verbose_name=u'страна')
    image = ImageField(verbose_name=u'Картинка', upload_to=file_path_hotelImage)
    order = models.IntegerField(verbose_name=u'Порядок сортировки',default=10)

    class Meta:
        ordering = ['-order',]
        verbose_name =_(u'country_photo')
        verbose_name_plural =_(u'country_photos')

    def __unicode__(self):
        return u'изображение для отеля %s' %self.hotel.title

type_choices = (
    (u'exclusive',u'Эксклюзивный'),
    (u'health',u'Лечебный'),
    (u'hot',u'Горящий'),
)

def file_path_tourImage(instance, filename):
    return os.path.join('images','tourImage',  translify(filename).replace(' ', '_') )

class IntegerRangeField(models.IntegerField):
    def __init__(self, verbose_name=None, name=None, min_value=None, max_value=None, **kwargs):
        self.min_value, self.max_value = min_value, max_value
        models.IntegerField.__init__(self, verbose_name, name, **kwargs)
    def formfield(self, **kwargs):
        defaults = {'min_value': self.min_value, 'max_value':self.max_value}
        defaults.update(kwargs)
        return super(IntegerRangeField, self).formfield(**defaults)

def str_price(price):
    if not price:
        return u'0'
    value = u'%s' %price
    if price._isinteger():
        value = u'%s' %value[:len(value)-3]
        count = 3
    else:
        count = 6

    if len(value)>count:
        ends = value[len(value)-count:]
        starts = value[:len(value)-count]

        if len(starts)>3:
            starts = u'%s %s' % (starts[:1],starts[1:len(starts)])

        return u'%s %s' %(starts, ends)
    else:
        return u'%s' % value

class Tour(models.Model):
    country = models.ManyToManyField(Country, verbose_name=u'страна')
    hotel = models.ManyToManyField(Hotel, verbose_name=u'отель')
    title = models.CharField(verbose_name = u'название', max_length = 100)
    image_main = ImageField(verbose_name=u'изображение для тура', upload_to=file_path_tourImage)
    description = models.TextField(verbose_name = u'описание',)
    price = models.DecimalField(verbose_name=u'цена', decimal_places=2, max_digits=10)
    stars = IntegerRangeField(verbose_name=u'количество звёзд 1-5', min_value=1, max_value=5, blank=True, null=True)
    type = models.CharField(max_length=20, verbose_name=u'тип', choices=type_choices, blank=True)
    start_date = models.DateTimeField(verbose_name = u'Тур стартует', default=datetime.datetime.now)
    start_date_text = models.CharField(verbose_name = u'Текст над стартовой чертой', max_length = 100, blank=True)

    first_day_number = models.SmallIntegerField(verbose_name=u'число для первого дня', blank=True, null=True)
    first_day_title = models.CharField(verbose_name = u'название для первого дня', max_length = 50, blank=True)
    first_day_image = ImageField(verbose_name=u'изображение для первого дня', upload_to=file_path_tourImage, blank=True)

    second_day_number = models.SmallIntegerField(verbose_name=u'число для второго дня', blank=True, null=True)
    second_day_title = models.CharField(verbose_name = u'название для второго дня', max_length = 50, blank=True)
    second_day_image = ImageField(verbose_name=u'изображение для второго дня', upload_to=file_path_tourImage, blank=True)

    third_day_number = models.SmallIntegerField(verbose_name=u'число для третьего дня', blank=True, null=True)
    third_day_title = models.CharField(verbose_name = u'название для третьего дня', max_length = 50, blank=True)
    third_day_image = ImageField(verbose_name=u'изображение для третьего дня', upload_to=file_path_tourImage, blank=True)

    is_popular = models.BooleanField(verbose_name = u'популярный тур', default=False)
    order = models.IntegerField(verbose_name=u'Порядок сортировки',default=10)
    is_published = models.BooleanField(verbose_name = u'Опубликовано', default=True)

    objects = PublishedManager()

    class Meta:
        ordering = ['-order']
        verbose_name =_(u'tour')
        verbose_name_plural =_(u'tours')

    def __unicode__(self):
        return u'%s' % self.title

    def get_additional_images(self):
        return self.tourimage_set.all()

    def get_tour_slider_images(self):
        return self.tourimageslider_set.published()

    def get_orders(self):
        return self.order_set_tour.all()

    def get_countries(self):
        return self.country.all()

    def get_hotels(self):
        return self.hotel.all()

    def get_str_price(self):
        result = str_price(self.price)
        return result

    def get_countries(self):
        return self.country.all()

    def get_absolute_url(self):
        return u'/tours/%s/' % self.id

class TourImage(models.Model):
    tour = models.ForeignKey(Tour, verbose_name=u'тур')
    image = ImageField(verbose_name=u'Картинка', upload_to=file_path_tourImage)
    order = models.IntegerField(verbose_name=u'Порядок сортировки',default=10)

    class Meta:
        ordering = ['-order',]
        verbose_name =_(u'country_photo')
        verbose_name_plural =_(u'country_photos')

    def __unicode__(self):
        return u'изображение к туру %s' %self.tour.title

class TourImageSlider(models.Model):
    tour = models.ForeignKey(Tour, verbose_name=u'тур')
    image_main = ImageField(verbose_name=u'главное изображение', upload_to=file_path_tourImage)
    image_main_title = models.CharField(verbose_name = u'подпись на главном изображении', max_length = 100, blank=True)
    image_main_title_colorpicker = models.CharField(verbose_name = u'цвет подписи на главном изображении', max_length = 7, blank=True)
    interesting_facts_colorpicker = models.CharField(verbose_name = u'цвет текста интересных фактов', max_length = 7, blank=True)
    map_image = ImageField(verbose_name=u'изображение карты', upload_to=file_path_tourImage)
    map_title = models.CharField(verbose_name = u'заголовок карты', max_length = 50)
    map_subtitle = models.CharField(verbose_name = u'подзаголовок карты', max_length = 50, blank=True)
    #map_text_colorpicker = models.CharField(verbose_name = u'цвет подписи к карте', max_length = 7, blank=True)

    order = models.IntegerField(verbose_name=u'Порядок сортировки',default=10)
    is_published = models.BooleanField(verbose_name = u'Опубликовано', default=True)

    objects = PublishedManager()

    class Meta:
        ordering = ['-order']
        verbose_name =_(u'tour_slider_image')
        verbose_name_plural =_(u'tour_slider_images')

    def __unicode__(self):
        return u'%s' % self.image_main_title

    def get_facts(self):
        return self.fact_tour_is.all()

    def get_map_cropimg_url(self):
        file, ext = os.path.splitext(self.map_image.url)
        url = file + "_crop.png"
        return url

post_save.connect(pre_crop_map, sender=TourImageSlider)

class Fact(models.Model):
    country = models.ForeignKey(Country, verbose_name=u'страна', blank=True, null=True, related_name='fact_country')
    hotel = models.ForeignKey(Hotel, verbose_name=u'страна', blank=True, null=True, related_name='fact_hotel')
    tour_is = models.ForeignKey(TourImageSlider, verbose_name=u'слайдер для тура', blank=True, null=True, related_name='fact_tour_is')
    value = models.IntegerField(verbose_name=u'значение')
    title = models.CharField(verbose_name=u'подпись', max_length=100)
    order = models.IntegerField(verbose_name=u'Порядок сортировки',default=10)
    is_published = models.BooleanField(verbose_name = u'Опубликовано', default=True)

    objects = PublishedManager()

    class Meta:
        ordering = ['-order',]
        verbose_name =_(u'fact')
        verbose_name_plural =_(u'facts')

    def __unicode__(self):
        return u'интересный факт №%s' %self.id

class AdvertasingOnMain(models.Model):
    tour = models.ForeignKey(Tour, verbose_name=u'тур')
    image = ImageField(verbose_name=u'Картинка', upload_to=file_path_tourImage)

    class Meta:
        verbose_name =_(u'advertasing_item')
        verbose_name_plural =_(u'advertasing_items')

    def __unicode__(self):
        return u'предложение на главной странице №%s' %self.id

    def admin_adv_preview(self):
        image = self.image
        if image:
            im = get_thumbnail(self.image, '96x96', crop='center', quality=99)
            return u'<span><img src="%s" width="96" height="96"></span>' %im.url
        else:
            return u'<span></span>'
    admin_adv_preview.allow_tags = True
    admin_adv_preview.short_description = u'Превью'

class Order(models.Model):
    fullname = models.CharField(verbose_name = u'полное имя', max_length = 100)
    contacts = models.TextField(verbose_name = u'контактные данные')
    note = models.TextField(verbose_name = u'дополнительная информация', blank=True)
    tour = models.ForeignKey(Tour, verbose_name=u'тур', blank=True, null=True, related_name='order_set_tour')
    hotel = models.ForeignKey(Hotel, verbose_name=u'отель', blank=True, null=True, related_name='order_set_hotel')
    create_date = models.DateTimeField(verbose_name=u'Дата оформления', default=datetime.datetime.now)

    class Meta:
        verbose_name = _(u'order')
        verbose_name_plural = _(u'orders')
        ordering = ('-create_date',)

    def __unicode__(self):
        return u'заказ №%s' % self.id
