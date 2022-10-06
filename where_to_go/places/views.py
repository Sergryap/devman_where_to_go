from django.forms import model_to_dict
from django.http import HttpResponse
from django.shortcuts import render
import json

from .models import Place


# Create your views here.
def start(request):
    template = 'places/index.html'
    places = Place.objects.all().prefetch_related('images')
    place_list = []
    for place in places:
        place_dict = {
            "title": place.title,
            "img": [d['image'] for d in place.images.values()],
            "description_short": place.description_short,
            "description_long": place.description_long,
            "coordinates": {
                "lng": place.coordinate_lng,
                "lat": place.coordinate_lat
            }
        }
        place_json = json.dumps(place_dict)

        context_dict = {
            "place_json": place_json,
            "placeId": None,
            "title": None,
            "coordinates": None
        }
        place_list.append(context_dict)
    context = {"place_list": place_list}

    return render(request, template, context=context)
