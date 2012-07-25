# -*- coding: utf-8 -*-
from django.core.mail.message import EmailMessage
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView, View, DetailView, ListView, FormView
from apps.mainblock.models import Country, AdvertasingOnMain, Tour, Hotel
from apps.mainblock.forms import OrderForm
from django.db.models.loading import get_model
from django.db.models import Max, Min
from apps.siteblocks.models import Settings
from apps.utils.utils import crop_map_image_util
import settings

class CropMapImage(TemplateView):
    template_name = 'utils/crop_image.html'
    output_size = [300, 300]

    def get_image(self, action):
        return action.map_image

    def get(self, request, **kwargs):
        model_name = self.kwargs.get('model', None)
        item_id = self.kwargs.get('pk', None)

        model = get_model('mainblock', model_name)
        object = model.objects.get(pk=item_id)

        context = self.get_context_data(**kwargs)
        context['image'] = object.map_image
        context['output_size'] = self.output_size
        return self.render_to_response(context)

    def post(self, request, **kwargs):
        next = request.REQUEST.get('next', None)
        model_name = self.kwargs.get('model', None)
        item_id = self.kwargs.get('pk', None)

        model = get_model('mainblock', model_name)
        object = model.objects.get(pk=item_id)

        crop_map_image_util(
            post=request.POST,
            original_img=object.map_image,
            output_size=self.output_size
        )
        return HttpResponseRedirect(next)

crop_map_image = CropMapImage.as_view()

class ShowCountryView(DetailView):
    model = Country
    context_object_name = 'country'
    template_name = 'mainblock/show_country.html'

    def get_context_data(self, **kwargs):
        context = super(ShowCountryView, self).get_context_data()
        additional_images = self.object.get_additional_images()
        context['right_attached_photos'] = additional_images[:22]
        context['left_attached_photos'] = additional_images[22:]
        context['pop_tours'] = self.object.get_pop_tours()[:2]
        return context

show_country = ShowCountryView.as_view()


class ShowCountriesListView(ListView):
    model = Country
    context_object_name = 'countries'
    queryset = Country.objects.published()

countries_list = ShowCountriesListView.as_view()


class ShowHotelView(DetailView):
    model = Hotel
    context_object_name = 'hotel'
    template_name = 'mainblock/show_hotel.html'

    def get_context_data(self, **kwargs):
        context = super(ShowHotelView, self).get_context_data()
        additional_images = self.object.get_additional_images()
        context['right_attached_photos'] = additional_images[:22]
        context['left_attached_photos'] = additional_images[22:]
        #context['pop_tours'] = self.object.get_pop_tours()[:2]
        return context

show_hotel = ShowHotelView.as_view()


class ShowHotelsListView(ListView):
    model = Hotel
    context_object_name = 'hotels'
    queryset = Hotel.objects.published()

hotels_list = ShowHotelsListView.as_view()


class ShowTourView(DetailView):
    model = Tour
    context_object_name = 'tour'
    template_name = 'mainblock/show_tour.html'

    def get_context_data(self, **kwargs):
        context = super(ShowTourView, self).get_context_data()
        additional_images = self.object.get_additional_images()
        context['right_attached_photos'] = additional_images[:22]
        context['left_attached_photos'] = additional_images[22:]
        hotels = self.object.get_hotels()
        hotel = hotels[0]
        context['hotel'] = hotel
        context['other_hotels'] = hotels.exclude(id=hotel.id)
        return context

show_tour = ShowTourView.as_view()

class ShowRandomTourView(TemplateView):
    template_name = 'mainblock/show_tour.html'

    def get_context_data(self, **kwargs):
        context = super(ShowRandomTourView, self).get_context_data()
        random_tour_set = Tour.objects.published().order_by('?')
        try:
            tour = random_tour_set[0]
        except:
            tour = False

        if tour:
            context['tour'] = tour
            additional_images = tour.get_additional_images()
            context['right_attached_photos'] = additional_images[:22]
            context['left_attached_photos'] = additional_images[22:]
            hotels = tour.get_hotels()
            hotel = hotels[0]
            context['hotel'] = hotel
            context['other_hotels'] = hotels.exclude(id=hotel.id)
        else:
            self.template_name = 'index.html'
            context['pop_countries'] = Country.objects.filter(is_published=True, is_popular=True)
            context['advertasing'] = AdvertasingOnMain.objects.order_by('?')[:3]
        return context

random_tour = ShowRandomTourView.as_view()

def GetLoadIdsPage(queryset, loaded_count): #для пагинации
    counter = 0
    id_loaded_items = ''
    for item in queryset:
        counter = counter + 1
        div = counter % loaded_count
        id_loaded_items = u'%s,%s' % (id_loaded_items, item.id)
        if div == 0:
            id_loaded_items = u'%s|' % id_loaded_items

    if id_loaded_items.startswith(',') or id_loaded_items.startswith('|'):
        id_loaded_items = id_loaded_items[1:]
    if id_loaded_items.endswith(',') or id_loaded_items.endswith('|'):
        id_loaded_items = id_loaded_items[:-1]
    id_loaded_items = id_loaded_items.replace('|,', '|')

    result = u'False!%s' % id_loaded_items
    return result


class ShowToursListView(TemplateView):
    template_name = 'mainblock/tour_list.html'

    def get_context_data(self, **kwargs):
        context = super(ShowToursListView, self).get_context_data()
        publ_tours = Tour.objects.published()

        type_val = self.request.GET.get('type', None)
        country_id = self.request.GET.get('by_country', None)
        if type_val:
            publ_tours = publ_tours.filter(type=type_val)

        if country_id:
            publ_tours = publ_tours.filter(country__id=country_id)

        if type_val == None:
            item_first_set = publ_tours.filter(is_popular=True).order_by("?")
            try:
                item_first = item_first_set[0]
                context['item_first'] = item_first
                context['tours'] = publ_tours.exclude(id=item_first.id)
            except:
                item_first = False
                context['tours'] = publ_tours
        else:
            context['tours'] = publ_tours

        dic = publ_tours.aggregate(Min('price'), Max('price'))
        context['max_price'] = dic['price__max']
        context['min_price'] = dic['price__min']
        loaded_count = 12 # количество туров на одной странице не считая главного item_first
        queryset = context['tours']
        result = GetLoadIdsPage(queryset, loaded_count)
        splited_result = result.split('!')
        next_id_loaded_items = splited_result[1]
        next_id_loaded_items_array = next_id_loaded_items.split('|')
        try:
            curr_ids = next_id_loaded_items_array[0]
        except:
            curr_ids = False
        page_prev = False
        try:
            page_next = next_id_loaded_items_array[1]
        except:
            next_id_loaded_items_array = False
            page_next = False

        context['tours'] = context['tours'][:loaded_count]
        context['next_id_loaded_items'] = next_id_loaded_items_array
        context['curr_ids'] = curr_ids
        context['type'] = type_val
        context['page_prev'] = page_prev
        context['page_next'] = page_next

        return context

tours_list = ShowToursListView.as_view()


class LoadToursView(View):
    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            if 'type' not in request.POST:
                return HttpResponseBadRequest()

            if 'price_max' in request.POST:
                try:
                    price_max = int(request.POST['price_max'])
                except:
                    return HttpResponseBadRequest()
            else:
                price_max = False

            if 'max_star' in request.POST:
                try:
                    max_star = request.POST['max_star']
                except:
                    return HttpResponseBadRequest()
            else:
                max_star = False

            queryset = Tour.objects.published()
            type_val = request.POST['type']
            if type_val != 'all':
                queryset = queryset.filter(type=type_val)

            if price_max:
                queryset = queryset.filter(price__lte=price_max)

            if max_star:
                queryset = queryset.filter(stars__lte=max_star)

            dic = queryset.aggregate(Min('price'), Max('price'))
            max_price = dic['price__max']
            min_price = dic['price__min']

            loaded_count = 12

            result = GetLoadIdsPage(queryset, loaded_count)
            splited_result = result.split('!')
            try:
                remaining_count = int(splited_result[0])
            except:
                remaining_count = False
            next_id_loaded_items = splited_result[1]
            next_id_loaded_items_array = next_id_loaded_items.split('|')
            try:
                curr_ids = next_id_loaded_items_array[0]
            except:
                curr_ids = False
            page_prev = False
            try:
                page_next = next_id_loaded_items_array[1]
            except:
                next_id_loaded_items_array = False
                page_next = False

            items_html = render_to_string(
                'mainblock/tours_template.html',
                    {'tours': queryset[:loaded_count], 'request': request,
                     'type': type_val, 'next_id_loaded_items': next_id_loaded_items_array, 'curr_ids': curr_ids,
                     'page_prev': page_prev, 'page_next': page_next,
                     'max_price': max_price, 'min_price': min_price}
            )
            return HttpResponse(items_html)
        else:
            return HttpResponseBadRequest()

load_tours_list = LoadToursView.as_view()

class ItemsLoaderView(View):
    def post(self, request, *args, **kwargs):
        if not request.is_ajax():
            return HttpResponseRedirect('/')
        else:
            if 'load_ids' not in request.POST or 'all_load_ids' not in request.POST:
                return HttpResponseBadRequest()

            load_ids_str = request.POST['load_ids']
            all_load_ids = request.POST['all_load_ids']

            num_curr_page = 0
            counter = 0
            for ids in all_load_ids.split('|'):
                counter = counter + 1
                if ids == load_ids_str:
                    num_curr_page = counter

            load_ids = load_ids_str.split(',')
            try:
                queryset = Tour.objects.published().filter(id__in=load_ids)
            except Tour.DoesNotExist:
                return HttpResponseBadRequest()

            next_id_loaded_items_array = all_load_ids.split('|')
            num_curr = next_id_loaded_items_array.index(load_ids_str)
            array_length = len(next_id_loaded_items_array)

            png_num_curr = num_curr + 1
            if png_num_curr < 4:
                min_border = 0
                max_border = 5
            elif png_num_curr > array_length - 3:
                min_border = array_length - 4
                max_border = array_length
            else:
                min_border = png_num_curr - 2
                max_border = png_num_curr + 2

            try:
                if num_curr == 0:
                    page_prev = False
                else:
                    num_prev = num_curr - 1
                    page_prev = next_id_loaded_items_array[num_prev]
            except:
                page_prev = False
            try:
                if num_curr == array_length - 1:
                    page_next = False
                else:
                    num_next = num_curr + 1
                    page_next = next_id_loaded_items_array[num_next]
            except:
                page_next = False

            response = HttpResponse()
            load_template = 'items_loader/tours_load_template.html'
            items_html = render_to_string(
                'items_loader/base_loader.html',
                    {'items': queryset, 'load_template': load_template, 'current_ids': load_ids,
                     'num_curr_page': num_curr_page, 'next_id_loaded_items': next_id_loaded_items_array,
                     'curr_ids': load_ids_str, 'page_prev': page_prev, 'page_next': page_next,
                     'min_border': min_border, 'max_border': max_border, }
            )
            response.content = items_html
            return response

items_loader = ItemsLoaderView.as_view()

class OrderFormView(FormView):
    form_class = OrderForm
    template_name = 'mainblock/order_form.html'

    def get_form_kwargs(self):
        kwargs = super(OrderFormView, self).get_form_kwargs()
        initial = self.get_initial()

        hotel = self.kwargs['hotel']
        tour = self.kwargs['tour']
        if hotel == 'none':
            hotel = False
        else:
            try:
                hotel = int(hotel)
            except:
                hotel = False

        if hotel:
            try:
                hotel_val = Hotel.objects.get(id=hotel)
            except Hotel.DoesNotExist:
                hotel_val = False
        else:
            hotel_val = False

        if tour == 'none':
            tour = False
        else:
            try:
                tour = int(tour)
            except:
                tour = False

        if tour:
            try:
                tour_val = Tour.objects.get(id=tour)
            except Tour.DoesNotExist:
                tour_val = False
        else:
            tour_val = False

        if hotel_val:
            initial['hotel'] = hotel_val

        if tour_val:
            initial['tour'] = tour_val

        kwargs.update({
            'initial': initial,
            })
        return kwargs

    def get(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        context = self.get_context_data(**kwargs)
        context['form'] = form

        hotel = self.kwargs['hotel']
        tour = self.kwargs['tour']
        if hotel == 'none':
            hotel = False
        else:
            try:
                hotel = int(hotel)
            except:
                hotel = False

        if hotel:
            try:
                hotel_val = Hotel.objects.filter(id=hotel)
            except Hotel.DoesNotExist:
                hotel_val = False
        else:
            hotel_val = False

        if tour == 'none':
            tour = False
        else:
            try:
                tour = int(tour)
            except:
                tour = False

        if tour:
            try:
                tour_val = Tour.objects.filter(id=tour)
            except Tour.DoesNotExist:
                tour_val = False
        else:
            tour_val = False

        if tour_val:
            context['form'].fields['tour'].queryset = tour_val
        else:
            context['form'].fields['tour'].queryset = Tour.objects.extra(where=['1=0'])

        if hotel_val:
            context['form'].fields['hotel'].queryset = hotel_val
        else:
            context['form'].fields['hotel'].queryset = Hotel.objects.extra(where=['1=0'])
        return self.render_to_response(context)

prepare_order = OrderFormView.as_view()

@csrf_exempt
def SaveOrderForm(request):
    if request.is_ajax():
        data = request.POST.copy()
        form = OrderForm(data)
        if form.is_valid():
            saved_object = form.save()
            subject = u'%s - Новая заявка.' % settings.SITE_NAME
            subject = u''.join(subject.splitlines())
            message = render_to_string(
                'mainblock/admin_message_template.html',
                    {
                    'saved_object': saved_object,
                    'site_name': settings.SITE_NAME,
                }
            )
            try:
                emailto = Settings.objects.get(name='workemail').value
            except Settings.DoesNotExist:
                emailto = False

            if emailto:
                msg = EmailMessage(subject, message, settings.DEFAULT_FROM_EMAIL, [emailto])
                msg.content_subtype = "html"
                msg.send()

            return HttpResponse('success')
        else:
            id_hotel = data['hotel']
            try:
                id_hotel = int(id_hotel)
            except:
                id_hotel = False

            if id_hotel:
                try:
                    hotel = Hotel.objects.filter(id=id_hotel)
                    form.fields['hotel'].queryset = hotel
                except Hotel.DoesNotExist:
                    return HttpResponseBadRequest()
            else:
                form.fields['hotel'].queryset = Hotel.objects.extra(where=['1=0'])
            id_tour = data['tour']
            try:
                id_tour = int(id_tour)
            except:
                id_tour = False

            if id_tour:
                try:
                    tour = Tour.objects.filter(id=id_tour)
                    form.fields['tour'].queryset = tour
                except Tour.DoesNotExist:
                    return HttpResponseBadRequest()
            else:
                form.fields['tour'].queryset = Tour.objects.extra(where=['1=0'])

            form_html = render_to_string(
                'mainblock/order_form.html',
                    {'form': form}
            )
            return HttpResponse(form_html)
    else:
        return HttpResponseBadRequest()