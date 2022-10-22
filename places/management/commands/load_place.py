import re
import requests
from django.core.files.base import ContentFile
from django.utils.crypto import md5
from django.core.management.base import BaseCommand
from places.models import Place, Image
from bs4 import BeautifulSoup


class Command(BaseCommand):
    """Команда для парсинга данных и записи в базу данных"""

    @staticmethod
    def load_image(place: Place, image_content: bytes, position: int):
        """Загрузка одной фотографии для объекта 'place'"""
        content_file = ContentFile(image_content, name=md5(image_content).hexdigest())
        Image.objects.create(place=place, image=content_file, position=position)

    @staticmethod
    def create_location_data(location: dict):
        """Получение необходимых данных о локации из исходного словаря"""
        description = {
            'description_short': location.get('description_short', ''),
            'description_long': location.get('description_long', ''),
            'lng': location['coordinates']['lng'],
            'lat': location['coordinates']['lat'],
        }
        images = location.get('imgs', [])
        title = location['title']

        return description, images, title

    def upload_url(self, link: str):
        """Загрузка всех данных для одной локации из ссылки link"""
        response = requests.get(link)
        response.raise_for_status()
        location_init = response.json()
        description, images, title = self.create_location_data(location_init)
        place, created = Place.objects.get_or_create(title=title, defaults=description)

        if created:
            print(f'Создаю метку с названием: "{title}"')
            for position, img in enumerate(images, start=1):
                print(f'Загружаю фото: "{img}"')
                response = requests.get(img)
                response.raise_for_status()
                self.load_image(place, response.content, position)
            print('Загрузка прошла успешно', f'Добавлена метка с названием "{title}"', sep='\n')
        else:
            print(f'Позиция с названием "{title}" уже имеется в базе данных')

    def upload_all(self, link_places: str):
        """Загрузка всех данных для всех локаций из ссылки link_places"""
        src = requests.get(link_places)
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
            help='Полная загрузка всех локаций из "https://github.com/devmanorg/where-to-go-places/tree/master/places"'
        )
        parser.add_argument(
            '-u', '--url', type=str,
            help='Загрузка локации с одного указанного url, содержащего ссылку на json-файл'
        )

    def handle(self, *args, **options):
        link_all = options['all']
        link_one = options['url']
        # если аргумент --all_default указан, то загрузка по умолчанию
        link_all_default = (
            'https://github.com/devmanorg/where-to-go-places/tree/master/places'
            if options['all_default'] else None
        )
        link_all_places = link_all or link_all_default

        if link_all_places:
            # загрузка всех мест разом
            self.upload_all(link_all_places)
        else:
            # загрузка по одному
            self.upload_url(link_one)
