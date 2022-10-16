from where_to_go.settings import MEDIA_ROOT
from django.core.management.base import BaseCommand
from places.models import Place, Image
import requests
from os import path
from bs4 import BeautifulSoup


class Command(BaseCommand):
    """
    Команда для парсинг данных и записи в базу данных
    """

    def add_arguments(self, parser):
        parser.add_argument('-a', '--all', action='store_true',
                            help='Полная загрузка с https://github.com/devmanorg/where-to-go-places/tree/master/places'
                            )
        parser.add_argument('-u', '--url', type=str, help='Загрузка с одного указанного url')

    @staticmethod
    def __upload_url(link):
        response = requests.get(link)
        response.raise_for_status()
        reviews = response.json()
        coordinates = reviews.pop('coordinates')
        reviews['lng'] = coordinates['lng']
        reviews['lat'] = coordinates['lat']
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
                Image.objects.create(image=filename, defaults={'place': place})
                response = requests.get(img)
                response.raise_for_status()
                with open(filename_all, 'wb') as file:
                    file.write(response.content)
            print('Загрузка прошла успешно')
            print(f'Добавлена метка с названием "{title}"')
        else:
            print(f'Позиция с названием "{title}" уже имеется в базе данных')

    def handle(self, *args, **options):
        upload_all = options['all']
        link = options['url']

        if upload_all:
            # загрузка всех мест разом
            src = requests.get('https://github.com/devmanorg/where-to-go-places/tree/master/places')
            src.raise_for_status()
            soup = BeautifulSoup(src.text, 'lxml')
            link_blocks = soup.find_all(class_='js-navigation-open Link--primary')
            for block in link_blocks:
                url = f'https://raw.githubusercontent.com/devmanorg/where-to-go-places/master/places/{block.text}'
                self.__upload_url(url)
        else:
            # загрузка по одному
            self.__upload_url(link)
