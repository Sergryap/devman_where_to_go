import re
import requests
from django.core.files.base import ContentFile
from django.utils.crypto import md5
from where_to_go.settings import MEDIA_ROOT
from django.core.management.base import BaseCommand
from places.models import Place, Image
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
    def load_image(place: Place, image_content: bytes, position: int):
        # загрузка одной фотографии для объекта 'place'
        content_file = ContentFile(image_content, name=md5(image_content).hexdigest())
        image = Image.objects.create(place=place, image=content_file, position=position)

        return image

    def upload_images_to_place(self, images: list, place: Place):
        """
        Загрузка фотографий для объекта 'place' в БД и в папку 'media/place_images' из списка 'images'
        """
        for position, img in enumerate(images, start=1):
            print(f'Загружаю фото: "{img}"')
            response = requests.get(img)
            response.raise_for_status()
            self.load_image(
                place=place,
                image_content=response.content,
                position=position
            )

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

    def upload_all(self, link_of_places):
        """
        Загрузка всех данных для всех локаций из общей ссылки link_of_places
        """
        src = requests.get(link_of_places)
        src.raise_for_status()
        soup = BeautifulSoup(src.text, 'lxml')
        link_blocks = soup.find_all('a', attrs={'href': re.compile(r'.+\.json')})
        for block in link_blocks:
            url = ''.join(['https://raw.githubusercontent.com', block['href'].replace('blob/', '')])
            self.upload_url(url)

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
        link_all_default = (
            'https://github.com/devmanorg/where-to-go-places/tree/master/places'
            if options['all_default'] else None
        )
        link_all_places = link_all if link_all else link_all_default

        if link_all_places:
            # загрузка всех мест разом
            self.upload_all(link_all_places)
        else:
            # загрузка по одному
            self.upload_url(link_one)
