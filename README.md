# REST API News

## Оглавление
- [Описание](#description)
- [Используемые технологии](#technologies)
- [Запуск проекта без докера](#launch)
- [Запуск проекта с докером](#launch)
- [Примеры работы с API для всех пользователей](#unauth)
- [Примеры работы с API для авторизованных пользователей](#auth)

<a id=description></a>
## Описание
API включает в себя посты, каналы, комментарии, ответы, возможность подписаться и узнать подписчиков, реакции. Авторизация реализованна через JWT-токен.
### Реализован функционал дающий возможность:
* Подписываться на пользователя.
* Просматривать, создавать новые, удалять и изменять посты.
* Просматривать и создавать каналы.
* Комментировать, смотреть, удалять и обновлять комментарии.
* Отвечать на комментарии.
* Ставить реакции на посты.
* Отвечать на комментарии.

#### К API есть документация по адресу `http://localhost:8000/redoc/`
---
<a id=technologies></a>
## Используемые технологии:
- Python 3.7
- Django 2.2.19
- Django REST Framework
- PostgreSQL
- Nginx
- Gunicorn
- Docker
- Simple JWT+ Djoser
- Django Filter 

<a id=launch></a>
## Запуск проекта без Docker:
### Клонировать репозиторий и перейти в него в командной строке:
```bash
git clone git@github.com:V-pix/api_final_yatube.git

```
### Перейти в репозиторий в командной строке:
```bash
cd news
```
### Cоздать виртуальное окружение:
```bash
python -m venv venv
```
### Активировать виртуальное окружение:
```bash
source venv/bin/activate        # для Linux
source venv/Scripts/activate    # для Windows
```
### Установить зависимости из файла requirements.txt:
```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```
### Создать миграции:
```bash
python manage.py makemigrations
```
### Выполнить миграции:
```bash
python manage.py migrate
```
### Создать суперпользователя:
```bash
python manage.py createsuperuser
```
### Запустить проект:
```bash
python manage.py runserver
```
<a id=launch></a>
## Запуск проекта с докером
Выполните установку git, docker и docker-compose
```sh
sudo apt install git docker docker-compose -y
```
Клонируйте репозиторий и перейдите в его директорию:
```sh
git clone git@github.com:V-pix/foodgram-project-react.git
cd foodgram-project-react
```

<a id=unauth></a>
## Примеры работы с API для всех пользователей
Для неавторизованных пользователей работа с API доступна в режиме чтения,
что-либо изменить или создать не получится.
```bash
GET api/v1/posts/ - получить список всех публикаций.
При указании параметров limit и offset выдача должна работать с пагинацией
GET api/v1/posts/{id}/ - получение публикации по id
GET api/v1/chanels/ - получение списка доступных каналов
GET api/v1/chanels/{id}/ - получение информации о канале по id
GET api/v1/{post_id}/comments/ - получение всех комментариев к публикации
GET api/v1/{post_id}/comments/{id}/ - Получение комментария к публикации по id
```
Получение доступа к эндпоинту /api/v1/follow/
(подписки) доступен только для авторизованных пользователей.
```bash
GET /api/v1/follow/ - подписка пользователя от имени которого сделан запрос
на пользователя переданного в теле запроса. Анонимные запросы запрещены.
```
- Авторизованные пользователи могут создавать посты,
комментировать их и подписываться на других пользователей.
- Пользователи могут изменять(удалять) контент, автором которого они являются.

Доступ авторизованным пользователем доступен по JWT-токену (Joser),
который можно получить выполнив POST запрос по адресу:
```bash
POST /api/v1/jwt/create/
```
Передав в body данные пользователя (например в postman):
```bash
{
"username": "string",
"password": "string"
}
```
Полученный токен добавляем в headers (postman), после чего буду доступны все функции проекта:
```bash
Authorization: Bearer {your_token}
```
Обновить JWT-токен:
```bash
POST /api/v1/jwt/refresh/ - обновление JWT-токена
```
Проверить JWT-токен:
```bash
POST /api/v1/jwt/verify/ - проверка JWT-токена
```
Так же в проекте API реализована пагинация (LimitOffsetPagination):
```bash
GET /api/v1/posts/?limit=5&offset=0 - пагинация на 5 постов, начиная с первого
```
