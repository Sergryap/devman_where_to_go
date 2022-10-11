from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse
from .models import Place
from os import path


def details_url(request, pk):
    instances = Place.objects.all().prefetch_related('images')
    instance = instances.get(pk=pk)
    details = {
        "title": instance.title,
        "imgs": [
            path.join('media', img['image'])
            for img in instance.images.order_by('position').values()
        ],
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
    places = Place.objects.all()
    features = []

    for place in places:

        feature = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [
                    place.coordinate_lng,
                    place.coordinate_lat,
                ]
            },
            "properties": {
                "title": place.title,
                "placeId": place.pk,
                "detailsUrl": reverse(details_url, kwargs={'pk': place.pk})
            }
        }
        features.append(feature)
    places_geojson = {"type": "FeatureCollection", "features": features}
    return render(request, template, context={"places_geojson": places_geojson})
