from where_to_go.settings import MEDIA_ROOT
from django.core.management.base import BaseCommand
from places.models import Place, Image
import requests
from os import path


class Command(BaseCommand):

    # Команда для парсинг данных из JSON-файла и записи в базу данных:
    # $ python3 manage.py load_place http://адрес/файла.json


    def add_arguments(self, parser):
        parser.add_argument('url', type=str)

    def handle(self, *args, **options):
        url = options['url']
        response = requests.get(url)
        response.raise_for_status()
        reviews = response.json()
        reviews['coordinate_lng'] = reviews['coordinates']['lng']
        reviews['coordinate_lat'] = reviews['coordinates']['lat']
        del reviews['coordinates']
        imgs = reviews.pop('imgs')
        place, created = Place.objects.get_or_create(**reviews)

        for img in imgs:
            filename = path.join('place_images', path.split(img)[1])
            filename_all = path.join(MEDIA_ROOT, filename)

            Image.objects.get_or_create(image=filename, place=place)

            response = requests.get(img)
            response.raise_for_status()
            with open(filename_all, 'wb') as file:
                file.write(response.content)
