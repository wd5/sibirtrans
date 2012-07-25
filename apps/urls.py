# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, include, url

#from apps.app.urls import urlpatterns as app_url
from django.views.decorators.csrf import csrf_exempt

from views import index, set_cookie_contact_id, for_tourists
from apps.mainblock.views import items_loader, load_tours_list, prepare_order

urlpatterns = patterns('',
    url(r'^$',index, name='index'),
    (r'^load_items/$',csrf_exempt(items_loader)),
    (r'^load_tours/$',csrf_exempt(load_tours_list)),
    (r'^prepare_order/(?P<tour>[^/]+)/(?P<hotel>[^/]+)/$',csrf_exempt(prepare_order)),
    (r'^send_order/$','apps.mainblock.views.SaveOrderForm'),
    url(r'^countries/$','apps.mainblock.views.countries_list', name='countries'),
    url(r'^countries/(?P<pk>[^/]+)/$','apps.mainblock.views.show_country', name='show_country'),
    url(r'^hotels/$','apps.mainblock.views.hotels_list', name='hotels'),
    url(r'^hotels/(?P<pk>[^/]+)/$','apps.mainblock.views.show_hotel', name='show_hotel'),
    url(r'^tours/$','apps.mainblock.views.tours_list', name='tours'),
    (r'^tours/luckytour/$','apps.mainblock.views.random_tour'),
    url(r'^tours/(?P<pk>[^/]+)/$','apps.mainblock.views.show_tour', name='show_tour'),
    url(r'^for_tourists/$',for_tourists, {'slug':'visa'}, name='for_tourists'),
    (r'^for_tourists/(?P<slug>[^/]+)/', for_tourists),

    (r'^about/contacts/', 'apps.siteblocks.views.show_contacts'),

    (r'^set_cookie_contact_id/', set_cookie_contact_id),
    (r'^faq/checkform/$','apps.faq.views.SaveQuestionForm'),

)
#url(r'^captcha/', include('captcha.urls')),

#urlpatterns += #app_url


