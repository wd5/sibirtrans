# -*- coding: utf-8 -*-
from apps.pages.models import Page
from apps.utils.utils import url_spliter
from django import template

register = template.Library()

@register.inclusion_tag("pages/block_page_summary.html")
def block_page_summary(alias):
    try:
        page = Page.objects.get(url=alias)
        return {'page': page}
    except Page.DoesNotExist:
        return {}


@register.inclusion_tag("pages/block_menu.html")
def block_menu(url):
    current = url_spliter(url, 1)
    menu = Page.objects.filter(parent=None, is_published=True, is_at_menu=True)
    return {'menu': menu, 'current': current}


@register.inclusion_tag("pages/block_footer_menu.html")
def block_footer_menu(url):
    current = url_spliter(url, 1)
    menu = Page.objects.filter(parent=None, is_published=True, is_at_footer_menu=True)
    return {'menu': menu, 'current': current}


@register.inclusion_tag("pages/for_tourists_menu.html")
def for_tourists_menu(param):
    if param == 'title':
        title = True
    else:
        title = False
    try:
        page = Page.objects.get(id=5)
    except:
        page = False
    return {'page': page, 'title': title}