# -*- coding: utf-8 -*-
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView, View, DetailView
from apps.mainblock.models import Country, AdvertasingOnMain
from django.db.models.loading import get_model
from apps.utils.utils import crop_map_image_util

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

