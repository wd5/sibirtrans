# -*- coding: utf-8 -*-

from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.simple import direct_to_template
from apps.pages.models import Page
from apps.siteblocks.models import Settings
import settings

def index(request):
    try:
        page = Page.objects.get(url = 'index')
    except Page.DoesNotExist:
        page = False
    return direct_to_template(request, 'pages/index.html', locals())

def page(request, url):
    if not url.endswith('/'):
        return HttpResponseRedirect("%s/" % request.path)
    if not url.startswith('/'):
        url = "/" + url

    # вывод страниц нижнего уровня
    spl_url = url
    if spl_url.startswith('/'):
        spl_url = spl_url[1:]
    if spl_url.endswith('/'):
        spl_url = spl_url[:-1]
    spl_url = spl_url.split('/')
    first = True
    for item in spl_url:
        if first:
            page = get_object_or_404(Page, url__exact="/" + item + "/")
            first = False
        else:
            page = get_object_or_404(page.get_children(), url__exact="/" + item + "/")

    #page = get_object_or_404(Page, url__exact=url)
    return direct_to_template(request, 'pages/default.html', locals())

@csrf_exempt
def static_page(request, template):
    return direct_to_template(request, template, locals())