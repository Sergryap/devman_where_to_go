from where_to_go.settings import MEDIA_ROOT
from django.core.management.base import BaseCommand
from places.models import Place, Image
import requests
from os import path
from bs4 import BeautifulSoup

from environs import Env
env = Env()
env.read_env()


class Command(BaseCommand):
    """
    Команда для парсинг данных и записи в базу данных
    """

    def add_arguments(self, parser):
        parser.add_argument('-a', '--all', type=str, help='Полная загрузка с указанного url')
        parser.add_argument('-ad', '--all_default', action='store_true', help='Загрузка из url по умолчанию')
        parser.add_argument('-u', '--url', type=str, help='Загрузка с одного указанного url')

    @staticmethod
    def upload_url(link):
        """
        Загрузка данных для позиции на карте из ссылки link
        """
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

    @staticmethod
    def get_head_url_json(link_all):
        """
        Получение общей части ссылки на url json с данными для позиции на карте
        """
        details = link_all.split("/")
        del details[details.index('tree')]
        return '/'.join(['https://raw.githubusercontent.com'] + details[3:])

    def handle(self, *args, **options):
        link_all = options['all']
        link_one = options['url']
        # если аргумент --all_default указан то загрузка по умолчанию
        link_all_default = env('URL_PLACES_DEFAULT') if options['all_default'] else None
        link_all = link_all if link_all else link_all_default

        if link_all:
            # загрузка всех мест разом
            head_url_json = self.get_head_url_json(link_all)
            src = requests.get(link_all)
            src.raise_for_status()
            soup = BeautifulSoup(src.text, 'lxml')
            link_blocks = soup.find_all(class_='js-navigation-open Link--primary')
            for block in link_blocks:
                url = f'{head_url_json}/{block.text}'
                self.upload_url(url)
        else:
            # загрузка по одному
            self.upload_url(link_one)
