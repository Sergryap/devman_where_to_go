from where_to.settings import MEDIA_ROOT
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
        coordinates = reviews.pop('coordinates')
        reviews['coordinate_lng'] = coordinates['lng']
        reviews['coordinate_lat'] = coordinates['lat']
        imgs = reviews.pop('imgs')
        title = reviews.pop('title')
        place, created = Place.objects.get_or_create(
            title=title,
            defaults=reviews)

        if created:
            print(f'Создаю метку с названием: "{title}"')
            for img in imgs:
                print(f'Загружаю фото: "{img}"')
                filename = path.join('place_images', path.split(img)[1])
                filename_all = path.join(MEDIA_ROOT, filename)
                Image.objects.get_or_create(
                    image=filename,
                    defaults={'place': place})

                response = requests.get(img)
                response.raise_for_status()
                with open(filename_all, 'wb') as file:
                    file.write(response.content)
            print('Загрузка прошла успешно')
            print(f'Добавлена метка с названием "{title}"')
        else:
            print(f'Позиция с названием "{title}" уже имеется в базе данных')
