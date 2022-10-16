# Куда пойти — Москва глазами Артёма
## Сайт о самых интересных местах в Москве. Авторский проект Артёма.
![where_to_go_prew](https://user-images.githubusercontent.com/99894266/194736763-58a2ed39-4340-4031-8c8e-a2b6d47667be.jpg)
*[Пример работающего сайта](http://45.84.226.238:8000/)*
<br>**Важно! Запускайте с протоколом `http://`**
## Как устроен сайт
Сайт представляет собой интерактивную карту Москвы, на которой отмечаются места активного отдыха и различных достопримечательностей с подробными описаниями и комментариями.
### Как добавить или изменить метки на карте через админ-панель
1. Для доступа в админку сайта перейдите по ссылке:
<br><br>[http://45.84.226.238:8000/admin/](http://45.84.226.238:8000/admin/)
<br><br>![admin_1](https://user-images.githubusercontent.com/99894266/194737078-280eb029-410c-4c0f-9890-8bbf5334f69f.jpg)
1. Для добавления нового места на карте перейдите в `Places`:
<br><br>[http://45.84.226.238:8000/admin/places/place/](http://45.84.226.238:8000/admin/places/place/)
<br><br> и нажмите `ADD PLACE`:
<br><br>![admin_2](https://user-images.githubusercontent.com/99894266/194737430-8d9fd208-b375-4352-b707-edc800a2317d.jpg)
1. Для изменения уже существующего места перейдите по нужному пункту:
<br><br>![admin_3](https://user-images.githubusercontent.com/99894266/194737488-4f3381a2-5d8d-4922-830a-803a5c1bb0cd.jpg)
1. Добавьте или измените данные или фото:
<br><br>![admin_4](https://user-images.githubusercontent.com/99894266/194737540-87e56f77-62e7-41eb-829f-d4d43e95bada.jpg)
***
## Как добавить метку на карте через терминал
Для добавления новой метки на карту средствами разработчика используйте команду `load_place`
<br><br>При этом вы должны находится в активированном виртуальном окружении, все необходимые файлы должны быть загружены, библиотеки установлены
* Для добавления одиночной позиции используйте команду:
<br><br>`python3 manage.py load_place --url <файл.json>`
<br><br>Содержимое файла `<файл.json>` должно иметь вид:
```{
    "title": "Генератор Маркса или «Катушка Тесла»",
    "imgs": [
        "https://raw.githubusercontent.com/devmanorg/where-to-go-places/master/media/d3b5cc74cc94c802b51c85542b2f9ad5.jpg",
        "https://raw.githubusercontent.com/devmanorg/where-to-go-places/master/media/b742b82f77028d6a8c9be681cab25a3d.jpg",
        "https://raw.githubusercontent.com/devmanorg/where-to-go-places/master/media/57f990fd24a55324fc1fc541cac41b99.jpg",
        "https://raw.githubusercontent.com/devmanorg/where-to-go-places/master/media/2d5be0d4e83fdde3e8c98f18e0d2e365.jpg",
        "https://raw.githubusercontent.com/devmanorg/where-to-go-places/master/media/d4a8ab43eff1f7e83491610682d13984.jpg",
        "https://raw.githubusercontent.com/devmanorg/where-to-go-places/master/media/7945e1e565530ab6943c40d64f21cfb7.jpg"
    ],
    "description_short": "Место, в котором рождаются искусственные молнии и облака.",
    "description_long": "<p>Внешний вид этого монстроподобного, внушительного комплекса заставляет сердца посетителей биться чаще, а некоторое сходство с катушкой Тесла (на самом деле это генератор Аркадьева-Маркса) влечёт сюда всех любителей научпопа, индастриала и других интересующихся. Для того, чтобы попасть на территорию действующего испытательного стенда ВНИЦ ВЭИ, коим и является это окутанное мифами место, рекомендуется договориться с охраной. Несанкционированное попадание в пределы испытаний может повлечь самые серьёзные последствия!</p>",
    "coordinates": {
        "lng": "36.88324860715219",
        "lat": "55.92555463090268"
    }
}
```
* Для добавления сразу нескольких позиций из указанного url используйте команду:
<br><br>`python3 manage.py load_place --all <url>`
<br>Ссылка `<url>` должна вести на страницу собержащую данные о локациях на подобие [этой](https://github.com/devmanorg/where-to-go-places/tree/master/places)

* Для добавления сразу нескольких позиций из url по умолчанию используйте команду:
<br><br>`python3 manage.py load_place -ad`
***
## Как установить сайт на удаленном сервере
#### Упрощенный вариант для ознакомительных целей
* Загрузите данные на сервер:
<br>`git clone https://github.com/Sergryap/devman_where_to_go.git`
* Создайте виртуальное окружение:
<br>`python3 -m -venv venv`
* Активируйте виртуальное окружение:
<br>`source venv/bin/activate`
* Установите все зависимости:
<br>`pip install -r requirements.txt`
* Создайте в корневом каталоге вашего проекта файл `.env` и задайте в нем переменные окружения по образцу:
```
SECRET_KEY=<секретный ключ вашего проекта джанго>
ALLOWED_HOSTS=<ip разрешенных серверов>
URL_PLACES_DEFAULT=<ссылка на страницу с данными по локациям для загрузки по умолчанию>
```
где:
<br>SECRET_KEY - секретный ключ для конкретной установки Django. Для начала установите любую случайную строку.
<br>ALLOWED_HOSTS - имена хостов/доменов (через запятую), которым разрешено обслуживать сайт Django
##### Для генерации нового SECRET_KEY можно воспользоваться командой:
`python3 manage.py get_secret_key`
<br><br>Подробнее см. здесь:
[https://docs.djangoproject.com/en/4.1/ref/settings/](https://docs.djangoproject.com/en/4.1/ref/settings/)
* Выполните команду, для создания базы данных:
<br>`python3 manage.py migrate`
* Создайте первого суперпользователя:
<br>`python3 manage.py createsuperuser`
* Загрузите данные в базу данных сайта:
<br>`python3 manage.py load_place -ad`
* Запустите виртуальный сервер:
<br>`python3 manage.py runserver 0.0.0.0:8000`
* Сайт будет доступен по ссылке:
<br>`http://<IP вашего сервера>:8000/`

