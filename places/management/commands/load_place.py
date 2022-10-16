from where_to_go.settings import MEDIA_ROOT
from django.core.management.base import BaseCommand
from places.models import Place, Image
import requests
from os import path, mkdir
from bs4 import BeautifulSoup

from environs import Env
env = Env()
env.read_env()


class Command(BaseCommand):
    """
    Команда для парсинг данных и записи в базу данных
    """

    @staticmethod
    def get_location_details(link):
        """
        Получение данных о загружаемой локации из ссылки link
        """
        response = requests.get(link)
        response.raise_for_status()
        place = response.json()
        coordinates = place.pop('coordinates')
        place['lng'] = coordinates['lng']
        place['lat'] = coordinates['lat']
        images = place.pop('imgs')
        title = place.pop('title')
        return *Place.objects.get_or_create(title=title, defaults=place), title, images

    @staticmethod
    def create_dir_media():
        if not path.isdir(MEDIA_ROOT):
            mkdir(MEDIA_ROOT)
            mkdir(path.join(MEDIA_ROOT, 'place_images'))

    @staticmethod
    def upload_images_to_place(images, place):
        """
        Загрузка фотографий для объекта 'place' в БД и в папку 'media/place_images' из списка 'images'
        """
        for position, img in enumerate(images, start=1):
            print(f'Загружаю фото: "{img}"')
            filename = path.join('place_images', path.split(img)[1])
            filename_all = path.join(MEDIA_ROOT, filename)
            Image.objects.create(image=filename, place=place, position=position)
            response = requests.get(img)
            response.raise_for_status()
            with open(filename_all, 'wb') as file:
                file.write(response.content)

    def upload_url(self, link):
        """
        Загрузка всех данных для одной локации из ссылки link
        """
        place, created, title, images = self.get_location_details(link)

        if created:
            print(f'Создаю метку с названием: "{title}"')
            self.upload_images_to_place(images, place)
            print('Загрузка прошла успешно', f'Добавлена метка с названием "{title}"', sep='\n')
        else:
            print(f'Позиция с названием "{title}" уже имеется в базе данных')

    def add_arguments(self, parser):
        parser.add_argument(
            '-a', '--all', type=str,
            help='Полная загрузка всех локаций с указанного url'
        )
        parser.add_argument(
            '-ad', '--all_default', action='store_true',
            help='Полная загрузка всех локаций из url, заданного в ключе "URL_PLACES_DEFAULT" внешнего окружения'
        )
        parser.add_argument(
            '-u', '--url', type=str,
            help='Загрузка локации с одного указанного url, содержащего ссылку на json-файл'
        )

    def handle(self, *args, **options):
        link_all = options['all']
        link_one = options['url']
        # если аргумент --all_default указан то загрузка по умолчанию
        link_all_default = env('URL_PLACES_DEFAULT') if options['all_default'] else None
        link_all_places = link_all if link_all else link_all_default
        self.create_dir_media()

        if link_all_places:
            # загрузка всех мест разом
            src = requests.get(link_all_places)
            src.raise_for_status()
            soup = BeautifulSoup(src.text, 'lxml')
            link_blocks = soup.find_all(class_='js-navigation-open Link--primary')
            for block in link_blocks:
                url = ''.join(['https://raw.githubusercontent.com', block['href'].replace('blob/', '')])
                self.upload_url(url)
        else:
            # загрузка по одному
            self.upload_url(link_one)
