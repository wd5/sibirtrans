# -*- coding: utf-8 -*-
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView, View, ListView
from apps.siteblocks.models import Contact
from apps.pages.models import Page


class ShowContactsView(ListView):
    model = Contact
    template_name = 'siteblocks/show_contacts.html'
    context_object_name = 'contacts'
    queryset = model.objects.published()

    def get_context_data(self, **kwargs):
        context = super(ShowContactsView, self).get_context_data(**kwargs)
        queryset = Contact.objects.published()
        cookies = self.request.COOKIES
        contact_id = False
        if 'st_contact_id' in cookies:
            try:
                contact_id = int(cookies['st_contact_id'])
            except:
                contact_id = False

        try:
            context['page'] = Page.objects.get(url='/contacts/')
        except:
            context['page'] = False

        try:
            context['contact_curr'] = queryset.get(pk=contact_id)
        except:
            context['contact_curr'] = queryset[0]

        return context

show_contacts = ShowContactsView.as_view()
