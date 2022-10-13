from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from .models import Place


def get_details_url(request, pk):
    place = get_object_or_404(Place, pk=pk)
    details = {
        'title': place.title,
        'imgs': [img.image.url for img in place.images.all()],
        'description_short': place.description_short,
        'description_long': place.description_long,
        'coordinates': {
            'lng': place.lng,
            'lat': place.lat
        }
    }
    return JsonResponse(details, json_dumps_params={'ensure_ascii': False})


def start(request):
    template = 'places/index.html'
    places = Place.objects.all()
    features = []

    for place in places:

        feature = {
            'type': 'Feature',
            'geometry': {
                'type': 'Point',
                'coordinates': [
                    place.lng,
                    place.lat,
                ]
            },
            'properties': {
                'title': place.title,
                'placeId': place.pk,
                'detailsUrl': reverse(get_details_url, kwargs={'pk': place.pk})
            }
        }
        features.append(feature)
    places = {'type': 'FeatureCollection', 'features': features}
    return render(request, template, context={'places': places})
