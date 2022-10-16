# Куда пойти — Москва глазами Артёма
## Сайт о самых интересных местах в Москве. Авторский проект Артёма.
![Screenshot from 2022-10-16 17-06-34](https://user-images.githubusercontent.com/99894266/196034572-599405e8-8f00-49a9-be9c-5c5cb0f2e69a.png)
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
<br><br>![Screenshot from 2022-10-16 17-01-14](https://user-images.githubusercontent.com/99894266/196034293-240de9ae-60a8-437e-8a93-acb46376ad3b.png)

1. Для изменения уже существующего места перейдите по нужному пункту в колонке **title**

1. Добавьте или измените данные или фото:
<br><br>![Screenshot from 2022-10-16 17-04-22](https://user-images.githubusercontent.com/99894266/196034412-9594599d-0e6e-4b34-bdf7-9a72dde2177c.png)

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
<br>Ссылка `<url>` должна вести на страницу, содержащую данные о локациях по подобию [этой страницы](https://github.com/devmanorg/where-to-go-places/tree/master/places)

* Для добавления сразу нескольких позиций из url по умолчанию используйте команду:
<br><br>`python3 manage.py load_place -ad`
<br> При работе этой команды возможны временные паузы в связи с ограничениями github.
***
## Как установить сайт на удаленном сервере
#### Упрощенный вариант для ознакомительных целей
* Загрузите данные на сервер:
<br>`git clone https://github.com/Sergryap/devman_where_to_go.git`
* Перейдите в созданную папку проекта:
<br>`cd devman_where_to_go`
* Создайте виртуальное окружение:
<br>`python3 -m venv venv`
* Активируйте виртуальное окружение:
<br>`source venv/bin/activate`
* Установите все зависимости:
<br>`pip install -r requirements.txt`
<br>![Screenshot from 2022-10-16 16-39-58](https://user-images.githubusercontent.com/99894266/196033665-ab90bff3-530b-4334-94b7-2cb0c3b38f6f.png)

* Создайте в корневом каталоге вашего проекта файл `.env` и задайте в нем переменные окружения по образцу:
```
SECRET_KEY=<секретный ключ вашего проекта джанго>
ALLOWED_HOSTS=<ip разрешенных серверов>
URL_PLACES_DEFAULT=<ссылка на страницу с данными по локациям для загрузки по умолчанию>
```
<br>![Screenshot from 2022-10-16 16-55-50](https://user-images.githubusercontent.com/99894266/196034180-82f58e4e-be68-450b-a2c4-2f8241eba949.png)

<br>![Screenshot from 2022-10-16 16-57-25](https://user-images.githubusercontent.com/99894266/196034160-2f7abe4a-a828-4d11-86d6-53eda914985d.png)

где:
<br>SECRET_KEY - секретный ключ для конкретной установки Django. Для начала установите любую случайную строку.
<br>ALLOWED_HOSTS - имена хостов/доменов (через запятую), которым разрешено обслуживать сайт Django.
<br>URL_PLACES_DEFAULT - ссылка на страницу github, содержащая данные о локациях по подобию [этой страницы](https://github.com/devmanorg/where-to-go-places/tree/master/places)
##### Для генерации нового SECRET_KEY можно воспользоваться командой:
`python3 manage.py get_secret_key`
<br><br>Подробнее см. здесь:
[https://docs.djangoproject.com/en/4.1/ref/settings/](https://docs.djangoproject.com/en/4.1/ref/settings/)
* Выполните команду, для создания базы данных:
<br>`python3 manage.py migrate`
* Создайте первого суперпользователя:
<br>`python3 manage.py createsuperuser`
<br>![Screenshot from 2022-10-16 16-42-07](https://user-images.githubusercontent.com/99894266/196033937-8b0a0f8c-b85a-4342-b722-d1e8b4c1f7c5.png)
* Загрузите данные в базу данных сайта:
<br>`python3 manage.py load_place -ad`
<br>![Screenshot from 2022-10-16 16-42-39](https://user-images.githubusercontent.com/99894266/196033759-85f5bbab-1e86-4552-997b-6636c293575c.png)

* Запустите виртуальный сервер:
<br>`python3 manage.py runserver 0.0.0.0:8000`
<br>![Screenshot from 2022-10-16 16-45-30](https://user-images.githubusercontent.com/99894266/196033858-6440bbfe-4e11-4087-a5b4-cc71bc037fb1.png)

* Сайт будет доступен по ссылке:
<br>`http://<IP вашего сервера>:8000/`

