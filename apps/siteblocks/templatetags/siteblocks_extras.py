# -*- coding: utf-8 -*-
from apps.siteblocks.models import Settings, Contact
from django import template

register = template.Library()

@register.inclusion_tag("siteblocks/block_setting.html")
def block_static(name):
    try:
        setting = Settings.objects.get(name=name)
    except Settings.DoesNotExist:
        setting = False
    return {'block': block, }


@register.inclusion_tag("siteblocks/block_header_contacts.html", takes_context=True)
def header_contacts(context):
    if 'request' in context:
        request = context['request']

    cookies = request.COOKIES
    contact_id = False
    if 'st_contact_id' in cookies:
        contact_id = cookies['st_contact_id']

    contacts = Contact.objects.published()
    try:
        if contact_id:
            try:
                latest = Contact.objects.get(id=contact_id)
            except:
                latest = contacts.latest('order')
        else:
            latest = contacts.latest('order')
    except:
        latest = False
    try:
        contacts = contacts.exclude(pk=latest.id)
    except:
        pass
    return {'contacts': contacts, 'latest': latest}
