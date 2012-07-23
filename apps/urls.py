# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, include, url

#from apps.app.urls import urlpatterns as app_url

from views import index, set_cookie_contact_id, for_tourists

urlpatterns = patterns('',
    url(r'^$',index, name='index'),
    url(r'^countries/$',index, name='countries'),
    url(r'^for_tourists/$',for_tourists, {'slug':'visa'}, name='for_tourists'),
    (r'^for_tourists/(?P<slug>[^/]+)/', for_tourists),

    (r'^about/contacts/', 'apps.siteblocks.views.show_contacts'),

    (r'^set_cookie_contact_id/', set_cookie_contact_id),


)
#url(r'^captcha/', include('captcha.urls')),

#urlpatterns += #app_url


