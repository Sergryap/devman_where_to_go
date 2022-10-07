from django.forms import model_to_dict
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
import json

from django.urls import reverse

from .models import Place


def details_url(request, pk):
    instances = Place.objects.all().prefetch_related('images')
    instance = instances.get(pk=pk)
    details = {
        "title": instance.title,
        "imgs": [img['image'] for img in instance.images.values()],
        "description_short": instance.description_short,
        "description_long": instance.description_long,
        "coordinates": {
            "lng": instance.coordinate_lng,
            "lat": instance.coordinate_lat
        }
    }
    return JsonResponse(details, safe=False, json_dumps_params={'ensure_ascii': False})


# Create your views here.
def start(request):
    template = 'places/index.html'
    places = Place.objects.all().prefetch_related('images')
    features = []

    for place in places:
        feature = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [
                    round(float(place.coordinate_lng), 2),
                    round(float(place.coordinate_lng), 6)
                ]
            },
            "properties": {
                "title": place.title.split("«")[1][:-1],
                "placeId": place.pk,
                "detailsUrl": reverse(details_url, kwargs={'pk': place.pk})
            }
        }
        features.append(feature)

    context = {"features": features}

    return render(request, template, context=context)


