# -*- coding: utf-8 -*-
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView, View
from apps.siteblocks.models import Contact
from apps.pages.models import Page
from apps.mainblock.models import Country, AdvertasingOnMain
from apps.faq.forms import QuestionForm
from apps.faq.models import Question


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['pop_countries'] = Country.objects.filter(is_published=True, is_popular=True)
        context['advertasing'] = AdvertasingOnMain.objects.order_by('?')[:3]
        return context

index = IndexView.as_view()

class SetCookieContactView(View):
    def post(self, request, *args, **kwargs):
        if not request.is_ajax():
            return HttpResponseBadRequest()
        else:
            if 'st_contact_city' not in request.POST:
                return HttpResponseBadRequest()
            else:
                st_contact_city = request.POST['st_contact_city']

            try:
                curr_contact = Contact.objects.get(city=st_contact_city)
                contact_id = curr_contact.id
            except:
                curr_contact = False
                contact_id = False

            response = HttpResponse()

            if not curr_contact:
                cookies = request.COOKIES
                contact_id = False
                if 'st_contact_id' in cookies:
                    contact_id = cookies['st_contact_id']

            response.set_cookie('st_contact_id', contact_id, 1209600)
            return response

set_cookie_contact_id = csrf_exempt(SetCookieContactView.as_view())

class ForTouristsView(TemplateView):
    template_name = 'pages/default_for_tourists.html'

    def get_context_data(self, **kwargs):
        context = super(ForTouristsView, self).get_context_data(**kwargs)

        slug_name = self.kwargs.get('slug', None)
        context['form'] = QuestionForm

        try:
            context['page'] = Page.objects.get(id=5)
        except:
            context['page'] = False
        if  slug_name=='faq':
            context['questions'] = Question.objects.published()
        else:
            try:
                context['current_page'] = Page.objects.get(url='/%s/' % slug_name)
            except:
                context['current_page'] = False

        return context

for_tourists = ForTouristsView.as_view()
